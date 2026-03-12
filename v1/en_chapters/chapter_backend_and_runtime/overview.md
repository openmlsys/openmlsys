# Overview

Figure :numref:`ch07/ch07-compiler-backend-01` illustrates the
architecture of the AI compiler backend, situated between the frontend
and the hardware driver layer.

![Architecture of AI compilerbackend](../img/ch07/compiler-backend-architecture.pdf)
:label:`ch07/ch07-compiler-backend-01`

Graph optimization is a crucial step that involves transforming the
Intermediate Representation (IR) into a format that aligns with the
hardware features, facilitating operator selection. Since the frontend's
IR is abstracted from low-level runtime details, additional effort is
required to map the IR to a set of operators, such as MatMul,
Convolution, and ReLU. Sometimes, a single operator is sufficient to
handle a subset of the IR's functions. In such cases, the operator
fusion technique can be employed to fuse a group of IR nodes together.
Similarly, if a direct backend counterpart for a complex IR node is
unavailable, it can be partitioned into smaller operators.

Once the graph optimization is complete, the compiler backend proceeds
with operator selection, which involves matching the optimized IR with
appropriate operators that can be executed on the target device with
optimal efficiency. This process is similar to pattern matching. While
the easiest approach would be to map each IR node to a separate hardware
operator, such an approach may not be hardware-friendly. Instead,
existing compilers generally provide multiple candidate operators for
each IR node. The following steps are typically involved in the operator
selection process:

1.  The IR nodes received from the frontend are partitioned or fused to
    generate a low-level IR that is meaningful to the hardware.

2.  The compiler backend carefully selects operator mappings for the IR
    nodes, aiming to create a complete sequence of operators.

3.  The backend determines the format and data type of each input and
    output, ensuring fine-grained optimization on the IR.

4.  Finally, the compiler backend traverses the resulting sequence of
    operators, allocates input and output memory for each operator, and
    loads the operators onto the target device for computation.

By following this process, the compiler backend optimizes the IR by
selecting suitable operators, determining their input and output
requirements, and allocating memory accordingly. This enables efficient
execution of the AI program on the target device.

To further enhance the performance of a single operator, the compiler
backend often utilizes an operator compiler like TVM (Tensor Virtual
Machine) or XLA (Accelerated Linear Algebra). An operator compiler
analyzes the statements in an operator implementation, and it offers
various levels of optimization, including operator-level optimizations,
code generation, and runtime support. This stack is designed to enable
efficient execution of an operator on a wide range of hardware
platforms.
