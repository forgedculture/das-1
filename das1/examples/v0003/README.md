# DAS-1 v0.003 draft evidence pack

Status: draft. v0.003 is not claimable. This pack exists so the evidence shape can be
built and tested ahead of release, and so the v0.003 machine checks have something to
run against.

Run it:

    python tools/das1_verify.py verify \
      --das-version v0.003 \
      --receipts das1/examples/v0003/receipt_packs \
      --exceptions das1/examples/exceptions \
      --drills das1/examples/v0003/drills \
      --tool-catalogs das1/examples/v0003/tool_catalogs \
      --policy-snapshots das1/examples/policy_snapshots \
      --ir-annexes das1/examples/ir_annexes \
      --delegation-records das1/examples/v0003/delegation_records \
      --classification-registers das1/examples/v0003/classification_registers \
      --report conformance-v0003-report.json

Exceptions, policy snapshots, and IR annexes are shared with the v0.002 pack, because
AEC-02, AEC-04, AEC-11, and AEC-12 are unchanged.

## What each artifact is here to show

Delegation records (AEC-13)

- `pass_dlg_root_0001.json` — depth 0. An orchestrator holding R4/A5 grants R3/A4 with a
  narrowed tool and data-class set. Subset on every axis.
- `pass_dlg_child_0002.json` — depth 1. The deployer sub-delegates without raising anything:
  `cd_pipeline` is withheld and the ceiling is held level rather than promoted.
- `pass_dlg_cascade_parent_0003.json` / `pass_dlg_cascade_child_0004.json` — the D3 subject.
  The parent is revoked mid-execution and the child carries `revoked_by_delegation_id`,
  showing it died by cascade rather than by its own revocation. This is precisely the gap
  AEC-05 leaves open and AEC-13 closes.

Classification register (AEC-14)

- One register naming the classification authority, the evidence basis, the contest
  resolution path, the higher-class ambiguity default, and all four reclassification triggers.
- `cls_e4` is a worked contested classification: proposed R2 by delivery, contested by
  security, resolved at R3 by the board, with the resolution referenced.
- `cmp_bulk_export_0001` is the composition test case. Writing export parts (R2) and rotating
  the manifest (R2) are each individually reversible. Run as one sequence they publish a
  complete customer table to a bucket with an external read path, which is an irreversible
  egress. The sequence is governed at R4.

Receipts

- `pass_composition_step_1.json` and `pass_composition_step_2.json` are the composition case
  in evidence: both are classified R2, both carry `composed_class: R4`, and both carry the
  R4 approval and preflight. Under v0.002 these two receipts would have passed every check
  while the composed effect faced no gate at all.
- `pass_r1_delegated_allow.json` shows A5 latitude that is real only inside an R2 ceiling.
- `pass_cap_breaker_block.json` is the AEC-10 case: the cap fired in the execution path and
  nothing was written.
- `pass_cascade_revoke.json` is the human-initiated cascade revoke behind D3.

Drills

- D1 and D2 as at v0.002, re-run across two delegation hops.
- D3 delegation cascade: one descendant blocked, zero executed after revoke, lineage resolved
  back to the human principal, cascade inside the AEC-05 budget.
- D4 cap breaker: execution halted in the execution path, cap owner paged in 41s against a
  5m response target.

## Note on fixtures

Everything here is built to pass. That proves the checks do not false-positive; it proves
nothing about whether they fire. `tools/test_v0003_checks.py` mutates these artifacts into
specific violations and asserts each check catches it.
