# ISA Mapping Analysis: A2A Opcodes vs. Oracle1 FORMAT Specification

**Author:** Babel (FLUX multilingual scout agent)
**Date:** 2025-01
**Status:** PROPOSED — A2A opcodes MUST yield to FORMAT spec

---

## Executive Summary

Oracle1's unified FORMAT specification defines **CONF_\*** opcodes at `0x60-0x69` (Format E),
which directly collide with flux-a2a's existing A2A protocol opcodes (TELL, ASK, DELEGATE, etc.)
currently occupying `0x60-0x6F`. Additionally, A2A-extended ops at `0x70-0x7F` are in an
unsafe zone adjacent to FORMAT's memory/control region. **All A2A and paradigm opcodes must be
relocated** to the unused `0xD0-0xFD` range to avoid byte-level conflicts.

---

## 1. Conflict Matrix

Byte-level conflict analysis between A2A opcode space and FORMAT opcode space.

### 1.1 Critical Conflicts (0x60-0x69)

| Byte | A2A (old)           | FORMAT (Oracle1)     | Severity |
|------|---------------------|----------------------|----------|
| 0x60 | TELL                | CONF_ADD             | **FATAL** |
| 0x61 | ASK                 | CONF_SUB             | **FATAL** |
| 0x62 | DELEGATE            | CONF_MUL             | **FATAL** |
| 0x63 | BROADCAST           | CONF_DIV             | **FATAL** |
| 0x64 | TRUST_CHECK         | CONF_FADD            | **FATAL** |
| 0x65 | CAP_REQUIRE         | CONF_FSUB            | **FATAL** |
| 0x66 | *(unused)*          | CONF_FMUL            | CONFLICT (future) |
| 0x67 | *(unused)*          | CONF_FDIV            | CONFLICT (future) |
| 0x68 | *(unused)*          | CONF_MERGE           | CONFLICT (future) |
| 0x69 | *(unused)*          | CONF_THRESHOLD       | CONFLICT (future) |

### 1.2 Adjacency Risk Zone (0x6A-0x7F)

| Byte | A2A (old)           | FORMAT (Oracle1)     | Severity |
|------|---------------------|----------------------|----------|
| 0x6A-0x6F | *(unused)*    | *(unassigned by FORMAT)* | LOW (padding) |
| 0x70 | OP_BRANCH           | *(FORMAT gap)*        | MEDIUM (in FORMAT E zone) |
| 0x71 | OP_MERGE            | *(FORMAT gap)*        | MEDIUM |
| 0x72 | OP_DISCUSS          | *(FORMAT gap)*        | MEDIUM |
| 0x73 | OP_DELEGATE         | *(FORMAT gap)*        | MEDIUM |
| 0x74 | OP_CONFIDENCE       | *(FORMAT gap)*        | MEDIUM |
| 0x75 | *(skipped)*         | *(FORMAT gap)*        | LOW |
| 0x76 | OP_META             | *(FORMAT gap)*        | MEDIUM |
| 0x77-0x7F | *(unused)*    | *(FORMAT may extend)* | MEDIUM |

### 1.3 Paradigm/Topic Overlap Check (0x80-0xB7)

| Byte | A2A Paradigm (old)    | FORMAT (Oracle1)     | Severity |
|------|------------------------|----------------------|----------|
| 0x80 | IEXP                   | *(none assigned)*    | NONE |
| 0x81 | IROOT                  | *(none assigned)*    | NONE |
| 0x82-0x8A | WEN paradigm ops   | *(none assigned)*    | NONE |
| 0xA0-0xA7 | LAT temporal ops  | *(none assigned)*    | NONE |
| 0xB0-0xB2 | Topic register    | *(none assigned)*    | NONE |

### 1.4 System Opcodes

| Byte | A2A            | FORMAT              | Severity |
|------|----------------|---------------------|----------|
| 0xFE | PRINT          | PRINT (implied)     | NONE (shared) |
| 0xFF | HALT           | HALT (Format A)     | NONE (shared) |

---

## 2. Overlap Analysis: Base Opcodes (0x00-0x5F)

Analyzing whether A2A base opcodes in `0x00-0x5F` overlap with FORMAT slots even
when names differ.

### 2.1 Semantic Mapping (Same Byte, Different Name)

