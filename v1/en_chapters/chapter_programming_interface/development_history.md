# Overview

With the advent of machine learning systems, the design of user-friendly
and high-performance APIs has become a paramount concern for system
designers. In the early stages of machine learning frameworks (as
depicted in Figure :numref:`ch03/framework_development_history`), developers often
opted for high-level programming languages like Lua (Torch) and Python
(Theano) to write machine learning programs. These frameworks offered
essential functions, including model definition and automatic
differentiation, which are integral to machine learning. They were
particularly well-suited for creating small-scale machine learning
applications targeted toward scientific research purposes.

<figure id="fig:ch03/framework_development_history">
<embed src="../img/ch03/framework_development_history.pdf" />
<figcaption> Evolution of Machine Learning Programming Frameworks: A
Historical Perspective</figcaption>
</figure>

The rapid advancement of deep neural networks (DNNs) since 2011 has
sparked groundbreaking achievements in various AI application domains,
such as computer vision, speech recognition, and natural language
processing. However, training DNNs requires substantial computational
power. Unfortunately, earlier frameworks like Torch (primarily using
Lua) and Theano (mainly using Python) were unable to fully harness this
computing power. On the other hand, general-purpose APIs like CUDA C for
computational accelerators such as NVIDIA GPUs have become increasingly
mature, and multi-thread libraries like POSIX Threads built on CPU
multi-core technology have gained popularity among developers.
Consequently, many machine learning users sought to develop
high-performance deep learning applications utilizing C/C++. These
requirements led to the emergence of frameworks like Caffe, which
employed C/C++ as their core APIs.

However, customization of machine learning models is often necessary to
suit specific deployment scenarios, data types, identification tasks,
and so on. This customization typically falls on the shoulders of AI
application developers, who may come from diverse backgrounds and may
not fully leverage the capabilities of C/C++. This became a significant
bottleneck that hindered the widespread adoption of programming
frameworks like Caffe, which heavily relied on C/C++.

In late 2015, Google introduced TensorFlow, which revolutionized the
landscape. In contrast to Torch, TensorFlow adopted a design where the
frontend and backend were relatively independent. The frontend,
presented to users, utilized the high-level programming language Python,
while the high-performance backend was implemented in C/C++. TensorFlow
provided numerous Python-based frontend APIs, gaining wide acceptance
among data scientists and machine learning researchers. It seamlessly
integrated into Python-dominated big data ecosystems, benefiting from
various big data development libraries such as NumPy, Pandas, SciPy,
Matplotlib, and PySpark. Python's exceptional interoperability with
C/C++, as demonstrated in multiple Python libraries, further enhanced
TensorFlow's appeal. Consequently, TensorFlow combined the flexibility
and ecosystem of Python with high-performance capabilities offered by
its C/C++ backend. This design philosophy was inherited by subsequent
frameworks like PyTorch, MindSpore, and PaddlePaddle.

Subsequently, as observed globally, prominent enterprises started
favoring open-source machine learning frameworks, leading to the
emergence of Keras and TensorLayerX. These high-level libraries
significantly expedited the development of machine learning
applications. They provided Python APIs that allowed quick importing of
existing models, and these high-level APIs were decoupled from the
intricate implementation details of specific machine learning
frameworks. As a result, Keras and TensorLayerX could be utilized across
different machine learning frameworks.

While deep neural networks continued to evolve, new challenges surfaced
regarding the APIs of machine learning frameworks. Around 2020, novel
frameworks like MindSpore and JAX emerged to tackle these challenges.
MindSpore, in addition to inheriting the hybrid interfaces (Python and
C/C++) from TensorFlow and PyTorch, expanded the scope of machine
learning programming models. This expansion facilitated efficient
support for a diverse range of AI backend chips, including NVIDIA GPU,
Huawei Ascend , and ARM. Consequently, machine learning applications can
be swiftly deployed across a wide array of heterogeneous devices.

Simultaneously, the proliferation of ultra-large datasets and
ultra-large DNNs necessitated distributed execution as a fundamental
design requirement for machine learning programming frameworks. However,
implementing distributed execution in TensorFlow and PyTorch required
developers to write substantial amounts of code for allocating datasets
and DNNs across distributed nodes. Yet, many AI developers are not
well-versed in distributed programming. In this regard, JAX and
MindSpore significantly improves the situation by enabling the seamless
execution of programs on a single node across various other nodes.
