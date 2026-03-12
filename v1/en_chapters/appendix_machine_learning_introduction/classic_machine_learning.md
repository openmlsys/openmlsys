## Classic Machine Learning Methods

Many classic machine learning algorithms, such as Support Vector Machine (SVM), K-Nearest Neighbor (KNN) classification algorithm, and K-Means Clustering Algorithm, differ in various ways---some have network parameters while others do not, some are supervised learning algorithms while others are unsupervised, and their training processes also differ. However, from a systems perspective, they are all based on matrix operations. Below, we briefly introduce these algorithms.

### Support Vector Machine

**Support Vector Machine** (SVM) is a classic machine learning classification algorithm whose core idea is to maximize the distance from the decision boundary to the data points. Here, we use linearly separable data as an example; for non-linearly separable data, the **Kernel Method** can be applied in a similar manner.

If the training data is linearly separable, the objective of SVM is to maximize the **margin**. First, let us define the maximum margin classifier as follows:
$$\min_{{w},b} ~~~\frac{1}{2} ||{w}||^2$$
$$s.t. ~~~y_i ({w}^T {x_i} + b) \geq 1, ~~~\forall 1 \leq i \leq n$$
Its Lagrange multiplier formulation is
$$L({w},b,{\lambda}) = \frac{1}{2} ||{w}||^2 + \sum_{i=1}^n \lambda_i (1-y_i({w}^T {x_i} + b))$$
Since $\frac{1}{2} ||{w}||^2$ is convex, and $\lambda_i (1-y_i({w}^T {x_i} + b))$ is linear (and therefore also convex), the solution to the optimization problem is
$$\max_{\lambda>0} \min_{{w},b} L({w},b, {\lambda})$$
Taking the derivatives of $L$ with respect to ${w},b$, we have
$$\nabla_{{w}} L= {w} - \sum_{i=1}^n \lambda_i y_i {x_i}$$
$$\nabla_b L = - \sum_{i=1}^n \lambda_i y_i$$
Setting the derivatives of $L$ with respect to ${w},b$ to zero, we obtain ${w}^* = \sum_{i=1}^n \lambda_i y_i {x_i}$ and $\sum_{i=1}^n \lambda_i y_i = 0$.
Since when $\lambda$ is fixed, the value of $b$ does not contribute to the objective function, we can set $b^* = 0$.
At this point, by duality theory and the KKT conditions, we obtain:
$$y_i ({w}^{*T} {x_i} + b^*) > 1 \Rightarrow \lambda_i^* = 0$$
$$\lambda_i^* > 0  \Rightarrow y_i ({w}^{*T} {x_i} + b^*) = 1$$
$${w}^* = \sum_{i=1}^n \lambda_i^* y_i {x_i}$$
If $y_i ({w}^{*T} {x_i} + b^*) = 1$, then ${x_i}$ is one of the points closest to the hyperplane $({w}^*,b^*)$; otherwise, it is not. Therefore, ${w}^*$ is a linear combination of the points ${x_i}$ that are closest to the hyperplane $({w}^*,b^*)$.

In this way, through the SVM algorithm, we achieve data classification while maximizing the distance from the decision boundary to the nearest points.
We define the ${x_i}$ satisfying $y_i ({w}^{*T} {x_i} + b^*) = 1$ as **support vectors**, and call the classifier $\hat{y}=sgn({w}^{*T} {x_i} + b^*)$ the support vector machine.

### K-Nearest Neighbor Algorithm

**K-Nearest Neighbor** (KNN) is also a traditional machine learning algorithm that can be used for basic machine learning tasks such as classification and regression. Unlike the SVM algorithm introduced above, the core idea of the K-Nearest Neighbor algorithm is not to separate data of different classes using a decision boundary, but rather to predict the properties of a data point based on the properties of its K nearest neighbors.

When KNN is used for classification, a vote is conducted to predict the class of a sample point. The voters are the K sample points closest to the observation point, where each voting sample point may be assigned different weights, and the "content" of the vote is the class label of the sample point. When processing the voting results, a majority vote decision method is used. That is, if most of the K nearest sample points belong to a certain class, then the sample point is also assigned to that class.

The KNN algorithm can be described as follows: (1) compute the distance from the point to be classified to each known-class point; (2) sort these points by distance and select the K nearest points; (3) tally the votes according to each point's weight, where the vote content is the point's class label; (4) return the class with the highest vote count as the predicted class for the point to be classified.

The KNN algorithm has several key issues that require attention, including the choice of the hyperparameter K, the distance metric, and the classification decision rule. For the hyperparameter K, it should not be too large, as this would lead to significant approximation error, nor too small, as this would lead to significant estimation error. For the distance metric, one can choose Manhattan distance, Euclidean distance, Minkowski distance, and so on. To reduce the error and impact of the K value on prediction results, we can typically impose certain rules on the classification decision, such as giving closer points larger weights and more distant points smaller weights during voting. When implementing the KNN algorithm programmatically, parameters such as weights are computed in matrix form to improve computational efficiency.

### K-Means Clustering Algorithm

**K-Means Clustering Algorithm** is a common unsupervised clustering algorithm in machine learning. Here, we first define the clustering problem: given data points ${x_1},\cdots, {x_n} \in \mathbb{R}^d$ and $K\in \mathbb{N}$, we need to partition them into $K$ clusters ${C_1}, \cdots, {C_K} \in \mathbb{R}^d$ along with the corresponding cluster center ${ C_{(1)}}, \cdots, {C_{(n)}}$ for each data point, so as to minimize the sum of distances $\sum_i ||{x_i} - {C_{(i)}}||^2$.

The K-Means clustering algorithm solves the clustering problem as follows:

-   Randomly initialize ${C_1}, \cdots, {C_K}$

-   Assign each ${x_i}$ to the cluster whose center is nearest

-   Compute and update ${C_K} = \frac{\sum_{{C_{(i)}}={C_K}} {x_i}}{\sum_{{C_{(i)}}={C_K}} 1}$

-   Repeat the above steps until the algorithm converges

It can be proven that the K-Means clustering algorithm monotonically decreases the sum of distances $\sum_i ||{x_i} - {C_{(i)}}||^2$ and eventually converges. However, the algorithm may converge to a local minimum.

Chapter conclusion:

From a systems perspective, regardless of the specific algorithm, machine learning algorithms involving high-dimensional data tasks are all implemented through matrix operations.

## References

:bibliography:`../references/appendix.bib`