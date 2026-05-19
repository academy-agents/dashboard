Known bugs:


# Heartbeats don't work
[Pending]
The UserAgent treats every message from an agent as a heartbeat,
but this mechanism appears to be broken now.
We should switch over to using mailbox/agent liveness info provided
by the exchange directly.

# Shutdown doesn't work
[Fixed]
The shutdown button on the agent cards no longer trigger agent shutdown
Fixed in git rev: 4c3525b57ea630fefccddcd9caf1cd8758f9bfbd


# Log issues
[Pending]
Logging issues are being worked out with the switch away from `init_logging()` to the `recommended` loggers from BenC.
The issue here is that logConfig objects are handled by the manager and we do not use a manager in the `user-agent-launcher`.
We use `http_exchange_client.register_agent -> make Runtime(registration=AgentReg)` which leaves out a point to plug in log configuration.

# HTTP Timeouts
[Addressed]
The following bug was addressed by upgrading academy-py to latest which has support for handling
aiohttp timeouts within the HTTPExchangeClient. The fix basically is:

> factory = HttpExchangeFactory(client_timeout=aiohttp.ClientTimeout(total=None, sock_connect=30))

```
[2026-05-15 23:35:57.671] ERROR    (academy.logging) Background task raised an exception.
Traceback (most recent call last):
  File "/Users/yadu/src/nexus/.venv/lib/python3.13/site-packages/aiohttp/streams.py", line 372, in _wait
    await waiter
asyncio.exceptions.CancelledError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/yadu/src/nexus/.venv/lib/python3.13/site-packages/academy/logging.py", line 213, in execute_and_log_traceback
    return await fut
           ^^^^^^^^^
  File "/Users/yadu/src/nexus/.venv/lib/python3.13/site-packages/academy/exchange/client.py", line 224, in _listen_for_messages
    async for message in self._transport.listen():
    ...<10 lines>...
            await asyncio.sleep(0)
  File "/Users/yadu/src/nexus/.venv/lib/python3.13/site-packages/academy/exchange/cloud/client.py", line 252, in listen
    async for line_in_bytes in response.content:
    ...<11 lines>...
        current_message_lines.append(line)
  File "/Users/yadu/src/nexus/.venv/lib/python3.13/site-packages/aiohttp/streams.py", line 53, in __anext__
    rv = await self.read_func()
         ^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/yadu/src/nexus/.venv/lib/python3.13/site-packages/aiohttp/streams.py", line 377, in readline
    return await self.readuntil(max_size=max_line_length)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/yadu/src/nexus/.venv/lib/python3.13/site-packages/aiohttp/streams.py", line 414, in readuntil
    await self._wait("readuntil")
  File "/Users/yadu/src/nexus/.venv/lib/python3.13/site-packages/aiohttp/streams.py", line 371, in _wait
    with self._timer:
         ^^^^^^^^^^^
  File "/Users/yadu/src/nexus/.venv/lib/python3.13/site-packages/aiohttp/helpers.py", line 713, in __exit__
    raise asyncio.TimeoutError from exc_val
TimeoutError
```
