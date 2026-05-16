"""UserAgent that receives messages from monitored agents and drives the dashboard."""

from __future__ import annotations

import asyncio
import logging
import uuid
from typing import Any

from academy.agent import action
from academy.agent import Agent
from academy.identifier import AgentId

from academy_nexus.user_agent.dashboard import Dashboard
from academy_nexus.user_agent.message import Log
from academy_nexus.user_agent.message import Message
from academy_nexus.user_agent.message import Registration
from academy_nexus.user_agent.message import Stats
from academy_nexus.user_agent.message import UserPrompt

logger = logging.getLogger(__name__)


class UserAgent(Agent):
    """Receives messages from MonitoredAgents and serves a live web dashboard."""

    def __init__(
        self,
        host: str = '0.0.0.0',
        port: int = 8000,
        base_url: str = '',
    ) -> None:
        super().__init__()
        self.base_url = base_url
        self.host = host
        self.port = port
        logger.info(f'Starting user agent on Port: {port}')

    async def agent_on_startup(self) -> None:
        """Start the Flask dashboard on startup."""
        loop = asyncio.get_event_loop()
        formatted_base_url = self.base_url.format(
            agent_id=self.agent_id.uid,
            port=self.port,
        )
        self._dashboard = Dashboard(
            host=self.host,
            port=self.port,
            base_url=formatted_base_url,
        )

        def _shutdown_callback(agent_id: str) -> None:
            asyncio.run_coroutine_threadsafe(
                self._agent_manager.get_handle(
                    AgentId(uid=uuid.UUID(agent_id)),
                ).shutdown(),
                loop,
            )

        self._dashboard.set_shutdown_callback(_shutdown_callback)
        self._dashboard.start()
        logger.info('Starting dashboard')

    @action
    async def message(self, sender: str, message: Message) -> None:
        """Route an incoming message to the appropriate dashboard handler.

        sender: Agent ID UUID string
        message: Message object
        """
        self._dashboard.agent_heartbeat(sender)
        if isinstance(message, Log):
            self._dashboard.push_log(sender, message)
        elif isinstance(message, Stats):
            self._dashboard.push_stats(sender, message)
        elif isinstance(message, Registration):
            self._dashboard.register_agent(sender, message)

    @action
    async def prompt_user(
        self,
        sender: str,
        user_prompt: UserPrompt,
    ) -> str:
        """Prompt the user for a response and block until the user selects one."""
        loop = asyncio.get_event_loop()
        prompt_id = self._dashboard.push_prompt(sender, user_prompt)
        return await loop.run_in_executor(
            None,
            self._dashboard.wait_for_response,
            prompt_id,
        )

    @action
    async def get_messages(self) -> dict[str, Any]:
        """Return a snapshot of the current dashboard state."""
        return self._dashboard._snapshot()
