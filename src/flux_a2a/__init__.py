"""
FLUX-A2A Signal Protocol — Agent-to-Agent First-Class JSON Language.

Signal is the inter-agent communication layer for the FLUX multilingual
ecosystem. JSON is the universal AST, not just a serialization format.
Every expression, branch, fork, and co-iteration is a JSON primitive.

Usage:
    from flux_a2a import interpret, evaluate, compile_program
    from flux_a2a.schema import Program, Expression, Agent, Result

    program = Program.from_dict({...})
    result = interpret(program)
"""

__version__ = "0.1.0"
__all__ = [
    # Schema
    "LanguageTag",
    "ProgramMeta",
    "Agent",
    "TrustEntry",
    "Expression",
    "BranchDef",
    "ForkDef",
    "CoIterateDef",
    "MergePolicy",
    "ConflictResolution",
    "Program",
    "Message",
    "MessageBus",
    "Result",
    "ConfidenceScore",
    # Interpreter
    "Interpreter",
    "interpret",
    "evaluate",
    # Compiler
    "Compiler",
    "compile_program",
    "BytecodeChunk",
    # Co-iteration
    "SharedProgram",
    "AgentCursor",
    "CoIterationEngine",
    "ConflictResolutionStrategy",
    "MergeStrategy",
    # Forking
    "BranchPoint",
    "ForkContext",
    "BranchManager",
    "ForkTree",
    "ForkManager",
    "MergePolicyType",
]

from flux_a2a.schema import (
    Agent,
    BranchDef,
    CoIterateDef,
    ConflictResolution,
    ConfidenceScore,
    Expression,
    ForkDef,
    LanguageTag,
    MergePolicy,
    Message,
    MessageBus,
    Program,
    ProgramMeta,
    Result,
    TrustEntry,
)
from flux_a2a.interpreter import Interpreter, evaluate, interpret
from flux_a2a.compiler import BytecodeChunk, Compiler, compile_program
from flux_a2a.co_iteration import (
    AgentCursor,
    CoIterationEngine,
    ConflictResolutionStrategy,
    MergeStrategy,
    SharedProgram,
)
from flux_a2a.fork_manager import (
    BranchManager,
    BranchPoint,
    ForkContext,
    ForkManager,
    ForkTree,
    MergePolicyType,
)
