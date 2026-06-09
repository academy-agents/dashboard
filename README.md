# Academy-Dashboard

<img src="academy_dashboard/user_agent/assets/modcon_logo.png" alt="ModCon" height="120"> <img src="academy_dashboard/user_agent/assets/CAF.png" alt="CAF" height="120">


**Observability and Oversight for Academy Agents**

As agents act autonomously, the ability to observe what they are doing and intervene
when appropriate becomes a critical capability. `academy-dashboard` addresses these
challenges in agentic deployments through the following extensions for `Academy`:

* `UserAgent`: Specialized Academy agents that 1. accepts information from MonitoredAgents \
   and 2. presents this information over a web based dashboard.
* `MonitoredAgent`: Extends academy's `Agent` class to support observability and control features.

Here are some of the supported capabilities:

* Logging: Live log stream from `MonitoredAgents` is presented via the `UserAgent`
* Human-in-the-loop: `MonitoredAgents` can send user prompts to the `UserAgent` where a user can respond over a webpage
* Performance Stats: Dashboard presents performance stats collected from `MonitoredAgents`
* Shutdown: `MonitoredAgent`s can be terminated from the dashboard provided by `UserAgents`
* Location: Locate your agents on a map

## Using the `UserAgent`

There are two supported modes for using starting a `UserAgent`:


#### `Hosted UserAgent`

>>   Go to [dashboard.academy-agents.org](https://dashboard.academy-agents.org/)

    1) Login with Globus Auth \
    2) Click the `[+]` button to launch a new `UserAgent` \
    3) Copy the agent UUID and plug this back into your scripts \

### `Local Deployment`:

Launch locally with: `user-agent-launcher`,

```bash
:>user-agent-launcher
User Agent UUID >>>>
     a9337401-3d22-4205-923a-0040bb8d3a7b
 * Serving Flask app 'academy_dashboard.user_agent.dashboard'
 * Debug mode: off

```

> NOTE: MonitoredAgents need the User Agent's UUID (printed above) to establish a connection.

```bash
:> user-agent-launcher -h
usage: user-agent-launcher [-h] [-p PORT] [-r REGISTRATION_FILE] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

options:
  -h, --help            show this help message and exit
  -p, --port PORT       Port at which the flask service is listening
  -r, --registration_file REGISTRATION_FILE
                        UserAgent registration file
  -l, --log_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Log level
```

## Using the `MonitoredAgent`

> NOTE: Use `export USER_AGENT_ID=<USER_AGENT_UUID_FROM_ABOVE_STEPS>` for examples in the [examples](https://github.com/academy-agents/dashboard/tree/main/examples) directory.

> NOTE: This document is in development.

> NOTE: The example below is trimmed for brevity. Refer [examples](https://github.com/academy-agents/dashboard/tree/main/examples) for complete code.

```python
from academy_dashboard import MonitoredAgent
from academy_dashboard import UserAgent


class Sleeper(MonitoredAgent):

    def __init__(self, user_agent_handle: Handle[UserAgent]) -> None:
        super().__init__(user_agent_handle=user_agent_handle)
        print('Spinner init done')

    @loop
    async def cycle(self, shutdown: asyncio.Event) -> None:
        """Log and sleep in loop."""
        counter = 0
        while not shutdown.is_set():
            await asyncio.sleep(2)
            logging.info('Sleeper iteration %d', counter)
            counter += 1
        logging.info('Sleeper exiting!!!! ')


async def main(user_agent_id: UUID) -> None:
    async with await Manager.from_exchange_factory(
        factory=HttpExchangeFactory(),
        executors=ProcessPoolExecutor(max_workers=2),
    ) as manager:

        # 1. Get Handle to UserAgent
        agent_id = AgentId(uid=user_agent_id, name='UserAgent')
        user_agent_handle = manager.get_handle(agent_id)

        # 2. Launch a single agent:
        sleeper = await manager.launch(
            Sleeper,
            kwargs={'user_agent_handle': user_agent_handle},  # <-- Pass handle to UserAgent
        )

        # 3. Wait for the sleeper agent, which will go on until cancelled
        #    with a ctrl+c
        await manager.wait([sleeper])
        logging.info('All done!')


if __name__ == '__main__':
    user_agent_id = os.environ['USER_AGENT_ID']
    raise SystemExit(asyncio.run(main(UUID(user_agent_id))))
```
