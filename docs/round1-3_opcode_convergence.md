# FLUX VM Opcode Convergence — Research Report (Rounds 1–3)

> **Task ID**: R1-R3-OPCODE  
> **Agent**: opcode-convergence-researcher  
> **Date**: 2026-07-14

---

## Round 1: Opcode Audit Across All Runtimes

### 1.1 Canonical ISA — flux-multilingual TypeScript (`opcodes.ts`)

The TypeScript `Op` enum in `flux-multilingual/src/lib/flux/opcodes.ts` defines the **canonical 87 opcodes** (spanning ranges 0x00–0xFF). Despite being described as "104 opcodes" in project documentation, only 87 are actually defined, with gaps reserved for future use.

| Range | Category | Count | Opcodes |
|-------|----------|-------|---------|
| 0x00–0x07 | Control flow | 8 | NOP, MOV, LOAD, STORE, JMP, JZ, JNZ, CALL |
| 0x08–0x0F | Integer arithmetic | 8 | IADD, ISUB, IMUL, IDIV, IMOD, INEG, INC, DEC |
| 0x10–0x17 | Bitwise | 8 | IAND, IOR, IXOR, INOT, ISHL, ISHR, ROTL, ROTR |
| 0x18–0x1F | Comparison | 8 | ICMP, IEQ, ILT, ILE, IGT, IGE, TEST, SETCC |
| 0x20–0x27 | Stack ops | 8 | PUSH, POP, DUP, SWAP, ROT, ENTER, LEAVE, ALLOCA |
| 0x28–0x2F | Function ops | 8 | RET, CALL_IND, TAILCALL, MOVI, IREM, CMP, JE, JNE |
| 0x30–0x37 | Memory mgmt | 8 | REGION_CREATE/DESTROY/TRANSFER, MEMCOPY, MEMSET, MEMCMP, JL, JGE |
| 0x38–0x3F | Type ops | 5 | CAST, BOX, UNBOX, CHECK_TYPE, CHECK_BOUNDS |
| 0x40–0x47 | Float arithmetic | 8 | FADD, FSUB, FMUL, FDIV, FNEG, FABS, FMIN, FMAX |
| 0x48–0x4F | Float comparison | 5 | FEQ, FLT, FLE, FGT, FGE |
| 0x50–0x57 | String ops | 5 | SLEN, SCONCAT, SCHAR, SSUB, SCMP |
| 0x60–0x7F | A2A Agent Protocol | 6 | TELL, ASK, DELEGATE, BROADCAST, TRUST_CHECK, CAPABILITY_REQ |
| 0xFE–0xFF | System | 2 | PRINT, HALT |
| **Total** | | **87** | |

### 1.2 Per-Runtime Audit

#### flux-runtime-deu (`vm.py` — `Op` enum)

**Total opcodes**: 87  
**Bytecode compatibility**: **100% byte-identical** to the TypeScript canonical ISA.  
**Unique opcodes**: None.  
**Language-specific enforcement**: Kasus (case-based) access control at the VM execution layer, NOT at the opcode level. German case grammar maps to capability levels:
- Nominativ → CAP_PUBLIC (0)
- Akkusativ → CAP_READWRITE (2)  
- Dativ → CAP_REFERENCE (1)
- Genitiv → CAP_TRANSFER (3)

#### flux-runtime-san (`vm.py` — `Opcode` enum)

**Total opcodes**: 50  
**Bytecode compatibility**: Subset of canonical ISA with identical hex values for shared opcodes.  
**Unique opcodes**: None at the bytecode level.  
**Missing from canonical**: ISHL, ISHR, ROTL, ROTR, SETCC, ENTER, LEAVE, ALLOCA, TAILCALL, IREM, JL, JGE, CAST, BOX, UNBOX, CHECK_TYPE, CHECK_BOUNDS, FNEG, FABS, FMIN, FMAX, FEQ, FLT, FLE, FGT, FGE, SLEN, SCONCAT, SCHAR, SSUB, SCMP, REGION_CREATE, REGION_DESTROY, REGION_TRANSFER, MEMCOPY, MEMSET, MEMCMP  
**Language-specific enforcement**: Vibhakti (8-case Sanskrit grammar) scope system and Lakāra (execution mode) gating at the VM execution layer.

