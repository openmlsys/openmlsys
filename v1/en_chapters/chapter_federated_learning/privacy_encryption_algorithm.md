## Privacy Encryption Algorithms

During the federated learning process, user data is only used for training on local devices and does not need to be uploaded to the central FL-Server. This can prevent the direct leakage of users' personal data. However, in the federated learning framework, uploading model weights to the cloud in plaintext still poses the risk of indirectly leaking user privacy. After obtaining the plaintext weights uploaded by users, adversaries can recover users' personal training data through reconstruction, model inversion, and other attacks, leading to user privacy leakage.

The MindSpore Federated framework provides secure aggregation algorithms based on Local Differential Privacy (LDP), Multi-Party Computation (MPC), and Huawei's proprietary Sign-based Dimension Selection differential privacy algorithm (SignDS), which add noise or perturbation to the local model weights before uploading them to the cloud. These algorithms address the privacy leakage problem in federated learning while ensuring model usability.

### LDP-Based Secure Aggregation

Differential privacy is a mechanism for protecting user data privacy. Differential privacy is defined as:
$$
Pr[\mathcal{K}(D)\in S] \le e^{\epsilon} Pr[\mathcal{K}(D') \in S]+\delta
$$

For two datasets $D$ and $D'$ that differ by only one record, the probability that the output of a randomized algorithm $\mathcal{K}$ falls within a subset of set $S$ satisfies the above formula. $\epsilon$ is the differential privacy budget, $\delta$ is the perturbation parameter, and smaller values of $\epsilon$ and $\delta$ indicate that the output distributions of $\mathcal{K}$ on $D$ and $D'$ are closer.

In federated learning, suppose the model weight matrix after local training on an FL-Client is $W$. Since the model "memorizes" the characteristics of the training set during training, an adversary can use $W$ to reconstruct the user's training dataset.

MindSpore Federated provides an LDP-based secure aggregation algorithm to prevent privacy data leakage when local model weights are uploaded to the cloud.

The FL-Client generates a differential noise matrix $G$ with the same dimensions as the local model weight matrix $W$, and then adds the two together to obtain a weight matrix $W_p$ that satisfies the differential privacy definition:

$$
W_p=W+G
$$

The FL-Client uploads the noisy model weight matrix $W_p$ to the cloud-side FL-Server for federated aggregation. The noise matrix $G$ essentially adds a layer of masking to the original model, reducing the risk of the model leaking sensitive data while also affecting the convergence of model training. How to achieve a better balance between model privacy and usability remains an open research question. Experiments show that when the number of participants $n$ is sufficiently large (generally above 1000), most noise can cancel each other out, and the local differential privacy mechanism has no significant impact on the accuracy and convergence of the aggregated model.

### MPC-Based Secure Aggregation

Although differential privacy technology can adequately protect user data privacy, when the number of participating FL-Clients is small or the Gaussian noise amplitude is large, model accuracy can be significantly affected. To simultaneously satisfy both model protection and model convergence requirements, MindSpore Federated provides an MPC-based secure aggregation scheme.

Although differential privacy technology can adequately protect user data privacy, when the number of participating FL-Clients is small or the Gaussian noise amplitude is large, model accuracy can be significantly affected. To simultaneously satisfy both model protection and model convergence requirements, MindSpore Federated provides an MPC-based secure aggregation scheme.

In this training mode, suppose the set of participating FL-Clients is $U$. For any FL-Client $u$ and $v$, they negotiate a pair of random perturbations $p_{uv}$ and $p_{vu}$ that satisfy

$$
\label{puv}
    p_{uv}=
    \begin{cases}
    -p_{vu}, &u{\neq}v\\
    0, &u=v
    \end{cases}
$$
Thus, each FL-Client $u$ adds the perturbations negotiated with other users to its original model weights $x_u$ before uploading them to the FL-Server:

$$
x_{encrypt}=x_u+\sum\limits_{v{\in}U}p_{uv}
$$

Consequently, the FL-Server aggregation result $\overline{x}$ is:
$$
\label{eq:juhejieguo}
\overline{x}=\sum\limits_{u{\in}U}(x_{u}+\sum\limits_{v{\in}U}p_{uv})=\sum\limits_{u{\in}U}x_{u}+\sum\limits_{u{\in}U}\sum\limits_{v{\in}U}p_{uv}=\sum\limits_{u{\in}U}x_{u}
$$
The above process only introduces the main idea of the aggregation algorithm. The MPC-based aggregation scheme is lossless in terms of accuracy, at the cost of additional communication rounds.

### LDP-SignDS Algorithm-Based Secure Aggregation

For the previous dimension-wise noise-adding LDP algorithm, the noise scale added to each dimension is essentially proportional to the number of model parameters. Therefore, for high-dimensional models, a very large number of participants may be needed to mitigate the impact of noise on model convergence. To address this "dimension dependence" issue, MindSpore Federated further provides the **Sign-based Dimension Selection (SignDS)** :cite:`jiang2022signds` algorithm based on dimension selection.

The main idea of the SignDS algorithm is as follows: for each true local update $\Delta\in\mathbb{R}^{d}$, the FL-Client first selects a small subset of the most significantly updated dimensions to construct a Top-K set $S_k$, and then selects a dimension set $J$ based on this to return to the FL-Server. The FL-Server constructs a corresponding sparse update $\Delta^\prime$ based on the dimension set $J$ and aggregates all sparse updates to update the global model. Since local model updates are correlated with local data information, directly selecting the true largest update dimensions may lead to privacy leakage. To address this, the SignDS algorithm provides privacy guarantees in two aspects. On one hand, the algorithm uses an Exponential Mechanism (EM :cite:`mcsherry2007mechanism`)-based dimension selection algorithm **EM-MDS**, ensuring that the selected dimension set satisfies strict $\epsilon$-LDP guarantees; on the other hand, when constructing sparse updates, a constant value is assigned to the selected dimensions instead of directly using the actual update values, ensuring that the sparse updates are no longer directly correlated with local data. Since the dimension selection satisfies $\epsilon$-LDP and the update values assigned to the selected dimensions are independent of local data, by the post-processing property of differential privacy :cite:`dwork2014algorithmic`, the constructed sparse updates also satisfy $\epsilon$-LDP guarantees. **Compared to the previous dimension-wise noise-adding LDP algorithm, the SignDS algorithm can significantly improve training accuracy for high-dimensional models. Moreover, since FL-Clients only need to upload a small subset of dimension values rather than all model weights, the uplink communication volume of federated learning is also greatly reduced.**

Below, we provide detailed introductions to the construction of the Top-K set $S_k$ and the EM-MDS dimension selection algorithm.

First, since actual update values can be positive or negative, directly assigning the same constant value to all selected dimensions may significantly change the model update direction and affect model convergence. To solve this problem, SignDS proposes a sign-based Top-K set construction strategy. Specifically, the algorithm introduces an additional sign variable $s\in\\{-1,1\\}$. This variable is randomly sampled with equal probability by the FL-Client and is used to determine the Top-K set $S_k$ of the local update $\Delta$. If $s=1$, we sort $\Delta$ by **actual update values** and record the $k$ dimensions with the **largest** updates as $S_k$. We further randomly select a subset of dimensions from $S_k$ and use $s=1$ as the update value for these dimensions to construct the sparse update. Intuitively, the update values of dimensions in $S_k$ are likely to be greater than zero. Therefore, assigning $s=1$ to the selected dimensions will not cause a large deviation in the model update direction, thereby mitigating the impact on model accuracy. Similarly, when $s=-1$, we select the $k$ dimensions with the **smallest** updates as $S_k$ and assign $s=-1$ to the selected dimensions.

Next, we further introduce the EM-MDS algorithm for dimension selection. In brief, the purpose of the EM-MDS algorithm is to randomly select a dimension set $J\in\mathcal{J}$ from the output dimension domain $\mathcal{J}$ with a certain probability $\mathcal{P}$, where different dimension sets correspond to different probabilities. We assume that $J$ contains a total of $h$ dimensions, of which $\nu$ dimensions belong to the Top-K set (i.e., $|S_k \cap J|=\nu$, where $\nu\in[0,h]$), and the other $h-\nu$ dimensions belong to the non-Top-K set. Intuitively, the larger $\nu$ is, the more Top-K dimensions $J$ contains, and the better the model convergence. Therefore, we want to assign higher probabilities to dimension sets with larger $\nu$. Based on this idea, we define the score function as:
$$
u(S_{k}, J) = 𝟙(|S_k\cap J| \geq \nu_{th}) =  𝟙(\nu \geq \nu_{th})
$$
:eqlabel:`score_function`

$u(S_{k}, J)$ measures whether the number of Top-K dimensions contained in the output dimension set $J$ exceeds a certain threshold $\nu_{th}$ ($\nu_{th}\in[1,h]$): it equals 1 if exceeded, and 0 otherwise. Furthermore, the sensitivity of $u(S_{k}, J)$ can be computed as:

$$
\phi = \max_{J\in\mathcal{J}} ||u(S_{k}, J) - u(S^\prime_{k}, J)||= 1 - 0 = 1
$$
:eqlabel:`sensitivity`

Note that :eqref:`sensitivity` holds for any pair of different Top-K sets $S_k$ and $S_k^\prime$.

Based on the above definitions, the EM-MDS algorithm is described as follows:

*Given the Top-K set $S_k$ of the true local update $\Delta\in\mathbb{R}^{d}$ and the privacy budget $\epsilon$, the sampling probability of the output dimension set $J\in\mathcal{J}$ is:*

$$
    \mathcal{P}=\frac{\mathrm{exp}(\frac{\epsilon}{\phi}\cdot u(S_{k}, J))}{\sum_{J^\prime\in\mathcal{J}}\mathrm{exp}(\frac{\epsilon}{\phi}\cdot u(S_{k}, J^\prime))}
    =
    \frac{\mathrm{exp}(\epsilon\cdot 𝟙(\nu \geq \nu_{th}))}{\sum_{\tau=0}^{\tau=h}\omega_{\tau}\cdot \mathrm{exp}(\epsilon\cdot 𝟙(\tau\geq\nu_{th}))}
    =
    \frac{\mathrm{exp}(\epsilon\cdot 𝟙(\nu \geq \nu_{th}))}{\sum_{\tau=0}^{\tau=\nu_{th}-1}\omega_{\tau} + \sum_{\tau=\nu_{th}}^{\tau=h}\omega_{\tau}\cdot \mathrm{exp}(\epsilon)}
$$
:eqlabel:`emmds`

*where $\nu$ is the number of Top-K dimensions contained in $J$, $\nu_{th}$ is the score function threshold, $J^\prime$ is any output dimension set, and $\omega_{\tau}=\binom{k}{\tau}\binom{d-k}{h-\tau}$ is the number of all sets containing $\tau$ Top-K dimensions.*

We further provide the privacy proof of the EM-MDS algorithm:

For each FL-Client, given a randomly sampled sign value $x$, let the Top-K sets of any two local updates $\Delta$ and $\Delta^\prime$ be denoted as $S_k$ and $S_k^\prime$. For any output dimension set $J\in\mathcal{J}$, let $\nu=|S_k \cap J|$ and $\nu^\prime=|S_k^\prime \cap J|$ be the intersection sizes of $J$ with the two Top-K dimension sets. According to :eqref:`emmds`, the following inequality holds:

$$
\frac{\mathrm{Pr}\[J|\Delta\]}{\mathrm{Pr}\[J|\Delta^\prime\]} = \frac{\mathrm{Pr}\[J|S_{k}\]}{\mathrm{Pr}\[J|S^\prime_{k}\]} = \frac{\frac{\mathrm{exp}(\frac{\epsilon}{\phi}\cdot u(S_{k}, J))}{\sum_{J^\prime\in\mathcal{J}}\mathrm{exp}(\frac{\epsilon}{\phi}\cdot u(S_{k}, J^\prime))}}{\frac{\mathrm{exp}(\frac{\epsilon}{\phi}\cdot u(S^\prime_{k}, J))}{\sum_{J^\prime\in\mathcal{J}}\mathrm{exp}(\frac{\epsilon}{\phi}\cdot u(S^\prime_{k}, J^\prime))}}
    = \frac{\frac{\mathrm{exp}(\epsilon\cdot 𝟙(\nu \geq \nu_{th}))}{\sum_{\tau=0}^{\tau=h}\omega_{\tau}\cdot \mathrm{exp}(\epsilon\cdot 𝟙(\tau\geq\nu_{th}))}}{\frac{
    \mathrm{exp}(\epsilon\cdot 𝟙(\nu^\prime \geq \nu_{th}))}{\sum_{\tau=0}^{\tau=h}\omega_{\tau}\cdot \mathrm{exp}(\epsilon\cdot 𝟙(\tau\geq\nu_{th}))}} \\
    = \frac{\mathrm{exp}(\epsilon\cdot 𝟙(\nu \geq \nu_{th}))}{
    \mathrm{exp}(\epsilon\cdot 𝟙(\nu^\prime \geq \nu_{th}))}
    \leq \frac{\mathrm{exp}(\epsilon\cdot 1)}{\mathrm{exp}(\epsilon\cdot 0)} = \mathrm{exp}(\epsilon)
$$

*This proves that the EM-MDS algorithm satisfies the $\epsilon$-LDP guarantee.*

It is worth noting that computing :eqref:`emmds` requires first determining the Top-K dimension count threshold $\nu_{th}$. To this end, we first derive the probability distribution and expectation of the number of Top-K dimensions contained in any output dimension set $J$ given the threshold $\nu_{th}$:

$$
\mathrm{Pr}(\nu=\tau|\nu_{th})=
    \begin{cases}
        \omega_{\tau} / \Omega \quad \quad \quad \quad \quad \mathrm{ } &if \quad \tau\in\[0,\nu_{th}\) \\
        \omega_{\tau}\cdot\mathrm{exp}(\epsilon) / \Omega \quad \quad &if \quad \tau\in\[\nu_{th},h\]
    \end{cases}
$$
:eqlabel:`discrete-prob`

$$
    \mathbb{E}\[\nu|\nu_{th}\] = \sum_{\tau=0}^{\tau=h}\tau\cdot \mathrm{Pr}(\nu=\tau|\nu_{th})
$$
:eqlabel:`expectation`

Here, $\Omega$ is the denominator part of $\mathcal{P}$ in :eqref:`emmds`. Intuitively, the higher $\mathbb{E}\[\nu|\nu_{th}\]$ is, the greater the probability that the randomly sampled set $J$ contains Top-K dimensions, and thus the better the model utility. Therefore, we determine the threshold that maximizes $\mathbb{E}\[\nu|\nu_{th}\]$ as the target threshold $\nu_{th}^{\*}$, i.e.:

$$
\nu_{th}^{\*} = \underset{\nu_{th}\in\[1, h\]}{\operatorname{argmax}} \mathbb{E}\[\nu|\nu_{th}\]
$$
:eqlabel:`threshold`

Finally, we describe the detailed workflow of the SignDS algorithm in :numref:`signds_workflow`. Given a local model update $\Delta$, we first randomly sample a sign value $s$ and construct the Top-K set $S_k$. Next, we determine the threshold $\nu_{th}^{\*}$ according to :eqref:`threshold` and select the output set $J$ following the probability defined in :eqref:`emmds`. Considering that the output domain $\mathcal{J}$ contains $\binom{d}{k}$ possible dimension sets, directly sampling a combination from $\mathcal{J}$ with a certain probability would require very high computational and space costs. Therefore, we adopt an inverse sampling algorithm to improve computational efficiency. Specifically, we first sample a random value $\beta\sim U(0,1)$ from the standard uniform distribution, and determine the number of Top-K dimensions $\nu$ in the output dimension set based on the cumulative distribution function $CDF_{\tau}$ of $p(\nu=\tau|\nu_{th})$ in :eqref:`discrete-prob`. Finally, we randomly select $\nu$ dimensions from the Top-K set $S_k$ and randomly sample $h-\nu$ dimensions from the non-Top-K set to construct the final output dimension set $J$.

![SignDS Workflow](../img/ch10/ch10-federated-learning-signds.PNG)
:width:`800px`
:label:`signds_workflow`
