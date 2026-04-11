# FLUX A2A — Agent-to-Agent Protocol

Reference implementation of the A2A communication layer.

## Components
- **A2AMessage**: Typed messages (TELL/ASK/REPLY/BCAST/FORK/JOIN/SYNC/VOTE/PROPOSE/MERGE)
- **A2ARouter**: Routes messages based on capabilities and interests
- **A2AClient**: Client-side interface for send/receive/poll
- **AgentProfile**: Capability and interest registration

## Usage

```python
from a2a import A2AClient, AgentProfile, A2ARouter

router = A2ARouter()
oracle1 = A2AClient(AgentProfile("oracle1", ["coordination"], ["fleet"]), router)
jetsonclaw1 = A2AClient(AgentProfile("jetsonclaw1", ["cuda"], ["hardware"]), router)

# Direct question
qid = oracle1.ask("cuda available?", "jetsonclaw1")
msgs = jetsonclaw1.poll()
jetsonclaw1.reply(qid, {"answer": "yes"}, "oracle1")

# Broadcast
oracle1.tell({"status": "fleet meeting in 5 min"})
```

13 tests passing.