#### flux-runtime-wen (`vm.py` — `Opcode` enum)

**Total opcodes**: 50  
**Bytecode compatibility**: **INCOMPATIBLE** — uses completely different hex values for the same-named opcodes!  
**Unique opcodes (16)**:

| Hex | Name | Domain | Description |
|-----|------|--------|-------------|
| 0x60 | IEXP | Math | Exponentiation (幂) |
| 0x61 | IROOT | Math | Square root (根) |
| 0x70 | VERIFY_TRUST | Confucian/五常 | Trust verification (信) |
| 0x71 | CHECK_BOUNDS | Confucian/五常 | Bounds checking (義) |
| 0x72 | OPTIMIZE | Confucian/五常 | Path optimization (智) |
| 0x80 | ATTACK | Military (兵) | Push data / attack (攻) |
| 0x81 | DEFEND | Military (兵) | Buffer data / defend (守) |
| 0x82 | ADVANCE | Military (兵) | Proceed (進) |
| 0x83 | RETREAT | Military (兵) | Back off (退) |
| 0x90 | SEQUENCE | Control (制) | Sequential execution (則) |
| 0x91 | LOOP | Control (制) | Loop construct (循) |
| 0xA0 | HEX_JUMP | I Ching | Jump to hexagram address (變卦) |
| 0xA1 | HEX_CALL | I Ching | Call hexagram subroutine (卦呼) |
| 0xA2 | TRIGRAM_ADDR | I Ching | Trigram-based addressing (八卦址) |
| 0xB0 | SET_TOPIC | Topic | Set topic register (定題) |
| 0xB1 | USE_TOPIC | Topic | Use topic as implicit operand (用題) |
| 0xB2 | CLEAR_TOPIC | Topic | Clear topic register (清題) |

**Critical issue**: `RET=0x08` (canonical: `0x28`), `HALT=0x09` (canonical: `0xFF`), `IADD=0x10` (canonical: `0x08`). Same names, different bytes — **bytecode is not cross-compatible**. Also implements **domain-aware dispatch**: same opcode produces different side effects depending on textual domain (Math, Confucian, Military, Control, Agent).

#### flux-runtime-lat (`vm.py` — `Opcode` enum)

**Total opcodes**: 39  
**Bytecode compatibility**: **INCOMPATIBLE** — yet another hex mapping.  
**Unique opcodes (8)**:

| Hex | Name | Domain | Description |
|-----|------|--------|-------------|
| 0xA0 | LOOP_START | Temporal | Loop begin (Imperfectum tense) |
| 0xA1 | LOOP_END | Temporal | Loop end |
| 0xA2 | LAZY_DEFER | Temporal | Deferred computation (Futurum tense) |
| 0xA3 | CACHE_LOAD | Temporal | Load cached result (Perfectum tense) |
| 0xA4 | CACHE_STORE | Temporal | Store to cache |
| 0xA5 | ROLLBACK_SAVE | Temporal | Save state (Plusquamperfectum) |
| 0xA6 | ROLLBACK_RESTORE | Temporal | Restore saved state |
| 0xA7 | EVENTUAL_SCHEDULE | Temporal | Schedule eventual computation (Futurum Exactum) |

**Critical issue**: `HALT=0x01` (canonical: `0xFF`), `MOV=0x10` (canonical: `0x01`), `IADD=0x50` (canonical: `0x08`). Latin grammar (6 tenses, 4 moods, 6 cases) maps to execution strategies at the VM layer.

#### flux-runtime-zho (`fir.py` — `FirOpcode` enum)

**Total FIR opcodes**: 34  
**Layer**: FIR (intermediate representation), NOT bytecode. Uses Python `IntEnum(auto())` — no fixed hex values.  
**Unique opcodes (4)**:

| Name | Description |
|------|-------------|
| TOPIC_SET | Set topic register (主题设定 → R63) for zero-anaphora resolution |
| TOPIC_GET | Get topic register (零形回指) — implicit subject reference |
| CLASSIFY | Classifier type annotation (量词类型标注) — maps Chinese measure words to types |
| HONORIFY | Honorific elevation (敬称提升) — context/register tagging |

