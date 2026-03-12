# Programming Model

Machine learning frameworks comprise various components that facilitate
the efficient development of algorithms, data processing, model
deployment, performance optimization, and hardware acceleration. When
designing the application programming interfaces (APIs) for these
components, a key consideration is striking the right balance between
framework performance and usability. To achieve optimal performance,
developers utilize C or C++, as these programming languages enable
efficient invocation of the APIs provided by the operating system and
hardware accelerators.

Regarding usability, machine learning framework users, including data
scientists, biologists, chemists, and physicists, often possess strong
industrial backgrounds and are skilled in using high-level scripting
languages like Python, Matlab, R, and Julia. While these languages offer
remarkable programming usability, they lack deep optimization
capabilities for underlying hardware or operating systems compared to C
and C++. Therefore, the core design objective of machine learning
frameworks encompasses two aspects: providing easy-to-use APIs for
implementing algorithms using high-level languages like Python, and
providing low-level APIs centered around C and C++ to assist framework
developers in implementing numerous high-performance components and
efficiently executing them on hardware. This chapter describes
strategies for achieving this design objective.

The chapter aims to achieve the following learning objectives:

1.  Understanding the workflows and programming principles of machine
    learning frameworks.

2.  Understanding the design of neural network models and layers.

3.  Understanding how machine learning frameworks bridge Python and
    C/C++ functions.

4.  Understanding the support for functional programming in machine
    learning frameworks.

```toc
:maxdepth: 2

Overview
Machine_Learning_Workflow
Neural_Network_Programming
Functional_Programming
Bridging_Python_and_C_C++_Functions
Chapter_Summary
```
