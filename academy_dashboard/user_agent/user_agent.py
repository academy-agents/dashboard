"""UserAgent that receives messages from monitored agents and drives the dashboard."""

from __future__ import annotations

import asyncio
import contextvars
import logging
import uuid
from concurrent.futures import Future
from typing import Any

from academy.agent import action
from academy.agent import Agent
from academy.agent import loop
from academy.exchange.transport import MailboxStatus
from academy.identifier import AgentId

from academy_dashboard.user_agent.dashboard import AgentStatus
from academy_dashboard.user_agent.dashboard import Dashboard
from academy_dashboard.user_agent.message import Log
from academy_dashboard.user_agent.message import Message
from academy_dashboard.user_agent.message import Registration
from academy_dashboard.user_agent.message import Stats
from academy_dashboard.user_agent.message import UserPrompt

logger = logging.getLogger(__name__)


class UserAgent(Agent):
    """Receives messages from MonitoredAgents and serves a live web dashboard."""

    def __init__(
        self,
        host: str = '0.0.0.0',
        port: int = 8000,
        base_url: str = '',
        liveness_interval: int = 30,
    ) -> None:
        super().__init__()
        self.base_url = base_url
        self.host = host
        self.port = port
        self.liveness_interval = liveness_interval
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
        ctx = contextvars.copy_context()

        def _shutdown_callback(agent_id: str) -> None:
            done: Future[None] = Future()

            def _create_task() -> None:
                coro = self._agent_manager.get_handle(
                    AgentId(uid=uuid.UUID(agent_id)),
                ).shutdown()
                task = loop.create_task(coro, context=ctx)
                task.add_done_callback(
                    lambda t: done.set_exception(t.exception())
                    if t.exception()
                    else done.set_result(t.result()),
                )

            loop.call_soon_threadsafe(_create_task)
            try:
                done.result()
            except Exception:
                # Log and continue
                logger.exception(f'Agent[{agent_id[:4]} failed to shutdown')

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

    @loop
    async def check_liveness(self, shutdown: asyncio.Event) -> None:
        """Poll agent liveness."""
        while not shutdown.is_set():
            peer_ids = list(self._dashboard._agents)

            prompt_counts: dict[str, int] = {}
            for prompt in self._dashboard._prompts:
                prompt_counts[prompt['agent_id']] = (
                    prompt_counts.get(prompt['agent_id'], 0) + 1
                )

            for peer_id in peer_ids:
                try:
                    mailbox_status = await self.agent_exchange_client.status(
                        AgentId(uid=uuid.UUID(peer_id)),
                    )
                except Exception:
                    logger.exception('Failed to get status for agent %s', peer_id[:8])
                    continue

                agent_data = self._dashboard._agents[peer_id]

                if mailbox_status == MailboxStatus.TERMINATED:
                    new_status = AgentStatus.TERMINATED
                elif mailbox_status == MailboxStatus.ACTIVE:
                    new_status = (
                        AgentStatus.WAITING
                        if prompt_counts.get(peer_id)
                        else AgentStatus.ACTIVE
                    )
                else:
                    new_status = AgentStatus.MISSING

                if agent_data.get('status') != new_status.value:
                    self._dashboard.push_status(peer_id, new_status)

            await asyncio.sleep(self.liveness_interval)

    @action
    async def get_messages(self) -> dict[str, Any]:
        """Return a snapshot of the current dashboard state."""
        return self._dashboard._snapshot()