| Byte | A2A Name     | FORMAT Name    | Semantically Equivalent? | Action    |
|------|--------------|----------------|--------------------------|-----------|
| 0x00 | NOP          | HALT (Fmt A:0) | **NO — opposite!**       | WARNING   |
| 0x00 | NOP          | NOP (Fmt A:1)  | YES                      | No action |
| 0x01 | MOV          | NOP (Fmt A)    | No                       | N/A       |
| 0x02 | LOAD         | RET (Fmt A:2)  | No                       | N/A       |
| 0x03 | STORE        | IRET (Fmt A:3) | No                       | N/A       |
| 0x05 | JZ           | PUSH (Fmt B:4) | No                       | N/A       |
| 0x06 | JNZ          | POP (Fmt B:5)  | No                       | N/A       |
| 0x0E | INC          | INC (Fmt B:0)  | YES                      | No action |
| 0x0F | DEC          | DEC (Fmt B:1)  | YES                      | No action |
| 0x13 | INOT         | NOT (Fmt B:2)  | YES                      | No action |
| 0x0D | INEG         | NEG (Fmt B:3)  | YES                      | No action |
| 0x20 | PUSH         | ADD (Fmt E)    | No                       | N/A       |
| 0x21 | POP          | SUB (Fmt E)    | No                       | N/A       |
| 0x2B | MOVI         | MOVI (Fmt D:0) | YES (same semantics)     | No action |

### 2.2 Key Observation

The FORMAT spec uses a **format-tagged** encoding where the top bits determine which
decode format (A-G) applies. This means FORMAT opcodes are not purely byte-mapped the
way A2A opcodes are — FORMAT bytes are interpreted through format-specific decoders.

**Critical:** The FORMAT conflict at `0x60-0x69` is **real** because Oracle1 assigns
these bytes specifically to CONF_* operations regardless of format decode. A2A opcodes
at `0x60-0x6F` MUST be relocated.

For `0x00-0x5F`, the FORMAT format-tagged system means there is no direct byte collision
— different FORMATs reuse the same byte values with different decode widths. However,
the A2A single-byte encoding system is incompatible with FORMAT's multi-format scheme
at these addresses, and any future convergence must use the FORMAT encoding for the
base ISA range.

---

## 3. Relocation Proposal

### 3.1 New Opcode Map for A2A and Paradigm Opcodes

All relocated ops move to `0xD0-0xFD`, a clean range unused by both A2A (old) and FORMAT.

| Range     | Category         | Count | Old Range   | New Range   |
|-----------|------------------|-------|-------------|-------------|
| 0xD0-0xD5 | A2A existing     | 6     | 0x60-0x65   | 0xD0-0xD5  |
| 0xD6-0xDB | A2A extended     | 6     | 0x70-0x76   | 0xD6-0xDB  |
| 0xDC-0xE6 | WEN paradigm     | 11    | 0x80-0x8A   | 0xDC-0xE6  |
| 0xE7-0xEE | LAT paradigm     | 8     | 0xA0-0xA7   | 0xE7-0xEE  |
| 0xEF-0xF1 | Topic register   | 3     | 0xB0-0xB2   | 0xEF-0xF1  |
| 0xF2-0xFD | Future reserve   | 12    | *(new)*     | 0xF2-0xFD  |

### 3.2 Detailed Relocation Table

#### A2A Existing (0xD0-0xD5)

| New Byte | Old Byte | Opcode       | Description                     |
|----------|----------|--------------|---------------------------------|
| 0xD0     | 0x60     | TELL         | Send one-way message to agent   |
| 0xD1     | 0x61     | ASK          | Question/request to agent       |
| 0xD2     | 0x62     | DELEGATE     | Transfer task to agent          |
| 0xD3     | 0x63     | BROADCAST    | Announce to all agents          |
| 0xD4     | 0x64     | TRUST_CHECK  | Verify trust relationship       |
| 0xD5     | 0x65     | CAP_REQUIRE  | Require capability              |

#### A2A Extended (0xD6-0xDB)

| New Byte | Old Byte | Opcode          | Description                        |
|----------|----------|-----------------|------------------------------------|
| 0xD6     | 0x70     | OP_BRANCH       | Fork execution into parallel paths |
| 0xD7     | 0x71     | OP_MERGE        | Combine results from agents        |
| 0xD8     | 0x72     | OP_DISCUSS      | Structured multi-round discussion  |
| 0xD9     | 0x73     | OP_DELEGATE     | Delegate with wait-for-result      |
| 0xDA     | 0x74     | OP_CONFIDENCE   | Set/query confidence level         |
| 0xDB     | 0x76     | OP_META         | VM modifies own opcodes            |

#### WEN Paradigm (0xDC-0xE6)

