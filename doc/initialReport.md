# Implementation of P2P Federated Learning using SAC

[Leonardo Randacio](leonardo.randacio@studio.unibo.it)

## Abstract

This project is an implementation of the algorithm proposed in "Tobias Wink and Zoltan Nochta. An approach for peer-to-peer federated learning.
In 2021 51st Annual IEEE/IFIP International Conference on Dependable Systems
and Networks Workshops (DSN-W), pages 150–157, 2021.". The
goal is to simulate peer-to-peer Federated Learning implementing an n-out-
of-n secret sharing schema and Secure Average Computation algorithm to let
the peers collaborate in the training of a Neural Network, without the risk
of direct or indirect training data theft, allowing the presence of semi-honest
peers. The project will showcase some emblematic cases probing strengths
and weaknesses of the approach.

## Goal/Requirements

The project goals are to create the peer code for the system and to test it in emblematic
simulations such as:

- Base case with 3 honest peers and IID Data
- 2 honest peers and 1 dishonest, who sends random weights
- Increasing the dimension of the NN
- Non-IID Data, such as an unbalanced feature distribution
- Failure of one peer

### System Requirements

The main language used will be python:

- PyUnit will be used for testing.
- Pipenv will be used for package managing
- Docker will be used for containerization
