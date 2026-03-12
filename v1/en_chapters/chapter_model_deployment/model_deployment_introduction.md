# Overview

After training a model, we need to save it and its parameters to files
to make them persistent. However, because different training frameworks
adopt different data structures for such files, the inference system
must support models trained using different training frameworks and
convert the data in the files into a unified data structure. During the
conversion from a training model to an inference model, optimization
operations such as operator fusion and constant folding on the model can
be performed to improve the inference performance.

The hardware restrictions of different production environments must be
considered when we deploy an inference model. For instance, a
large-scale model needs to be deployed on a server in a computing or
data center with strong computing power, whereas a mid-scale model
should be deployed on an edge server, PC, or smartphone --- such devices
often have limited computing resources and memory. For simple,
small-scale models, ultra-low power microcontrollers can be used. In
addition, different hardware supports different data types (such as
float32, float16, bfloat16, and int8). To adapt to the hardware
restrictions, a trained model may sometimes need to be compressed in
order to reduce model complexity or data precision and reduce model
parameters.

Before a model can be used for inference, it needs to be deployed in the
runtime environment. To optimize model inference, which may be affected
by latency, memory usage, and power consumption, we can design chips
dedicated for machine learning --- such dedicated chips usually
outperform general-purpose ones in terms of energy efficiency. Another
approach is to fully leverage hardware capabilities through
software-hardware collaboration. Take a CPU as an example. When
designing and optimizing models for a specific CPU architecture, we can
suitably divide data blocks to meet the cache size, rearrange data to
facilitate contiguous data access during computing, reduce data
dependency to improve the parallelism of hardware pipelines, and use
extended instruction sets to improve the computing performance.

Because models are an important enterprise asset, it is important to
ensure their security after they are deployed in the runtime
environment. This chapter will discuss some of the common protection
measures and use model obfuscation as an example.

Some of the common methods used in the industry to address the preceding
challenges are as follows:

1.  **Model compression:** Technologies that reduce the model size and
    computation complexity by means of quantization and pruning. Such
    technologies can be categorized according to whether retraining is
    required.

2.  **Operator fusion:** Technologies that combine multiple operators
    into one by simplifying expressions and fusing attributes, aiming to
    reduce the computation complexity and size of the model.

3.  **Constant folding:** Forward computation of operators that meet
    certain conditions is completed in the offline phase, reducing the
    computation complexity and size of a model. This requires that the
    inputs of operators be constants in the offline phase.

4.  **Data format:** According to the operator library and hardware
    restrictions and exploration of the optimal data format of each
    layer on the network, data is rearranged or data rearrangement
    operators are inserted, in order to reduce the inference latency
    during model deployment.

5.  **Model obfuscation:** Network nodes or branches are added and
    operator names are changed for a trained model, so that it is
    difficult for attackers to understand the original model structure
    even if they steal the model. An obfuscated model may be directly
    executed in the deployment environment, thereby ensuring the
    security of the model during execution.
