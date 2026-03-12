## Overview

Data processing in machine learning scenarios is a typical ETL (Extract, Transform, Load) process. The first stage (Extract) loads datasets from storage devices, and the second stage (Transform) performs transformations on the datasets. Although different machine learning systems adopt different technical approaches when building their data modules, the core components generally include data loading, data shuffling, data transformation, data mini-batch assembly, and data sending. The functionality of each component is described as follows:

-   **Data Loading Component (Load)**: Responsible for loading and reading datasets from storage devices. It must consider both the diversity of storage devices (e.g., local disk/memory, remote disk and memory, etc.) and the diversity of dataset formats (e.g., csv format, txt format, etc.). Based on the characteristics of machine learning tasks, AI frameworks have also proposed unified data storage formats (e.g., Google's TFRecord, Huawei's MindRecord, etc.) to provide higher-performance data loading.

-   **Data Shuffling Component (Shuffle)**: Responsible for randomly shuffling the order of input data according to user-specified methods to improve model robustness.

-   **Data Transformation Component (Map)**: Responsible for performing data transformations, with built-in preprocessing operators for various data types, such as resizing and flipping for images, random noise addition and pitch shifting for audio, and stopword removal and random masking for text processing.

-   **Data Batching Component (Batch)**: Responsible for assembling and constructing a mini-batch of data to send to training/inference.

-   **Data Sending Component (Send)**: Responsible for sending processed data to accelerators such as GPUs or Huawei Ascend for subsequent model computation and updates. High-performance data modules often choose to execute data transfer to devices asynchronously with computation on accelerators to improve overall training throughput.

![Core components of the data module](../img/ch07/7.1/pipeline.png)
:width:`800px`
:label:`pipeline`

Implementing the above components is just the foundation of a data module. We also need to focus on the following aspects:

#### Usability

Data processing involved in AI model training/inference is highly flexible. On one hand, datasets in different application scenarios vary significantly in type and characteristics. When loading datasets, the data module must support specific storage formats for multiple types such as images, text, audio, and video, as well as multiple storage device types including memory, local disks, distributed file systems, and object storage systems. The module needs to abstract and unify the I/O differences in data loading under these complex situations to reduce users' learning costs. On the other hand, different data types often have different processing requirements. In common machine learning tasks, image tasks frequently involve resizing, flipping, and blurring; text tasks require tokenization and vectorization; and speech tasks need Fast Fourier Transform, reverb enhancement, and frequency shifting. To help users address data processing needs in the vast majority of scenarios, the data module needs to support a sufficiently rich set of data preprocessing operators for various types. However, new algorithms and data processing requirements are constantly and rapidly emerging, so we need to support users in conveniently using custom processing operators within the data module to handle scenarios not covered by built-in operators, achieving the best balance between flexibility and efficiency.

#### Efficiency

Since common AI accelerators such as GPUs and Huawei Ascend are primarily designed for Tensor data type computation and do not possess general-purpose data processing capabilities, current mainstream machine learning system data modules typically use CPUs to execute data pipelines. Ideally, before each training iteration begins, the data module should have data ready to minimize the time accelerators spend waiting for data. However, data loading and preprocessing in the data pipeline often face challenging I/O performance and CPU computation performance issues. The data module needs to design file formats that support random access with high read throughput to resolve data loading bottlenecks, and also needs to design reasonable parallel architectures to efficiently execute data pipelines to address computation performance issues. To achieve high-performance training throughput, mainstream machine learning systems all adopt asynchronous execution of data processing and model computation to hide data preprocessing latency.

#### Order Preservation

Unlike conventional data-parallel computing tasks, machine learning model training is sensitive to data input order. When training models using stochastic gradient descent, data is typically fed to the model in a pseudo-random order in each epoch, with a different random order in each training epoch. Since the model's final parameters are sensitive to the order of input data, to help users better debug and ensure reproducibility across different experiments, we need to design mechanisms in the system so that the final order in which data is fed to the model is uniquely determined by the output order of the data shuffling component, rather than being made non-deterministic by parallel data transformations. We will discuss the requirements and specific implementation details of order preservation in later sections.