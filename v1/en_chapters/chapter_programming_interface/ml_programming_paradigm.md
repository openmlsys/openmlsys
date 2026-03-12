# Functional Programming

In the following, we will discuss the reasons behind the growing trend
of incorporating functional programming into the design of machine
learning frameworks.

## Benefits of Functional Programming

Training constitutes the most critical phase in machine learning, and
the manner in which training is depicted hinges significantly on
optimizer algorithms. Predominantly, contemporary machine learning tasks
utilize first-order optimizers, favored for their ease of use. With
machine learning advancing at a rapid pace, both software and hardware
are incessantly updated to stay abreast. Consequently, an increasing
number of researchers are beginning to investigate higher-order
optimizers, noted for their superior convergence performance. Frequently
utilized second-order optimizers, such as the Newton method,
quasi-Newton method, and AdaHessians, necessitate the computation of a
Hessian matrix incorporating second-order derivative information. Two
considerable challenges arise from this computation: 1) how to manage
such a hefty computational load efficiently; 2) how to express
higher-order derivatives in programmatic language.

In recent times, numerous large AI models have been introduced, which
include (with the number of parameters noted in parentheses) OpenAI
GPT-3 (175B) in 2020; PanGu (100B), PanGu-$\alpha$ (200B), Google's
Switch Transformer (1.6T), and WuDao (1.75T) in 2021; along with
Facebook's NLLB-200 (54B) in 2022. The demand for ultra-large model
training is escalating, and data parallelism alone cannot meet this
growing requirement. Conversely, model parallelism demands manual model
segmentation, a process that is time-intensive and laborious.
Consequently, the main challenge future machine learning frameworks must
overcome is how to actualize automatic parallelism. At its core, a
machine learning model is a representation of a mathematical model.
Hence, the ability to succinctly represent machine learning models has
risen to a key concern in the design of programming paradigms for
machine learning frameworks.

Recognizing the challenges presented by the practical implementation of
machine learning frameworks, researchers have identified that functional
programming could offer beneficial solutions. Functional programming, in
computer science, is a programming paradigm that envisions computation
as the evaluation of mathematical functions, actively avoiding state
changes and data mutations. This paradigm harmonizes well with
mathematical reasoning. Neural networks are composed of interconnected
nodes, with each node performing basic mathematical operations.
Functional programming languages allow developers to portray these
mathematical operations in a language that closely mirrors the
operations, enhancing the readability and maintainability of programs.
Concurrently, in functional languages, functions are kept separate,
simplifying the management of concurrency and parallelism.

In summary, functional programming is anticipated to confer the
following benefits to machine learning frameworks:

1.  It is suited for machine learning scenarios where higher-order
    derivatives are needed.

2.  It simplifies the development of parallel programming interfaces.

3.  It results in a more concise code representation.

## Framework Support for Functional Programming

Machine learning frameworks have increasing support for functional
programming. In 2018, Google rolled out JAX. Contrary to traditional
machine learning frameworks, JAX amalgamates neural network computation
and numerical computation. Its interfaces are compatible with native
data science interfaces in Python, such as NumPy and SciPy. Moreover,
JAX extends distribution, vectorization, high-order derivation, and
hardware acceleration in a functional programming style, characterized
by Lambda closure and no side effects.

In 2020, Huawei introduced MindSpore, the functional differential
programming architecture of which allows users to concentrate on the
native mathematical expressions of machine learning models. In 2022,
taking inspiration from Google's JAX, PyTorch launched functorch.
Functorch is essentially a library aimed at providing composable vmap
(vectorization) and autodiff transforms compatible with PyTorch modules
and PyTorch autograd, thereby achieving excellent eager-mode
performance. It can be inferred that functorch meets the requirements
for distributed parallelism in PyTorch static graphs. Code
`ch02/code2.4` gives an example of functorch.

**ch02/code2.4**
```
from functorch import combine_state_for_ensemble, vmap
minibatches = data[:num_models]
models = [MLP().to(device) for _ in range(num_models)]
fmodel, params, buffers = combine_state_for_ensemble(models)
predictions1_vmap = vmap(fmodel, out_dims=1)(params, buffers, minibatches)
```

Functorch introduces *vmap*, standing for \"vectorized map\". Its role
is to adapt functions designed for individual inputs so that they can
handle batches of inputs, therefore facilitating efficient vectorized
calculations. Unlike the batch processing capabilities of standard
PyTorch modules, vmap can convert any operation to be batch-aware
without the need to alter the operation's original structure. Moreover,
vmap offers greater flexibility to batch dimensions, allowing users to
specify which dimension should be treated as the batch dimension
(specifying the $out\_dim$ argument), a contrast to the default
behaviour of the standard PyTorch where the first dimension is usually
chosen as the batch dimension.

By tracing the development of machine learning frameworks, it becomes
evident that the functional programming paradigm become increasingly
popular. This can be attributed to functional programming's ability to
express machine learning models intuitively and its convenience for
implementing automatic differentiation, high-order derivation, and
parallel execution. Consequently, future machine learning frameworks are
likely to adopt layered frontend interfaces that are not exclusively
designed for machine learning scenarios. Instead, they will primarily
offer differential programming in their abstraction designs, making
gradient-based software easy to be developed for various applications.
