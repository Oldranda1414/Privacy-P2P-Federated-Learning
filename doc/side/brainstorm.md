# brainstorm

## design

Probably the best way to design the nodes is with a finite state machine. Ideally a simple module could be made to create finite state machines
```mermaid
class FiniteStateMachine {
    __init__(list[State])
    start()
}

class State {
    __init__(name: str, func: Callable)
}

with func = (): str

```

example modified from chatgpt

```py
class FSM:
    def __init__(self, handlers: dict[str, Callable[str]], initial_state: str):
        self.state = initial_state
        self.handlers = handlers

    def run(self):
        """Run the handler of the current state"""
        if self.state not in self.handlers:
            raise ValueError(f"No handler for state {self.state}")
        # The handler returns the next state
        self.state = self.handlers[self.state]()

# Example usage
def idle_handler():
    print("Currently IDLE")
    return "active"

def active_handler():
    print("Currently ACTIVE")
    return "idle"

# Build FSM
fsm = FSM("idle", {
    "idle": idle_handler
    "active": active_handler
})

fsm.run()

```

Due to the possible high computational, and consequently time, cost of the training step, probably it would be necessary for the nodes to poll eachother to make sure they are all alive and well, or the training step might be rendered useless if one node fails.

## tech

### nix

nix flake for devenv configuration

### UV

use UV for python build system

links:

(https://docs.astral.sh/uv/)
(https://github.com/astral-sh/uv)

### Rich

use Rich for pretty terminal output

(https://pypi.org/project/rich/)

## Optional Requirements

Should the case where a group of peers are training and another one joins at some point be considered or should the max number of peers (considering failures) be known at all times? (I would like the second case, to counter scope creep)

## add to doc

### CAP

It seems obvious that the project should sacrifice A(vailibility), as P(artition) always occurs and C(onsistency) seems paramount.

Eventual Consistency could be considered, but seems to much of a hassle to work with, so simply renouncing A(vailibility) seems the simplest and safest option.

TODO ask chatgpt what it thinks of this once project requirements are available.
### graphs

class diagram, duh
actors (& components?)

## Study notes

### C1

CAP theorem.

The modern vision of the CAP theorem is that Availibility and Consistency should be provided until Partition occurs. Plans should be made for when Partition inevitably occurs and a counscious choice between Consistency and Availibility should be made.

TODO
For this project I think that a protocol could be enacted when partition occurs. If only one node does not respond then a timer could be initialized after which all nodes shutdown, saving their results.

A more complex solution could have the nodes reorganize if a non temporary partition occurs.

### C2

The many impossibilities found in ds are usefull to understand the boundries of what can be done.

In practice a good enough solution, within the impossibility imposed boundries, is possibile.


#### video notes

watched this to complete understanding
http://infoq.com/presentations/distributed-consensus/

FLP tells us that it is impossible to have reliable systems in async comunication, because we can never tell if a node is down or if it is a slow network.

to solve this: 

- in practice we simply use timers and ping nodes
- in theory we state that a message from a working node will arrive eventually

Important to define if the protocol for the project is leader based or leaderless. I immagine it leaderless as of now, but maybe consensus is too hard in a leaderless protocol.
Actually really thinking about it the project is peer 2 peer by definition, so it better be leaderless, lol

TODO
Remember to say that the protocol is leaderless (see lines above if confused)

### M2

TODO Define what type of faluts can occur and how they are handled or removed.

TODO dependability of systems can be expressed in terms of availability, reliability, safety, maintainability. Evaluate if this should be done in some manner for the project

### M6

TODO define a specific architectural style for the project:

- layered architecture
- object-based architecture
- data-centered architecture
- event-based architecture
- shared data-space architecture

maybe give a look at the book to better understand this stuff

### M10

TODO define the type of the comunication model chosen for the project:

- message-passing communication
- control-oriented communication
- data-oriented communication

## Agile steps

- docker python ping pong (with configurable number of peers) DONE
- fsm with background polling (not sure this is the best solution, think about this) DONE
- data load, marshall and unmarshall
- SAC with dummy data (checkout how to do sync with p2p)
- ai

