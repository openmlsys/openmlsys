# Chapter Summary

1.  The advent of large-scale machine learning models has sparked an
    exponential increase in the need for computational power and memory,
    leading to the emergence of distributed training systems.

2.  Distributed training systems often utilize data parallelism, model
    parallelism, or a combination of both, based on memory limitations
    and computational constraints.

3.  Pipeline parallelism is another technique adopted by distributed
    training systems, which involves partitioning a mini-batch into
    micro-batches and overlapping the forward and backward propagation
    of different micro-batches.

4.  Although distributed training systems usually function in compute
    clusters, these networks sometimes lack the sufficient bandwidth for
    the transmission of substantial gradients produced during training.

5.  To meet the demand for comprehensive communication bandwidth,
    machine learning clusters integrate heterogeneous high-performance
    networks, such as NVLink, NVSwitch, and InfiniBand.

6.  To accomplish synchronous training of a machine learning model,
    distributed training systems frequently employ a range of collective
    communication operators, among which the AllReduce operator is
    popularly used for aggregating the gradients computed by distributed
    nodes.

7.  Parameter servers play a crucial role in facilitating asynchronous
    training and sparse model training. Moreover, they leverage model
    replication to address issues related to data hotspots and server
    failures.
