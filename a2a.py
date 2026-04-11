"""
FLUX A2A Protocol — Agent-to-Agent Communication Reference Implementation.

Implements the A2A layer on top of FLUX bytecodes:
- Agents exchange messages via FLUX A2A opcodes
- Messages are typed, routed, and acknowledged
- Supports broadcast, direct, and pub/sub patterns
"""
import json
import time
import hashlib
from enum import IntEnum
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any, Callable


class A2AType(IntEnum):
    """A2A message types (matching ISA opcodes 0x50-0x5F)."""
    TELL = 0x50      # Broadcast to all
    ASK = 0x51       # Direct question
    REPLY = 0x52     # Answer to ASK
    BCAST = 0x53     # Network broadcast
    FORK = 0x54      # Spawn sub-agent
    JOIN = 0x55      # Wait for sub-agent
    SYNC = 0x56      # Synchronize state
    VOTE = 0x57      # Cast vote
    PROPOSE = 0x58   # Propose change
    MERGE = 0x59     # Merge results


@dataclass
class A2AMessage:
    """A2A protocol message."""
    msg_type: A2AType
    sender: str
    recipient: str  # "fleet" for broadcast
    payload: Dict[str, Any]
    msg_id: str = ""
    in_reply_to: str = ""
    timestamp: float = 0.0
    ttl: int = 10  # hops remaining
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.time()
        if not self.msg_id:
            content = f"{self.sender}:{self.recipient}:{self.msg_type}:{self.timestamp}"
            self.msg_id = hashlib.sha256(content.encode()).hexdigest()[:16]


@dataclass
class AgentProfile:
    """Agent capability profile for routing."""
    name: str
    capabilities: List[str]
    interests: List[str]  # topics this agent cares about
    max_concurrent: int = 5
    current_load: int = 0


class A2ARouter:
    """Routes messages between agents based on capabilities and interests."""
    
    def __init__(self):
        self.agents: Dict[str, AgentProfile] = {}
        self.handlers: Dict[str, List[Callable]] = {}
        self.mailbox: Dict[str, List[A2AMessage]] = {}
        self.message_log: List[A2AMessage] = []
    
    def register(self, profile: AgentProfile):
        """Register an agent with the router."""
        self.agents[profile.name] = profile
        self.mailbox[profile.name] = []
    
    def send(self, msg: A2AMessage) -> bool:
        """Send a message through the router."""
        self.message_log.append(msg)
        
        if msg.recipient == "fleet":
            # Broadcast to all registered agents
            delivered = 0
            for name, profile in self.agents.items():
                if name != msg.sender:
                    if self._matches_interest(msg, profile):
                        self.mailbox[name].append(msg)
                        delivered += 1
            return delivered > 0
        else:
            # Direct message
            if msg.recipient in self.mailbox:
                self.mailbox[msg.recipient].append(msg)
                return True
            return False
    
    def receive(self, agent_name: str) -> List[A2AMessage]:
        """Get pending messages for an agent."""
        msgs = self.mailbox.get(agent_name, [])
        self.mailbox[agent_name] = []
        return msgs
    
    def _matches_interest(self, msg: A2AMessage, profile: AgentProfile) -> bool:
        """Check if a message matches an agent's interests."""
        for key in msg.payload:
            if key in profile.interests or key in profile.capabilities:
                return True
        # Default: accept all broadcasts
        return True
    
    def find_agent_for(self, capability: str) -> Optional[str]:
        """Find the best agent for a capability (lowest load)."""
        candidates = []
        for name, profile in self.agents.items():
            if capability in profile.capabilities and profile.current_load < profile.max_concurrent:
                candidates.append((profile.current_load, name))
        
        if not candidates:
            return None
        candidates.sort()
        return candidates[0][1]
    
    def route_to_capability(self, capability: str, msg: A2AMessage) -> bool:
        """Route a message to the agent best suited for a capability."""
        agent = self.find_agent_for(capability)
        if agent:
            msg.recipient = agent
            return self.send(msg)
        return False
    
    def get_stats(self) -> dict:
        """Return routing statistics."""
        return {
            "agents": len(self.agents),
            "total_messages": len(self.message_log),
            "pending": sum(len(m) for m in self.mailbox.values()),
        }