**Type system**: Chinese measure words (量词) → 20 FIR types (INTEGER, SEQUENCE, DOCUMENT, MACHINE, AGENT, COUNTER, DISTANCE, SPEED, VESSEL, MESSAGE, STEP, KIND, ANIMAL, PERSON, HONORED, ITEM, WEIGHT, TIME, REPORT, ANCHOR)

#### flux-runtime-kor (`fir.py` — `FirOp` enum)

**Total FIR opcodes**: 24  
**Layer**: FIR (intermediate representation), NOT bytecode.  
**Unique opcodes (1)**:

| Name | Description |
|------|-------------|
| 파이 (PHI) | Explicit SSA phi node for control-flow merge points |

**Type system**: Korean honorific levels → 4 trust-level types (系统/동료/사용자/관리자)

### 1.3 Opcode Compatibility Matrix

| Opcode Name | TS (canonical) | DEU | SAN | WEN | LAT | ZHO (FIR) | KOR (FIR) |
|-------------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| NOP | 0x00 | 0x00 | 0x00 | 0x00 | 0x00 | ✓ | ✓ |
| MOV | 0x01 | 0x01 | 0x01 | 0x01 | 0x10 | — | — |
| LOAD | 0x02 | 0x02 | 0x02 | 0x02 | 0x20 | ✓ | ✓ |
| STORE | 0x03 | 0x03 | 0x03 | 0x03 | 0x21 | ✓ | ✓ |
| JMP | 0x04 | 0x04 | 0x04 | 0x04 | 0x30 | — | — |
| JZ | 0x05 | 0x05 | 0x05 | 0x05 | 0x31 | — | — |
| JNZ | 0x06 | 0x06 | 0x06 | 0x06 | 0x32 | — | — |
| CALL | 0x07 | 0x07 | 0x07 | 0x07 | 0x40 | ✓ | ✓ |
| RET | 0x28 | 0x28 | 0x28 | **0x08** | 0x41 | — | — |
| HALT | **0xFF** | 0xFF | 0xFF | **0x09** | **0x01** | ✓ | ✓ |
| PRINT | **0xFE** | 0xFE | 0xFE | **0x0A** | **0x80** | — | — |
| IADD | **0x08** | 0x08 | 0x08 | **0x10** | **0x50** | — | — |
| ISUB | **0x09** | 0x09 | 0x09 | **0x11** | **0x51** | — | — |
| IMUL | **0x0A** | 0x0A | 0x0A | **0x12** | **0x52** | — | — |
| IDIV | **0x0B** | 0x0B | 0x0B | **0x13** | **0x53** | — | — |
| MOVI | **0x2B** | 0x2B | 0x2B | **0x22** | **0x11** | — | — |
| JE | **0x2E** | 0x2E | 0x2E | **0x30** | **0x33** | — | — |
| JNE | **0x2F** | 0x2F | 0x2F | **0x31** | **0x34** | — | — |
| TELL | **0x60** | 0x60 | 0x60 | **0x40** | **0x81** | — | — |
| ASK | **0x61** | 0x61 | 0x61 | **0x41** | **0x82** | — | — |
| DELEGATE | **0x62** | 0x62 | 0x62 | **0x42** | **0x90** | — | — |
| BROADCAST | **0x63** | 0x63 | 0x63 | **0x43** | **0x83** | — | — |
| TRUST_CHECK | **0x64** | 0x64 | 0x64 | **0x50** | **0x91** | — | — |
| CAP_REQUIRE | **0x65** | 0x65 | 0x65 | **0x51** | **0x92** | — | — |

**Key findings**:
- **DEU and SAN** are byte-compatible with the canonical TypeScript ISA.
- **WEN and LAT** have **completely different** hex encodings — same opcode names, different bytes.
- **ZHO and KOR** operate at the FIR layer (not bytecode), so hex compatibility is not applicable.

### 1.4 Opcode Count Summary

