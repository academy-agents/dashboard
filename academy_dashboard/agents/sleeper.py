from __future__ import annotations

import asyncio
import logging

from academy.agent import loop
from academy.handle import Handle

from academy_dashboard.monitored_agent import MonitoredAgent
from academy_dashboard.user_agent.user_agent import UserAgent


class Sleeper(MonitoredAgent):
    """An Agent that sleeps."""

    def __init__(self, user_agent_handle: Handle[UserAgent]) -> None:
        super().__init__(user_agent_handle=user_agent_handle)
        print('Spinner init done')

    @loop
    async def cycle(self, shutdown: asyncio.Event) -> None:
        """Log and sleep in loop."""
        counter = 0
        while not shutdown.is_set():
            await asyncio.sleep(30)
            logging.info('Sleeper iteration %d', counter)
            counter += 1
        logging.info('Sleeper exiting!!!! ')
