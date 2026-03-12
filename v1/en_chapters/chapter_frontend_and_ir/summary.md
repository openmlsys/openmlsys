# Chapter Summary

-   Intermediate Representation (IR) serves as one of the fundamental
    data structures of a compiler. It represents the transition from the
    source language to the target language during the process of program
    compilation.

-   Classical compilers categorize IRs into three types based on their
    structure: linear IR, graphical IR, and hybrid IR.

-   The demands imposed by machine learning frameworks necessitate new
    forms of IRs, as classical IRs fail to fully satisfy these
    requirements. Therefore, innovative IRs that are more compatible
    with these frameworks must be developed based on classical IRs.

-   The central principle in automatic differentiation is the
    decomposition of a program's arithmetic operations into a finite set
    of basic operations. Knowing the derivative evaluation rules for all
    these operations allows for the calculation of the derivative for
    each basic operation. Subsequently, these results are aggregated
    using the chain rule to obtain the derivative result for the entire
    program.

-   Automatic differentiation operates in two modes---forward-mode and
    reverse-mode---based on the sequence adopted by the chain rule for
    combining derivatives.

-   Forward-mode automatic differentiation is applied when evaluating
    the derivative of a network where the input dimension is smaller
    than the output dimension. In contrast, reverse-mode automatic
    differentiation is employed when the output dimension of a network
    is smaller than the input dimension.

-   Implementation methods for automatic differentiation encompass
    elemental libraries, operator overloading, and source
    transformation.

-   Type systems, which are utilized to define various types, detail the
    operations of each type and outline the interactions among types.
    Comprising a set of types and the type-based rules that delineate
    program behavior, type systems are extensively used in compilers,
    interpreters, and static checking tools.

-   Static analysis involves the inspection and verification of code
    through lexical analysis, syntactic analysis, control flow analysis,
    and data flow analysis, all of which are conducted without executing
    the programs.

-   The objective of compilation optimization is to boost the efficiency
    of the IRs generated during the compilation process. Notably,
    compilation optimization conducted at the frontend is
    hardware-agnostic.