| Runtime | Layer | Total | Unique | Byte-Compat with Canonical |
|---------|-------|-------|--------|--------------------------|
| TypeScript | Bytecode | 87 | 0 | 100% (IS the canonical) |
| DEU | Bytecode | 87 | 0 | 100% |
| SAN | Bytecode | 50 | 0 | Subset |
| WEN | Bytecode | 50 | 16 | **0%** (different hex) |
| LAT | Bytecode | 39 | 8 | **0%** (different hex) |
| ZHO | FIR | 34 | 4 | N/A |
| KOR | FIR | 24 | 1 | N/A |
| A2A (compiler.py) | BcOp | 38 | 6 | N/A (string-based) |

---

## Round 2: Converged Opcode Set Design

### 2.1 Core Opcodes (Intersection — Shared by ALL Bytecode Runtimes)

These 27 opcodes are present (by name) in all four bytecode VMs (TS, DEU, SAN, WEN, LAT):

```
NOP, MOV, LOAD, STORE, JMP, JZ, JNZ, CALL, RET, HALT, PRINT,
IADD, ISUB, IMUL, IDIV, IMOD, INEG, INC, DEC, CMP,
JE, JNE, MOVI, PUSH, POP,
TELL, ASK, DELEGATE, BROADCAST, TRUST_CHECK, CAP_REQUIRE
```

### 2.2 Paradigm Opcodes (Language-Specific)

| Category | Opcodes | Runtime(s) | Rationale |
|----------|---------|------------|-----------|
| **Chinese Topic** | SET_TOPIC, USE_TOPIC, CLEAR_TOPIC, TOPIC_SET, TOPIC_GET, CLASSIFY, HONORIFY | WEN, ZHO | Zero-anaphora resolution, measure word typing |
| **Confucian/五常** | VERIFY_TRUST, CHECK_BOUNDS, OPTIMIZE | WEN | Five Constants: 仁義禮智信 baked into operations |
| **Military/兵** | ATTACK, DEFEND, ADVANCE, RETREAT | WEN | Military strategy as computation |
| **I Ching** | HEX_JUMP, HEX_CALL, TRIGRAM_ADDR | WEN | Hexagram-based addressing |
| **Latin Temporal** | LOOP_START, LOOP_END, LAZY_DEFER, CACHE_LOAD, CACHE_STORE, ROLLBACK_SAVE, ROLLBACK_RESTORE, EVENTUAL_SCHEDULE | LAT | 6 Latin tenses as execution modes |
| **Korean Phi** | 파이 (PHI) | KOR | Explicit SSA merge nodes |
| **Sanskrit** | (none at opcode level) | SAN | Enforcement via vibhakti scope + lakāra gating at VM layer |
| **German** | (none at opcode level) | DEU | Enforcement via kasus case → capability at VM layer |
| **Korean** | 권한요구 (CAP_REQUIRE) | KOR | Already in A2A set |

### 2.3 New A2A Agent Opcodes

Seven new opcodes for inter-agent coordination in the converged ISA:

| Hex | Name | Purpose | Semantics |
|-----|------|---------|-----------|
| **0x70** | **OP_BRANCH** | Fork execution into parallel agents | Spawns N child agents, each executing a branch of code. Parent waits at merge point. Operands: [branch_count, branch_table_offset] |
| **0x71** | **OP_MERGE** | Combine results from agents | Gathers results from completed branches. Operands: [merge_strategy, result_buffer_offset]. Strategies: FIRST, BEST_CONF, CONSENSUS, WEIGHTED |
| **0x72** | **OP_DISCUSS** | Structured agent discussion | Multi-round deliberation. Operands: [round_count, topic_ref, participant_mask]. Returns final consensus value |
| **0x73** | **OP_DELEGATE** | Push subtask to agent | (Extends existing DELEGATE with wait-for-result semantics) Operands: [agent_id, task_offset, timeout] |
| **0x74** | **OP_CONFIDENCE** | Set/query confidence | Push/pop confidence level. Range 0.0–1.0. Operands: [level]. Affects downstream merge decisions. |
| **0x75** | **OP_CAP_REQUIRE** | Capability requirement check | (Already exists at 0x65 in canonical — promoted to universal requirement). Validate agent has permission before proceeding. |
| **0x76** | **OP_META** | Self-referential opcode | The VM modifying its own opcodes at runtime. Operands: [old_opcode, new_opcode, scope]. Enables agents to redefine instruction semantics. **Most dangerous — requires GENITIV scope or ADMINISTRATOR honorific.** |

