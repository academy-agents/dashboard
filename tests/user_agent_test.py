from __future__ import annotations

from collections.abc import AsyncGenerator
from concurrent.futures import ThreadPoolExecutor
from unittest import mock
from unittest.mock import patch

import pytest
import pytest_asyncio
from academy.exchange import LocalExchangeFactory
from academy.manager import Manager

from academy_dashboard.user_agent import UserAgent
from academy_dashboard.user_agent.dashboard import Dashboard
from academy_dashboard.user_agent.message import Log
from academy_dashboard.user_agent.message import Registration
from academy_dashboard.user_agent.message import Stats
from academy_dashboard.user_agent.message import UserPrompt


@pytest_asyncio.fixture
async def manager() -> AsyncGenerator[Manager]:
    """Manager test fixture."""
    async with await Manager.from_exchange_factory(
        factory=LocalExchangeFactory(),
        executors=ThreadPoolExecutor(max_workers=4),
    ) as manager:
        yield manager


@pytest_asyncio.fixture
async def patched_user_agent(
    manager: Manager,
) -> AsyncGenerator[tuple[UserAgent, mock.Mock], None]:
    """UserAgent fixture with Dashboard patched."""
    mock_dashboard = mock.Mock(spec=Dashboard)
    with patch(
        'academy_dashboard.user_agent.user_agent.Dashboard',
        return_value=mock_dashboard,
    ):
        user_agent_handle = await manager.launch(UserAgent)
        yield user_agent_handle, mock_dashboard


@pytest.mark.asyncio
async def test_message(patched_user_agent):
    """Test propagation of messages from UserAgent to dashboard."""
    handle, mock_dashboard = patched_user_agent

    log = Log(
        agent_id='abc',
        agent_name='test-agent',
        message='hello',
        level='INFO',
    )
    await handle.message(sender='abc', message=log)
    mock_dashboard.push_log.assert_called_once_with('abc', log)

    stats = Stats(
        agent_id='abc',
        cpu_percent=10.0,
        memory_rss_mb=100,
        memory_vms_mb=100,
        gpu=[],
    )
    await handle.message(sender='abc', message=stats)
    mock_dashboard.push_stats.assert_called_once_with('abc', stats)

    registration = Registration(
        agent_id='abc',
        agent_name='test-agent',
        fqdn='University',
        cpu='NA',
        gpu='?',
        arch='x86_64',
        python_version='3.13.10',
        os='Linux',
        geolocation={'state': 'IL'},
    )
    await handle.message(sender='abc', message=registration)
    mock_dashboard.register_agent.assert_called_once_with('abc', registration)


@pytest.mark.asyncio
async def test_user_prompt(patched_user_agent: tuple[UserAgent, mock.Mock]):
    """Test user prompt roundtrip."""
    handle, mock_dashboard = patched_user_agent
    mock_dashboard.push_prompt.return_value = 'prompt_id'
    mock_dashboard.wait_for_response.side_effect = (
        lambda pid: 'You'
        if pid == 'prompt_id'
        else pytest.fail(f'unexpected prompt_id {pid!r}')
    )
    prompt = UserPrompt(
        agent_id='abc',
        prompt='Who are you?',
        responses=['You', 'Me'],
    )
    response = await handle.prompt_user(sender='abc', user_prompt=prompt)

    assert response == 'You'
    mock_dashboard.push_prompt.assert_called_once_with('abc', prompt)
