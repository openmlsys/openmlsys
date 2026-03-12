# Overview

An effective computer architecture is expected to be both
energy-efficient---quantified by the number of basic operations executed
per unit of energy---and versatile---defined by the range of tasks a
chip can undertake. We can evaluate these aspects by considering two
primary chip categories. The first includes general-purpose processors
like CPUs, capable of managing a diverse array of computing tasks,
though at the cost of lower energy efficiency, averaging around 0.1
TOPS/W. Conversely, application-specific integrated circuits (ASICs)
offer enhanced energy efficiency but have more restricted task
capabilities. With respect to chip design, general-purpose processors
have integrated various acceleration technologies such as superscalar,
single-instruction multi-data (SIMD), and single-instruction
multi-thread (SIMT) to boost their energy efficiency.

General-Purpose Graphics Processing Units (GPUs) achieve a respectable
equilibrium between energy efficiency and versatility. Modern GPUs
incorporate numerous optimization designs for vector, matrix, and tensor
computing. For instance, NVIDIA GPUs are equipped with Tensor Cores,
Transformer Cores, and Structure Sparsity Cores, which are specifically
designed to expedite the distinctive types of computation prevalent in
neural networks. Despite these enhancements, GPUs' requirement to
support a wide range of computing tasks results in larger footprints and
increased power consumption.

A promising solution to this challenge is deep learning hardware
accelerators. Notable examples include Google's Tensor Processing Units
(TPUs), Apple's Neural Processing Units (NPUs), and Huawei's Ascend
Chips. For instance, Google's TPU, a chip designed to expedite deep
learning computations, uses a systolic array to optimize matrix
multiplication and convolution operations, fully utilizing local data
with minimal memory access.
