# Data Processing Framework

In the previous two chapters, we introduced the frontend and backend of compilers, elaborating on the optimization process of transforming source programs into target programs. Beyond enabling high-performance execution on accelerator chips during training and inference, we also need to efficiently deliver data to these chips to achieve optimal end-to-end performance. Machine learning model training and inference require loading datasets from storage devices (such as local disks, memory, and remote storage systems), performing a series of processing transformations on the datasets, and sending the processed results to GPUs, Huawei Ascend, or other accelerators for model computation. Performance issues at any step in this pipeline can negatively impact training and inference throughput. In this chapter, we will focus on how to design and implement a data system tailored for machine learning scenarios, helping users easily construct various complex data pipelines while ensuring sufficiently high execution performance so that data preprocessing does not become a performance bottleneck for model training and inference.

This chapter introduces the data module in machine learning systems from three dimensions: usability, efficiency, and order preservation. In the first two sections, we discuss how to build a user-friendly data module, including how to design programming abstractions that allow users to describe complex preprocessing workflows in just a few lines of code, and how to provide rich built-in operators for usability while flexibly supporting user-defined operators to cover long-tail requirements. After users construct their data processing workflows, the data module is responsible for efficiently scheduling and executing the data pipeline to achieve optimal data processing throughput. Efficiently executing the data pipeline is a challenging task, as we face both I/O performance issues in data loading and computational performance issues in data processing. To address these challenges, we will introduce file format designs for high-throughput data loading, as well as parallel architecture designs that fully leverage multi-core CPU computing power. Moreover, unlike conventional data-parallel computing tasks, most machine learning scenarios have special `order preservation` requirements for data input and output sequences. We will dedicate a section to introducing what order preservation is and how to design corresponding components within the data module's parallel architecture to meet this requirement. After studying the above content, readers will gain a deep understanding of how to build an efficient and user-friendly data module for machine learning scenarios. Finally, as extended content, we will draw on practical experience from both academia and industry to introduce how to scale our data processing module to meet training performance requirements when single-machine processing performance is insufficient. The learning objectives of this chapter include:

-   Understand the key components and their functions in the machine learning data module architecture

-   Understand the design of different data module user programming interfaces

-   Master file format design for high-performance data loading

-   Master the parallel architecture of the data module in machine learning systems

-   Master the concept and solutions for data order preservation in machine learning system data modules

-   Understand two approaches for scaling single-machine data processing performance


```toc
:maxdepth: 2

requirements
program_model
performance
data_order
extension
summary
```