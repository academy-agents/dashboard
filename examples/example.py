"""Example: launch a UserAgent and a MonitoredAgent and exchange messages.

Architecture:

    +---------------+        messages        +------------+
    | MonitoredAgent| ---------------------->| UserAgent  |
    |  (worker)     |   receive_message()    |            |
    +---------------+                        +------------+
          |                                        |
          | logging.info / agent.log()             | get_messages()
          v                                        v
     forwarded automatically              inspect from client

Both agents run inside a local ProcessPoolExecutor so no remote
infrastructure is required to run this example.
"""

from __future__ import annotations

import asyncio
import logging
import os
import uuid
from concurrent.futures import ProcessPoolExecutor

from academy.exchange.cloud import HttpExchangeFactory
from academy.identifier import AgentId
from academy.manager import Manager

from academy_dashboard.agents import Sleeper
from academy_dashboard.agents import Spinner


async def main(user_agent_id: str) -> None:
    """Launch MonitoredAgents."""
    async with await Manager.from_exchange_factory(
        factory=HttpExchangeFactory(),
        executors=ProcessPoolExecutor(max_workers=8),
    ) as manager:
        # 1. Get a handle to a running UserAgent
        agent_id = AgentId(uid=uuid.UUID(user_agent_id), name='UserAgent')
        user_agent_handle = manager.get_handle(agent_id)

        # 2. Launch a few agents:
        spinner = await manager.launch(
            Spinner,
            kwargs={'user_agent_handle': user_agent_handle},
        )
        sleeper1 = await manager.launch(
            Sleeper,
            kwargs={'user_agent_handle': user_agent_handle},
        )
        sleeper2 = await manager.launch(
            Sleeper,
            kwargs={'user_agent_handle': user_agent_handle},
        )

        await spinner.trigger_user_query()
        handles = [spinner, sleeper1, sleeper2]

        # 3. Trigger work on the worker — log messages are forwarded automatically.
        await spinner.run(iterations=5)
        [handle.shutdown() for handle in handles]
        logging.info('All done!')


if __name__ == '__main__':
    user_agent_id = os.environ['USER_AGENT_ID']
    raise SystemExit(asyncio.run(main(user_agent_id)))
