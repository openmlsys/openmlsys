## Horizontal Federated Learning

### Horizontal Federation in Cloud-Cloud Scenarios

In a horizontal federated learning system, multiple participants with the same data structure collaboratively build a machine learning model through a cloud server. A typical assumption is that the participants are honest while the server is honest but curious; therefore, no participant is allowed to leak raw gradient information to the server. The training process of such a system typically consists of the following four steps:

Step 1: Participants compute training gradients locally, mask selected gradients using encryption, differential privacy, or secret sharing techniques, and send the masked results to the server.

Step 2: The server performs secure aggregation without learning any participant's gradient information.

Step 3: The server sends the aggregated results back to the participants.

Step 4: Participants update their respective models using the decrypted gradients.

Compared to traditional distributed learning, federated learning faces the challenges of unstable training nodes and high communication costs. These challenges prevent federated learning from synchronizing weights across different training nodes after every single training step, as traditional distributed learning does. To improve the computation-to-communication ratio and reduce the high energy consumption caused by frequent communication, Google proposed the Federated Averaging algorithm (FedAvg) in 2017 :cite:`fedavg`. :numfef:`ch10-federated-learning-fedavg` illustrates the overall process of FedAvg. In each training round, clients perform multiple local training steps. Then the server aggregates the weights from multiple clients and computes a weighted average.

![Federated Averaging Algorithm](../img/ch10/ch10-federated-learning-fedavg.png)
:width:`800px`
:label:`ch10-federated-learning-fedavg`

### Horizontal Federation in Device-Cloud Scenarios

The overall process of device-cloud federated learning is the same as cloud-cloud federated learning, but device-cloud federated learning faces additional challenges in the following three aspects:

1. High communication costs. Unlike cloud-cloud federated learning, the communication overhead in device-cloud federated learning primarily lies in the volume of data per communication round, whereas the overhead in cloud-cloud federated learning mainly lies in the frequency of communication. In device-cloud federated learning scenarios, the typical communication network may be WLAN or mobile data, where network communication speeds can be orders of magnitude slower than local computation, making high communication costs a critical bottleneck for federated learning.

2. System heterogeneity. Due to variations in client device hardware (CPU, memory), network connections (3G, 4G, 5G, WiFi), and power supply (battery level), each device in the federated learning network may have different storage, computation, and communication capabilities. Limitations of the network and the devices themselves may result in only a subset of devices being active at any given time. Furthermore, devices may encounter unexpected situations such as battery depletion or network disconnection, leading to temporary unavailability. This heterogeneous system architecture affects the formulation of the overall federated learning strategy.

3. Privacy concerns. Since clients in device-cloud federated learning cannot participate in every iteration round, the difficulty of data privacy protection is higher than in other distributed learning methods. Moreover, during the federated learning process, transmitting model update information between devices and the cloud still poses the risk of exposing sensitive information to third parties or the central server. Privacy protection becomes a critical issue that device-cloud federated learning must address.

To address the challenges posed by device-cloud federated learning, MindSpore Federated designed a distributed FL-Server architecture. The system consists of three components: the scheduler module, the server module, and the client module. The system architecture is shown in :numref:`ch10-federated-learning-architecture`. The functionalities of each module are described below:

- Federated Learning Scheduler:

  The Federated Learning Scheduler (FL-Scheduler) assists in cluster networking and is responsible for issuing management tasks.

- Federated Learning Server:

  The Federated Learning Server (FL-Server) provides client selection, time-limited communication, and distributed federated aggregation capabilities. The FL-Server must be capable of supporting tens of millions of device-cloud devices and supporting the access and secure processing logic of edge servers.

- Federated Learning Client:

  The Federated Learning Client (FL-Client) is responsible for local data training and securely encrypts the uploaded weights when communicating with the FL-Server.

![Federated Learning System Architecture](../img/ch10/ch10-federated-learning-architecture.svg)

:label:`ch10-federated-learning-architecture`

In addition, MindSpore Federated has designed four key features for device-cloud federated learning:

1. Time-limited communication: After the FL-Server and FL-Client establish a connection, a global timer and counter are initiated. When the FL-Server receives model parameters from FL-Clients that meet a certain proportion of all initially connected FL-Clients within a preset time window, aggregation can proceed. If the proportion threshold is not reached within the time window, the system proceeds to the next iteration. This ensures that even with a massive number of FL-Clients, the entire federated learning process will not stall due to excessively long training times or disconnections of individual FL-Clients.

2. Loosely-coupled networking: An FL-Server cluster is used. Each FL-Server receives and distributes weights to a subset of FL-Clients, reducing the bandwidth pressure on any single FL-Server. Additionally, FL-Clients are supported to connect in a loosely-coupled manner. The mid-session withdrawal of any FL-Client will not affect the global task, and any FL-Client can obtain the complete data needed for training from any FL-Server at any time.

3. Encryption module: To prevent model gradient leakage, MindSpore Federated deploys multiple encryption algorithms: Local Differential Privacy (LDP), secure aggregation algorithms based on Multi-Party Computation (MPC), and Huawei's proprietary Sign-based Dimension Selection differential privacy algorithm (SignDS).

4. Communication compression module: MindSpore Federated uses quantization and sparsification techniques to compress and encode weights into smaller data formats when the FL-Server distributes model parameters and when FL-Clients upload model parameters, and decodes the compressed data back to the original format at the receiving end.