| New Byte | Old Byte | Opcode          | Description                |
|----------|----------|-----------------|----------------------------|
| 0xDC     | 0x80     | IEXP            | Exponentiation             |
| 0xDD     | 0x81     | IROOT           | Square root                |
| 0xDE     | 0x82     | VERIFY_TRUST    | Verify trust/integrity     |
| 0xDF     | 0x83     | CHECK_BOUNDS    | Validate bounds            |
| 0xE0     | 0x84     | OPTIMIZE        | Optimize path              |
| 0xE1     | 0x85     | ATTACK          | Push data                  |
| 0xE2     | 0x86     | DEFEND          | Buffer data                |
| 0xE3     | 0x87     | ADVANCE         | Advance                    |
| 0xE4     | 0x88     | RETREAT         | Back off                   |
| 0xE5     | 0x89     | SEQUENCE        | Sequential execution       |
| 0xE6     | 0x8A     | LOOP            | Loop construct             |

#### LAT Paradigm (0xE7-0xEE)

| New Byte | Old Byte | Opcode              | Description                     |
|----------|----------|---------------------|---------------------------------|
| 0xE7     | 0xA0     | LOOP_START          | Loop begin (Imperfectum)        |
| 0xE8     | 0xA1     | LOOP_END            | Loop end                        |
| 0xE9     | 0xA2     | LAZY_DEFER          | Defer computation (Futurum)     |
| 0xEA     | 0xA3     | CACHE_LOAD          | Load cached result (Perfectum)  |
| 0xEB     | 0xA4     | CACHE_STORE         | Store to cache (Perfectum)      |
| 0xEC     | 0xA5     | ROLLBACK_SAVE       | Save state (Plusquamperfectum)  |
| 0xED     | 0xA6     | ROLLBACK_RESTORE    | Restore state                   |
| 0xEE     | 0xA7     | EVENTUAL_SCHEDULE   | Schedule eventual (Fut.Exactum) |

#### Topic Register (0xEF-0xF1)

| New Byte | Old Byte | Opcode         | Description                      |
|----------|----------|----------------|----------------------------------|
| 0xEF     | 0xB0     | SET_TOPIC      | Set topic register               |
| 0xF0     | 0xB1     | USE_TOPIC      | Use topic as implicit operand    |
| 0xF1     | 0xB2     | CLEAR_TOPIC    | Clear topic register             |

#### Future Reserve (0xF2-0xFD)

Reserved for future paradigm opcodes (e.g., Korean honorifics, Sanskrit vibhakti,
German kasus, etc.) — 12 slots available.

---

## 4. Unified Opcode Table

Complete merged table: FORMAT occupies authoritative `0x00-0xCF`, A2A+paradigm occupies
relocated `0xD0-0xFF`.

### 4.1 FORMAT Authoritative Slots (0x00-0xCF)

These slots are governed by Oracle1's FORMAT spec. A2A runtimes must treat these
as reserved/authoritative.

```
0x00-0x03  Format A   HALT, NOP, RET, IRET
0x04-0x07  (gap)      Available for future format
0x08-0x0F  Format B   INC, DEC, NOT, NEG, PUSH, POP, CONF_LOAD, CONF_STORE
0x10-0x17  Format C   SYS, ..., STRIPCONF
0x18-0x1F  Format D   MOVI, ADDI, SUBI, ANDI, ORI, XORI, SHLI, SHRI
0x20-0x2F  Format E   ADD, SUB, MUL, DIV, MOD, AND, OR, XOR, SHL, SHR, MIN, MAX, CMP_EQ/LT/GT/NE
0x30-0x37  Format E   FADD, FSUB, FMUL, FDIV, FMIN, FMAX, FTOI, ITOF
0x38-0x3F  Format E   LOAD, STORE, MOV, SWP, JZ, JNZ, JLT, JGT
0x40-0x47  Format F   MOVI16, ADDI16, SUBI16, JMP, JAL
0x48-0x4F  Format G   LOADOFF, STOREOFF, LOADI
0x50-0x5F  (gap)      Available for future formats
0x60-0x69  CONF_*     CONF_ADD, CONF_SUB, CONF_MUL, CONF_DIV, CONF_FADD, CONF_FSUB, CONF_FMUL, CONF_FDIV, CONF_MERGE, CONF_THRESHOLD
0x6A-0xCF  (gap)      Future FORMAT extensions
```

### 4.2 A2A+Paradigm Relocated Slots (0xD0-0xFF)

