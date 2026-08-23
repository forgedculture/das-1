# Glossary

- AEC: Authority Engineering Controls (core controls)
- AECX: Extension controls (catalog)
- Agent: A system that can choose, sequence, or request actions through tools, connectors, workflows, code execution, or delegated agents on behalf of a human or organization.
- Autonomy level: The declared position of an agent on the autonomy dimension defined in Annex A, describing how much latitude the agent has with a result. Distinct from risk class, which describes the consequence of an action.
- Autonomy mode: The v0.002 term for the autonomy dimension. Refers to Annex A; overlay language using this term remains valid.
- Classification register: The record of how actions are classified into risk classes, naming the classifying owner and the review date, required as the AEC-14 receipt.
- Composed effect: The combined outcome of a sequence of actions within one authorized task, which may exceed the risk class of any individual action in that sequence.
- Connector: An integration that gives an agent or workflow access to an external account, system, dataset, or service.
- Delegated agent: An agent or worker invoked by another agent or workflow under a bounded task, data, tool, time, cost, and authority scope.
- Delegation envelope: The bounded set of authority a delegating agent grants to a delegated agent, which under AEC-13 MUST be a subset of the delegating agent's own authority on every axis.
- Delegation lineage: The chain of delegation records linking an executing agent back to the original human principal, required by AEC-13 to be reconstructable from receipts.
- Delegation record: The artifact produced by each delegation naming the delegating agent, the delegated agent, the granted scope, the granted risk ceiling, and an expiry.
- Overlay: A bundle that tightens core controls and adds extension controls for a specific environment
- Profile: Protocol/ecosystem-specific guidance that shows how to meet core controls
- Skill: A reusable capability package that may include instructions, helper code, templates, assets, tool declarations, or operational policy.
- Standing instruction artifact: A persistent project, user, organization, workflow, or runtime customization that is loaded by default or selected by policy to steer agent behavior.
- Tool broker: A boundary component that exposes, mediates, authorizes, logs, or revokes tool access for agents or workflows.
