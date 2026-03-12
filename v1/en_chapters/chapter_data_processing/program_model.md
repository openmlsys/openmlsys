## Usability Design

In this section, we focus on how to design a user-friendly data module for machine learning systems. As mentioned earlier, usability requires the data module to provide good programming abstractions and interfaces so that users can conveniently construct data processing pipelines, while also supporting users in flexibly registering and using custom operators within the data pipeline to meet diverse and specialized requirements. We will explore this topic from two aspects: programming interface abstraction and custom operator registration mechanisms.

### Programming Abstraction and Interfaces

In :numref:`image_process_pipeline`, we present a classic data preprocessing pipeline for training an image classification model. After loading the dataset from storage devices, we perform a series of operations on the image data, including decoding, resizing, rotation, normalization, and channel transposition. We also apply specific preprocessing operations to the dataset labels, and finally send the processed data to the accelerator chip for model computation. We hope that the programming abstractions provided by the data module are sufficiently high-level so that users can describe the data processing logic in just a few lines of code without getting bogged down in excessive, repetitive implementation details. At the same time, we need to ensure that this set of high-level abstractions is sufficiently general to meet diverse data preprocessing requirements. Once we have a good programming abstraction, we will use a code snippet that implements the data preprocessing pipeline described in the figure below using MindSpore's data module programming interfaces as an example to demonstrate how significantly a well-designed programming abstraction can reduce the user's programming burden.

![Data preprocessing example](../img/ch07/7.2/image_process_pipeline.png)
:width:`800px`
:label:`image_process_pipeline`


In fact, programming abstractions for data computation have long been extensively studied in the field of general-purpose data-parallel computing systems, and a relatively unified consensus has been reached --- that is, to provide LINQ-style :cite:`meijer2006linq` programming abstractions. The key characteristic is to let users focus on describing dataset creation and transformations, while delegating the efficient implementation and scheduling of these operations to the data system's runtime. Some excellent systems such as Naiad :cite:`murray2013naiad`,
Spark :cite:`zaharia2010spark`, and DryadLINQ :cite:`fetterly2009dryadlinq` have all adopted this programming model. We will use Spark as an example for a brief introduction.

Spark provides users with a programming model based on the concept of Resilient Distributed Datasets (RDD). An RDD is a read-only distributed data collection. Users primarily describe the creation and transformation of RDDs through Spark's programming interfaces. Let us elaborate with a Spark example. The following code demonstrates counting the number of lines containing the "ERROR" field in a log file. We first create a distributed dataset `file` by reading from a file (as mentioned earlier, an RDD represents a collection of data; here `file` is actually a collection of log lines).
We apply a filter operation to this `file` dataset to obtain a new dataset `errs` that retains only log lines containing the "ERROR" field. Then we apply a map operation to each element in `errs` to obtain the dataset `ones`. Finally, we perform a reduce operation on the `ones` dataset to get our desired result --- the number of log lines containing the "ERROR" field in the `file` dataset.

```java
val file = spark.textFile("hdfs://...")
val errs = file.filter(_.contains("ERROR"))
val ones = errs.map(_ => 1)
val count = ones.reduce(_+_)
```



We can see that users need only four lines of code to accomplish the complex task of counting specific field occurrences in a distributed dataset. This is made possible by Spark's core RDD programming abstraction. From the computation flow visualization in :numref:`rdd_transformation_example`, we can also clearly see that after creating the dataset, users only need to describe the operators applied to the dataset, while the execution and implementation of the operators are handled by the system's runtime.

