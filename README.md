# Academy-Nexus

**Observability and Oversight for Academy Agents**

As agents act autonomously, the ability to observe what they are doing and intervene
when appropriate becomes a critical capability. `academy-nexus` addresses these
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

>>   Go to [nexus.academy-agents.org](https://nexus.academy-agents.org/)

    1) Login with Globus Auth \
    2) Click the `[+]` button to launch a new `UserAgent` \
    3) Copy the agent UUID and plug this back into your scripts \

### `Local Deployment`:

Launch locally with: `user-agent-launcher`,

```bash
:>user-agent-launcher
User Agent UUID >>>>
     a9337401-3d22-4205-923a-0040bb8d3a7b
 * Serving Flask app 'academy_nexus.user_agent.dashboard'
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

```python
import os

USER_AGENT_ID=os.environ('USER_AGENT_UUID')
```
