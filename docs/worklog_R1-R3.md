# R1-R3 A2A Language Design Worklog

---
Task ID: R1-R3-A2A
Agent: a2a-language-designer
Task: Deep research on A2A agent-first-class language design (Rounds 1-3)

Work Log:
- Round 1: Analyzed agent communication vs API vs human communication paradigms
- Round 1: Surveyed existing protocols: MCP, Google A2A, OpenAI Agents SDK, CrewAI, AutoGen
- Round 1: Researched JSON-fluidity problem: JSON-LD, AT Protocol Lexicon, code-as-data patterns
- Round 2: Designed 6 agent-first-class language primitives with JSON schemas
- Round 2: Defined bytecode encodings for 35 new opcodes across all primitives
- Round 2: Specified failure modes and edge cases for each primitive
- Round 3: Researched script-compile-meta_compile execution spectrum
- Round 3: Designed ExecutionMode system with per-expression mode switching
- Round 3: Designed transition semantics between modes preserving execution state
- Implemented protocol.py with 1300+ lines of Python dataclasses
- All primitives verified with JSON round-trip tests
- All 140 existing tests pass unchanged

Stage Summary:
- Produced docs/round1-3_a2a_language_design.md with 5000+ words of research
- Implemented src/flux_a2a/protocol.py with 6 primitives and mode system
- Designed BranchPrimitive (parallel/sequential/competitive exploration with 7 merge strategies)
- Designed ForkPrimitive (agent inheritance with fine-grained state/context/trust control)
- Designed CoIteratePrimitive (multi-agent shared program with 4 shared state modes)
- Designed DiscussPrimitive (structured debate/brainstorm/review/negotiate discourse)
- Designed SynthesizePrimitive (map_reduce/ensemble/chain/vote/weighted_merge combination)
- Designed ReflectPrimitive (meta-cognition: strategy/progress/uncertainty/confidence self-assessment)
- Extended Signal ISA from 48 to 83 opcodes (35 new opcodes)
- Created ProtocolRegistry for dynamic opcode dispatch
- Schema versioning via schema_version field (AT Protocol Lexicon pattern)
