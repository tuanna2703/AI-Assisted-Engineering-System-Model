# Environment Mechanism Mapping

Status: Complete for the bounded investigation.

The current Execution Environment provides persistent Agent instructions, task context, skills, MCP capability, Python/CLI execution, filesystem persistence, and IDE tooling. Fresh inspection demonstrated that the Agent can invoke the AESM Runtime, but no current mechanism automatically connects a normal engineering request to the Runtime or presents authoritative Execution Context to the Agent.

The minimum supported boundary is: create/discover Process Instance -> obtain/present authoritative Execution Context -> dispatch permitted Runtime operations -> return updated authoritative state.

Runtime remains authoritative for Process Instance identity, Context, state mutation, recognition, validation, persistence, lifecycle/process-state control, and traceability. Agent remains responsible for engineering reasoning and work. Conversation history is not authoritative.

MCP, CLI, skills, or other environment mechanisms remain candidate delivery mechanisms; none is selected as normative by this mapping.

Next: separately define the smallest concrete Agent–Runtime bridge boundary before implementation.