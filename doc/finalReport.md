# Project Final Report Template

<!-- copied this template: https://github.com/pikalab-unibo/sd-project-rules/blob/main/final-report-template.md -->

[Leonardo Randacio](leonardo.randacio@studio.unibo.it)

## Abstract

This project is an implementation of the algorithm proposed in \[[Wink et al., 2021][1]\].The goal is to simulate peer-to-peer Federated Learning implementing an n-out- of-n secret sharing schema and Secure Average Computation algorithm to let the peers collaborate in the training of a Neural Network, without the risk of direct or indirect training data theft, allowing the presence of semi-honest peers. The project will showcase some emblematic cases probing strengths and weaknesses of the approach.

## Goal

The project implements the Secure Average Computation (SAC) algorithm proposed in \[[Wink et al., 2021][1]\] to implement a distributed system with the following characteristics:

- Peer to peer: no central server, all members of the system have the same role
- Federated Learning: the peers collaborate in the training of a common machine learning model for which every peer contributes with part of the training dataset
- Data privacy: every peer has knowledge only on it's own dataset and does not acquire knowledge of the other peers' datasets

The deliverable enables the user to easily repeat the [considered scenarios](#scenarios).

### Scenarios

To test the effect of SAC the following scenarios have been implemented:

- **Control Scenario** : centralized machine learning training
- **Base Scenario** : P2P machine learning with SAC and IID (Independent and Identically Distributed) data distributions across peers
- **Extreme Scenario** : P2P machine learning with SAC and IID (Independent and Identically Distributed) data distributions across peers

## Requirements Analysis

<!-- TODO check if these are right -->

<!-- TODO check the commented ones -->

During project analysis the following requirements have been identified.

1. **Business Requirements**
    1. The system should demonstrate a practical application of advanced distributed systems and privacy-preserving computation concepts for an academic context.
    1. The system should enable the comparison of a novel federated learning algorithm (SAC) against a traditional centralized baseline to evaluate its efficacy and overhead.
1. **Domain Requirements**
    1. The implementation of the SAC protocol must adhere to algorithmic specifications outlined in [Wink et al., 2021].
    1. The system must operate in a true peer-to-peer (P2P) topology, with no central server managing the learning process or aggregating model parameters.
    <!-- 1. The global machine learning model must be a linear model (e.g., Logistic Regression or Linear SVM) whose training can be expressed as an averaging of local parameters. -->
    1. The system must guarantee data privacy: a peer must not be able to derive the raw data or the class distribution of any other peer from the messages it receives.
    1. The system must be capable of converging to a globally trained model despite non-IID (Independent and Identically Distributed) data distributions across peers.
1. **Functional Requirements**
    1. **User Functional Requirements**
        1. Main Usage
            1. Users (the experimenter) must be able to run the system to execute the control scenario (centralized training) on a specified dataset and save the results.
            1. Users must be able to run the system to execute the base scenario (SAC with IID data distribution across peers) and save the results.
            1. Users must be able to run the system to execute the extreme scenario (SAC with highly non-IID, class-skewed data distribution) and save the results.
            1. Users must be able to define key experiment parameters via a configuration file or command-line arguments (e.g., number of peers, number of training rounds, dataset path, learning rate).
        1. Results & Analysis
            1. Users must be able to view the final accuracy and loss of the trained model for each executed scenario.
            1. Users must be able to generate plots comparing the convergence (accuracy/loss over training rounds) of the different scenarios.
    1. **System Functional Requirements**
        1. Centralized Training (Control Scenario)
            1. The system must implement a standard centralized training algorithm on the entire dataset to produce a baseline model.
        1. P2P Network Management
            1. The system must instantiate a configurable number of peer processes.
            1. Peers must be able to exchange messages directly with their neighbors in the P2P overlay.
        1. Federated Learning with SAC
            1. Each peer must train a local model on its own subset of the data.
            1. Each peer must execute the SAC protocol to securely mask its model parameters before broadcasting them.
            1. Each peer must collect masked parameters from all other peers, combine them, and remove its own mask to reveal the secure average.
            1. Each peer must update its local model with the securely averaged global parameters.
            1. This process must repeat for a configurable number of training rounds or until a convergence criterion is met.
        1. Data Handling
            1. The system must partition a provided dataset (e.g., MNIST, CIFAR-10) among the peers according to the selected scenario (balanced for base, class-skewed for extreme).
1. **Non-Functional Requirements**
    1. The results of the SAC scenarios must be verifiable and reproducible across multiple runs with the same configuration.
    1. The process of configuring and running the three scenarios must be well-documented and require minimal manual setup.
    1. The code must be modular, separating concerns like P2P communication, the SAC protocol, ML training, and data loading, to facilitate understanding and usage.
    1. The system should be designed to complete a experiment with a typical configuration (e.g., 10 peers, 100 rounds) in a reasonable time frame on a single development machine (using processes/localhost). Performance optimization for a real distributed setting is not a primary goal.
5. **Implementation Requirements**
    1. The project must include a comprehensive README.md file with instructions for installation, dependency management, and usage.

### Technologies

To configure a reproducible development environment [Nix](https://nixos.org/) will be used.

The various cases will be implemented as docker projects and a shell script will be implemented to enable the user to easily define the scenario that should be executed using command line parameters.

To configure the docker containers [Nix](https://nixos.org/) will be used.

The de facto standard language for machine learning projects is python, so this is the language that will be used.

For python project management [Uv](https://docs.astral.sh/uv/) will be used.

[Just](https://github.com/casey/just) is used to simplify running cli commands.

## Design

### Structure

Which entities need to by modelled to solve the problem?

(UML Class diagram)

How should entities be modularised?

(UML Component/Package/Deployment Diagrams)

### Behaviour

How should each entity behave?

(UML State diagram or Activity Diagram)

### Interaction

How should entities interact with each other?

(UML Sequence Diagram)

## Implementation Details

Just report interesting / non-trivial / non-obvious implementation details.

This section is expected to be short in case some documentation (e.g. Javadoc or Swagger Spec) has been produced for the software artifacts.
This this case, the produced documentation should be referenced here.

## Self-assessment

Choose a criterion for the evaluation of the produced software and __its compliance to the requirements above__.

Pseudo-formal or formal criteria are preferred.

In case of a test-driven development, describe tests here and possibly report the amount of passing tests, the total amount of tests and, possibly, the test coverage.

## Deployment Instructions

The only project dependency necessary to run the simulations is (Docker)[https://www.docker.com/].

Unfortunately Docker's installation is not provided by Nix development environment functionalities, as it seems (there is currently no good mechanism for configuring services on non-NixOS hosts)[https://discourse.nixos.org/t/how-to-run-docker-daemon-from-nix-not-nixos/43413/2]. This means that docker must be installed 'manually'.

The easiest way to get Docker (and it's many products) installed is by installing (Docker Desktop)[https://docs.docker.com/desktop/].

## Development Instructions

Project tool dependencies, apart from Docker, are defined by a Nix flake.

To install the development dependencies of the project [Nix](https://nixos.org/download/) must be installed.

To enter the projects development environment, execute the following command while in the repository root:

```sh
nix develop
```

Unfortunately Docker's installation is not provided by Nix development environment functionalities, as it seems (there is currently no good mechanism for configuring services on non-NixOS hosts)[https://discourse.nixos.org/t/how-to-run-docker-daemon-from-nix-not-nixos/43413/2]. This means that docker must be installed 'manually'.

The easiest way to get Docker (and it's many products) installed is by installing (Docker Desktop)[https://docs.docker.com/desktop/].

## Usage Examples

[Just](https://github.com/casey/just) is used to simplify running cli commands.

To see available commands:

```sh
just
```

<!-- TODO complete this -->

<!-- INSTRUCTIONS
Show how to use the produced software artifacts.
Ideally, there should be at least one example for each scenario proposed above.
-->

## Conclusion

Recap what you did

### Future works

Racap what you did __not__

### What I learned

Racap what did you learn

![example](./assets/mermaid/architecture.png)

<!-- linked references -->

[1]: https://ieeexplore.ieee.org/document/9502443