![The core of Spark programming --- RDD transformations](../img//ch07/7.2/RDD.png)

:width:`800px`
:label:`rdd_transformation_example`
The data modules in mainstream machine learning systems have also adopted similar programming abstractions, such as TensorFlow's data module tf.data :cite:`murray2021tf`
and MindSpore's data module MindData. Next, we will use MindData's interface design as an example to introduce how to design good programming abstractions for the machine learning scenario to help users conveniently construct the diverse data processing pipelines needed in model training.

MindData is the data module of the machine learning system MindSpore, primarily responsible for completing data preprocessing tasks in machine learning model training. The core programming abstraction that MindData provides to users is based on Dataset transformations. Here, Dataset is a data frame concept (Data
Frame), meaning a Dataset is a multi-row, multi-column relational data table where each column has a column name.

![MindSpore
Dataset example](../img/ch07/7.2/dataset_table.png)
:width:`800px`
:label:`mindspore dataset example`

Based on this programming model, combined with the key processing steps in the machine learning data workflow introduced in the first section, MindData provides users with dataset operation operators for performing shuffle, map, batch, and other transformation operations on datasets. These operators take a Dataset as input and produce a newly processed Dataset as output. We list the typical dataset transformation interfaces as follows:

:Dataset operation interfaces supported by MindSpore

| Dataset Operation    | Description                                                        |
| -------------------- | ------------------------------------------------------------------ |
| batch                | Groups multiple data rows in the dataset into a mini-batch         |
| map                  | Applies transformation operations to each data row in the dataset  |
| shuffle              | Randomly shuffles the order of data rows in the dataset            |
| filter               | Filters data rows in the dataset, retaining only rows that pass the filter condition |
| prefetch             | Prefetches data from the storage medium                            |
| project              | Selects certain columns from the Dataset table for subsequent processing |
| zip                  | Merges multiple datasets into one dataset                          |
| repeat               | In multi-epoch training, repeats the entire data pipeline multiple times |
| create_dict_iterator | Creates an iterator that returns dictionary-type data for the dataset |
| ...                  | ...                                                                |

The above describes the dataset interface abstractions, while the specific operations on datasets are actually defined by concrete data operator functions. For user convenience, MindData has built-in implementations of rich data operator libraries for common data types and their common processing needs in the machine learning domain. For the vision domain, MindData provides common operators such as Decode, Resize, RandomRotation, Normalize, and HWC2CHW (channel transposition); for the text domain, MindData provides operators such as Ngram, NormalizeUTF8, and BertTokenizer; for the audio domain, MindData provides operators such as TimeMasking, LowpassBiquad, and ComplexNorm. These commonly used operators can cover the vast majority of user requirements.

In addition to supporting flexible Dataset transformations, MindData also provides flexible Dataset creation to address the challenge of numerous dataset types with varying formats and organizations. There are mainly three categories:

-   Creating from built-in datasets: MindData has a rich set of built-in classic datasets, such as CelebADataset, Cifar10Dataset, CocoDataset, ImageFolderDataset, MnistDataset, VOCDataset, etc. If users need to use these common datasets, they can achieve out-of-the-box usage with a single line of code. MindData also provides efficient implementations for loading these datasets to ensure users enjoy the best read performance.

-   Loading from MindRecord: MindRecord is a high-performance, general-purpose data storage file format designed for MindData. Users can convert their datasets to MindRecord and then leverage MindSpore's relevant APIs for efficient reading.

-   Creating from a Python class: If users already have a Python class for reading their dataset, they can use MindData's GeneratorDataset interface to call that Python class to create a Dataset, providing users with great flexibility.

![MindSpore
Dataset multiple creation methods](../img/ch07/7.2/dataset.png)

Finally, we use an example of implementing the data processing pipeline described at the beginning of this section using MindData to demonstrate how user-friendly the Dataset-centric data programming abstraction is. We need only about 10 lines of code to accomplish our desired complex data processing. Throughout the entire process, we focus solely on describing the logic, while delegating operator implementation and execution scheduling to the data module, which greatly reduces the user's programming burden.

```python
import mindspore.dataset as ds
import mindspore.dataset.transforms.c_transforms as c_transforms
import mindspore.dataset.transforms.vision.c_transforms as vision
dataset_dir = "path/to/imagefolder_directory"

# create a dataset that reads all files in dataset_dir with 8 threads
dataset = ds.ImageFolderDatasetV2(dataset_dir, num_parallel_workers=8)

#create a list of transformations to be applied to the image data
transforms_list = [vision.Decode(),
                    vision.Resize((256, 256)),
                    vision.RandomRotation((0, 15)),
                    vision.Normalize((100,  115.0, 121.0), (71.0, 68.0, 70.0)),
                    vision.HWC2CHW()]
onehot_op = c_transforms.OneHot(num_classes)

# apply the transform to the dataset through dataset.map()
dataset = dataset.map(input_columns="image", operations=transforms_list)
dataset = dataset.map(input_columns="label", operations=onehot_op)

```

### Custom Operator Support

With the dataset transformation-based programming abstraction and the rich transformation operator support for various data types in machine learning, we can cover the vast majority of user data processing needs. However, since the machine learning field itself is rapidly evolving with new data processing requirements constantly emerging, there may be situations where a data transformation operator that users want to use is not covered by the data module. Therefore, we need to design a well-crafted user-defined operator registration mechanism so that users can conveniently use custom operators when constructing data processing pipelines.

In machine learning scenarios, Python is the primary development programming language for users, so we can assume that user-defined operators are more often Python functions or Python classes. The difficulty of supporting custom operators in the data module is mainly related to how the data module schedules computation. For example, PyTorch's dataloader primarily implements computation scheduling at the Python level, and thanks to Python's flexibility, inserting custom operators into the dataloader's data pipeline is relatively straightforward. In contrast, systems like TensorFlow's tf.data and MindSpore's MindData primarily implement computation scheduling at the C++ level, making it more challenging for the data module to flexibly insert user-defined Python operators into the data flow. Next, we will use MindData's custom operator registration and usage implementation as an example to discuss this topic in detail.

![C-level operators and Python-level operators in MindData](../img/ch07/7.2/operation.png)

:width:`800px`
:label:`mindspore operator example`

Data preprocessing operators in MindData can be divided into C-level operators and Python-level operators. C-level operators provide higher execution performance, while Python-level operators can conveniently leverage rich third-party Python packages for development. To flexibly cover more scenarios, MindData supports users in developing custom operators using Python. If users pursue higher performance, MindData also supports users in compiling their C-level operators and registering them as plugins in MindSpore's data processing pipeline.

For custom data processing operators passed into dataset transformation operators such as map and filter, MindData's Pipeline executes them through the created Python runtime after startup. It should be noted that custom Python operators must ensure that both input and output are of the numpy.ndarray type. During execution, when MindData's Pipeline encounters a user-defined PyFunc operator in a dataset transformation, it passes the input data to the user's PyFunc as numpy.ndarray type. After the custom operator finishes execution, the result is returned to MindData as numpy.ndarray. During this process, the executing dataset transformation operator (such as map, filter, etc.) is responsible for the PyFunc's runtime lifecycle and exception handling. If users pursue higher performance, MindData also supports user-defined C operators. The dataset-plugin repository :cite:`minddata` serves as MindData's operator plugin repository, encompassing operators tailored for specific domains (remote sensing, medical imaging, meteorology, etc.). This repository carries MindData's plugin capability extensions and provides a convenient entry point for users to write new MindData operators. Users can write operators, compile, and install the plugin, and then use the newly developed operators in the map operations of the MindData Pipeline.



![MindSpore custom operator registration](../img/ch07/7.2/dataset-plugin.png)

:width:`800px`
:label:`mindspore_user_defined_operator`