# Distributed Training

As the field of machine learning continues to accelerate at a rapid
pace, it has given rise to increasingly sophisticated models. These
models are characterized by a staggering quantity of parameters, the
gigantic size of a training dataset, and highly sophisticated
structures, which in turn place significant demands on both computing
and memory resources. Consequently, the limitations of single-machine
systems have become increasingly apparent, and they no longer suffice
for training these large machine learning models. This necessitates the
advent of distributed training systems, designed to alleviate the strain
on resources.

In this chapter, we dive deep into the fundamentals, design aspects, and
practical implementations of distributed machine learning systems. We
commence our discussion by elucidating what distributed training systems
entail, followed by an exploration of the rationale behind their design
and the potential benefits they offer. Subsequently, we scrutinize the
most commonly adopted methods of distributed training, encompassing data
parallelism, model parallelism, and pipeline parallelism. Each of these
methods can typically be implemented via one of two techniques:
collective communication or parameter servers, both of which come with
their unique sets of merits and drawbacks.

The key learning objectives of this chapter are as follows:

1.  Grasping the advantages offered by distributed training systems.

2.  Understanding widely-used parallelism methods, namely, data
    parallelism, model parallelism, hybrid parallelism, and pipeline
    parallelism.

3.  Comprehending the architecture of a machine learning cluster.

4.  Understanding collective communication operators and their
    applications in distributed training systems.

5.  Developing an understanding of parameter server architectures.

```toc
:maxdepth: 2

Overview
Parallelism_Methods
Pipeline_Parallelism_with_Micro-Batching
Architecture_of_Machine_Learning_Clusters
Collective_Communication
Parameter_Server
Federated_Learning
Training_Large_Language_Models
Chapter_Summary
Further_Reading
```

