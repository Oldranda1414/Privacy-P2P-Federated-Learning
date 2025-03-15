# Progect Final Report Template

[Leonardo Randacio](leonardo.randacio@studio.unibo.it)

## Abstract

This project is an implementation of the algorithm proposed in "Tobias Wink and Zoltan Nochta, An approach for peer-to-peer federated learning, In 2021 51st Annual IEEE/IFIP International Conference on Dependable Systems and Networks Workshops (DSN-W), pages 150–157, 2021". The
goal is to simulate peer-to-peer Federated Learning implementing an n-out-
of-n secret sharing schema and Secure Average Computation algorithm to let
the peers collaborate in the training of a Neural Network, without the risk
of direct or indirect training data theft, allowing the presence of semi-honest
peers. The project will showcase some emblematic cases probing strengths
and weaknesses of the approach.

## Goal/Requirements

Detailed description of the project goals, requirements, and expected outcomes.

Use case Diagrams, examples, or Q/A simulations are welcome.

### Scenarios

Informal description of the ways users are expected to interact with your project.
It should describe _how_ and _why_ a user should use / interact with the system.

### Self-assessment policy

How should the quality of the produced software be assessed?

How should the effectiveness of the project outcomes be assessed?

## Requirements Analysis

Is there any implicit requirement hidden within this project's requirements?

Is there any implicit hypothesis hidden within this project's requirements?

Are there any non-functional requirements implied by this project's requirements?

What model/paradigm/techonology is the best suited to face this project's requirements?

What's the abstraction gap among the available models/paradigms/techonologies and the problem to be solved?

## Design

This is where the logical/abstract contribution of the project is presented.

Notice that, when describing a software project, three dimensions need to be taken into account: structure, behaviour, and interaction.

Always remember to report __why__ a particular design has been choosen.
Reporting wrog design choices which has been evalued during the design phase is welcome too.

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

### What did we learned

Racap what did you learned
