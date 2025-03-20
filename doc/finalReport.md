# Progect Final Report Template

[Leonardo Randacio](leonardo.randacio@studio.unibo.it)

## Abstract

This project is an implementation of the algorithm proposed in \[[Wink et al., 2021][1]\].The
goal is to simulate peer-to-peer Federated Learning implementing an n-out-
of-n secret sharing schema and Secure Average Computation algorithm to let
the peers collaborate in the training of a Neural Network, without the risk
of direct or indirect training data theft, allowing the presence of semi-honest
peers. The project will showcase some emblematic cases probing strengths
and weaknesses of the approach.

## Goal/Requirements

The project implements the Secure Average Computation (SAC) algorithm proposed in \[[Wink et al., 2021][1]\] to implement a distributed system with the following characteristics:

- Peer to peer: no central server, all members of the system have the same role
- Federated Learning: the peers collaborate in the training of a common machine learning model for which every peer contributes with part of the training dataset
- Data privacy: every peer has knowledge only on it's own dataset and does not acquire knowledge of the other peers' datasets

The deliverable enables the user to easily repeat the [considered scenarios](#scenarios) and also provides some options to further tweak the scenarios for further insight.

### Scenarios

To test the effectiveness of the approach proposed in \[[Wink et al., 2021][1]\] the following scenarios will be implemented:

#### Base Scenarios

Base Scenarios implement systems where behaviour is as expected, as in all peers are honest and fully collaborate to generate the best model possible.

These scenarios are a benchmark to test the efficency of the approach for different machine learning problems and models.

These scenarios are also a control cases for the [Failure Scenarios](#failure-scenarios).

The following ML problems and models will be tested:

<!-- TODO ADD THIS PART TAKING INSIPRATION BY MACHINE LEARNING BOOK -->

#### Failure Scenarios

Failure Scenarios implement the following anomalous cases:

- Crash failure: a peer stops working or is disconnected from the network;
- Byzantine failure: a peer sends random data, jeopardizing the training of the neural network;

<!-- consider adding the case where a node disconnects and then reconnects or where a new peer simply adds itself to the network -->

#### Centralized scenarios

Centralized Scenarios act as control cases for the [Base Scenarios](#base-scenarios), by merely implementing the same neural networks with the same datasets of the [Base Scenarios](#base-scenarios) in a centralized manner.

For completeness' sake a list of all problems and models implemented follows:

<!-- TODO ADD THESE BASED ON DECISIONS MADE IN BASE SCENARIOS-->

## Requirements Analysis

The best suited language for machine learning projects is python, so this is the language that will be used

The various cases will be implemented as docker projects and a shell script will be implemented to enable the user to easily define the scenario that should be executed using command line parameters.

<!-- TODO ADD SPECIFIC LIBRARIES USED AT PROJECT END -->

## Design

<!-- TODO SEE IF SOMETHING SHOULD BE SAID HERE -->

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

Explain here how to install and launch the produced software artifacts.
Assume the softaware must be installed on a totally virgin environment.
So, report __any__ conviguration step.

Gradle and Docker may be useful here to ensure the deployment and launch processes to be easy.

## Usage Examples

Show how to use the produced software artifacts.

Ideally, there should be at least one example for each scenario proposed above.

## Conclusion

Recap what you did

### Future works

Racap what you did __not__

### What I learned

Racap what did you learned

<!-- linked references -->

[1]: https://ieeexplore.ieee.org/document/9502443
