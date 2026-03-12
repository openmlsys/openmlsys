# Chapter Summary

1.  Model deployment is restricted by factors including the model size,
    runtime memory usage, inference latency, and inference power
    consumption.

2.  Models can be compressed using techniques such as quantization,
    pruning, and knowledge distillation in the offline phase. In
    addition, some model optimization techniques, such as operator
    fusion, can also reduce the model size, albeit to a lesser degree.

3.  Runtime memory usage can be improved by optimizing the model size,
    deployment framework size, and runtime temporary memory usage.
    Methods for optimizing the model size have been summarized earlier.
    Making the framework code simpler and more modular helps optimize
    the deployment framework. Memory pooling can help implement memory
    overcommitment to optimize the runtime temporary memory usage.

4.  Model inference latency can be optimized from two aspects. In the
    offline phase, the model computation workload can be reduced using
    model optimization and compression methods. Furthermore, improving
    the inference parallelism and optimizing operator implementation can
    help maximize the utilization of the computing power. In addition to
    the computation workload and computing power, consideration should
    be given to the load/store overhead during inference.

5.  Power consumption during inference can be reduced through offline
    model optimization and compression technologies. By reducing the
    computational workload, these technologies also facilitate power
    consumption reduction, which coincides with the optimization method
    for model inference latency.

6.  In addition to the optimization of factors related to model
    deployment, this chapter also discussed technologies regarding
    deployment security, such as model obfuscation and model encryption.
    Secure deployment protects the model assets of enterprises and
    prevents hackers from attacking the deployment environment by
    tampering with models.
