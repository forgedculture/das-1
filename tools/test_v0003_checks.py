"""Negative tests for the DAS-1 v0.003 machine checks.

Why this exists: the v0.003 example pack is hand-built to pass. A green gate over
passing fixtures proves the checks do not false-positive; it proves nothing about
whether they actually fire. Each case here mutates a passing artifact into a
specific control violation and asserts the matching check catches it.

DAS-1 does not accept a control without a receipt and a drill. By the same logic
it should not accept a verifier check without evidence the check bites.

Usage:
  python3 tools/test_v0003_checks.py     # from the repo root
"""
import json, importlib.util, sys, tempfile
from pathlib import Path

spec = importlib.util.spec_from_file_location("v", "tools/das1_verify.py")
v = importlib.util.module_from_spec(spec)
sys.modules["v"] = v
spec.loader.exec_module(v)

BASE = Path("das1/examples/v0003")
SCH = Path("schemas")

def load(p): return json.loads(Path(p).read_text())

def write_pack(files, sub):
    d = Path(tempfile.mkdtemp()) / sub
    d.mkdir(parents=True)
    for name, obj in files.items():
        (d / name).write_text(json.dumps(obj))
    return d

results = []
def check(name, failed, expect_msg):
    ok = failed and any(expect_msg.lower() in f.message.lower() for f in failed)
    results.append((ok, name, (failed[0].message if failed else "NO FAILURE RAISED")))

# ---- receipts ----
def receipt_case(name, mutate, expect):
    r = load(BASE / "receipt_packs/pass_composition_step_1.json")
    mutate(r)
    d = write_pack({"r.json": r}, "receipt_packs")
    f, _ = v.verify_receipts(d, SCH / "receipt.schema.json", das_version="v0.003")
    check(name, f, expect)

receipt_case("AEC-14 composition hole: R2 in an R4 sequence with no approval",
             lambda r: [r.pop(k, None) for k in ("approval_id", "approver_id", "preflight_id")],
             "composed_class R4 requires")
receipt_case("AEC-14 composed_class below the action's own class",
             lambda r: r.update(composed_class="R1"),
             "is lower than the action's own class")
receipt_case("AEC-13 delegated action with no root principal",
             lambda r: r.pop("root_principal_id"),
             "requires root_principal_id")
receipt_case("AEC-13 action exceeding its granted ceiling",
             lambda r: r.update(risk_class="R4", composed_class="R4"),
             "exceeds granted_risk_ceiling")
receipt_case("AEC-10 cap satisfied in the reporting layer",
             lambda r: r.update(cap_enforcement_point="reporting_layer"),
             "does not satisfy AEC-10")
receipt_case("Annex A: A2 recording an executed R3",
             lambda r: r.update(autonomy_level="A2", risk_class="R3", granted_risk_ceiling="R3", execution_status="executed"),
             "must not record an executed")

# ---- delegation records ----
def dlg_case(name, mutate_map, expect):
    files = {p.name: load(p) for p in (BASE / "delegation_records").glob("*.json")}
    mutate_map(files)
    d = write_pack(files, "delegation_records")
    f, _ = v.verify_delegation_records(d, SCH / "delegation-record.schema.json")
    check(name, f, expect)

def raise_ceiling(files):
    files["pass_dlg_child_0002.json"]["granted_risk_ceiling"] = "R4"
dlg_case("AEC-13 subset rule: child granted a higher risk ceiling", raise_ceiling, "exceeds the delegating agent's")

def raise_autonomy(files):
    files["pass_dlg_child_0002.json"]["granted_autonomy_level"] = "A5"
dlg_case("AEC-13 subset rule: child granted higher autonomy", raise_autonomy, "subset rule applies to both axes")

def grant_unheld_tool(files):
    files["pass_dlg_child_0002.json"]["granted_scope"]["tools"].append("authz_gateway")
dlg_case("AEC-13 subset rule: child granted a tool the parent lacks", grant_unheld_tool, "not held by the delegating agent")

