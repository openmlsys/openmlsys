# Chapter Summary

1.  The compiler backend performs three primary tasks: graph
    optimization, operator selection, and memory allocation.

2.  Graph optimization reduces resource overhead, adapts the graph to
    hardware capabilities, and enhances execution performance while
    maintaining the model's numerical properties.

3.  Graph optimization techniques can be hardware-agnostic (e.g., memory
    I/O optimization) or hardware-specific (e.g., subgraph
    transformation to adapt to hardware instruction restrictions).

4.  Operator selection involves mapping the compute nodes in an IR to
    suitable operators for hardware execution.

5.  When selecting an optimized operator, factors such as data format
    and type must be considered, as they impact operator performance on
    the target hardware.

6.  An IR is generated after graph optimization and operator selection.
    Based on the IR, memory is allocated for input and output tensors of
    each operator before launching them to hardware for execution.

7.  Memory reuse is designed to improve memory utilization and
    accommodate larger models within limited device memory.

8.  Fusion of communication operators enhances communication efficiency.
    Properly allocating memory for in-place operators reduces memory
    footprint and improves computing efficiency.

9.  Operator compilers play a vital role in optimizing hardware
    performance. Critical optimization techniques include scheduling
    strategies and the polyhedral model algorithm.
