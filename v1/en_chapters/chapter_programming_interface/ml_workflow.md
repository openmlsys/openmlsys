# Machine Learning Workflow

In machine learning systems, the fundamental design objective of
programming models is to offer comprehensive workflow programming
support for developers. A typical machine learning task adheres to the
workflow depicted in Figure :numref:`ch03/workflow`. This workflow involves loading the
training dataset, training, testing, and debugging models. The following
APIs are defined to facilitate customization within the workflow
(assuming that high-level APIs are provided as Python functions):

1.  **Data Processing API:** Users first require a data processing API
    to read datasets from a disk. Subsequently, they need to preprocess
    the data to make it suitable for input into machine learning models.
    Code `ch02/code2.2.1` is an example of how PyTorch can be used
    to load data and create data loaders for both training and testing
    purposes.

**ch02/code2.2.1**
```python
import pickle
from torch.utils.data import Dataset, DataLoader
data_path = '/path/to/data'
dataset = pickle.load(open(data_path, 'rb')) # Example for a pkl file
batch_size = ... # You can make it an argument of the script

class CustomDataset(Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels
        
    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, idx):
        sample = self.data[idx]
        label = self.labels[idx]
        return sample, label

training_dataset = CustomDataset(dataset['training_data'], dataset['training_labels'])
testing_dataset = CustomDataset(dataset['testing_data'], dataset['testing_labels'])

training_dataloader = DataLoader(training_dataset, batch_size=batch_size, shuffle=True)  # Create a training dataloader
testing_dataloader = DataLoader(testing_dataset, batch_size=batch_size, shuffle=False) # Create a testing dataloader
```

2.  **Model Definition API:** Once the data is preprocessed, users need
    a model definition API to define machine learning models. These
    models include model parameters and can perform inference based on
    given data. Code
    `ch02/code2.2.2` is an example of how to create a custom
    model in Pytorch:

**ch02/code2.2.2**
```python
import torch.nn as nn
class CustomModel(nn.Module):
    def __init__(self, input_size, output_size):
        super(CustomModel, self).__init__()
        self.linear = nn.Linear(input_size, output_size)  # A single linear layer

    def forward(self, x):
        return self.linear(x)
```

3.  **Optimizer Definition API:** The outputs of models need to be
    compared with user labels, and their difference is evaluated using a
    loss function. The optimizer definition API enables users to define
    their own loss functions and import or define optimization
    algorithms based on the actual loss. These algorithms calculate
    gradients and update model parameters. Code
    `ch02/code2.2.3` is an example of an optimizer definition
    in Pytorch:

**ch02/code2.2.3**
```python
import torch.optim as optim
import torch.nn
model = CustomModel(...)
# Optimizer definition (Adam, SGD, etc.)
optimizer = optim.Adam(model.parameters(), lr=1e-4, momentum=0.9) 
loss = nn.CrossEntropyLoss() # Loss function definition
```

4.  **Training API:** Given a dataset, model, loss function, and
    optimizer, users require a training API to define a loop that reads
    data from datasets in a mini-batch mode. In this process, gradients
    are computed repeatedly, and model parameters are updated
    accordingly. This iterative update process is known as *training*.
    Code `ch02/code2.2.4` is an example of how to train a model in
    Pytorch:

**ch02/code2.2.4**
```python
device = "cuda:0" if torch.cuda.is_available() else "cpu" # Select your training device
model.to(device) # Move the model to the training device
model.train() # Set the model to train mode
epochs = ... # You can make it an argument of the script
for epoch in range(epochs):
    for batch_idx, (data, target) in enumerate(training_dataloader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad() # zero the parameter gradients
        output = model(data) # Forward pass
        loss_value = loss(output, target) # Compute the loss
        loss_value.backward() # Backpropagation
        optimizer.step()
```

5.  **Testing and Debugging APIs:** Throughout the training process,
    users need a testing API to evaluate the accuracy of the model
    (training concludes when the accuracy exceeds the set goal).
    Additionally, a debugging API is necessary to verify the performance
    and correctness of the model. Code
    `ch02/code2.2.5` is an example of model evaluation in
    Pytorch:

**ch02/code2.2.5**
```python
model.eval() # Set the model to evaluation mode
overall_accuracy = []
for batch_idx, (data, target) in enumerate(testing_dataloader):
    data, target = data.to(device), target.to(device)
    output = model(data) # Forward pass
    accuracy = your_metrics(output, target) # Compute the accuracy
    overall_accuracy.append(accuracy) # Print the accuracy
# For debugging, you can print logs inside the training or evaluation loop, or use python debugger.
```

![Workflow within a machine learningsystem](../img/ch03/workflow.pdf)
:label:`ch03/workflow`
