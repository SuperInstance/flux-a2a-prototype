# A2A Language Design Research: Rounds 1-3

**FLUX Signal Protocol — Agent-First-Class JSON Language**

> *"Agents don't speak APIs. APIs are for machines talking to machines about data. Agents need something richer: a language where branching is a primitive, forking is inheritance, and consensus is a control flow construct."*

---

## Table of Contents

- [Round 1: What Makes Agent Communication Different?](#round-1-what-makes-agent-communication-different)
  - [1.1 The Communication Trichotomy](#11-the-communication-trichotomy)
  - [1.2 Existing Agent Protocols: A Critical Survey](#12-existing-agent-protocols-a-critical-survey)
  - [1.3 The JSON-Fluidity Problem](#13-the-json-fluidity-problem)
- [Round 2: Agent-First-Class Language Primitives](#round-2-agent-first-class-language-primitives)
  - [2.1 Branch — Parallel Exploration](#21-branch--parallel-exploration)
  - [2.2 Fork — Agent Inheritance](#22-fork--agent-inheritance)
  - [2.3 Co-Iterate — Multi-Agent Shared Program](#23-co-iterate--multi-agent-shared-program)
  - [2.4 Discuss — Structured Agent Discourse](#24-discuss--structured-agent-discourse)
  - [2.5 Synthesize — Result Combination](#25-synthesize--result-combination)
  - [2.6 Reflect — Meta-Cognition](#26-reflect--meta-cognition)
- [Round 3: The Script-Compile Spectrum](#round-3-the-script-compile-spectrum)
  - [3.1 Why Agents Need Both Scripts and Compilation](#31-why-agents-need-both-scripts-and-compilation)
  - [3.2 The Three Modes](#32-the-three-modes)
  - [3.3 Mode Representation in the A2A Language](#33-mode-representation-in-the-a2a-language)
  - [3.4 Bytecode Encoding for New Opcodes](#34-bytecode-encoding-for-new-opcodes)
- [Appendix: Complete Protocol Specification](#appendix-complete-protocol-specification)

---

## Round 1: What Makes Agent Communication Different?

### 1.1 The Communication Trichotomy

To design a language for agent-to-agent (A2A) communication, we must first understand how it differs from the two dominant communication paradigms: API communication and human communication.

#### API Communication: Request/Response

APIs are the dominant machine-to-machine communication model. They are:

- **Synchronous**: A client sends a request, blocks, and waits for a response. Even "async" APIs typically use futures/promises that resolve to a single response.
- **Stateless**: Each request contains all necessary context. The server maintains no conversation memory (except what the client explicitly provides via tokens/sessions).
- **Deterministic**: Given the same input, the same output is expected. Errors are well-defined (400, 500, etc.).
- **Hierarchical**: URLs form trees. Operations map to CRUD. The ontology is fixed by the API designer.
- **Single-writer**: One client modifies state at a time. Concurrency is handled through locking or optimistic concurrency.

This works brilliantly for data CRUD, but it fails for the kind of exploratory, uncertain, collaborative work that agents do. An agent trying to solve a novel problem cannot express "I'm going to try three approaches in parallel, and if two agree, go with that" as an API call.

#### Human Communication: Turn-Based Contextual

Humans communicate through:

- **Asynchronous turn-taking**: Speaker A says something, speaker B responds — but both parties maintain internal context that doesn't need to be transmitted.
- **Ambiguity tolerance**: Humans handle vagueness, metaphors, and implicit context. "It's complicated" is a valid answer.
- **Contextual shorthand**: After establishing shared context, communication becomes extremely compressed ("the thing we discussed" — zero tokens to identify a complex concept).
- **Parallel processing**: Multiple people can work on different parts of a problem simultaneously, merging results through discussion.
- **Conflict resolution**: Disagreements are resolved through argument, evidence, authority, or voting — not error codes.

Human communication is rich but unreliable. The same phrase means different things to different people. Context is lost between sessions. Agreement is hard to verify.

#### Agent Communication: The Third Paradigm

Agents need properties from both paradigms, plus properties that neither provides:

| Property | APIs | Humans | Agents (need) |
|----------|------|--------|---------------|
| Determinism | Yes | No | Configurable (confidence scores) |
| Parallelism | Limited | Yes | First-class (branch, fork) |
| Statefulness | No | Yes | Yes (inherited context) |
| Ambiguity handling | No | Yes | Yes (uncertainty quantification) |
| Consensus | No | Slow | Yes (vote, merge strategies) |
| Compositionality | Yes (chaining) | No | Yes (nested primitives) |
| Self-reflection | No | Yes | Yes (meta-cognition) |
| Evolution | Versioned | Organic | Both (schema evolution + learning) |

The key insight: **agent communication is computation**, not just data exchange. When an agent sends a `branch` command to a fleet, it's not requesting data — it's spawning parallel computations and specifying how to merge results. When an agent `discuss`es with another, it's running a collaborative optimization algorithm.

This is why JSON-as-AST is the right foundation. Every Signal program is simultaneously:
1. A **message** (it can be sent between agents)
2. A **program** (it can be executed by an interpreter)
3. A **schema** (it defines the shape of its outputs)
4. A **document** (it's human-readable JSON)

### 1.2 Existing Agent Protocols: A Critical Survey

#### MCP (Model Context Protocol — Anthropic)

**What it gets right:**
- Clean separation of tools, prompts, and resources
- JSON-RPC transport — familiar and debuggable
- Server/client model maps well to existing infrastructure
- Standardized capability negotiation

**What it misses for A2A:**
- Fundamentally **client-server**: a model talks to tools. Two models don't talk to each other as equals.
- No concept of **branching** or **parallel exploration**. A model calls one tool at a time.
- No **confidence propagation**. Tool results are assumed correct.
- No **merge semantics**. If two agents call the same tool differently, there's no protocol for reconciliation.
- No **meta-cognition**. The model can't express "I'm uncertain, spawn a branch."

**FLUX Signal's advantage:** MCP is a protocol for giving models access to tools. Signal is a language for agents to think together. MCP answers "how does an agent use tools?" Signal answers "how do agents collaborate?"

#### Google A2A Protocol

**What it gets right:**
- Agent-to-agent task delegation as first-class concept
- Task lifecycle management (submitted, working, completed, etc.)
- Streaming support for long-running tasks
- Agent card discovery mechanism

**What it misses for A2A:**
- Still **task-oriented**, not **program-oriented**. An agent delegates a task, not a program.
- No **branching semantics**. A task goes to one agent, not three in parallel.
- No **co-iteration**. Two agents can't work on the same evolving document.
- No **confidence or trust** propagation between agents.
- **Stateless delegation** — the receiving agent starts fresh, without context inheritance.

**FLUX Signal's advantage:** Google A2A treats agents as services that accept tasks. Signal treats agents as collaborators that share programs, state, and context. Google's model is "hire a contractor." Signal's model is "pair program."

#### OpenAI Agents SDK

**What it gets right:**
- Handoff protocol between agents
- Guardrails and validation
- Tracing and observability built in
- Good developer experience

**What it misses for A2A:**
- Handoffs are **sequential**, not parallel. Agent A hands off to Agent B, who hands off to Agent C.
- No native **merge** when multiple agents produce conflicting results.
- Tightly coupled to OpenAI's API — not transport-agnostic.
- No concept of a **shared program** that multiple agents execute simultaneously.

**FLUX Signal's advantage:** OpenAI's SDK orchestrates a relay race. Signal orchestrates a parallel search. In a relay race, each runner does their leg sequentially. In a parallel search, multiple runners explore different routes simultaneously, compare notes, and the best route wins.

#### CrewAI / AutoGen

**What they get right:**
- Multi-agent orchestration as a first-class concern
- Role-based agent design (researcher, writer, reviewer)
- Task decomposition and delegation
- Conversation flow management

**What they miss for A2A:**
- **Python-bound**: The orchestration logic is Python code, not a portable language.
- No **compilation path**. You can't optimize hot agent workflows.
- No **standardized serialization**. The "language" is whatever the framework's Python API provides.
- **Framework-specific**: Agents written for CrewAI can't talk to agents written for AutoGen.
- No **confidence scoring** or **uncertainty quantification** built in.

**FLUX Signal's advantage:** CrewAI and AutoGen are frameworks for building multi-agent systems in Python. Signal is a language for expressing multi-agent computation that any agent, in any runtime, can execute. The difference between a Python framework and a language is the difference between a recipe book and a language — the latter enables expressing things the recipe book author never imagined.

### 1.3 The JSON-Fluidity Problem

JSON is the universal serialization format. But it has fundamental limitations when used as the foundation for an evolving agent language:

#### Problem 1: Code as Data

Lisp's S-expressions achieve what JSON cannot: code IS data, and data IS code. In Lisp, `(+ 1 2)` is simultaneously a list and a computation. In JSON, `{"op": "add", "args": [1, 2]}` is data that requires an interpreter to become computation.

This matters for agents because agents need to **manipulate programs as data**. An agent should be able to:
- Take an existing program, modify a parameter, and re-execute it
- Compose smaller programs into larger ones
- Generate programs programmatically
- Serialize and transmit partial computations

**Signal's approach:** JSON IS the AST. There is no separate parse step. `{"op": "add", "args": [1, 2]}` is not serialized from an intermediate form — it IS the form. The interpreter walks JSON directly. This gives us 80% of Lisp's code-as-data advantage with JSON's universal tooling.

#### Problem 2: Ambient Context

How do you represent "I'm thinking about this in the background"? In human conversation, we maintain ambient awareness — ongoing thoughts that color our responses without being the main topic.

In JSON, every field is explicit. There's no way to say "the confidence for everything below is 0.7 unless otherwise stated" without repeating it. This leads to verbose, repetitive structures.

**Signal's approach:** The `confidence` field on every Expression serves as ambient context. It propagates downward through nested expressions unless overridden. The `meta` field on every node allows attaching arbitrary ambient state. The `mode` field (Round 3) controls interpretation strategy globally.

We also adopt a pattern from **JSON-LD**: the `@context` field. In Signal, a program can declare default context that applies to all expressions:

```json
{
  "signal": {
    "context": {
      "confidence": 0.8,
      "lang": "zho",
      "trust_threshold": 0.6
    },
    "body": [...]
  }
}
```

#### Problem 3: Schema Evolution

When you add a new field to a JSON schema, old agents that don't understand it will silently ignore it. This is a feature for forward compatibility but a bug for semantic correctness.

**Signal's approach:** We adopt the **AT Protocol's Lexicon** strategy. Every primitive has a `$schema` version. Agents declare which schema versions they understand. The interpreter validates against the declared version and falls back gracefully:

```json
{
  "op": "discuss",
  "$schema": "flux.a2a.discuss/v2",
  "topic": "...",
  "participants": [...]
}
```

Unknown schema versions trigger a `reflect` — the agent examines what it doesn't understand and decides whether to attempt execution, delegate to a newer agent, or request clarification.

#### Problem 4: Representing Processes, Not Just States

JSON represents states well (objects, arrays, numbers). It represents processes poorly. How do you express "loop until consensus" in JSON?

**Signal's approach:** Control flow primitives (`loop`, `while`, `match`) are first-class JSON expressions. The A2A primitives (`branch`, `fork`, `co_iterate`, `discuss`) represent processes as data structures. A `discuss` object IS the discussion protocol — its structure IS the process.

This is the key design principle: **in Signal, the shape of the data IS the shape of the computation**. A `branch` with three sub-branches is a parallel exploration with three paths. A `co_iterate` with two agents is a pair programming session. The JSON structure maps one-to-one to the computation graph.

---

## Round 2: Agent-First-Class Language Primitives

### 2.1 Branch — Parallel Exploration

#### Design Rationale

Branching is the most fundamental agent primitive. When an agent faces uncertainty, it should be able to split into parallel explorations — try multiple strategies simultaneously and merge results. This isn't an exotic feature; it's the default mode of thinking for any sufficiently complex problem.

In traditional programming, branching is `if/else`. In agent programming, branching is "try all paths and pick the best." The difference is between a decision tree (deterministic) and a search tree (exploratory).

#### JSON Schema

```json
{
  "op": "branch",
  "id": "string — unique branch identifier",
  "strategy": "parallel | sequential | competitive",
  "branches": [
    {
      "label": "string — branch name",
      "weight": "float 0.0-1.0 — merge weight",
      "agent": "optional Agent — who executes this branch",
      "body": [Expression...]
    }
  ],
  "merge": {
    "strategy": "consensus | vote | best | all | weighted_confidence | first_complete | last_writer_wins",
    "timeout_ms": "int — merge deadline",
    "fallback": "string — fallback merge strategy"
  },
  "confidence": "float — confidence of this branch operation"
}
```

#### Strategies Explained

- **parallel**: All branches execute simultaneously (or in simulated parallelism). Results are collected and merged.
- **sequential**: Branches execute in order. Each branch can see the previous branch's result via `_prev_branch_result`. Early termination if confidence exceeds threshold.
- **competitive**: Branches race. First to achieve confidence > threshold wins. Others are cancelled.

#### Bytecode Encoding

```
BRANCH_START <branch_id> <count> <merge_strategy>
  PUSH_LABEL <label_0>
  PUSH_WEIGHT <weight_0>
  PUSH_AGENT  <agent_0>        ; optional
  ...body instructions...
  BRANCH_END_SEGMENT <label_0>
  PUSH_LABEL <label_1>
  ...
BRANCH_MERGE <merge_strategy> <timeout_ms>
```

New opcodes: `BRANCH_START`, `BRANCH_END_SEGMENT`, `BRANCH_MERGE`

#### Example Usage

```json
{
  "op": "branch",
  "id": "sort-exploration",
  "strategy": "parallel",
  "branches": [
    {
      "label": "merge-sort",
      "weight": 0.4,
      "body": [
        {"op": "let", "name": "result", "value": {"op": "literal", "value": [1,2,3,4,5]}},
        {"op": "confidence", "level": 0.95}
      ]
    },
    {
      "label": "quick-sort",
      "weight": 0.35,
      "body": [
        {"op": "let", "name": "result", "value": {"op": "literal", "value": [5,4,3,2,1]}},
        {"op": "confidence", "level": 0.88}
      ]
    },
    {
      "label": "radix-sort",
      "weight": 0.25,
      "body": [
        {"op": "let", "name": "result", "value": {"op": "literal", "value": [1,3,5,2,4]}},
        {"op": "confidence", "level": 0.72}
      ]
    }
  ],
  "merge": {
    "strategy": "weighted_confidence",
    "timeout_ms": 10000,
    "fallback": "best"
  }
}
```

#### Failure Modes

1. **Timeout**: Not all branches complete before the merge deadline. Fallback strategy selects from completed branches only.
2. **All fail**: Every branch returns an error. Merge returns a composite error with all failure details.
3. **Deadlock**: In competitive mode, no branch achieves the confidence threshold. The branch with highest confidence wins by default.
4. **Resource exhaustion**: Too many parallel branches. The interpreter enforces a `max_parallel_branches` limit (default: 16).
5. **Merge conflict**: In consensus mode, branches disagree. Returns all values with a `disagreement` flag rather than picking arbitrarily.

### 2.2 Fork — Agent Inheritance

#### Design Rationale

Forking creates a child agent that inherits state from the parent. This is the agent equivalent of process `fork()` in Unix — but with fine-grained control over what state is inherited.

Unlike branching (which explores different strategies), forking creates a *copy of the agent itself* with modifications. This enables:
- **Speculative execution**: "Try this approach; if it works, merge back."
- **Parallel delegation**: "Handle this subtask while I continue."
- **Variant exploration**: "Same agent, different prompt/context/strategy."

The key insight: forking is **inheritance**, not just spawning. The child gets the parent's state, trust graph, and context — not just a task.

#### JSON Schema

```json
{
  "op": "fork",
  "id": "string — fork identifier",
  "from": "string — parent agent ID (optional, defaults to current)",
  "mutation": {
    "type": "prompt | context | strategy | capability",
    "changes": {
      "role": "optional new role",
      "trust": "optional new trust level",
      "capabilities": "optional new capability set",
      "system_prompt": "optional modified prompt"
    }
  },
  "inherit": {
    "state": ["list", "of", "state", "keys", "to", "inherit"],
    "context": "boolean — inherit ambient context",
    "trust_graph": "boolean — inherit trust relationships",
    "message_history": "boolean — inherit conversation history"
  },
  "body": [Expression...],
  "on_complete": "collect | discard | signal | merge",
  "merge_policy": {
    "strategy": "string — how to merge fork results back",
    "conflict": "parent_wins | child_wins | negotiate"
  }
}
```

#### Bytecode Encoding

```
FORK <fork_id> <parent_id> <mutation_type>
  INHERIT_STATE <key_count> <key_0> <key_1> ...
  INHERIT_CONTEXT <bool>
  INHERIT_TRUST <bool>
  ...body instructions...
FORK_COMPLETE <fork_id> <on_complete> <merge_strategy>
```

New opcodes: `FORK`, `INHERIT_STATE`, `INHERIT_CONTEXT`, `INHERIT_TRUST`, `FORK_COMPLETE`

#### Example Usage

```json
{
  "op": "fork",
  "id": "skeptical-reviewer",
  "from": "self",
  "mutation": {
    "type": "strategy",
    "changes": {
      "role": "adversary",
      "trust": 0.3,
      "system_prompt": "Find flaws in the proposed solution"
    }
  },
  "inherit": {
    "state": ["proposed_solution", "constraints", "data"],
    "context": true,
    "trust_graph": false,
    "message_history": false
  },
  "body": [
    {"op": "tell", "to": "parent", "message": "Starting adversarial review..."},
    {"op": "loop", "times": 5, "var": "i", "body": [
      {"op": "ask", "from": "parent", "question": "What about edge case ${i}?"}
    ]},
    {"op": "tell", "to": "parent", "message": "Review complete: 3 vulnerabilities found"}
  ],
  "on_complete": "merge"
}
```

#### Failure Modes

1. **Inheritance conflict**: Child tries to modify inherited state that's being used by parent. Resolved by copy-on-write semantics — child gets a snapshot.
2. **Orphaned fork**: Parent completes before child. Child continues executing but can't merge back. Result is collected independently.
3. **Fork bomb**: Unlimited recursive forking. Enforced via `max_fork_depth` (default: 4) and `max_total_forks` (default: 32).
4. **Merge rejection**: Child's merged result conflicts with parent's current state. `negotiate` conflict mode spawns a `discuss` between parent and child.
5. **State inconsistency**: Inherited state references keys that no longer exist. Fails gracefully with missing keys returning `null`.

### 2.3 Co-Iterate — Multi-Agent Shared Program

#### Design Rationale

Co-iteration is the most powerful primitive: multiple agents simultaneously traverse and modify the same program. Think of it as **pair programming**, but the programmers are AI agents and the "code" is a Signal JSON program.

This is fundamentally different from branching (which splits and merges) or forking (which copies and delegates). In co-iteration, agents share a single mutable program state. When Agent A modifies an expression, Agent B sees the modification immediately.

The critical challenge is **conflict resolution**: what happens when two agents try to modify the same expression simultaneously?

#### JSON Schema

```json
{
  "op": "co_iterate",
  "id": "string — co-iteration session ID",
  "rounds": "int | 'until_convergence' — number of rounds",
  "agents": [
    {
      "id": "string",
      "role": "modifier | auditor | observer | reviewer",
      "capabilities": ["read", "write", "suggest", "branch"],
      "priority": "int — conflict priority"
    }
  ],
  "program": {
    "body": [Expression...]
  },
  "shared_state": "conflict | merge | partitioned | isolated",
  "conflict_resolution": {
    "strategy": "priority | vote | last_writer | reject | branch",
    "priority_order": ["agent_ids in priority order"],
    "on_conflict": "notify | block | auto_resolve"
  },
  "merge_strategy": "sequential_consensus | parallel_merge | majority_vote | trust_weighted",
  "convergence": {
    "metric": "agreement | confidence_delta | value_stability",
    "threshold": 0.9,
    "max_rounds": 100
  }
}
```

#### Shared State Modes

- **conflict**: All agents read/write the same state. Conflicts detected and resolved per the `conflict_resolution` strategy.
- **merge**: Each agent has a local copy. After each round, all copies are merged (union of changes).
- **partitioned**: State is partitioned among agents by key prefix. Each agent "owns" its partition. Cross-partition reads are allowed; writes require negotiation.
- **isolated**: Each agent has fully independent state. No sharing. Useful for benchmarking different strategies on the same problem.

#### Bytecode Encoding

```
CO_ITERATE_START <session_id> <agent_count> <shared_state_mode>
  AGENT_CURSOR <agent_id> <role> <priority> <capabilities>
  ...program body instructions...
CO_ITERATE_ROUND <round_number>
  CONFLICT_DETECT
  CONFLICT_RESOLVE <strategy>
  CONSENSUS_CHECK <metric> <threshold>
CO_ITERATE_END <merge_strategy> <rounds_completed>
```

New opcodes: `CO_ITERATE_START`, `AGENT_CURSOR`, `CO_ITERATE_ROUND`, `CONFLICT_DETECT`, `CONFLICT_RESOLVE`, `CONSENSUS_CHECK`, `CO_ITERATE_END`

#### Example Usage

```json
{
  "op": "co_iterate",
  "id": "code-review-session",
  "rounds": "until_convergence",
  "agents": [
    {"id": "implementer", "role": "modifier", "capabilities": ["read", "write"], "priority": 2},
    {"id": "reviewer", "role": "auditor", "capabilities": ["read", "suggest"], "priority": 1},
    {"id": "tester", "role": "modifier", "capabilities": ["read", "write", "branch"], "priority": 0}
  ],
  "program": {
    "body": [
      {"op": "let", "name": "sort_fn", "value": "quick_sort"},
      {"op": "let", "name": "complexity_target", "value": "O(n log n)"},
      {"op": "let", "name": "test_pass_count", "value": 0}
    ]
  },
  "shared_state": "conflict",
  "conflict_resolution": {
    "strategy": "priority",
    "priority_order": ["implementer", "reviewer", "tester"],
    "on_conflict": "notify"
  },
  "merge_strategy": "trust_weighted",
  "convergence": {
    "metric": "agreement",
    "threshold": 0.95,
    "max_rounds": 50
  }
}
```

#### Failure Modes

1. **Divergent oscillation**: Agents keep changing values back and forth without converging. Detected when `value_stability` metric shows oscillation. Resolved by freezing the most-changed variable and forcing discussion.
2. **Deadlock**: Two agents with equal priority both try to write the same location and both block. Resolved by randomly elevating one agent's priority for this round.
3. **Agent dropout**: An agent fails mid-iteration. Remaining agents continue with reduced consensus threshold.
4. **State corruption**: A bug in one agent's logic corrupts shared state. The `auditor` role (read-only) can detect this by comparing expected vs. actual state transitions.

### 2.4 Discuss — Structured Agent Discourse

#### Design Rationale

Not all agent collaboration is about modifying shared state. Sometimes agents need to *argue*. The `discuss` primitive provides structured communication formats: debate, brainstorm, review, and negotiation.

This fills a gap that no existing protocol addresses. MCP has no concept of agent-to-agent argument. Google A2A has task delegation but not collaborative reasoning. CrewAI has conversation flows but they're hardcoded in Python, not expressible as data.

#### JSON Schema

```json
{
  "op": "discuss",
  "id": "string — discussion ID",
  "topic": "string — what is being discussed",
  "context": {
    "background": "any — shared context for the discussion",
    "constraints": ["list of constraints"],
    "goal": "string — what the discussion should achieve"
  },
  "participants": [
    {
      "id": "string",
      "stance": "pro | con | neutral | devil's_advocate | moderator",
      "expertise": ["list of domains"],
      "weight": "float — influence weight in voting"
    }
  ],
  "format": "debate | brainstorm | review | negotiate | peer_review",
  "structure": {
    "max_rounds": "int",
    "time_per_round_ms": "int — optional time limit",
    "turn_order": "round_robin | priority | free_for_all | moderated"
  },
  "until": {
    "condition": "consensus | timeout | rounds | majority | best_argument",
    "consensus_threshold": 0.8,
    "max_rounds": 10,
    "timeout_ms": 60000
  },
  "output": {
    "format": "decision | options | summary | transcript",
    "include_reasoning": true,
    "include_confidence": true
  }
}
```

#### Discussion Formats

- **debate**: Structured pro/con argumentation. Each participant argues for or against a proposition.
- **brainstorm**: Free-form idea generation. No criticism allowed until all ideas are collected.
- **review**: Systematic evaluation of a proposal/artifact. Participants take specific review angles.
- **negotiate**: Goal-oriented bargaining. Participants have positions and must converge.
- **peer_review**: Academic-style double-blind review. Reviewers evaluate independently, then discuss.

#### Bytecode Encoding

```
DISCUSS_START <discuss_id> <format> <until_condition>
  PARTICIPANT <agent_id> <stance> <weight>
  SET_TOPIC <topic_json>
  DISCUSS_ROUND <round_number>
    TURN <agent_id>
    ARGUMENT <proposition> <evidence> <confidence>
  DISCUSS_CHECK <until_condition>
DISCUSS_END <output_format>
```

New opcodes: `DISCUSS_START`, `PARTICIPANT`, `SET_TOPIC`, `DISCUSS_ROUND`, `TURN`, `ARGUMENT`, `DISCUSS_CHECK`, `DISCUSS_END`

#### Example Usage

```json
{
  "op": "discuss",
  "id": "architecture-decision",
  "topic": "Should we use event sourcing or CRUD for the agent state store?",
  "context": {
    "background": "We need to support undo, replay, and multi-agent concurrent writes.",
    "constraints": ["Must support 1000+ writes/sec", "Must be queryable"],
    "goal": "Select an approach with team consensus > 80%"
  },
  "participants": [
    {"id": "architect-pro", "stance": "pro", "expertise": ["distributed systems"], "weight": 1.0},
    {"id": "architect-con", "stance": "con", "expertise": ["databases"], "weight": 0.9},
    {"id": "moderator", "stance": "moderator", "expertise": ["architecture"], "weight": 0.5}
  ],
  "format": "debate",
  "structure": {"max_rounds": 6, "turn_order": "moderated"},
  "until": {"condition": "consensus", "consensus_threshold": 0.8, "max_rounds": 6},
  "output": {"format": "decision", "include_reasoning": true, "include_confidence": true}
}
```

#### Failure Modes

1. **Unresolvable disagreement**: Participants cannot reach consensus within max_rounds. Output includes all arguments and a "no consensus" flag. The parent agent can then branch into implementing each option.
2. **Dominant participant**: One participant overwhelms others. The `moderator` stance includes rate-limiting and turn-balancing logic.
3. **Circular arguments**: The same points are repeated without progress. Detected via argument deduplication. Moderator forces participants to introduce new evidence.
4. **Topic drift**: Discussion strays from the original topic. Moderator's `topic` field serves as an anchor — arguments that don't address it are flagged as tangential.

### 2.5 Synthesize — Result Combination

#### Design Rationale

After branching, forking, or discussing, agents need to combine results. The `synthesize` primitive provides structured methods for this: map-reduce, ensemble combination, chain composition, and voting.

This is the complement to `branch` and `discuss` — if those primitives split computation and communication, `synthesize` brings it back together.

#### JSON Schema

```json
{
  "op": "synthesize",
  "id": "string",
  "sources": [
    {
      "id": "string — source identifier",
      "type": "branch_result | fork_result | discuss_result | external | variable",
      "ref": "string — reference to source"
    }
  ],
  "method": "map_reduce | ensemble | chain | vote | weighted_merge | best_effort",
  "config": {
    "map_fn": "optional Expression — transform each source before combining",
    "reduce_fn": "optional Expression — how to combine mapped results",
    "weights": {"source_id": "float — weight for weighted methods"},
    "threshold": "float — for vote/consensus methods"
  },
  "output": {
    "type": "code | spec | question | decision | summary | value",
    "format": "json | text | bytecode | signal_program",
    "confidence": "propagate | min | max | average"
  }
}
```

#### Synthesis Methods

- **map_reduce**: Apply a map function to each source, then reduce the mapped results. Standard map-reduce pattern.
- **ensemble**: Combine all sources into a collection. Each source contributes equally (or by weight). No reduction — the ensemble IS the output.
- **chain**: Pipe sources sequentially — output of source N becomes input to source N+1. Like a Unix pipeline.
- **vote**: Sources propose options; majority vote selects the winner. Supports weighted voting.
- **weighted_merge**: Merge all source results with configurable weights. For structured data, performs field-wise weighted merge.
- **best_effort**: Return the highest-confidence result. If multiple sources tie, return all.

#### Bytecode Encoding

```
SYNTH_START <synth_id> <method> <source_count>
  SOURCE_REF <source_id> <type> <ref>
  MAP_FN <expression...>
  REDUCE_FN <expression...>
SYNTH_MERGE <method> <config_json>
SYNTH_OUTPUT <type> <format> <confidence_mode>
```

New opcodes: `SYNTH_START`, `SOURCE_REF`, `MAP_FN`, `REDUCE_FN`, `SYNTH_MERGE`, `SYNTH_OUTPUT`

#### Example Usage

```json
{
  "op": "synthesize",
  "id": "merge-analysis",
  "sources": [
    {"id": "perf-analysis", "type": "branch_result", "ref": "perf-branch"},
    {"id": "security-review", "type": "fork_result", "ref": "security-fork"},
    {"id": "ux-evaluation", "type": "discuss_result", "ref": "ux-discussion"}
  ],
  "method": "weighted_merge",
  "config": {
    "weights": {"perf-analysis": 0.4, "security-review": 0.4, "ux-evaluation": 0.2},
    "threshold": 0.6
  },
  "output": {
    "type": "decision",
    "format": "json",
    "confidence": "propagate"
  }
}
```

#### Failure Modes

1. **Incompatible sources**: Sources have fundamentally different output types (e.g., one produces code, another produces text). The `map_fn` can normalize types before merging.
2. **Missing source**: A referenced source doesn't exist or hasn't completed. Synthesis waits up to `timeout_ms` or proceeds with available sources.
3. **Reduce failure**: The reduce function fails on mapped results. Falls back to `ensemble` method — returns all mapped results without reduction.

### 2.6 Reflect — Meta-Cognition

#### Design Rationale

Meta-cognition is what separates a simple executor from an intelligent agent. An agent that can examine its own reasoning process, identify uncertainty, and adjust its strategy is qualitatively more capable than one that can't.

The `reflect` primitive enables agents to:
- **Self-assess**: "How confident am I in my current approach?"
- **Strategy shift**: "This isn't working — try a different strategy."
- **Uncertainty detection**: "I don't know enough to proceed — ask for help or branch."
- **Progress monitoring**: "Am I making progress toward the goal, or am I stuck?"

This is the most novel primitive — no existing agent framework provides first-class meta-cognition as a language construct.

#### JSON Schema

```json
{
  "op": "reflect",
  "id": "string",
  "on": "strategy | progress | uncertainty | confidence | all",
  "scope": {
    "from_step": "int — reflect on computation from this step",
    "to_step": "int — to this step (default: current)",
    "focus": ["optional list of state keys to examine"]
  },
  "analysis": {
    "method": "introspection | benchmark | comparison | statistical",
    "baseline": "optional — what to compare against",
    "metrics": ["confidence_trend", "state_change_rate", "loop_depth", "branch_divergence"]
  },
  "output": {
    "type": "adjustment | question | branch | log | signal",
    "action": {
      "adjust_strategy": "optional new strategy config",
      "spawn_branch": "optional branch config if output=branch",
      "ask_agent": "optional agent to ask if output=question",
      "confidence_delta": "optional float — adjust current confidence"
    },
    "min_confidence": "float — minimum confidence to proceed without action",
    "report_to": "optional agent ID to send reflection report"
  }
}
```

#### Reflection Types

- **strategy**: Is the current approach effective? Should the agent switch strategies?
- **progress**: Is the agent making progress toward the goal? Is it stuck in a loop?
- **uncertainty**: Where is the agent most uncertain? What additional information would help?
- **confidence**: How has confidence changed over the computation? Is it trending up or down?
- **all**: Comprehensive reflection across all dimensions.

#### Bytecode Encoding

```
REFLECT <reflect_id> <on_type> <scope_from> <scope_to>
  ANALYZE <method> <metrics_json>
  REFLECT_OUTPUT <output_type>
  ADJUST_STRATEGY <new_config>    ; if output=adjustment
  SPAWN_BRANCH <branch_config>    ; if output=branch
  ASK_AGENT <agent_id> <question> ; if output=question
  SIGNAL_REPORT <to_agent>        ; if output=signal
```

New opcodes: `REFLECT`, `ANALYZE`, `REFLECT_OUTPUT`, `ADJUST_STRATEGY`, `SPAWN_BRANCH`

#### Example Usage

```json
{
  "op": "reflect",
  "id": "mid-computation-check",
  "on": "uncertainty",
  "scope": {
    "from_step": 0,
    "focus": ["classification_result", "feature_importance"]
  },
  "analysis": {
    "method": "statistical",
    "metrics": ["confidence_trend", "branch_divergence"]
  },
  "output": {
    "type": "branch",
    "action": {
      "spawn_branch": {
        "id": "investigate-uncertainty",
        "strategy": "competitive",
        "branches": [
          {"label": "gather-more-data", "body": [{"op": "ask", "from": "data-agent", "question": "Get more samples for low-confidence features"}]},
          {"label": "simplify-model", "body": [{"op": "tell", "to": "self", "message": "Reduce model complexity to improve confidence"}]}
        ]
      }
    },
    "min_confidence": 0.6,
    "report_to": "coordinator"
  }
}
```

#### Failure Modes

1. **Infinite reflection**: Reflect triggers a branch, which triggers another reflect, ad infinitum. Enforced via `max_reflect_depth` (default: 3) — reflections within reflections are collapsed into a single deeper reflection.
2. **No actionable insight**: Reflection doesn't find any significant issues. Returns a `no_action` result with a summary, and execution continues normally.
3. **False positive uncertainty**: Reflection identifies uncertainty where none exists (e.g., a low confidence score that's actually correct). The `min_confidence` threshold prevents unnecessary branching.
4. **Reflection cost**: Deep reflection on large computations is expensive. The `scope` field limits what's examined, and the `focus` field restricts analysis to specific state keys.

---

## Round 3: The Script-Compile Spectrum

### 3.1 Why Agents Need Both Scripts and Compilation

A common misconception in agent system design is the assumption that interpreted execution (scripts) is always sufficient. The reasoning goes: "Agents generate JSON, we interpret it, done."

This misses three critical capabilities that compilation provides:

**1. Performance-critical hot paths.** An agent that runs the same co-iteration loop 10,000 times doesn't need to re-parse JSON each time. Compilation to bytecode eliminates parsing overhead and enables CPU-friendly execution (register allocation, instruction scheduling, dead code elimination).

**2. Agent self-improvement.** The most powerful form of agent learning is not just accumulating data — it's improving its own execution engine. An agent that observes "I spend 80% of my time in `co_iterate` with `conflict_resolution=priority`" can compile a specialized version of the interpreter that optimizes exactly this pattern. This is meta-compilation: the agent compiles a better version of itself.

**3. Deterministic replay.** Compiled bytecode is deterministic. Given the same bytecode and the same inputs, the same outputs are guaranteed. This is essential for debugging agent behavior, auditing decisions, and replaying past executions for analysis. Interpreted JSON can have nondeterminism from evaluation order, floating point, and hash-based data structures.

### 3.2 The Three Modes

#### Script Mode: Execute JSON Directly

```json
{
  "signal": {
    "mode": "script",
    "body": [...]
  }
}
```

- **No optimization passes**. JSON is walked directly by the interpreter.
- **Maximum flexibility**. Any valid JSON expression is accepted, including unknown opcodes (which become NOPs).
- **Full introspection**. Every evaluation step is logged and inspectable.
- **Slow but safe**. Good for prototyping, debugging, and exploration.

Use cases: rapid prototyping, agent exploratory programming, debugging sessions, learning/demonstration.

#### Compile Mode: Optimize Hot Paths

```json
{
  "signal": {
    "mode": "compile",
    "optimizations": ["dead_branch_elim", "cse", "constant_fold", "branch_fusion", "hot_path_inline"],
    "body": [...]
  }
}
```

- **Optimization passes applied**. The compiler transforms JSON into bytecode with optimizations.
- **Hot path detection**. Frequently-executed branches are inlined and specialized.
- **Type specialization**. If a variable is observed to always be a number, subsequent operations use integer arithmetic instead of dynamic dispatch.
- **Branch fusion**. Sequential branches with the same merge strategy are fused into a single parallel dispatch.

Use cases: production agent workloads, repeated co-iteration patterns, high-throughput A2A communication, performance-sensitive deployments.

#### Meta-Compile Mode: Self-Improvement

```json
{
  "signal": {
    "mode": "meta_compile",
    "observations": {
      "hot_ops": ["co_iterate", "branch", "reflect"],
      "common_patterns": [
        {"pattern": "branch → co_iterate → synthesize", "frequency": 0.4},
        {"pattern": "reflect → fork → merge", "frequency": 0.25}
      ],
      "optimization_targets": ["co_iterate_conflict_resolution", "branch_merge_overhead"]
    },
    "output": {
      "type": "specialized_interpreter",
      "target_ops": ["co_iterate", "branch", "synthesize"]
    },
    "body": [...]
  }
}
```

- **Pattern extraction**. The meta-compiler observes execution patterns and extracts common subprograms.
- **Specialized interpreter generation**. Generates a custom interpreter optimized for the observed patterns.
- **Self-modifying code**. The agent can replace its own execution engine with the meta-compiled version.
- **Evolution tracking**. Each meta-compilation is recorded with before/after performance metrics.

This is the most experimental mode and represents the frontier of agent self-improvement. The key insight: **agents don't just execute programs — they evolve the execution engine itself.**

### 3.3 Mode Representation in the A2A Language

The `mode` field appears at the program level and can also be set per-expression:

```json
{
  "signal": {
    "id": "hybrid-program",
    "mode": "script",
    "body": [
      {"op": "let", "name": "x", "value": 42},

      {"op": "mode", "value": "compile",
       "optimizations": ["constant_fold", "hot_path_inline"],
       "body": [
         {"op": "loop", "times": 1000, "var": "i", "body": [
           {"op": "mul", "args": [{"op": "get", "name": "x"}, {"op": "get", "name": "i"}]}
         ]}
       ]},

      {"op": "mode", "value": "script"},

      {"op": "reflect", "on": "progress", "output": {"type": "log"}}
    ]
  }
}
```

**Transition semantics:**
- `script → compile`: The compiler takes the current execution state (variable bindings, confidence levels) and compiles the remainder of the body. Compiled section runs with optimized bytecode.
- `compile → script`: The interpreter switches back to direct JSON evaluation. Compiled state is preserved but not used for new expressions.
- `script → meta_compile`: The meta-compiler begins observing the current execution. It doesn't modify anything immediately — it collects observations.
- `meta_compile → compile`: The meta-compiler outputs a specialized interpreter. Subsequent expressions use this specialized interpreter.
- Any mode can transition to any other mode. The state (variables, trust graph, confidence) is preserved across transitions.

### 3.4 Bytecode Encoding for New Opcodes

The complete set of new opcodes introduced by the six A2A primitives and the mode system:

| Opcode | Category | Operands | Description |
|--------|----------|----------|-------------|
| `BRANCH_START` | Agent | id, count, strategy | Begin a parallel branch section |
| `BRANCH_END_SEGMENT` | Agent | label | End one branch segment |
| `BRANCH_MERGE` | Agent | strategy, timeout | Merge all branch results |
| `FORK` | Agent | id, parent, mutation | Spawn child agent |
| `INHERIT_STATE` | Agent | key_count, keys... | Declare state inheritance |
| `INHERIT_CONTEXT` | Agent | bool | Inherit ambient context |
| `INHERIT_TRUST` | Agent | bool | Inherit trust graph |
| `FORK_COMPLETE` | Agent | id, on_complete | Complete a fork |
| `CO_ITERATE_START` | Agent | id, count, mode | Begin co-iteration |
| `AGENT_CURSOR` | Agent | id, role, priority | Register agent cursor |
| `CO_ITERATE_ROUND` | Agent | round_num | Begin a co-iteration round |
| `CONFLICT_DETECT` | Agent | (none) | Detect position conflicts |
| `CONFLICT_RESOLVE` | Agent | strategy | Resolve a conflict |
| `CONSENSUS_CHECK` | Agent | metric, threshold | Check convergence |
| `CO_ITERATE_END` | Agent | strategy, rounds | End co-iteration session |
| `DISCUSS_START` | Agent | id, format, until | Begin a discussion |
| `PARTICIPANT` | Agent | id, stance, weight | Register a participant |
| `SET_TOPIC` | Agent | topic_json | Set discussion topic |
| `DISCUSS_ROUND` | Agent | round_num | Begin a discussion round |
| `TURN` | Agent | agent_id | Agent's turn to speak |
| `ARGUMENT` | Agent | prop, evidence, conf | Present an argument |
| `DISCUSS_CHECK` | Agent | condition | Check termination condition |
| `DISCUSS_END` | Agent | format | End discussion, produce output |
| `SYNTH_START` | Agent | id, method, count | Begin synthesis |
| `SOURCE_REF` | Agent | id, type, ref | Reference a synthesis source |
| `MAP_FN` | Agent | expression... | Map function |
| `REDUCE_FN` | Agent | expression... | Reduce function |
| `SYNTH_MERGE` | Agent | method, config | Execute merge |
| `SYNTH_OUTPUT` | Agent | type, format, conf | Format synthesis output |
| `REFLECT` | Meta | id, on_type, scope | Begin reflection |
| `ANALYZE` | Meta | method, metrics | Run analysis |
| `REFLECT_OUTPUT` | Meta | output_type | Produce reflection output |
| `ADJUST_STRATEGY` | Meta | config | Adjust execution strategy |
| `SPAWN_BRANCH` | Meta | branch_config | Spawn from reflection |
| `MODE_SWITCH` | System | mode, opts | Switch execution mode |

**Total new opcodes: 35**

Combined with the existing 33 opcodes in `BcOp`, the complete Signal ISA has **68 opcodes** organized into six categories: Stack, Arithmetic/Logic, Variables/Control, Agent Communication, Agent Operations, and Meta/System.

---

## Appendix: Complete Protocol Specification

The complete protocol is implemented in `src/flux_a2a/protocol.py` as Python dataclasses. Key design decisions:

1. **All primitives are dataclasses** with `to_dict()` and `from_dict()` for JSON serialization.
2. **Every primitive carries confidence** — uncertainty is a first-class value.
3. **Every primitive has a `meta` dict** for extensibility without schema breakage.
4. **Schema versioning** uses the `$schema` pattern from AT Protocol's Lexicon.
5. **Backward compatibility** is achieved by ignoring unknown fields (they go into `meta`).
6. **Forward compatibility** is achieved by the `reflect` primitive — when an agent encounters something it doesn't understand, it reflects on the gap rather than failing.

The six primitives form a complete agent collaboration vocabulary:

- **branch**: Split into parallel explorations
- **fork**: Create variant agents with inherited state
- **co_iterate**: Multiple agents on the same program
- **discuss**: Structured argumentation and deliberation
- **synthesize**: Combine results from multiple sources
- **reflect**: Self-examination and strategy adjustment

Together with the existing primitives (tell, ask, delegate, broadcast, signal, trust, confidence, merge) and the script-compile-meta_compile mode system, these form the foundation of the FLUX A2A Signal Protocol — a language where collaboration is a control flow construct.

---

*Document version: 0.1.0 — Rounds 1-3 Complete*
*Next: Round 4 — Type System for Agent Communication; Round 5 — Transport Layer Design*