### 2.4 Bytecode Versioning — Research Findings

| System | Versioning Strategy | Key Insight |
|--------|-------------------|-------------|
| **JVM** | Magic number `0xCAFEBABE` + major.minor version in class file header | Old programs run on new VMs via backward compatibility. `INVOKEDYNAMIC` and `DEFAULTMETHOD` added without breaking old code. |
| **WebAssembly** | Fixed header with version + section sizes + feature flags | Wasm binary starts with magic `\0asm`. Sections declare required features. Old engines can still run programs that don't use new features. |
| **Erlang BEAM** | Module versioning + OTP release vs upgrade | Hot code loading: same module can be loaded twice, old processes keep old version. 100% backward compatible. |
| **x86** | CPUID feature flags (CPUID.EAX, CPUID.EDX, CPUID.ECX) | New instructions detected at runtime. Old binaries run unchanged on CPUs that support new instructions. |
| **FLUX Proposal** | 18-byte header with `version` field + `flags` field | Header already has version slot. Use `flags` bits for feature negotiation. |

**Recommended approach for FLUX**: **Capability-negotiated versioning**

```
Bytecode Header (18 bytes):
  [0x00-0x03] magic: b'FLUX'
  [0x04-0x05] version: uint16 LE  (1 = core, 2 = +A2A, 3 = +meta)
  [0x06-0x07] flags: uint16 LE  (bit 0 = has_float, bit 1 = has_string, bit 2 = has_topic_ops, ...)
  [0x08-0x09] n_funcs: uint16
  [0x0A-0x0D] type_off: uint32
  [0x0E-0x11] code_off: uint32
```

- VMs declare their maximum supported version via CPUID-like introspection.
- Bytecode declares its required minimum version.
- Execution proceeds if `vm_version >= bytecode_version`.
- Unknown opcodes below 0x70 are treated as **NOP** (fail-open).
- Unknown opcodes 0x70+ trigger **capability check** (fail-secure).

---

## Round 3: Implementation

### 3.1 `opcodes.py` — Universal Opcode Registry

Located at: `/home/z/my-project/repos/flux-a2a/src/flux_a2a/opcodes.py`

**Key classes**:
- `FluxOpcode(IntEnum)` — Universal opcode enumeration (canonical hex values)
- `OpcodeCategory(Enum)` — Category taxonomy (CORE, ARITHMETIC, BITWISE, etc.)
- `FluxOpcodeRegistry` — Registry with:
  - `get_by_name()`, `get_by_hex()`, `get_category()`
  - `get_runtime_mapping()` — hex translation between runtimes
  - `list_opcodes_by_category()`
  - `negotiate_version()` — version negotiation between VM and bytecode
  - `translate_instruction()` — cross-runtime bytecode translator

### 3.2 `bytecode.py` — Cross-Runtime Bytecode Tools

Located at: `/home/z/my-project/repos/flux-a2a/src/flux_a2a/bytecode.py`

**Key classes**:
- `FluxBytecodeEncoder` — Encode instructions to binary format
- `FluxBytecodeDecoder` — Decode binary to instruction stream
- `BytecodeVersion` — Version negotiation and capability detection
- `CrossRuntimeTranslator` — Translate WEN/LAT bytecode → canonical format
- `BytecodeValidator` — Validate bytecode against VM capabilities

### 3.3 Cross-Runtime Translation

The most critical piece: translating between **WEN** and **LAT** bytecode (which use non-standard hex encodings) and the canonical format:

```
WEN: RET=0x08, IADD=0x10, HALT=0x09
LAT: HALT=0x01, MOV=0x10, IADD=0x50
CAN: RET=0x28, IADD=0x08, HALT=0xFF
```

The translator performs a two-pass process:
1. **Detect source runtime** by heuristics (opcode density, magic bytes, header presence)
2. **Translate each instruction** using the runtime mapping table

### 3.4 Opcode Statistics Summary

