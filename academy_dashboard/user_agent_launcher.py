"""Launch the User Agent in local threads and wait."""

from __future__ import annotations

import argparse
import asyncio
import logging
import pickle
from pathlib import Path
from uuid import UUID

import aiohttp
from academy.exchange.cloud.client import HttpExchangeFactory
from academy.exchange.transport import AgentRegistration
from academy.runtime import Runtime
from academy.runtime import RuntimeConfig

from academy_dashboard.user_agent.user_agent import UserAgent


def load_registation(registration_path: Path) -> dict[str, UUID | AgentRegistration]:
    """Load registration info from a file."""
    if registration_path.exists():
        with open(registration_path, 'rb') as f:
            return pickle.load(f)
    else:
        return {}


def save_registation(
    registration_path: Path,
    agent_registration: AgentRegistration,
    agent_id: UUID,
) -> None:
    """Write registration info to file."""
    registration_info = {
        'agent_registration': agent_registration,
        'agent_id': agent_id,
    }
    with open(registration_path, 'wb') as f:
        pickle.dump(registration_info, f)


async def launch(port: int, registration_file: Path, log_level: str = 'WARNING') -> None:
    """Launch UserAgent in ThreadPoolExecutor and write Agent UUID info to file."""
    agent_info = load_registation(registration_file)

    log_level_int = logging.getLevelName(log_level)
    # Configure the log stream to output to a file and the console
    logging.basicConfig(
        level=log_level_int,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(),
        ],
    )

    # Todo: Logging is messed up when no manager is available to handle LogConfig objects

    factory = HttpExchangeFactory(
        client_timeout=aiohttp.ClientTimeout(total=None, sock_connect=30),
    )

    if not agent_info:
        async with await factory.create_user_client() as client:
            registration = await client.register_agent(UserAgent)
    else:
        registration = agent_info['agent_registration']

    agent = UserAgent(port=port)
    runtime = Runtime(
        agent=agent,
        exchange_factory=factory,
        registration=registration,
        config=RuntimeConfig(
            terminate_on_error=False,
            terminate_on_success=False,
        ),
    )
    agent_id = runtime.agent_id.uid

    print(f'\033[38;5;129mUser Agent UUID >>>> \n     {agent_id!s}\033[0m')

    if not agent_info:
        save_registation(registration_file, registration, agent_id)

    return await runtime.run_until_complete()


def main() -> None:
    """Entry point for the user-agent-launcher command."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--port',
        default=8000,
        type=int,
        help='Port at which the flask service is listening',
    )
    parser.add_argument(
        '-r',
        '--registration_file',
        default=Path('user_agent_registration.pkl'),
        type=Path,
        help='UserAgent registration file',
    )
    parser.add_argument(
        '-l',
        '--log_level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Log level',
    )
    args = parser.parse_args()
    asyncio.run(
        launch(
            port=args.port,
            registration_file=args.registration_file,
            log_level=args.log_level,
        ),
    )


if __name__ == '__main__':
    main()
