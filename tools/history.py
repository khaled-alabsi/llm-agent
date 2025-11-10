"""History compaction tool that uses the LLM to summarize chat history.

This tool deliberately operates ONLY on chat messages, never on the tool
definitions. It returns a compacted list of messages in the same schema
(`role`, `content`) so the agent can continue the run with reduced size.
"""

from __future__ import annotations

import json
from typing import Any, Callable, Dict, List, Optional

from core.llm import LLMClient


class HistoryTools:
    def __init__(self, llm_supplier: Callable[[], LLMClient]):
        self._llm_supplier = llm_supplier

    def summarize_history(
        self,
        messages: List[Dict[str, Any]],
        *,
        keep_last_n: int = 6,
    ) -> Dict[str, Any]:
        """Summarize the chat history while keeping the last N messages intact.

        Returns a dict with keys:
          - status: "success" or "error"
          - messages: the compacted messages (on success)
          - message: error message (on error)
        """
        if not isinstance(messages, list):
            return {"status": "error", "message": "messages must be a list"}

        # Prepare the input: we only pass role/content to the summarizer
        slim_msgs = []
        for m in messages:
            role = m.get("role")
            content = m.get("content", "")
            if not role:
                continue
            slim_msgs.append({"role": role, "content": content})

        # Keep the last N verbatim; ask LLM to compress the older part
        head = slim_msgs[:-keep_last_n] if keep_last_n > 0 else slim_msgs
        tail = slim_msgs[-keep_last_n:] if keep_last_n > 0 else []

        # No programmatic compression: we will rely on LLM instructions only.

        prompt_system = (
            "You compress chat history for an agent. Return compact messages that retain "
            "all essential goals, constraints, decisions, file paths, and commands. "
            "Preserve meaning and intent. Do not invent content. Output ONLY a JSON object "
            "with a single key 'messages' whose value is an array of {role, content}."
        )
        # Provide ONLY the head to the LLM; we will append the tail programmatically after.
        prompt_user = {
            "head": head,
            "instructions": (
                "Summarize 'head' into the fewest messages needed. "
                "Keep roles as 'system'/'user'/'assistant' only. Do not remove important user requests; "
                "condense them faithfully. Preserve goals, constraints, decisions, file paths, commands, ids, "
                "and any numeric parameters. Be terse and avoid repetition."
            ),
        }

        llm = self._llm_supplier()
        try:
            result = llm.chat(
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": json.dumps(prompt_user)},
                ],
                tools=None,
                tool_choice=None,
                temperature=0.1,
                max_tokens=800,
            )
        except Exception as exc:  # noqa: BLE001
            # Network or provider error — return a crude compacted result so the agent can continue
            summary = {
                "role": "system",
                "content": "Condensed earlier context. Key points retained; refer to prior goals and constraints.",
            }
            crude = [summary] + tail if tail else [summary]
            return {
                "status": "error",
                "message": f"LLM request failed: {exc}",
                "messages": crude,
            }

        try:
            choice = result.get("choices", [{}])[0]
            content = choice.get("message", {}).get("content", "")
            # Attempt to parse JSON object from content
            data = json.loads(content)
            msgs = data.get("messages")
            if not isinstance(msgs, list):
                raise ValueError("missing 'messages' array")
            # Sanity normalize
            clean: List[Dict[str, str]] = []
            for m in msgs:
                role = m.get("role")
                text = m.get("content", "")
                if role and isinstance(text, str):
                    clean.append({"role": role, "content": text})
            if not clean:
                raise ValueError("empty compacted history")
            # Append the tail unchanged, programmatically, to avoid reliance on prompt wording
            clean.extend(tail)
            return {"status": "success", "messages": clean}
        except Exception as exc:  # noqa: BLE001
            # Fallback: crude compaction — one summary message plus tail
            crude: List[Dict[str, str]] = [
                {
                    "role": "system",
                    "content": "Condensed earlier context. Key points retained; refer to prior goals and constraints.",
                }
            ]
            crude.extend(tail)
            return {
                "status": "error",
                "message": f"failed to parse LLM summary: {exc}",
                "messages": crude,
            }
