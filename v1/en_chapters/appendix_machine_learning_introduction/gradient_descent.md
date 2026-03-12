## Gradient Descent and Backpropagation

The previous section provided a general introduction to classic neural networks. Now an important question arises: how are the parameters in these networks determined? If the problem can be solved by a simple perceptron, the parameters can be manually determined. However, for deep networks, parameter determination needs to be automated---this is the so-called network training, and this process requires us to define a **loss function** to guide the direction of training optimization.
Common loss functions include: 1) Mean Squared Error (MSE), which measures the distance between vectors,
$\mathcal{L} = \frac{1}{N}\|{y}-\hat{{y}}\|^{2}_{2} = \frac{1}{N}\sum_{i=1}^N(y_{i}-\hat{y}_{i})^{2}$
and Mean Absolute Error (MAE),
$\mathcal{L} = \frac{1}{N}\sum_{i=1}^{N}|y_{i}-\hat{y}_{i}|$
, where $N$ represents the number of data samples used for averaging, $y$ represents the ground truth labels, and $\hat{y}$ represents the predicted labels output by the network.
2) Cross Entropy, which can be used for classification tasks,
$\mathcal{L} = - \frac{1}{N} \sum_{i=1}^N \bigg(y_{i}\log\hat{y}_{i} + (1 - y_{i})\log(1 - \hat{y}_{i})\bigg)$, where the loss value is zero if and only if the output labels match the predicted labels.

With the loss value computed, we can use large amounts of labeled data and optimization methods to update the model parameters. The most commonly used method is **gradient descent**. As shown in :numref:`gradient_descent2`,
initially, the model parameters ${w}$ are randomly selected. Then the partial derivative of the loss with respect to the parameters $\frac{\partial \mathcal{L}}{\partial {w}}$ is computed, and optimization is performed through repeated iterations of
${w}:={w}-\alpha\frac{\partial \mathcal{L}}{\partial {w}}$. This optimization process effectively reduces the loss value to achieve the task objective, where $\alpha$ is the **learning rate** that controls the optimization step size.
In practice, the minimum value obtained by gradient descent is very likely a local minimum rather than the global minimum. However, since deep neural networks provide strong data representation capability, the local minimum can be very close to the global minimum, and the loss value can be sufficiently small.

![Introduction to gradient descent. (Left) Only one trainable parameter $w$; (Right) Two trainable parameters ${w}=[w_1,w_2]$. After continuously updating and iterating the parameters, the loss value $\mathcal{L}$ gradually decreases. However, due to the existence of many local optima, we often cannot reach the global optimum.](../img/ch_basic/gradient_descent2.png)
:width:`600px`
:label:`gradient_descent2`

The next question is: how do we implement gradient descent in deep neural networks? This requires computing the partial derivatives $\frac{\partial \mathcal{L}}{\partial {w}}$ of the parameters at each layer, which can be achieved using **backpropagation** :cite:`rumelhart1986learning,lecun2015deep`.
Next,
we introduce an intermediate quantity ${\delta}=\frac{\partial \mathcal{L}}{\partial {z}}$ to represent the partial derivative of the loss function $\mathcal{L}$
with respect to the neural network output ${z}$ (before the activation function, not $a$),
and ultimately obtain $\frac{\partial \mathcal{L}}{\partial {w}}$.

We illustrate the backpropagation algorithm with an example below.
Let the layer index be $l=1, 2, \ldots  L$ (the output layer, i.e., the last layer, has index $L$).
For each network layer, we have the output ${z}^l$, the intermediate value ${\delta}^l=\frac{\partial \mathcal{L}}{\partial {z}^l}$, and an activation output ${a}^l=f({z}^l)$
(where $f$ is the activation function).
We assume the model is a multi-layer perceptron using the Sigmoid activation function, with Mean Squared Error (MSE) as the loss function. That is, we define:

-   Network structure ${z}^{l}={W}^{l}{a}^{l-1}+{b}^{l}$

-   Activation function ${a}^l=f({z}^l)=\frac{1}{1+{\rm e}^{-{z}^l}}$

-   Loss function $\mathcal{L}=\frac{1}{2}\|{y}-{a}^{L}\|^2_2$

We can directly compute the partial derivative of the activation output with respect to the pre-activation output:

-   $\frac{\partial {a}^l}{\partial {z}^l}=f'({z}^l)=f({z}^l)(1-f({z}^l))={a}^l(1-{a}^l)$