class A2AClient:
    """Client-side A2A interface for a single agent."""
    
    def __init__(self, profile: AgentProfile, router: A2ARouter):
        self.profile = profile
        self.router = router
        self.router.register(profile)
    
    def tell(self, payload: dict, recipient: str = "fleet") -> bool:
        msg = A2AMessage(
            msg_type=A2AType.TELL,
            sender=self.profile.name,
            recipient=recipient,
            payload=payload,
        )
        return self.router.send(msg)
    
    def ask(self, question: str, recipient: str) -> str:
        msg = A2AMessage(
            msg_type=A2AType.ASK,
            sender=self.profile.name,
            recipient=recipient,
            payload={"question": question},
        )
        self.router.send(msg)
        return msg.msg_id
    
    def reply(self, original_id: str, answer: dict, recipient: str) -> bool:
        msg = A2AMessage(
            msg_type=A2AType.REPLY,
            sender=self.profile.name,
            recipient=recipient,
            payload=answer,
            in_reply_to=original_id,
        )
        return self.router.send(msg)
    
    def poll(self) -> List[A2AMessage]:
        return self.router.receive(self.profile.name)


# ── Tests ──────────────────────────────────────────────

import unittest


class TestA2AMessage(unittest.TestCase):
    def test_create(self):
        msg = A2AMessage(msg_type=A2AType.TELL, sender="a", recipient="b", payload={"x": 1})
        self.assertTrue(msg.msg_id)
        self.assertGreater(msg.timestamp, 0)
    
    def test_unique_ids(self):
        m1 = A2AMessage(msg_type=A2AType.TELL, sender="a", recipient="b", payload={})
        m2 = A2AMessage(msg_type=A2AType.TELL, sender="a", recipient="b", payload={})
        self.assertNotEqual(m1.msg_id, m2.msg_id)


class TestA2ARouter(unittest.TestCase):
    def setUp(self):
        self.router = A2ARouter()
        self.router.register(AgentProfile("oracle1", ["coordination"], ["fleet"]))
        self.router.register(AgentProfile("jetsonclaw1", ["cuda", "sensor"], ["hardware"]))
    
    def test_register(self):
        self.assertEqual(len(self.router.agents), 2)
    
    def test_direct_message(self):
        msg = A2AMessage(msg_type=A2AType.TELL, sender="oracle1", recipient="jetsonclaw1", payload={"task": "benchmark"})
        self.assertTrue(self.router.send(msg))
        msgs = self.router.receive("jetsonclaw1")
        self.assertEqual(len(msgs), 1)
    
    def test_broadcast(self):
        msg = A2AMessage(msg_type=A2AType.TELL, sender="oracle1", recipient="fleet", payload={"alert": "test"})
        self.router.send(msg)
        msgs = self.router.receive("jetsonclaw1")
        self.assertEqual(len(msgs), 1)
    
    def test_find_agent(self):
        agent = self.router.find_agent_for("cuda")
        self.assertEqual(agent, "jetsonclaw1")
    
    def test_find_agent_no_match(self):
        agent = self.router.find_agent_for("underwater-welding")
        self.assertIsNone(agent)
    
    def test_route_to_capability(self):
        msg = A2AMessage(msg_type=A2AType.ASK, sender="oracle1", recipient="", payload={"question": "cuda benchmark?"})
        self.assertTrue(self.router.route_to_capability("cuda", msg))
        msgs = self.router.receive("jetsonclaw1")
        self.assertEqual(len(msgs), 1)
    
    def test_stats(self):
        stats = self.router.get_stats()
        self.assertEqual(stats["agents"], 2)
        self.assertEqual(stats["total_messages"], 0)
    
    def test_poll_clears_mailbox(self):
        msg = A2AMessage(msg_type=A2AType.TELL, sender="oracle1", recipient="jetsonclaw1", payload={})
        self.router.send(msg)
        self.router.receive("jetsonclaw1")
        msgs2 = self.router.receive("jetsonclaw1")
        self.assertEqual(len(msgs2), 0)


class TestA2AClient(unittest.TestCase):
    def setUp(self):
        self.router = A2ARouter()
        self.o1 = A2AClient(AgentProfile("oracle1", ["coord"], ["fleet"]), self.router)
        self.jc1 = A2AClient(AgentProfile("jetsonclaw1", ["cuda"], ["hardware"]), self.router)
    
    def test_tell(self):
        self.assertTrue(self.o1.tell({"status": "active"}))
    
    def test_ask_reply(self):
        qid = self.o1.ask("cuda available?", "jetsonclaw1")
        msgs = self.jc1.poll()
        self.assertEqual(len(msgs), 1)
        self.assertTrue(self.jc1.reply(qid, {"answer": "yes"}, "oracle1"))
    
    def test_broadcast_receive(self):
        self.o1.tell({"alert": "fleet meeting"})
        msgs = self.jc1.poll()
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0].payload["alert"], "fleet meeting")


if __name__ == "__main__":
    unittest.main(verbosity=2)
