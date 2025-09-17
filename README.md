# Federated Learning Privacy Peer to Peer

This is a repository for the project for the university course "Distributed Systems"

For executing a simulation the only dependencies required to be installed are [Nix](https://nixos.org/download/) and [Docker](https://www.docker.com/).

The easiest way to get Docker (and it's many products) installed is by installing [Docker Desktop](https://docs.docker.com/desktop/).

To install all other dependencies (defined in a `flake.nix` file) run the following command:

```sh
nix develop
```

[Just](https://github.com/casey/just) is used to simplify running cli commands.

To see available commands:

```sh
just
```

The following command starts a simulation:

```sh
just run <number_of_peers>
```

Where `<number_of_peers>` is the number of peers involved in the simulation.
