"""Flask dashboard for real-time monitoring of Academy agents."""

from __future__ import annotations

import contextlib
import json
import logging
import os as _os
import queue
import threading
import time
from typing import Any

from flask import Flask
from flask import request
from flask import Response
from flask import send_from_directory

from academy_nexus.user_agent.message import Log
from academy_nexus.user_agent.message import Registration
from academy_nexus.user_agent.message import Stats
from academy_nexus.user_agent.message import UserPrompt
from academy_nexus.user_agent.web_elements import _HTML

_ASSETS_DIR = _os.path.join(_os.path.dirname(__file__), 'assets')

logger = logging.getLogger(__name__)

_LOG_BUFFER_SIZE = 2000


# ---------------------------------------------------------------------------
# Dashboard state + Flask app
# ---------------------------------------------------------------------------
class Dashboard:
    """Thread-safe state store that drives the Flask SSE dashboard."""

    def __init__(
        self,
        host: str = '0.0.0.0',
        port: int = 8000,
        base_url: str = '',
    ) -> None:
        self.host = host
        self.port = port
        self.base_url = base_url
        self._agents: dict[str, dict[str, Any]] = {}
        self._logs: list[dict[str, Any]] = []
        self._prompts: list[dict[str, Any]] = []
        self._subscribers: list[queue.Queue[str]] = []
        self._lock = threading.Lock()
        self._shutdown_callback: Any = None
        self._prompt_events: dict[str, threading.Event] = {}
        self._prompt_results: dict[str, str] = {}
        self._html = _HTML.replace('__BASE_URL__', self.base_url)
        self._app = self._build_app()

    # ── public API ────────────────────────────────────────────────────────

    def start(self) -> None:
        """Start Flask in a background daemon thread."""
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        t = threading.Thread(
            target=self._app.run,
            kwargs={'host': self.host, 'port': self.port, 'threaded': True},
            daemon=True,
        )
        t.start()

    def agent_heartbeat(self, sender: str) -> None:
        """Send agent heartbeat."""
        with self._lock:
            if sender not in self._agents:
                self._agents[sender] = {'last_seen': time.time()}
        self._broadcast('agent_connected', {'agent': sender})

    def _find_facility_logo(self, org: str, fqdn: str) -> str | None:
        """Return /assets/<filename> if any logo file keyword matches org.

        We ignore fqdn for now.
        """
        if not _os.path.isdir(_ASSETS_DIR):
            return None
        for fname in sorted(_os.listdir(_ASSETS_DIR)):
            fname_no_suffix = fname.split('.')[0]
            if fname_no_suffix == org:
                return f'/assets/{fname}'
        return '/assets/logo-Academy-2025-200x200-dark-bg.png'

    def register_agent(self, sender: str, reg: Registration) -> None:
        """Register agent."""
        raw = dict(reg.geolocation)  # copy so we can mutate
        # ipinfo.io returns location as "lat,lon" in a single 'loc' field.
        # Normalise to separate float keys so the JS can use d.geo.lat directly.
        if 'loc' in raw and 'lat' not in raw:
            try:
                lat_str, lon_str = raw['loc'].split(',')
                raw['lat'] = float(lat_str)
                raw['lon'] = float(lon_str)
            except (ValueError, AttributeError):
                pass
        geo = raw if raw.get('lat') else None
        org = raw.get('org', '')
        # Include ipinfo hostname alongside fqdn so logo matching has more signal.
        search_fqdn = f'{reg.fqdn} {raw.get("hostname", "")}'
        logo_url = self._find_facility_logo(org, search_fqdn)
        data: dict[str, Any] = {
            'agent': sender,
            'agent_name': reg.agent_name,
            'agent_id': reg.agent_id,
            'fqdn': reg.fqdn,
            'cpu': reg.cpu,
            'os': reg.os,
            'arch': reg.arch,
            'python_version': reg.python_version,
            'last_seen': time.time(),
            'geo': geo,
            'org': org,
            'logo_url': logo_url,
        }
        logger.info(
            'Registering %s[%s] from (%s)',
            data['agent_name'],
            data['agent_id'][:4],
            data['org'],
        )
        with self._lock:
            self._agents.setdefault(sender, {}).update(data)
        self._broadcast('registration', data)

    def push_log(self, sender: str, msg: Log) -> None:
        """Append a log entry from an agent and broadcast it to subscribers."""
        logger.debug('Pushing log %s %s')
        entry: dict[str, Any] = {
            'ts': time.strftime('%H:%M:%S'),
            'agent_name': msg.agent_name,
            'agent_id': str(msg.agent_id),
            'level': msg.level,
            'message': msg.message,
        }
        with self._lock:
            self._logs.append(entry)
            if len(self._logs) > _LOG_BUFFER_SIZE:
                self._logs = self._logs[-_LOG_BUFFER_SIZE:]
        self._broadcast('log', entry)

    def push_stats(self, sender: str, stats: Stats) -> None:
        """Update an agent's resource stats and broadcast to subscribers."""
        data: dict[str, Any] = {
            'agent': sender,
            'cpu_percent': stats.cpu_percent,
            'memory_rss_mb': round(stats.memory_rss_mb, 1),
            'memory_vms_mb': round(stats.memory_vms_mb, 1),
            'gpu_stats': stats.gpu,
            'last_seen': time.time(),
        }
        with self._lock:
            self._agents.setdefault(sender, {}).update(data)
        self._broadcast('stats', data)

    def push_prompt(
        self,
        sender: str,
        prompt: UserPrompt,
    ) -> str:
        """Broadcast a user-prompt request and return its ID for polling."""
        agent_name = self._agents[sender]['agent_name']
        entry: dict[str, Any] = {
            'id': f'{time.time():.6f}',
            'agent': agent_name,
            'agent_id': sender,
            'prompt': prompt.prompt,
            'responses': prompt.responses,
        }
        event = threading.Event()
        with self._lock:
            self._prompts.append(entry)
            self._prompt_events[entry['id']] = event
        self._broadcast('prompt', entry)
        return entry['id']

    def submit_response(self, prompt_id: str, response: str) -> None:
        """Record a response to a pending prompt and unblock any waiter."""
        with self._lock:
            self._prompts = [p for p in self._prompts if p['id'] != prompt_id]
            self._prompt_results[prompt_id] = response
            event = self._prompt_events.pop(prompt_id, None)
        if event is not None:
            event.set()

    def wait_for_response(self, prompt_id: str) -> str:
        """Block until a response is submitted for the given prompt ID."""
        with self._lock:
            event = self._prompt_events.get(prompt_id)
        if event is not None:
            event.wait()
        with self._lock:
            return self._prompt_results.pop(prompt_id, '')

    def dismiss_prompt(self, prompt_id: str) -> None:
        """Dismiss a pending prompt without a response."""
        self.submit_response(prompt_id, '')

    def set_shutdown_callback(self, callback: Any) -> None:
        """Set a callable(agent_id: str) invoked when the power button is clicked."""
        self._shutdown_callback = callback

    # ── SSE internals ─────────────────────────────────────────────────────

    def _subscribe(self) -> queue.Queue[str]:
        q: queue.Queue[str] = queue.Queue(maxsize=250)
        with self._lock:
            self._subscribers.append(q)
        return q

    def _unsubscribe(self, q: queue.Queue[str]) -> None:
        with self._lock:
            with contextlib.suppress(ValueError):
                self._subscribers.remove(q)

    def _broadcast(self, event: str, data: Any) -> None:
        msg = f'event: {event}\ndata: {json.dumps(data)}\n\n'
        with self._lock:
            dead = []
            for q in self._subscribers:
                try:
                    q.put_nowait(msg)
                except queue.Full:
                    dead.append(q)
            for q in dead:
                self._subscribers.remove(q)

    def _snapshot(self) -> dict[str, Any]:
        with self._lock:
            return {
                'agents': {k: dict(v) for k, v in self._agents.items()},
                'logs': list(self._logs[-200:]),
                'prompts': list(self._prompts),
            }

    # ── Flask app ─────────────────────────────────────────────────────────

    def _event_stream(self, q: queue.Queue[str]) -> Any:
        """Yield SSE messages from the queue, sending heartbeats when idle."""
        try:
            yield f'event: init\ndata: {json.dumps(self._snapshot())}\n\n'
            while True:
                try:
                    yield q.get(timeout=25)
                except queue.Empty:
                    yield ': heartbeat\n\n'
        finally:
            self._unsubscribe(q)

    def _build_app(self) -> Flask:
        app = Flask(__name__)

        @app.route('/')
        def index() -> Response:
            return Response(self._html, mimetype='text/html')

        @app.route('/events')
        def events() -> Response:
            q = self._subscribe()
            return Response(
                self._event_stream(q),
                mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'X-Accel-Buffering': 'no',
                    'Connection': 'keep-alive',
                },
            )

        @app.route('/assets/<path:filename>')
        def serve_asset(filename: str) -> Response:
            return send_from_directory(_ASSETS_DIR, filename)

        @app.route('/dismiss/<path:prompt_id>', methods=['POST'])
        def dismiss(prompt_id: str) -> tuple[str, int]:
            self.dismiss_prompt(prompt_id)
            return ('', 204)

        @app.route('/respond/<path:prompt_id>', methods=['POST'])
        def respond(prompt_id: str) -> tuple[str, int]:
            data = request.get_json(force=True, silent=True) or {}
            self.submit_response(prompt_id, data.get('response', ''))
            return ('', 204)

        @app.route('/shutdown/<path:agent_id>', methods=['POST'])
        def shutdown(agent_id: str) -> tuple[str, int]:
            if self._shutdown_callback is not None:
                self._shutdown_callback(agent_id)
            return ('', 204)

        return app