and the partial derivative of the loss function with respect to the activation output:

-   $\frac{\partial \mathcal{L}}{\partial {a}^{L}}=({a}^{L}-{y})$

With these results, to further obtain the partial derivatives of the loss function with respect to each parameter, we can use the **chain rule**, detailed as follows:

First, starting from the output layer ($l=L$, the last layer), we propagate the error backward. By the chain rule, we first compute the intermediate quantity of the output layer:

-   ${\delta}^{L}
    =\frac{\partial \mathcal{L}}{\partial {z}^{L}}
    =\frac{\partial \mathcal{L}}{\partial {a}^{L}}\frac{\partial {a}^L}{\partial {z}^{L}}=({a}^L-{y})\odot({a}^L(1-{a}^L))$

Besides the intermediate value ${\delta}^{L}$ of the output layer ($l=L$), how do we compute the intermediate values ${\delta}^{l}$ for the other layers ($l=1, 2, \ldots , L-1$)?

-   Given the model structure ${z}^{l+1}={W}^{l+1}{a}^{l}+{b}^{l+1}$, we can directly obtain $\frac{\partial {z}^{l+1}}{\partial {a}^{l}}={W}^{l+1}$; moreover, we already know that $\frac{\partial {a}^l}{\partial {z}^l}={a}^l(1-{a}^l)$

-   Then by the chain rule, we can obtain ${\delta}^{l}
    =\frac{\partial \mathcal{L}}{\partial {z}^{l}}
    =\frac{\partial \mathcal{L}}{\partial {z}^{l+1}}\frac{\partial {z}^{l+1}}{\partial {a}^{l}}\frac{\partial {a}^{l}}{\partial {z}^{l}}
    =({W}^{l+1})^\top{\delta}^{l+1}\odot({a}^l(1-{a}^l))$

Having computed the intermediate values ${\delta}^l, l=1, 2, \ldots , L$ for all layers using the above derivation, we can then compute the partial derivatives of the loss function with respect to the parameters of each layer: $\frac{\partial \mathcal{L}}{\partial {W}^l}$ and $\frac{\partial \mathcal{L}}{\partial {b}^l}$, and use gradient descent to update the parameters at each layer.

-   Given the model structure ${z}^l={W}^l{a}^{l-1}+{b}^l$, we can compute
    $\frac{\partial {z}^{l}}{\partial {W}^l}={a}^{l-1}$ and
    $\frac{\partial {z}^{l}}{\partial {b}^l}=1$

-   Then by the chain rule, we can obtain $\frac{\partial \mathcal{L}}{\partial {W}^l}=\frac{\partial \mathcal{L}}{\partial {z}^l}\frac{\partial {z}^l}{\partial {W}^l}={\delta}^l({a}^{l-1})^\top$
    ,
    $\frac{\partial \mathcal{L}}{\partial {b}^l}=\frac{\partial \mathcal{L}}{\partial {z}^l}\frac{\partial {z}^l}{\partial {b}^l}={\delta}^l$

After obtaining all partial derivatives $\frac{\partial \mathcal{L}}{\partial {W}^l}$ and
$\frac{\partial \mathcal{L}}{\partial {b}^l}$, we can update all parameters ${W}^l$
and ${b}^l$ using gradient descent:

-   ${W}^l:={W}^l-\alpha\frac{\partial \mathcal{L}}{\partial {W}^l}$,
    ${b}^l:={b}^l-\alpha\frac{\partial \mathcal{L}}{\partial {b}^l}$

However, there is still one issue to address: each time gradient descent updates the parameters, it needs to compute the loss value under the current parameters. When the training dataset is large ($N$ is large), computing the loss value using the entire training set for each update would be computationally prohibitive.
To reduce the computational cost, we use **Stochastic Gradient Descent** (SGD) to compute the loss value. Specifically, instead of using all training data, we randomly select a subset of data samples from the training set to compute the loss value, such as 16, 32, 64, or 128 data samples. The number of samples is called the **batch size**.
Furthermore, setting the learning rate is also very important. If the learning rate is too large, we may not be able to approach the valley of the minimum; if it is too small, training proceeds too slowly.
Adaptive learning rates, such as Adam :cite:`KingmaAdam2014`, RMSProp :cite:`tieleman2012rmsprop`, and
Adagrad :cite:`duchi2011adagrad`, automatically adjust the learning rate during training to achieve fast convergence and reach the minimum.