"""Generate A2A protocol Agent Card JSON objects from academy agent classes."""

from __future__ import annotations

import inspect
from typing import Any
from typing import get_args
from typing import get_origin
from typing import get_type_hints

from academy.handle import Handle


def _is_handle_type(hint: Any) -> bool:
    return get_origin(hint) is Handle


def collect_methods(
    agent_class: type,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Walk MRO and collect @action and @loop methods.

    Subclass wins on conflict
    """
    actions: dict[str, Any] = {}
    loops: dict[str, Any] = {}
    seen: set[str] = set()

    for klass in agent_class.__mro__:
        for attr_name, attr_val in vars(klass).items():
            if attr_name in seen:
                continue
            method_type = getattr(attr_val, '_agent_method_type', None)
            if method_type in ('action', 'loop'):
                seen.add(attr_name)
                if method_type == 'action':
                    actions[attr_name] = attr_val
                else:
                    loops[attr_name] = attr_val

    return actions, loops


def scan_hints(hints: dict[str, Any]) -> set[str]:
    """Scan hints from method signatures."""
    found: set[str] = set()

    for param, hint in hints.items():
        if param in ('return', 'self'):
            continue
        if _is_handle_type(hint):
            args = get_args(hint)
            if args:
                found.add(args[0].__name__)
    return found


def extract_handle_targets(agent_class: type) -> list[str]:
    """Return sorted list of agent type names found in Handle[X] annotations."""
    targets: set[str] = set()

    try:
        init_hints = get_type_hints(agent_class.__init__)  # type: ignore[misc]
    except NameError:
        init_hints = {}
    targets |= scan_hints(init_hints)

    actions, _ = collect_methods(agent_class)
    for method in actions.values():
        try:
            hints = get_type_hints(method)
        except NameError:
            hints = {}
        targets |= scan_hints(hints)

    return sorted(targets)


def method_to_skill(
    name: str,
    method: Any,
    method_type: str,
    agent_class: type,
) -> dict[str, Any]:
    """Translate loop and action methods as skills."""
    skip = {'self', 'return'}
    if method_type == 'loop':
        skip.add('shutdown')
    if getattr(method, '_action_method_context', False):
        skip.add('context')

    try:
        hints = get_type_hints(method)
    except NameError:
        hints = {}

    return {
        'id': f'{agent_class.__name__}.{name}',
        'name': name,
        'description': inspect.getdoc(method) or '',
        'tags': [method_type],
        'examples': [],
        'inputModes': ['application/json'],
        'outputModes': ['application/json'],
        'x_parameters': {k: str(v) for k, v in hints.items() if k not in skip},
    }


def generate_agent_card(
    agent_class: type,
    *,
    url: str = '',
    version: str = '0.1.0',
    authentication: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return an A2A Agent Card dict for the given agent class.

    Args:
        agent_class: The agent class to introspect.
        url: URL where the agent service is hosted.
        version: Agent version string.
        authentication: A2A authentication object; defaults to no auth schemes.
    """
    actions, loops = collect_methods(agent_class)

    skills = [
        method_to_skill(name, method, 'action', agent_class)
        for name, method in actions.items()
    ] + [
        method_to_skill(name, method, 'loop', agent_class)
        for name, method in loops.items()
    ]

    return {
        'name': agent_class.__name__,
        'description': inspect.getdoc(agent_class) or '',
        'url': url,
        'version': version,
        'capabilities': {
            'streaming': False,
            'pushNotifications': False,
            'stateTransitionHistory': False,
        },
        'authentication': authentication or {'schemes': []},
        'defaultInputModes': ['application/json'],
        'defaultOutputModes': ['application/json'],
        'skills': skills,
        'x_communicates_with': extract_handle_targets(agent_class),
    }
