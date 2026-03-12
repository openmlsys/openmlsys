## Vertical Federated Learning

Now we introduce another type of federated learning algorithm: Vertical Federated Learning. In vertical federated learning, the participating parties possess data with the same sample space but different feature spaces. They perform secure joint modeling using shared sample data, which has broad applications in fields such as finance and advertising. Compared to horizontal federated learning, vertical federated learning requires participants to collaboratively complete data intersection, joint model training, and joint model inference. Moreover, the more participants involved, the higher the complexity of the vertical federated learning system.

Below, we use a two-party example with Enterprise A and Enterprise B to introduce the basic architecture and workflow of vertical federated learning. Suppose Enterprise A has both feature data and label data and can build models independently; Enterprise B has feature data but lacks label data and thus cannot build models independently. Due to privacy regulations and industry standards, data between the two enterprises cannot be directly shared. Enterprise A and Enterprise B can adopt a vertical federated learning solution to collaborate: data stays local, and both parties use their shared sample data for joint modeling and training. Ultimately, both parties obtain a more powerful model.

### Vertical Federation Architecture

![Vertical Federated Two-Party Architecture](../img/ch10/ch10-federated-learning-vfl-arch.svg)
:width:`800px`
:label:`federated-learning-vfl-arch`

Model training in a vertical federated learning system generally consists of the following phases:
- Sample alignment: First, align the sample data with the same ID (Identification) across Enterprise A and Enterprise B. During the data alignment phase, the system employs encryption algorithms to protect the data, ensuring that neither party's user data is exposed.
- Joint training: After determining the shared user data between Enterprise A and Enterprise B, this shared data can be used to collaboratively train a business model. During the model training process, model parameter information is transmitted in an encrypted manner. The trained federated learning model can be deployed across all participating parties in the federated learning system.

### Sample Alignment

Private Set Intersection (PSI) technology is a commonly used solution for data sample alignment in vertical federated learning. There are multiple PSI implementation approaches in the industry: circuit-based, public-key encryption-based, oblivious transfer protocol-based, and fully homomorphic encryption-based. Different PSI approaches have their own advantages and disadvantages. For example, public-key encryption-based approaches do not require an auxiliary server to run but incur high computational overhead for public-key encryption; while oblivious transfer-based approaches have high computational performance but incur large communication overhead. Therefore, in specific applications, the best balance among functionality, performance, and security should be chosen based on the actual scenario.

RSA blind signature is a classic PSI method based on public-key encryption and is one of the widely adopted technologies in current vertical federated learning systems. Below, we describe the basic workflow of the RSA blind signature algorithm using Enterprise A and Enterprise B as an example.

![Vertical Federated Sample Alignment](../img/ch10/ch10-federated-learning-vfl-data.png)
:width:`600px`
:label:`federated-learning-vfl-data`

Enterprise A acts as the server and possesses a set containing label data and sample IDs. Enterprise B acts as the client and possesses a set of sample IDs. First, Enterprise A uses the RSA algorithm to generate a private key and a public key. The private key is retained on the server side, and the public key is sent to Enterprise B.

The server uses the RSA algorithm to compute the signatures of the IDs participating in sample alignment:
$$t_j=H^{'}(K_{a:j})$$
where $K_{a:j}=(H(a_j))^d \ mod \ n$ is the RSA encryption result of $H(a_j)$ encrypted with the private key $d$. $H()$ and $H^{'}()$ are hash functions.

_Similarly, on the client side, the sample IDs are encrypted with the public key and multiplied by a random number $R_{b,i}$ for blinding perturbation:
$$y_i=H(b_i)\cdot(R_{b,i})^e \ mod \ n$$
The client transmits the computed values $\{y_1,...,y_v\}$ to the server side. After receiving the $y_i$ values, the server signs them using the private key $d$ and computes:
$$y_i^{'}=y_i^d \ mod \ n$$
Then the server sends the computed $\{y_1^{'},...,y_v^{'}\}$ and $\{t_1,...,t_w\}$ to the client side.
Upon receiving $y_i^{'}$ and $t_j$, the client first performs the unblinding operation:
$$K_{b:i}={y_i}^{'}/R_{b,i}$$
and aligns its own ID signatures with the server's ID signatures to obtain the ID intersection $I$ in an encrypted and hashed state:
$${t_i}^{'}=H^{'}(K_{b:i}) \\I=\{t_1,...,t_w\}\cap \{{t_1}^{'},...,{t_v}^{'}\}$$

Finally, the aligned sample ID intersection $I$ is sent to the server, and the server uses its own mapping table to independently derive the plaintext results. In this way, Enterprise A and Enterprise B complete the intersection computation of user sets in an encrypted state, and throughout the entire process, non-overlapping sample IDs of both parties are never exposed.

### Joint Training

After sample ID alignment, developers can use the shared data to build machine learning models.

Currently, models such as linear regression, decision trees, and neural networks have been widely applied in vertical federated learning systems. During the model training process in vertical federated learning, a third-party collaborator C is generally introduced to implement the central server functionality, and it is assumed that this third-party collaborator C is trustworthy and will not collude with other participants. The central server acts as a neutral party during training, generating and distributing keys, and decrypting and computing encrypted data. However, the central server role is not mandatory; for example, in a two-party federated learning scenario, a third-party collaborator C is not needed to coordinate the training tasks of both parties, and Enterprise A, which holds the label data, can assume the role of the central server. Without loss of generality, we continue to describe the vertical federated learning joint training process using a scheme that includes the third-party collaborator C.

![Vertical Federated Joint Modeling](../img/ch10/ch10-federated-learning-vfl-train.svg)
:width:`800px`
:label:`federated-learning-vfl-train`

- Step 1: The third-party collaborator C creates a key pair and sends the public key to Enterprise A and B.
- Step 2: Enterprise A and B separately compute the intermediate results needed for gradient and loss computation, and encrypt and exchange them.
- Step 3: Enterprise A and B separately compute the encrypted gradients and add masks. Meanwhile, Enterprise A also computes the encrypted loss value. After computation, Enterprise A and B send the encrypted values to the third-party collaborator C.
- Step 4: The third-party collaborator C decrypts the gradients and loss values, and sends the results back to Enterprise A and B.
- Step 5: Enterprise A and B first remove the masks from the received gradient values, and then update their local model parameters.

Throughout the entire training process, any sensitive data between Enterprise A and B is encrypted using encryption algorithms before leaving their respective trust domains. Homomorphic Encryption (HE) is one of the commonly used algorithms in federated learning frameworks. Homomorphic encryption means that performing certain operations on two pieces of encrypted data and then directly decrypting the result yields the same outcome as performing the same operations on the original data. When this operation is addition, it is called additive homomorphic encryption. We denote the encryption function as $[[\cdot]]$.