| Category | Count (Converged) | Notes |
|----------|:------------------:|-------|
| Core (all runtimes) | 27 | Minimum shared set |
| Arithmetic (extended) | 16 | Including bitwise, float, string |
| Bitwise | 8 | IAND through ROTR |
| Comparison | 10 | ICMP, IEQ, ILT, ILE, IGT, IGE, CMP, JE, JNE, TEST |
| Stack | 8 | PUSH, POP, DUP, SWAP, ROT, ENTER, LEAVE, ALLOCA |
| Memory | 8 | REGION_*, MEM*, JL, JGE |
| Type | 5 | CAST, BOX, UNBOX, CHECK_TYPE, CHECK_BOUNDS |
| Float | 13 | Arithmetic + comparison |
| String | 5 | SLEN, SCONCAT, SCHAR, SSUB, SCMP |
| A2A (existing) | 6 | TELL, ASK, DELEGATE, BROADCAST, TRUST_CHECK, CAP_REQUIRE |
| A2A (new) | 7 | BRANCH, MERGE, DISCUSS, DELEGATE+, CONFIDENCE, CAP_REQUIRE+, META |
| Paradigm (WEN) | 16 | Topic, I Ching, Military, Confucian |
| Paradigm (LAT) | 8 | Temporal (tense-based execution) |
| Paradigm (ZHO) | 7 | Topic, Classifier, Honorific |
| Paradigm (KOR) | 2 | PHI, CAP_REQUIRE |
| **Total (converged)** | **147** | 27 core + 120 extended |

---

## Appendix: File Inventory

| File | Path | Purpose |
|------|------|---------|
| opcodes.py | `src/flux_a2a/opcodes.py` | Universal opcode registry |
| bytecode.py | `src/flux_a2a/bytecode.py` | Bytecode encoder/decoder + translator |
| This document | `docs/round1-3_opcode_convergence.md` | Research report |

## Appendix: Runtime Opcode Mapping Tables

### DEU/SAN → Canonical (identical, no translation needed)

All opcodes in DEU and SAN use the same hex values as the canonical TypeScript ISA. No translation required.

### WEN → Canonical

| WEN Hex | WEN Name | Canonical Hex | Note |
|:--------:|----------|:-----------:|:-----|
| 0x00 | NOP | 0x00 | Identical |
| 0x01 | MOV | 0x01 | Identical |
| 0x02 | LOAD | 0x02 | Identical |
| 0x03 | STORE | 0x03 | Identical |
| 0x04 | JMP | 0x04 | Identical |
| 0x05 | JZ | 0x05 | Identical |
| 0x06 | JNZ | 0x06 | Identical |
| 0x07 | CALL | 0x07 | Identical |
| 0x08 | RET | 0x28 | **MISMATCH** |
| 0x09 | HALT | 0xFF | **MISMATCH** |
| 0x0A | PRINT | 0xFE | **MISMATCH** |
| 0x10 | IADD | 0x08 | **MISMATCH** |
| 0x11 | ISUB | 0x09 | **MISMATCH** |
| 0x12 | IMUL | 0x0A | **MISMATCH** |
| 0x13 | IDIV | 0x0B | **MISMATCH** |
| 0x14 | IMOD | 0x0C | **MISMATCH** |
| 0x15 | INEG | 0x0D | **MISMATCH** |
| 0x16 | INC | 0x0E | **MISMATCH** |
| 0x17 | DEC | 0x0F | **MISMATCH** |
| 0x18 | IEQ | 0x19 | **MISMATCH** |
| 0x19 | IGT | 0x1C | **MISMATCH** |
| 0x1A | ILT | 0x1A | **MISMATCH** (same!) |
| 0x1B | ICMP | 0x18 | **MISMATCH** |
| 0x20 | PUSH | 0x20 | Identical |
| 0x21 | POP | 0x21 | Identical |
| 0x22 | MOVI | 0x2B | **MISMATCH** |
| 0x30 | JE | 0x2E | **MISMATCH** |
| 0x31 | JNE | 0x2F | **MISMATCH** |
| 0x40 | TELL | 0x60 | **MISMATCH** |
| 0x41 | ASK | 0x61 | **MISMATCH** |
| 0x42 | DELEGATE | 0x62 | **MISMATCH** |
| 0x43 | BROADCAST | 0x63 | **MISMATCH** |
| 0x50 | TRUST_CHECK | 0x64 | **MISMATCH** |
| 0x51 | CAP_REQUIRE | 0x65 | **MISMATCH** |
| 0x60 | IEXP | — | **WEN-unique** |
| 0x61 | IROOT | — | **WEN-unique** |
| 0x70 | VERIFY_TRUST | — | **WEN-unique** |
| 0x71 | CHECK_BOUNDS | — | **WEN-unique** |
| 0x72 | OPTIMIZE | — | **WEN-unique** |
| 0x80 | ATTACK | — | **WEN-unique** |
| 0x81 | DEFEND | — | **WEN-unique** |
| 0x82 | ADVANCE | — | **WEN-unique** |
| 0x83 | RETREAT | — | **WEN-unique** |
| 0x90 | SEQUENCE | — | **WEN-unique** |
| 0x91 | LOOP | — | **WEN-unique** |
| 0xA0 | HEX_JUMP | — | **WEN-unique** |
| 0xA1 | HEX_CALL | — | **WEN-unique** |
| 0xA2 | TRIGRAM_ADDR | — | **WEN-unique** |
| 0xB0 | SET_TOPIC | — | **WEN-unique** |
| 0xB1 | USE_TOPIC | — | **WEN-unique** |
| 0xB2 | CLEAR_TOPIC | — | **WEN-unique** |

