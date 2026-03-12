# Single-Node Reinforcement Learning System

This section focuses on the single-node reinforcement learning system,
which is a type of simple system for reinforcement learning with a
single agent. Here, "node" refers to a computing unit used for model
update. Reinforcement learning systems are classified into single-node
ones and distributed ones based on whether parallel processing is
performed during model update. In a single-node reinforcement learning
system, only one class object is instantiated and used as the agent. The
sampling process (based on interaction with the environment) and the
update process (based on the collected samples) are considered as
different private functions within this class. Unlike such a single-node
system, a distributed one is more complex.

## RL System

There are many forms of distributed reinforcement learning systems, and
the forms of the systems depend on the algorithms to implement. In the
most basic distributed reinforcement learning framework, it is assumed
that the reinforcement learning algorithm is implemented on only one
computing unit, and that the sampling and update processes are
implemented as two or more parallel processes in order to balance
computing resources. To coordinate these processes, inter-process
communication is required. In a more complex framework, the algorithm
runs on multiple computing devices (e.g., in a multi-node computing
cluster), and the functions of the agent may need to be implemented
through cross-node and cross-process communication. A more complex
computing system design is necessary for multiagent systems in which
models of multiple agents need to be updated at the same time. We will
describe the implementation mechanisms of these systems later.

## RLzoo

Taking RLzoo as an example, the following describes the basic modules
required for establishing a single-node reinforcement learning system.
Figure :numref:`ch011/ch11-rlzoo` shows a typical example of such a
system used in the RLzoo algorithm library[^1]. The basic components of
the system include the neural networks, adapters, policy networks, value
networks, environment instances, model learner, and experience replay
buffer.

Let's first introduce three components: neural networks, adapters, and
policy and value networks. Same as in deep learning, neural networks are
used for function approximation based on data. Figure
:numref:`ch011/ch11-rlzoo` involves three common types of neural
networks: fully-connected, convolutional, and recurrent neural networks.
A policy network is a parameterized policy representation by a deep
neural network, whereas a value network is a neural network representing
the state-value function or state-action value function. Policy networks
and value networks are common components in deep reinforcement learning.
The fully-connected, convolutional, and recurrent neural networks are
general neural networks, which are usually important components for
constituting the special networks in reinforcement learning --- policy
networks and value networks. In RLzoo, an adapter is a functional module
for transforming a general neural network into a special neural network.
There are three types of adapters: observation-based adapter, policy
adapter, and action adapter. They perform different tasks in order to
implement a special network for a reinforcement learning agent. First,
an observation-based adapter is used to select the network structure of
the head for the neural network used by the reinforcement learning agent
based on the observation type. Then, a policy adapter decides whether to
use the deterministic policy or stochastic policy as the output policy
for the tail of the policy network based on the type of the
reinforcement learning algorithm. Finally, an action adapter is used to
select the type of the output action distribution, which can be
discrete, continuous, or categorical. The three types of adapters are
collectively referred to as adapters in Figure
:numref:`ch011/ch11-rlzoo`.

![Reinforcement learning system used in the RLzoo algorithmlibrary](../img/ch11/ch11-rlzoo.pdf)
:label:`ch011/ch11-rlzoo`

The policy networks and value networks constitute the core learning
modules of the reinforcement learning agent. A learner is required to
update such modules based on rules (i.e., loss function provided by the
reinforcement learning algorithm). One of the most important roles in
the process of updating learning modules is the input learning data ---
the samples collected during the interaction between the agent and
environment. For *off-policy* reinforcement learning, the samples are
stored in the experience replay buffer, from which the learner obtains
certain samples to update the model. Reinforcement learning algorithms
are classified as either *on-policy* ones if the updated model is the
same as the model used for sampling or off-policy ones if the two models
are different. Off-policy reinforcement learning allows samples that are
collected through interaction with the environment to be extracted for
model update after they are stored in a large buffer for a long time. In
on-policy reinforcement learning, such a buffer may also exist, but it
stores only very recently collected data. This means that we can
consider the updated model and the model used for sampling to be
approximately the same. The experience replay buffer shown in Figure
:numref:`ch011/ch11-rlzoo`, along with the policy networks, value
networks, adapters, and learner, form a single-node reinforcement
learning agent in RLzoo. This agent interacts with environment instances
and collects data to update the model. Environment instantiation allows
parallel sampling in multiple environments.

## Other Systems

Recent research suggests that the development bottleneck in the
reinforcement learning algorithm field may not lie in only the
algorithm, but also in the simulation speed of the simulator from which
the agent can collect data. Issac Gym --- a GPU-based simulation engine
launched by NVIDIA in 2021 --- can run 2--3 times faster on a single GPU
than in CPU-based simulators. The acceleration of GPU-based execution is
described in Chapter 5. GPU-based simulation can significantly
accelerate reinforcement learning tasks because GPUs are capable of
multi-core parallel computing and eliminate the need for data
transmission and communication between CPUs and GPUs. Traditional
reinforcement learning environments such as OpenAI Gym (a common
reinforcement learning benchmark test environment) perform simulated
computing based on CPUs. In contrast, neural network training using deep
learning is performed on GPUs or TPUs.

Data samples collected when the agent interacts with the instantiated
simulation environment on a CPU are temporarily stored in a format of
CPU data. Such data is then transferred to the GPU and converted into a
format of GPU data for model training when necessary. Take PyTorch as an
example: a tensor of the torch.Tensor type can be transferred to the GPU
by setting *device* in the tensor.to(device) function to 'cuda'. In
addition, because model parameters are stored in the GPU's data type,
input data also needs to be transferred from the CPU to GPU when the
model is invoked to perform forward propagation. Furthermore, GPU data
output by the model may need to be converted back into the CPU's data
type. Such redundant conversions significantly increase the time
required for model learning and the workload in using the algorithm. The
design of the Isaac Gym simulator solves this problem of transformation
between computational hardware from underlying frameworks of the
simulators. Because both the simulator and models are implemented on the
GPU, they can communicate with each other without involving the CPU,
thereby eliminating the need for bidirectional data transmission between
the CPU and GPU. In this way, the Isaac Gym simulator accelerates the
simulation process in reinforcement learning tasks.

[^1]: RLzoo code address: <https://github.com/tensorlayer/RLzoo>
