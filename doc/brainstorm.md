# brainstorm

## tech

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

## Study notes

### C1

CAP theorem.

The modern vision of the CAP theorem is that Availibility and Consistency should be provided until Partition occurs. Plans should be made for when Partition inevitably occurs and a counscious choice between Consistency and Availibility should be made.

TODO
For this project I think that a protocol could be enacted when partition occurs. If only one node does not respond then a timer could be initialized after which all nodes shutdown, saving their results.

A more complex solution could have the nodes reorganize if a constant partition occurs.

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