```
0xD0     TELL              A2A: Send one-way message
0xD1     ASK               A2A: Question/request
0xD2     DELEGATE          A2A: Transfer task
0xD3     BROADCAST         A2A: Announce to all
0xD4     TRUST_CHECK       A2A: Verify trust
0xD5     CAP_REQUIRE       A2A: Require capability
0xD6     OP_BRANCH         A2A: Fork parallel paths
0xD7     OP_MERGE          A2A: Combine results
0xD8     OP_DISCUSS        A2A: Multi-round discussion
0xD9     OP_DELEGATE       A2A: Delegate with result
0xDA     OP_CONFIDENCE     A2A: Confidence level
0xDB     OP_META           A2A: Self-referential meta
0xDC     IEXP              WEN: Exponentiation
0xDD     IROOT             WEN: Square root
0xDE     VERIFY_TRUST      WEN: Verify trust/integrity
0xDF     CHECK_BOUNDS      WEN: Validate bounds
0xE0     OPTIMIZE          WEN: Optimize path
0xE1     ATTACK            WEN: Push data
0xE2     DEFEND            WEN: Buffer data
0xE3     ADVANCE           WEN: Advance
0xE4     RETREAT           WEN: Back off
0xE5     SEQUENCE          WEN: Sequential execution
0xE6     LOOP              WEN: Loop construct
0xE7     LOOP_START        LAT: Loop begin (Imperfectum)
0xE8     LOOP_END          LAT: Loop end
0xE9     LAZY_DEFER        LAT: Defer (Futurum)
0xEA     CACHE_LOAD        LAT: Load cache (Perfectum)
0xEB     CACHE_STORE       LAT: Store cache
0xEC     ROLLBACK_SAVE     LAT: Save state
0xED     ROLLBACK_RESTORE  LAT: Restore state
0xEE     EVENTUAL_SCHEDULE LAT: Eventual (Futurum Exactum)
0xEF     SET_TOPIC         Topic: Set register
0xF0     USE_TOPIC         Topic: Use register
0xF1     CLEAR_TOPIC       Topic: Clear register
0xF2-0xFD (reserved)       Future paradigm ops
0xFE     PRINT             System: Print
0xFF     HALT              System: Halt
```

---

## 5. Bridge Rules

### 5.1 Translation Direction

The bridge supports bidirectional translation:

- **Old → New** (`translate_a2a_to_format`): For migrating existing bytecode that uses
  the old 0x60-0x8A / 0xA0-0xB2 numbering to the new unified scheme.
- **New → Old** (`translate_format_to_a2a`): For debugging/inspection — mapping
  unified bytes back to their old A2A names.

### 5.2 Translation Tables

```python
# Old A2A byte → (new unified byte, Format class)
A2A_TO_FORMAT = {
    # A2A existing
    0x60: (0xD0, "A2A"),   # TELL
    0x61: (0xD1, "A2A"),   # ASK
    0x62: (0xD2, "A2A"),   # DELEGATE
    0x63: (0xD3, "A2A"),   # BROADCAST
    0x64: (0xD4, "A2A"),   # TRUST_CHECK
    0x65: (0xD5, "A2A"),   # CAP_REQUIRE
    # A2A extended
    0x70: (0xD6, "A2A"),   # OP_BRANCH
    0x71: (0xD7, "A2A"),   # OP_MERGE
    0x72: (0xD8, "A2A"),   # OP_DISCUSS
    0x73: (0xD9, "A2A"),   # OP_DELEGATE
    0x74: (0xDA, "A2A"),   # OP_CONFIDENCE
    0x76: (0xDB, "A2A"),   # OP_META
    # WEN paradigm
    0x80: (0xDC, "PARADIGM"),  # IEXP
    0x81: (0xDD, "PARADIGM"),  # IROOT
    0x82: (0xDE, "PARADIGM"),  # VERIFY_TRUST
    0x83: (0xDF, "PARADIGM"),  # CHECK_BOUNDS
    0x84: (0xE0, "PARADIGM"),  # OPTIMIZE
    0x85: (0xE1, "PARADIGM"),  # ATTACK
    0x86: (0xE2, "PARADIGM"),  # DEFEND
    0x87: (0xE3, "PARADIGM"),  # ADVANCE
    0x88: (0xE4, "PARADIGM"),  # RETREAT
    0x89: (0xE5, "PARADIGM"),  # SEQUENCE
    0x8A: (0xE6, "PARADIGM"),  # LOOP
    # LAT paradigm
    0xA0: (0xE7, "PARADIGM"),  # LOOP_START
    0xA1: (0xE8, "PARADIGM"),  # LOOP_END
    0xA2: (0xE9, "PARADIGM"),  # LAZY_DEFER
    0xA3: (0xEA, "PARADIGM"),  # CACHE_LOAD
    0xA4: (0xEB, "PARADIGM"),  # CACHE_STORE
    0xA5: (0xEC, "PARADIGM"),  # ROLLBACK_SAVE
    0xA6: (0xED, "PARADIGM"),  # ROLLBACK_RESTORE
    0xA7: (0xEE, "PARADIGM"),  # EVENTUAL_SCHEDULE
    # Topic
    0xB0: (0xEF, "PARADIGM"),  # SET_TOPIC
    0xB1: (0xF0, "PARADIGM"),  # USE_TOPIC
    0xB2: (0xF1, "PARADIGM"),  # CLEAR_TOPIC
}
```