def survive_cascade(files):
    files["pass_dlg_cascade_child_0004.json"]["status"] = "active"
    files["pass_dlg_cascade_child_0004.json"].pop("revoked_at", None)
    files["pass_dlg_cascade_child_0004.json"].pop("revoked_by_delegation_id", None)
dlg_case("AEC-13 cascade: descendant still active under a revoked ancestor", survive_cascade, "revocation must cascade")

def orphan(files):
    files["pass_dlg_child_0002.json"]["parent_delegation_id"] = "dlg_missing_9999"
dlg_case("AEC-13 lineage: parent does not resolve", orphan, "lineage is broken")

# ---- classification register ----
def cls_case(name, mutate, expect):
    r = load(BASE / "classification_registers/pass_classification_register.json")
    mutate(r)
    d = write_pack({"c.json": r}, "classification_registers")
    f, _ = v.verify_classification_registers(d, SCH / "classification-register.schema.json")
    check(name, f, expect)

cls_case("AEC-14 ambiguity default set to the lower class",
         lambda r: r.update(ambiguity_default="lower_class"), "must be higher_class")
cls_case("AEC-14 sequence governed below its composed class",
         lambda r: r["composition_rules"][0].update(governed_at_class="R2"), "must be governed at the composed class")
cls_case("AEC-14 register with no composition test case",
         lambda r: r.update(composition_rules=[]), "at least one composition_rules")
cls_case("AEC-14 missing a reclassification trigger",
         lambda r: r.update(reclassification_triggers=["tool", "scope"]), "is missing")
cls_case("AEC-14 declared individual max contradicts its member entries",
         lambda r: r["composition_rules"][0].update(individual_max_class="R1"), "member entries top out at")

# ---- drills ----
def drill_case(name, mutate, expect, das_version="v0.003"):
    files = {p.name: load(p) for p in (BASE / "drills").glob("*.json")}
    mutate(files)
    d = write_pack(files, "drills")
    f, _ = v.verify_drills(d, SCH / "drill-report.schema.json", das_version=das_version)
    check(name, f, expect)

drill_case("D3 passing with a descendant that executed after revoke",
           lambda fs: fs["pass_d3_delegation_cascade.json"].update(descendants_executed_after_revoke=1),
           "descendant execution(s) after revoke")
drill_case("D4 passing with a reporting-layer cap",
           lambda fs: fs["pass_d4_cap_breaker.json"].update(cap_enforcement_point="reporting_layer"),
           "is not a breaker")
drill_case("D4 passing without notifying the cap owner",
           lambda fs: fs["pass_d4_cap_breaker.json"].update(cap_owner_notified=False),
           "cap has a named owner")
drill_case("v0.003 evidence with no D3 at all",
           lambda fs: fs.pop("pass_d3_delegation_cascade.json"),
           "Missing required passing drill report for D3")

# ---- tool catalog ----
def cat_case(name, mutate, expect):
    r = load(BASE / "tool_catalogs/pass_tool_catalog.json")
    mutate(r)
    d = write_pack({"t.json": r}, "tool_catalogs")
    f, _ = v.verify_tool_catalogs(d, SCH / "tool-catalog.schema.json", das_version="v0.003")
    check(name, f, expect)

cat_case("Annex A.3: catalog entry with no autonomy_level",
         lambda r: r["tools"][0].pop("autonomy_level"), "requires autonomy_level")

# ---- v0.002 must stay unaffected ----
r = load(BASE / "receipt_packs/pass_composition_step_1.json")
for k in ("approval_id", "approver_id", "preflight_id"):
    r.pop(k, None)
d = write_pack({"r.json": r}, "receipt_packs")
f, _ = v.verify_receipts(d, SCH / "receipt.schema.json", das_version="v0.002")
results.append((not f, "v0.002 run ignores v0.003 controls (no false failure)",
                f[0].message if f else "clean"))

print()
passed = 0
for ok, name, detail in results:
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    if not ok:
        print(f"        -> {detail}")
    passed += ok
print(f"\n{passed}/{len(results)} negative tests behaved correctly")
sys.exit(0 if passed == len(results) else 1)
