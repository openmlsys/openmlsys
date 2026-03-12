# Design Objectives of Machine Learning Frameworks

*Machine learning frameworks* (e.g., TensorFlow, PyTorch, and MindSpore)
were designed and implemented so that machine learning algorithms could
be developed efficiently for different applications. In a broad sense,
these frameworks achieved the following common design objectives.

1.  **Neural network programming:** The huge success of deep learning
    has solidified neural networks as the core of many machine learning
    applications. People need to customize neural networks to meet their
    specific application requirements --- such customization typically
    results in the creation of convolutional neural networks (CNNs) and
    self-attention neural networks. In order to develop, train, and
    deploy these networks, we need a generic system software.

2.  **Automatic differentiation:** The training of neural networks
    involves continuously computing gradients through the combined use
    of training data, data annotation, and a loss function to
    iteratively improve model parameters. Computing gradients manually
    is a complex and time-consuming task. Consequently, a machine
    learning framework is expected to compute gradients automatically
    based on a neural network application provided by developers. This
    computation process is called automatic differentiation.

3.  **Data management and processing:** Data is the key to machine
    learning. There are several types of data, including training,
    validation, and test datasets, as well as model parameters. A
    machine learning system should be able to read, store, and
    preprocess (data augmentation and cleansing are examples of
    preprocessing) these types of data by itself.

4.  **Model training and deployment:** A machine learning model is
    expected to provide optimal performance. In order to achieve this,
    we need to use an optimization method --- for example, mini-batch
    stochastic gradient descent (SGD) --- to repeatedly compute
    gradients through multi-step iteration. This process is called
    training. Once the training is complete, we can then deploy the
    trained model to the inference device.

5.  **Hardware accelerators:** Many core operations in machine learning
    can be deemed as matrix computation. To accelerate such computation,
    machine learning developers leverage many specially designed
    hardware components referred to as hardware accelerators or AI
    chips.

6.  **Distributed training:** As the volume of training data and the
    number of neural network parameters increase, the amount of memory
    used by a machine learning system far exceeds what a single machine
    can provide. Therefore, a machine learning framework should be able
    to train models on distributed machines.

Early attempts by developers to design such a framework employed
traditional methods such as *neural network libraries* (e.g., Theano and
Caffe) and *data processing frameworks* (e.g., Apache Spark and Google's
Pregel), but the results were disappointing. At that time, neural
network libraries lacked the ability to manage and process large
datasets, deploy models, or perform distributed model execution, meaning
they were not qualified enough for developing today's product-level
machine learning applications even though they supported neural network
development, automatic differentiation, and hardware accelerators.
Furthermore, data-parallel computing frameworks were not suitable for
developing neural network--centered machine learning applications
because they lacked support for neural networks, automatic
differentiation, and accelerators, although such frameworks were already
mature in supporting distributed running and data management.

These drawbacks led many enterprise developers and university
researchers to design and implement their own software frameworks for
machine learning from scratch. In only a few short years, numerous
machine learning frameworks emerged --- well-known examples of these
include TensorFlow, PyTorch, MindSpore, MXNet, PaddlePaddle, OneFlow,
and CNTK. These frameworks boosted the development of AI significantly
in both upstream and downstream industries. Table
:numref:`intro-comparison` lists the differences between machine
learning frameworks and other related systems.


:Differences between machine learning frameworks and related systems

|Design Method               | Neural Network | Automatic Differentiation  | Data Management   | Training and Deployment   | Accelerator   | Distributed Training |
|----------------------------|----------------|----------------------------|-------------------|---------------------------|---------------|----------------------|
|Neural network libraries    | Yes            | Yes                        | No                | No                        | Yes           | No |
|Data processing frameworks  | No             | No                         | Yes               | No                        | No            | Yes |
|Machine learning frameworks | Yes            | Yes                        | Yes               | Yes                       | Yes           | Yes |
:label:intro-comparison

