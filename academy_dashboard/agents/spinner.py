from __future__ import annotations

import asyncio
import logging

from academy.agent import action
from academy.handle import Handle

from academy_dashboard.monitored_agent import MonitoredAgent
from academy_dashboard.user_agent.user_agent import UserAgent


class Spinner(MonitoredAgent):
    """A concrete MonitoredAgent that does some work and reports progress."""

    def __init__(self, user_agent_handle: Handle[UserAgent]) -> None:
        super().__init__(user_agent_handle=user_agent_handle)
        print('Spinner init done')

    @action
    async def run(self, iterations: int = 3) -> str:
        """Simulate work and emit log messages that are forwarded to UserAgent."""
        logging.info('Starting run!')
        for i in range(iterations):
            logging.info(
                f'{self.agent_name} iteration %d/%d',
                i + 1,
                iterations,
            )
            await asyncio.sleep(10)
        logging.warning('Finishing run!')
        return f'Finished {iterations} iterations'

    @action
    async def poke(self) -> int:
        """Mock action that emits a log."""
        logging.warning('I just got Poked!')
        return 4

    @action
    async def trigger_user_query(self) -> None:
        """Trigger a user query."""
        logging.info('Triggering user query!')
        response = await self.prompt_user_agent(
            'Should I continue?',
            responses=['Yes', 'No'],
        )
        try:
            _ = 5 / 0
        except ZeroDivisionError:
            logging.exception('Something went wrong!')
        logging.info(f'Got response: {response} from user query')
