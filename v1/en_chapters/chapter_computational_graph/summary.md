# Chapter Summary

1.  The computational graph technology is introduced to machine learning
    frameworks in order to achieve a trade-off between programming
    flexibility and computational efficiency.

2.  A computational graph contains tensors (as units of data) and
    operators (as units of operations).

3.  A computational graph represents the computational logic and status
    of a machine learning model and offers opportunities for
    optimizations.

4.  A computational graph is a directed acyclic graph. Operators in the
    graph are directly or indirectly dependent on or independent of each
    other, without circular dependencies.

5.  Control flows, represented by conditional control and loop control,
    determines how data flows in a computational graph.

6.  Computational graphs come in two types: static and dynamic.

7.  Static graphs support easy model deployment, offering high
    computational efficiency and low memory footprint at the expense of
    debugging performance.

8.  Dynamic graphs provide computational results on the fly, which
    increases programming flexibility and makes debugging easy for model
    optimization and iterative algorithm improvement.

9.  We can appropriately schedule the execution of operators based on
    their dependencies reflected in computational graphs.

10. For operators that run independently, we can consider concurrent
    scheduling to achieve parallel computing. For operators with
    computational dependencies, schedule them to run in serial.

11. Specific training tasks of a computational graph can run
    synchronously or asynchronously. The asynchronous mechanism
    effectively improves the hardware efficiency and shortens the
    training time.