### 5.3 Passthrough Rules

The following ranges require NO translation (they are already correct or shared):

- `0x00-0x5F`: Base opcodes (core, arithmetic, etc.) — shared namespace
- `0xFE-0xFF`: System ops (PRINT, HALT) — identical in both schemes

### 5.4 Signal JSON → FORMAT Bytecode Compilation

The bridge compiles A2A Signal primitives (tell, ask, branch, fork, co_iterate, discuss)
into sequences of unified FORMAT bytecodes:

| Signal Primitive | FORMAT Bytecode Sequence                    |
|------------------|---------------------------------------------|
| `tell`           | `0xD0 <agent_id:u16> <msg_len:u8> <msg:bytes>` |
| `ask`            | `0xD1 <agent_id:u16> <msg_len:u8> <msg:bytes>` |
| `branch`         | `0xD6 <n_paths:u8> [<path_offsets:u16>...]`    |
| `fork`           | `0xD2 <child_id:u16> <inherit_flags:u8>`       |
| `co_iterate`     | `0xD8 <n_agents:u8> <rounds:u16>`              |
| `discuss`        | `0xD8 <format:u8> <n_parts:u8> <rounds:u8>`    |

Confidence propagation uses FORMAT CONF_* ops at `0x60-0x69`:

| Confidence Operation | FORMAT Bytecode          |
|----------------------|--------------------------|
| conf_add             | `0x60 <value:f32>`       |
| conf_merge           | `0x68 <weights:bytes>`   |
| conf_threshold       | `0x69 <threshold:f32>`   |

### 5.5 Version Negotiation

The bridge embeds a version header in compiled bytecode:

```
Byte 0:    0x46 ('F') — FORMAT magic
Byte 1:    0x4C ('L') — FLUX magic
Byte 2:    version (u8) — unified spec version
Byte 3:    flags (u8)  — feature bitmask
Bytes 4+:  instruction stream
```

VMs seeing this header know the bytecode uses the **unified** (relocated) opcode scheme.
Legacy bytecode without the header uses the **old** A2A numbering and must be translated
by the bridge before execution.

---

## 6. Migration Path

1. **Phase 1 (immediate):** Bridge module handles bidirectional translation.
   All existing A2A bytecode is transparently translated at load time.
2. **Phase 2 (next release):** Compiler emits unified bytecodes natively.
   Old bytecodes are deprecated but still accepted via bridge.
3. **Phase 3 (future):** FORMAT becomes the single authoritative spec.
   A2A-specific ops are formally part of the FORMAT extension range.

---

## Appendix: Byte Occupancy Summary

```
0x00 ┌─────────────────────┐
     │   FORMAT A-G        │  Oracle1 authoritative
0x5F │   (core ISA)        │
0x60 ├─────────────────────┤  ⚠ CONFLICT ZONE (old A2A vs CONF_*)
     │   CONF_* ops        │  Oracle1 authoritative
0x69 │   (0x60-0x69)       │
0x6A ├─────────────────────┤
     │   FORMAT gap        │  Available
0xCF │                     │
0xD0 ├─────────────────────┤
     │   A2A existing      │  RELOCATED (was 0x60-0x65)
0xD5 │   (6 ops)           │
0xD6 ├─────────────────────┤
     │   A2A extended      │  RELOCATED (was 0x70-0x76)
0xDB │   (6 ops)           │
0xDC ├─────────────────────┤
     │   WEN paradigm      │  RELOCATED (was 0x80-0x8A)
0xE6 │   (11 ops)          │
0xE7 ├─────────────────────┤
     │   LAT paradigm      │  RELOCATED (was 0xA0-0xA7)
0xEE │   (8 ops)           │
0xEF ├─────────────────────┤
     │   Topic register    │  RELOCATED (was 0xB0-0xB2)
0xF1 │   (3 ops)           │
0xF2 ├─────────────────────┤
     │   Future reserve    │  12 slots
0xFD │                     │
0xFE ├─────────────────────┤
     │   System            │  PRINT, HALT (shared)
0xFF └─────────────────────┘
```