### LAT → Canonical

| LAT Hex | LAT Name | Canonical Hex | Note |
|:--------:|----------|:-----------:|:-----|
| 0x00 | NOP | 0x00 | Identical |
| 0x01 | HALT | 0xFF | **MISMATCH** |
| 0x10 | MOV | 0x01 | **MISMATCH** |
| 0x11 | MOVI | 0x2B | **MISMATCH** |
| 0x20 | LOAD | 0x02 | **MISMATCH** |
| 0x21 | STORE | 0x03 | **MISMATCH** |
| 0x30 | JMP | 0x04 | **MISMATCH** |
| 0x31 | JZ | 0x05 | **MISMATCH** |
| 0x32 | JNZ | 0x06 | **MISMATCH** |
| 0x33 | JE | 0x2E | **MISMATCH** |
| 0x34 | JNE | 0x2F | **MISMATCH** |
| 0x40 | CALL | 0x07 | **MISMATCH** |
| 0x41 | RET | 0x28 | **MISMATCH** |
| 0x50 | IADD | 0x08 | **MISMATCH** |
| 0x51 | ISUB | 0x09 | **MISMATCH** |
| 0x52 | IMUL | 0x0A | **MISMATCH** |
| 0x53 | IDIV | 0x0B | **MISMATCH** |
| 0x54 | IMOD | 0x0C | **MISMATCH** |
| 0x55 | INEG | 0x0D | **MISMATCH** |
| 0x56 | INC | 0x0E | **MISMATCH** |
| 0x57 | DEC | 0x0F | **MISMATCH** |
| 0x60 | PUSH | 0x20 | **MISMATCH** |
| 0x61 | POP | 0x21 | **MISMATCH** |
| 0x70 | CMP | 0x2D | **MISMATCH** |
| 0x80 | PRINT | 0xFE | **MISMATCH** |
| 0x81 | TELL | 0x60 | **MISMATCH** |
| 0x82 | ASK | 0x61 | **MISMATCH** |
| 0x83 | BROADCAST | 0x63 | **MISMATCH** |
| 0x90 | DELEGATE | 0x62 | **MISMATCH** |
| 0x91 | TRUST_CHECK | 0x64 | **MISMATCH** |
| 0x92 | CAP_REQUIRE | 0x65 | **MISMATCH** |
| 0xA0 | LOOP_START | — | **LAT-unique** |
| 0xA1 | LOOP_END | — | **LAT-unique** |
| 0xA2 | LAZY_DEFER | — | **LAT-unique** |
| 0xA3 | CACHE_LOAD | — | **LAT-unique** |
| 0xA4 | CACHE_STORE | — | **LAT-unique** |
| 0xA5 | ROLLBACK_SAVE | — | **LAT-unique** |
| 0xA6 | ROLLBACK_RESTORE | — | **LAT-unique** |
| 0xA7 | EVENTUAL_SCHEDULE | — | **LAT-unique** |
