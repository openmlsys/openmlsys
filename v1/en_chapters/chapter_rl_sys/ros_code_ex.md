# Case Study: Using ROS

In this section, we will guide you through the process of installing ROS
2 and configuring the environment. We will also provide a few code
examples to deepen your understanding of ROS 2 usage and concepts
introduced in the previous section.

Our environment consists of the following: ROS 2 Foxy Fitzroy, the
latest ROS 2 long-term support (LTS) release at the time of writing;
Ubuntu Focal 20.04; and Python 3.8 (our examples use Python 3.8.10)
installed in Ubuntu Focal. Ubuntu Focal is the official software for
installing ROS 2 Foxy Fitzroy. If you install ROS 2 via Debian packages
(recommended), you must use the version of Python 3 on Ubuntu. This is
because many Python dependencies of ROS 2 will be automatically
installed in the Python 3 path on Ubuntu via `apt install` (instead of
via `pip install`). In other words, when you select the ROS 2 version,
the versions of Ubuntu and Python you need are automatically determined.

If you want to use a Python virtual environment, you must also use the
Python interpreter provided by Ubuntu and add the `site-packages` option
during the creation stage because we need the ROS 2 dependencies
installed in the Python 3 path.

For example, a pipenv user can use the following command to create a
virtual environment that uses the installed Python 3 and has
`site-packages`:

```bash
pipenv --python $(/usr/bin/python3 -V | cut -d" " -f2) --site-packages
```

Due to Python 3 being installed, virtual environments created with conda
may experience some compatibility issues. Other versions of ROS 2 are
installed and operate in essentially the same way.

In this section and subsequent cases, we may use ROS 2, Ubuntu, and
Python to refer to ROS 2 Foxy Fitzroy, Ubuntu Focal, and Python 3.8,
respectively.

Cases in this section can be found in the ROS 2 official tutorial, which
is very detailed and ideal for ROS 2 beginners. You can learn more about
ROS 2 there.

**1. Installing ROS 2 Foxy Fitzroy**

Following the official tutorial makes it relatively easy to install ROS
2 on Ubuntu (e.g., installing ROS 2 Foxy Fitzroy and Ubuntu Focal). The
installation procedure of ROS 2 described in this section is primarily
based on this tutorial.

**2. Setting the system to support the UTF-8 locale**

Before installation, ensure that the Ubuntu system locale is set to a
value that supports UTF-8. You can check the current locale settings via
the locale command. If the value of `LANG` ends with `.UTF-8`, the
system already supports the UTF-8 locale. Otherwise, use the following
commands to set it as the UTF-8 value in English (US). You can change
the language code to match your desired language.

```bash
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

**3. Setting the software source**

You also need to add the software source of ROS 2 to the system by
running the following commands:

```bash
sudo apt update && sudo apt install curl gnupg2 lsb-release
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key  -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

**4. Installing ROS 2**

Once the preceding steps are complete, update the software source cache
and then install the ROS 2 Desktop version. This is the preferred
version because it contains the ROS 2 framework and most of the software
libraries commonly used in ROS 2 development, such as rviz.

```bash
sudo apt update
sudo apt install ros-foxy-desktop
```

In addition, install colcon (a build tool for ROS 2) and rosdep (which
can help us quickly install a dependency required by the ROS 2 project).

```bash
sudo apt-get install python3-colcon-common-extensions python3-rosdep
```

Now you have installed ROS 2. However, an additional step is required to
set up the environment before using ROS 2.

**5. Setting the environment**

For any installed version of ROS 2 (and ROS), you need to set up the
required environment by sourcing the corresponding `setup` script before
using the version. For example, for the newly installed ROS 2 Foxy
Fitzroy, you can run the following command in the terminal to set up the
environment required by ROS 2:

```bash
source /opt/ros/foxy/setup.bash
```

If you are using a shell other than `bash`, you may need to change the
file name extension of `setup` to the name of the corresponding shell.
For example, if you are using zsh, you would need to run the command
`source /opt/ros/foxy/setup.zsh`.

To avoid entering preceding command every time you use ROS 2, you can
add this command to your `.bashrc` file (or `.zshrc` and other
corresponding shell files). This way, every new command-line terminal
you build will be automatically set to the environment that ROS 2
requires.

The advantage of following this process to set up the environment is
that you can install multiple versions of ROS 2 (and ROS), and then
source the `setup.bash` file of the corresponding version when you use
it without interference from other versions.

If you are a heavy user of Python, adding `setup.bash` to `.bashrc` may
cause issues. This is because all your virtual environments will
automatically introduce the environment setup of ROS 2, and the Python
libraries in ROS 2 will be added to the paths of your virtual
environments. Although virtual environments may detect ROS 2 libraries,
those libraries will not be used or disrupt the program operation in
your virtual environments.

To avoid such issues, if you plan to develop a ROS 2 project primarily
using Python, you can create a virtual environment for the project and
add `source /opt/ros/foxy/setup.bash` to the `activate` script of the
virtual environment.

Note that you may need to add this `source` command to the very
beginning or close to the end of the script. (If, for example, you are a
pipenv user, you need to add this command before the
`hash -r 2>/dev/null` command instead of putting it at the end.)
Otherwise, the following error may occur when you activate the virtual
environment:

```bash
Shell for UNKNOWN_VIRTUAL_ENVIRONMENT already activated.
No action taken to avoid nested environments.
```

**6. Testing the installation**

After you run the `source` command, you can test whether ROS 2 is
successfully installed and the environment is set up correctly. You can
execute `printenv | grep -i R̂OS` on the command line where the `source`
command is executed. The output should contain the following three
environment variables:

```bash
ROS_VERSION=2
ROS_PYTHON_VERSION=3
ROS_DISTRO=foxy
```

In addition, you can open another two terminal windows that have
executed the `source` command, and then execute
Code `code/ch17/code_terminal_1` on terminal 1 and
Code `code/ch17/code_terminal_2` on terminal 2.

**code/ch17/code_terminal_1**
```
ros2 run demo_nodes_cpp talker
```

**code/ch17/code_terminal_2**
```
ros2 run demo_nodes_py listener
```

If the installation was successful and the `source` command is executed,
`talker` shows that it is broadcasting messages, and `listener` shows
that it has heard the messages.

Congratulations, you have now successfully installed ROS 2 and set up
the environment. The following sections will provide a few examples to
illustrate the core concepts of ROS 2 introduced in the previous
section.

## Node Creation

In this subsection, we will create a ROS 2 project and use Python to
write an example of `Hello World` to show the basic structure of ROS 2
nodes.

**1. Creating a new ROS 2 project**

First, create a folder in an appropriate location. This folder will be
the root directory of the ROS 2 project, that is, the "workspace"
introduced in the previous section. Because this workspace is manually
created, it is an overlay workspace. In contrast, the `source` command
executed earlier will help you prepare the underlay workspace on which
the overlay workplace is based.

Suppose you create a workspace and name it as `openmlsys-ros2`.

```bash
mkdir openmlsys-ros2
cd openmlsys-ros2
```

In this case, you then need to create a Python virtual environment for
the workspace and add the `source` command to the corresponding
`activate` script, as described in the previous subsection about
environment setup.

By default, all commands in the case study subsections are executed in
this newly built virtual environment. Because different tools for
managing virtual environments have different commands, we do not provide
examples of executable commands here.

Next, create a subfolder named `src` in this workspace folder. Within
this subfolder, create different ROS 2 packages. They are independent of
each other, but can call each other's functions to meet the requirements
of the entire ROS 2 project.

After the `src` subfolder is created, call the `colcon build` command,
which is a common build tool for ROS 2. This command attempts to build
the entire ROS 2 project (i.e., all packages in the current workspace).
After this command is executed successfully, three new folders will be
created in the workspace: `build`, `install`, and `log`. `build`
includes the intermediate outputs, `install` contains the final outputs
(i.e., well-built packages) of the build process, and `log` stores the
process logs.

At this point, with this new framework for the ROS 2 project, you are
ready to start coding.

**2. Creating a Python package under the ROS 2 framework**

In the `src` folder, create a ROS 2 package where you will write the
case of `Hello World`.

```bash
cd src
ros2 pkg create --build-type ament_python --dependencies rclpy std_msgs --node-name hello_world_node my_hello_world
```

`pkg create` in the `ros2` command can help you quickly create a
framework for the ROS 2 package. The `build-type` parameter indicates
that this is a pure Python package, and the `dependencies` parameter
indicates that the package will use two dependencies --- `rclpy` and
`std_msgs`. The `node-name` parameter shows that the package created has
a ROS 2 node named `hello_world_node`, and that `my_hello_world` at the
end is the name of the new package.

Go to the new package folder `my_hello_world`. Once the preceding
command is executed, a Python package folder named `my_hello_world` is
created. It is named after the package and contains files of
`__init__.py` and `hello_world_node.py`. The latter exists because you
use the `node_name` parameter. This is the Python package folder in
which you will write your Python code.

There are another two folders: `resource` and `test`. The former helps
ROS 2 locate the Python package, and can be ignored. The latter is used
to accommodate all the test code, and it already contains three test
files.

In addition to these three folders, there are three files:
`package.xml`, `setup.cfg`, and `setup.py`.

`package.xml` is the standard configuration file for the ROS 2 package.
In contains a lot of pre-generated content. However, you still need to
fill in or update the content in `version`, `description`, `maintainer`,
and `license`. You are advised to fill in all content completely each
time you create a ROS 2 package. In addition, `rclpy` and `std_msgs` are
listed as dependencies because you used the `dependencies` parameter. To
add or modify dependencies, you can directly modify the `depend` list in
`package.xml`. In addition to the most commonly used `depend` (for
`build`, `export`, and `execution`), you also have `build_depend`,
`build_export_depend`, `exec_depend`, `test_depend`, `buildtool_depend`,
and `dec_depend`. For details about `package.xml`, see the Wiki page.

Both `setup.cfg` and `setup.py` are files related to the Python package.
However, ROS 2 also uses them to learn how to install the Python package
to the `install` folder and what entry points --- programs that can be
directly called by the ROS 2 command-line commands --- need to be
registered. Notice that the name `hello_world_node` has been set to
`my_hello_world/hello_world_node.py` --- the alias of the `main()`
function in the Python file --- in `console_scripts`, a subitem of
`entry_points` in `setup.py`. You can call this function directly later
using the ROS 2 command-line commands and this new name as follows:

```bash
# ros2 run <package_name> <entry_point>
ros2 run my_hello_world hello_world_node
```

To add a new entry point, you can directly add it here.

In addition to the entry points, you should promptly update the items of
`version`, `maintainer`, `maintainer_email`, `description`, and
`license` in `setup.py`.

**3. First ROS 2 node**

Open the Python file `my_hello_world/hello_world_node.py` and delete its
content in order to write the desired code.

First, introduce the necessary packages:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
```

`rclpy` --- ROS Client Library for Python --- allows you to use various
functions within the ROS 2 framework through Python. The `Node` class is
the base class for all ROS 2 nodes. Your node class also needs to
inherit this base class. `std_msgs` contains some standard message
formats predefined by ROS 2 for intra-framework communication. You need
to use the `String` message format to pass string information.

Next, define your own ROS 2 node:

```python
class HelloWorldNode(Node):
    def __init__(self):
        super().__init__('my_hello_world_node')
        self.msg_publisher = self.create_publisher(String, 'hello_world_topic', 10)
        timer_period = 1.
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.count = 0
    
    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.count}'
        self.msg_publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.count += 1
```

As mentioned earlier, your node class `HelloWorldNode` inherits from the
`Node` base class.

In the `__init__()` method, call the initialization method of the base
class to name your node as `my_hello_world_node`. Next, create an
information publisher that publishes the information of the string type
to the topic `hello_world_topic` and maintains a buffer of size 10.
Then, create a timer that calls the `timer_callback()` method once every
second. Finally, initialize a counter to count the total number of
messages that have been published.

In the `timer_callback()` method, create a simple message of
`Hello World` with a counter and send it through the message publisher.
Then log the operation and increment the count by 1.

After the `Hello World` node class is defined, start defining the
`main()` function, which is the entry point in `setup.py`.

```python
def main(args=None):
    rclpy.init(args=args)
    hello_world_node = HelloWorldNode()
    rclpy.spin(hello_world_node)
    hello_world_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

This `main()` function is relatively simple. First, start the ROS 2
framework with the `rclpy.init()` method. Then, create an instance of
`HelloWorldNode` and add it to the running ROS 2 framework by means of
`rclpy.spin()`. This ensures that the instance participates in the ROS 2
event loop and runs correctly. `rclpy.spin()` is a blocking method that
runs continually until it is blocked (e.g., when the ROS 2 framework
stops running). At this time, your node will be destroyed and the ROS 2
framework closed. If you do not destroy an unused node, the garbage
collector will destroy it.

At this point, you have created your first ROS 2 node.

**4. First build and run**

You are now ready to build the new package. This involves installing the
Python package you have written into a place where ROS 2 can find it
rather than building a Python project.

```bash
# cd <workspace>
cd openmlsys-ros2
colcon build --symlink-install
```

Running this build command will build all Python and C++ packages in the
`src` folder in the workspace and then install them in the `install`
folder. The `–symlink-install` option requires `colcon` to build
`symlink` for the Python package so that installation is not replicated.
In this way, any subsequent changes in `src` will be reflected directly
in `install`, instead of repeatedly executing the build command.

After the build is completed successfully, the package is still not
ready to be used yet. For example, executing
`ros2 run my_hello_world hello_world_node` now will likely result in the
message `Package ’my_hello_world’ not found`.

To use the package, you need to let ROS 2 know where the `install`
folder is. Source the `local_setup.bash` file in the `install` folder as
follows:

```bash
source install/local_setup.bash
```

Unlike earlier when we added `setup.bash` to the `activate` script in
the virtual environment in order to eliminate the need for sourcing the
file separately each time, we cannot do the same with
`install/local_setup.bash`. Doing so would cause a problem.

Specifically, to run the ROS 2 package, you have to source both
`setup.bash` and `install/local_setup.bash` (either through the
`activate` script or manually). However, the condition of building the
pure Python ROS 2 package with C++ dependencies is sourcing only
`setup.bash` but not `local_setup.bash`. Subsequent cases will show such
a condition for a pure Python ROS 2 package that uses the package of
custom message interfaces (your own C++ package).

After successfully sourcing `install/local_setup.bash`, you can call the
written node.

From now on, unless otherwise specified, `setup.bash` and
`install/local_setup.bash` in any newly created window are sourced and
the `colcon build` command is executed in a terminal window where only
`setup.bash` is sourced and `install/local_setup.bash` is ignored.

```bash
ros2 run my_hello_world hello_world_node
```

Information similar to the following will be displayed:

```bash
[INFO] [1653270247.805815900] [my_hello_world_node]: Publishing: "Hello World: 0"
[INFO] [1653270248.798165800] [my_hello_world_node]: Publishing: "Hello World: 1"
```

You can also open a terminal window and execute
`ros2 topic echo /hello_world_topic`. Information similar to the
following will be displayed:

```bash
data: 'Hello World: 23'
---
data: 'Hello World: 24'
---
```

This means that your information is published to the target topic. The
command `ros2 topic echo <topic_name>` outputs the information received
by the topic with the specified name.

Congratulations, you have now successfully run your first ROS 2 node.

**5. A message subscriber node**

After a message is published, a message subscriber is also needed to
consume the published information.

Create a file named `message_subscriber.py` in the folder where
`hello_world_node.py` is located, as shown in
Code `ch17/messageSubscriber`:

**ch17/messageSubscriber**
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MessageSubscriber(Node):
    def __init__(self):
        super().__init__('my_hello_world_subscriber')
        self.msg_subscriber = self.create_subscription(
            String, 'hello_world_topic', self.subscriber_callback, 10
        )
    
    def subscriber_callback(self, msg):
        self.get_logger().info(f'Received "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    message_subscriber = MessageSubscriber()
    rclpy.spin(message_subscriber)
    message_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
```

This newly created file and its message subscriber node class are
similar to the file and its `HelloWorld` node class mentioned earlier.
During initialization, you need to use the base class initialization
method to assign the name `my_hello_world_subscriber` to the node, and
then create a message subscriber to subscribe to messages under the
topic `hello_world_topic`. You also need to specify the
`subscriber_callback()` method to process the received messages. In
`subscriber_callback()`, log the received messages. The `main()` method
for this node class is similar to that for the `HelloWorld` node class.

Before using this new node, add it as an entry point by adding the
following line in the appropriate location of `setup.py`:

```python
'message_subscriber = my_hello_world.message_subscriber:main'
```

If you run `ros2 run my_hello_world message_subscriber` in the terminal
window now, you will get an error message similar to "No executable
found". That is because ROS 2 can be aware of the newly added entry
point only after rebuilding the entire ROS 2 project.

Execute `colcon build –symlink-install` again in the workspace
directory. After the build is completed successfully, open two terminal
windows and make sure that the two setup files are sourced. Then call
them separately with the `ros2` commands:

```bash
# in terminal 1
ros2 run my_hello_world hello_world_node
# in terminal 2
ros2 run my_hello_world message_subscriber
```

After the commands are run, the "Hello World: N" message is published
continuously in terminal window 1, and the "Hello World: N" message is
received continuously in terminal window 2.

Congratulations, you have now successfully created a pair of ROS 2
nodes, one for sending messages and the other for subscribing to and
receiving messages.

## Parameter Reading

Nodes in a real-world project are far more complex than the simple
example provided earlier because, for example, they are parameterized.
This subsection will show you how to get a node to read a parameter.

Create a new file named `parametrised_hello_world_node.py` in the folder
where `hello_world_node.py` is located, as shown in
Code `code/ch17/parametrisedHelloWorldNode`:

**code/ch17/parametrisedHelloWorldNode**
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class ParametrisedHelloWorldNode(Node):
    def __init__(self):
        super().__init__('parametrised_hello_world_node')
        self.msg_publisher = self.create_publisher(String, 'hello_world_topic', 10)
        timer_period = 1.
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.count = 0
        self.declare_parameter('name', 'world')
    
    def timer_callback(self):
        name = self.get_parameter('name').get_parameter_value().string_value
        msg = String()
        msg.data = f'Hello {name}: {self.count}'
        self.msg_publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    hello_world_node = ParametrisedHelloWorldNode()
    rclpy.spin(hello_world_node)
    hello_world_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

This new parameterized `HelloWorldNode` class is similar to the previous
`HelloWorld` node class except for the following two differences:\
(1) The new class additionally uses the `self.declare_parameter()`
method in the initialization methods to declare the new node instance to
the ROS 2 framework. The new node instance has a parameter named `name`,
and the initial value of this parameter is `world`.\
(2) The new class attempts to obtain the actual value of the `name`
parameter in the callback function `timer_callback()` and uses that
value to form the content of the message to be sent.

First, register the `main()` method of the new file as a new entry
point. Similarly, add the following line to the corresponding position
in `setup.py`. Also, execute `colcon build –symlink-install` in the
workspace root directory to rebuild the project.

```bash
'parametrised_hello_world_node = my_hello_world.parametrised_hello_world_node:main'
```

After the build is successfully completed, if you execute
`ros2 run my_hello_world parametrised_hello_world_node` in the terminal,
you will see that this parameterized `HelloWorld` node runs normally and
continuously publishes messages like "Hello World: N". In this case, the
node uses the initial value `world`.

After you execute `ros2 param list` in a new terminal, you will see the
following information:

```bash
/parametrised_hello_world_node:
  name
  use_sim_time
```

This indicates that the node `parametrised_hello_world_node` does
declare and use a `name` parameter. Another parameter named
`use_sim_time` is a default parameter given by ROS 2 to indicate whether
the node uses the simulated time inside the ROS 2 framework rather than
the system time of the computer.

To assign the value `ROS2` to the `name` parameter, run the following
command in the terminal:

```bash
ros2 param set /parametrised_hello_world_node name "ROS2"
```

If the assignment is successful, the command returns "Set parameter
successful", and the terminal window where the parameterized
`HelloWorld` node is running continuously changes the messages it
publishes to "Hello ROS2: N".

Congratulations, you now know how to make ROS 2 nodes (and other types
of ROS 2 programs) use parameters.

## Server-Client Service Mode

As mentioned in the previous section, the ROS 2 framework has both a
publisher-subscriber communication mode and a server-client
communication mode. In this subsection, we will use a simple service
that concatenates two strings to demonstrate how the server-client mode
works.

**1. Custom service interfaces**

Before coding for the server and client, you need to define the
communication interfaces between them.

There are three types of interfaces in the ROS 2 framework.

The message/msg interface for nodes in publisher-subscriber mode: It is
used for unidirectional message delivery and only defines the format of
such messages. The service/srv interface for service nodes in
server-client mode: It is used for bidirectional message delivery and
defines the format of the requests sent from the client to the server
and the format of the responses sent from the server to the client. The
action interface for action nodes in action mode: It is used for
bidirectional message delivery and intermediate progress feedback. It
defines the format of the requests sent by the action initiating node to
the action node, the format of the results sent by the action node to
the action initiating node, and the format of the intermediate progress
feedback sent by the action node to the action initiating node. The
`std_msgs.msg.String` message interface in the predefined package
`std_msgs` is used for the `HelloWorld` nodes defined earlier. Because
the message interface is only responsible for defining the format of
unidirectional messages, predefined interface types are readily
available. For services and actions, however, you need to define an
interface type because the interfaces are responsible for defining the
format of bidirectional communications. Next, let's define the service
type interface for the string concatenation service.

First, create a new package in the `src` folder of the workspace, which
is dedicated to maintaining custom message, service, and action
interfaces.

```bash
cd openmlsys-ros2/src
ros2 pkg create --build-type ament_cmake my_interfaces
```

This is a new C++ package, not a Python one, because custom interface
types of ROS 2 can only support C++ packages. Once you have created the
package, update the related items in `package.xml`.

To facilitate maintenance, custom interfaces are generally placed in the
corresponding subfolders. As such, you can create three subfolders in
the new folder `src/my_interfaces`: `msg`, `srv`, and `action`.

```bash
cd my_interfaces
mkdir msg srv action
```

Next, create the service interfaces you want to define in the `srv`
subfolder.

```bash
cd srv
touch ConcatTwoStr.srv
```

After that, add the following contents to `ConcatTwoStr.srv`:

```bash
string str1
string str2
---
string ret
```

The contents above - - - are the format of the requests sent by the
client to the server, and those below are the format of the responses
sent by the server to the client.

Once the interfaces are defined, you also need to modify
`CMakeLists.txt`. Open `my_interfaces/CMakeLists.txt` and add the
following code before the line `if(BUILD_TESTING)`:

```bash
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/ConcatTwoStr.srv"
)
```

The code above instructs the build tool to find the required
`rosidl_default_generators` package and to build the custom interfaces
you specified.

After updating `CMakeLists.txt`, you also need to add
`rosidl_default_generators` to `package.xml` as a dependency of the
custom interface package. Open the `package.xml` file and add the
following code before the line
`<test_depend>ament_lint_auto</test_depend>`:

```bash
<build_depend>rosidl_default_generators</build_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

After `package.xml` is updated, you can build the custom interface
package.

```bash
cd openmlsys-ros2
colcon build --packages-select my_interfaces
```

Because the package `my_hello_world` has no changes, only the package
`my_interfaces` is selected using the option `–packages-select`. Also,
the option `–symlink-install` is not used because the custom interface
package is a C++ package that must be rebuilt after each change.

When running this build command, error messages such as
`ModuleNotFoundError: No module named ’XXX’` (XXX can be `em`,
`catkin_pkg`, `lark`, `numpy`, or other Python packages) may be
displayed. Most of these errors occur because the Python virtual
environment does not point to Python 3 of the Ubuntu system or include
`site-packages`. In this case, deleting the current virtual environment
and recreate a new one as described at the beginning of this section may
resolve the problem.

To verify whether the build is completed successfully, run
`ros2 interface show my_interfaces/srv/ConcatTwoStr` in a new terminal
window. The terminal will display the definition of the custom service
interface `ConcatTwoStr` if the build succeeded.

Now that you have defined the required service interfaces, you are ready
to code the server and the client.

**2. ROS 2 server**

Create a file named `concat_two_str_service.py` in the folder where
`hello_world_node.py` is located, as shown in
Code `ch17/concatTwoStrService`:

**ch17/concatTwoStrService**
```python
from my_interfaces.srv import ConcatTwoStr
import rclpy
from rclpy.node import Node

class ConcatTwoStrService(Node):
    def __init__(self):
        super().__init__('concat_two_str_service')
        self.srv = self.create_service(ConcatTwoStr, 'concat_two_str', self.concat_two_str_callback)

    def concat_two_str_callback(self, request, response):
        response.ret = request.str1 + request.str2
        self.get_logger().info(f'Incoming request\nstr1: {request.str1}\nstr2: {request.str2}')

        return response

def main(args=None):
    rclpy.init(args=args)
    concat_two_str_service = ConcatTwoStrService()
    rclpy.spin(concat_two_str_service)
    concat_two_str_service.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

The process of building a service is similar to that of building a
general node, with both the service and node being inherited from the
same base class `rclpy.node.Node`. In this file, first introduce the
custom service interface `ConcatTwoStr` from the built package
`my_interfaces`. Use `self.create_service()` to create a server object,
and specify the service interface type as `ConcatTwoStr`, the service
name as `concat_two_str`, and the callback function for processing
service requests as `self.concat_two_str_callback`. In the callback
function `self.concat_two_str_callback()`, compute `str1` and `str2`
obtained by the request object, assign the result to `ret` of the
response object, and record logs. Note that the structure of the request
and response objects conforms to the definition in `ConcatTwoStr.srv`.

In addition, add the `main()` method of this file as an entry point to
`setup.py`.

```python
'concat_two_str_service = my_hello_world.concat_two_str_service:main'
```

## Client

Create a file named `concat_two_str_client_async.py` in the folder where
`hello_world_node.py` is located, as shown in
Code `ch17/concatTwoStrClientAsync`:

**ch17/concatTwoStrClientAsync**
```python
import sys

from my_interfaces.srv import ConcatTwoStr
import rclpy
from rclpy.node import Node

class ConcatTwoStrClientAsync(Node):
    def __init__(self):
        super().__init__('concat_two_str_client_async')
        self.cli = self.create_client(ConcatTwoStr, 'concat_two_str')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = ConcatTwoStr.Request()

    def send_request(self):
        self.req.str1 = sys.argv[1]
        self.req.str2 = sys.argv[2]
        self.future = self.cli.call_async(self.req)

def main(args=None):
    rclpy.init(args=args)

    concat_two_str_client_async = ConcatTwoStrClientAsync()
    concat_two_str_client_async.send_request()

    while rclpy.ok():
        rclpy.spin_once(concat_two_str_client_async)
        if concat_two_str_client_async.future.done():
            try:
                response = concat_two_str_client_async.future.result()
            except Exception as e:
                concat_two_str_client_async.get_logger().info(
                    'Service call failed %r' % (e,))
            else:
                concat_two_str_client_async.get_logger().info(
                    'Result of concat_two_str: (%s, %s) -> %s' %
                    (concat_two_str_client_async.req.str1, concat_two_str_client_async.req.str2, response.ret))
            break

    concat_two_str_client_async.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Coding the client is slightly more complex than coding the server. In
the initialization method for the client node, first create a client
object, and specify the service interface type as `ConcatTwoSt` and the
service name as `concat_two_str`. Then, through a `while` loop, the
client will wait for the corresponding server to go online before
proceeding to the next step. This technique of using a loop for waiting
is used by many clients. When the server goes online, the initialization
method creates a template of the service request object and temporarily
stores the template in the `req` attribute of the client node. In
addition to the initialization method, the client node also defines
another method --- `send_request()` --- to read the first two parameters
of the command line when the program is started, store those parameters
in the service request object, and then send the object to the server
asynchronously.

In the `main()` method, first create a client and send a service
request, and then use a `while` loop to wait for the server to return
the result and log the result. `rclpy.ok()` is used to check whether ROS
2 is running properly so that that the client does not get trapped in an
infinite loop if ROS 2 stops running before the service ends.
`rclpy.spin_once()` differs from `rclpy.spin()` in that the former
executes an event loop only once whereas the latter executes an event
loop until ROS 2 stops. As such, using `rclpy.spin_once()` here is more
suitable because you already have a `while` loop. Note that the object
`concat_two_str_client.future` provides a number of methods to help
determine the current state of the service request.

You also need to add the `main()` method of this file as an entry point
to `setup.py`.

```python
'concat_two_str_client_async = my_hello_world.concat_two_str_client_async:main'
```

Now that the server and client are prepared, you can rebuild the package
`my_hello_world` in the workspace root directory.

```bash
cd openmlsys-ros2
colcon build --packages-select my_hello_world --symlink-install
```

Then, run the following commands in the respective terminal windows:

```bash
# in terminal 1
ros2 run my_hello_world concat_two_str_client_async Hello World
# in terminal 2
ros2 run my_hello_world concat_two_str_service
```

Information similar to the following will be shown if all goes well:

```bash
# in terminal 1
[INFO] [1653525569.843701600] [concat_two_str_client_async]: Result of concat_two_str: (Hello, World) -> HelloWorld
# in terminal 2
[INFO] [1653516701.306543500] [concat_two_str_service]: Incoming request
str1: Hello
str2: World
```

Congratulations, you have now created the custom interface type, server
node, and client node in the ROS 2 framework.

## Action Mode

The previous subsection describes the server-client mode within the ROS
2 framework. This subsection introduces the action mode by summing each
element of a number sequence one by one.

**1. Custom action interfaces**

Before coding the action-related node, you need to define the action
information interface.

You can use the package `my_interfaces` built earlier, create a new file
`MySum.action` in `my_interfaces/action`, and add the following
contents:

```bash
# Request
int32[] list
---
# Result
int32 sum
---
# Feedback
int32 sum_so_far
```

The action information interface is simple: The request of the action
has only one item, `list` of an integer sequence. The result of the
action has only one integer, item `sum`. And the intermediate feedback
has only one integer, item `sum_so_far`, to calculate the accumulated
sum to the current position.

Next, add this information interface to `CMakeLists.txt`. Specifically,
add `action/MySum.action` after `srv/ConcatTwoStr.srv` in the method
`rosidl_generate_interfaces()`.

Finally, build the changed package by running
`colcon build –packages-select my_interface` in the workspace root
directory.

**2. ROS 2 action server**

Create a file named `my_sum_action_server.py` in the folder where
`hello_world_node.py` is located, as shown in
Code `ch17/mySumActionServer`:

**ch17/mySumActionServer**
```python
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from my_interfaces.action import MySum

class MySumActionServer(Node):

    def __init__(self):
        super().__init__('my_sum_action_server')
        self._action_server = ActionServer(
            self, MySum, 'my_sum', self.execute_callback
        )

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        feedback_msg = MySum.Feedback()
        feedback_msg.sum_so_far = 0
        for elm in goal_handle.request.list:
            feedback_msg.sum_so_far += elm
            self.get_logger().info(f'Feedback: {feedback_msg.sum_so_far}')
            goal_handle.publish_feedback(feedback_msg)
        goal_handle.succeed()
        result = MySum.Result()
        result.sum = feedback_msg.sum_so_far
        return result

def main(args=None):
    rclpy.init(args=args)
    my_sum_action_server = MySumActionServer()
    rclpy.spin(my_sum_action_server)

if __name__ == '__main__':
    main()
```

Similarly, create an action server object in its initialization method
for this action server node class. Specify the defined `MySum` as the
information interface type, `my_sum` as the action name, and the
`self.execute_callback` method as the callback function for action
execution.

Next, define the action when a new target is received in the
`self.execute_callback()` method. Here, you can treat a target as the
`request` part of the defined `MySum` information interface. This is
because the target here is the structure that contains the information
related to the purpose of the action request, that is, the part defined
by the `request` part.

When you receive a target, first create a feedback message object
`feedback_msg` from `MySum` and use the `sum_so_far` item as an
accumulator. Then traverse the data in the `list` item in the target
request and accumulate the data item by item. Each time an item is
accumulated, a feedback message is sent via the
`goal_handle.publish_feedback()` method. Finally, when the computation
is complete, use `goal_handle.succeed()` to indicate that the action has
been successfully performed. In addition, create a new result object
through `MySum`, fill in the result value, and return it.

In the `main()` function, create an instance of the action server node
class and call `rclpy.spin()` to add the instance to the event loop.

Finally, add `main()` as an entry point by adding the following line in
the appropriate position in `setup.py`:

```bash
'my_sum_action_server = my_hello_world.my_sum_action_server:main'
```

## Action Client

Create a file named `my_sum_action_client.py` in the folder where
`hello_world_node.py` is located, as shown in
Code `ch17/mySumActionClient`:

**ch17/mySumActionClient**
```python
import sys
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from my_interfaces.action import MySum

class MySumActionClient(Node):
    def __init__(self):
        super().__init__('my_sum_action_client')
        self._action_client = ActionClient(self, MySum, 'my_sum')

    def send_goal(self, list):
        goal_msg = MySum.Goal()
        goal_msg.list = list

        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)
    
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected...')
            return
        
        self.get_logger().info('Goal accepted.')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)
    
    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sum}')
        rclpy.shutdown()
    
    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Received feedback: {feedback.sum_so_far}')

def main(args=None):
    rclpy.init(args=args)
    action_client = MySumActionClient()
    action_client.send_goal([int(elm) for elm in sys.argv[1:]])
    rclpy.spin(action_client)

if __name__ == '__main__':
    main()
```

This action client node class is slightly more complex than the server
node class introduced earlier, because you need to send requests,
receive feedback, and process results.

First, create an action client object in the initialization method of
the action client node class and specify `MySum` as the message
interface type and `my_sum` as the action name.

Then, declare the `self.send_goal()` method to generate and send a
target/request. Specifically, create a target object from `MySum` and
assign the received `list` parameter to the `list` attribute of the
target object. After the action server is ready, send the target
asynchronously and specify `self.feedback_callback` as the feedback
callback function. Finally, set `self.goal_response_callback` as the
callback function for the asynchronous operation that sends the target
information.

In `self.goal_response_callback()`, check whether the target request is
accepted and log the result. If the target request is accepted, obtain
the `future` object of the asynchronous operation through
`goal_handle.get_result_async()`, and set `self.get_result_callback` as
the callback function of the final result through the `future` object.

In the callback function `self.get_result_callback()` of the final
result, obtain the accumulation result and log it. Finally, call
`rclpy.shutdown()` to end the current node.

In the feedback message callback function `self.feedback_callback()`,
obtain the feedback message and log it. Because the callback function
for the feedback message may be executed multiple times, you are advised
to keep it as lightweight as possible by simplifying the process logic.

Finally, in the `main()` method, create an instance of the action client
node class that converts the parameters of the command line into the
target number sequence that needs to be summed. Call the `send_goal()`
method of the action client node class instance and transfer the target
sum number sequence to initiate the sum request.

Similarly, add `main()` as an entry point by adding the following line
in the appropriate position in `setup.py`:

```bash
'my_sum_action_client = my_hello_world.my_sum_action_client:main'
```

Now that the action server and action client are ready, you can rebuild
the package `my_hello_world` in the workspace root directory.

```bash
cd openmlsys-ros2
colcon build --packages-select my_hello_world --symlink-install
```

Then, run the following commands in the respective terminal windows:

```bash
# in terminal 1
ros2 run my_hello_world my_sum_action_client 1 2 3
# in terminal 2
ros2 run my_hello_world my_sum_action_server
```

Information similar to the following will be shown if all goes well:

```bash
# in terminal 1
[INFO] [1653561740.000499500] [my_sum_action_client]: Goal accepted.
[INFO] [1653561740.001171900] [my_sum_action_client]: Received feedback: 1
[INFO] [1653561740.001644000] [my_sum_action_client]: Received feedback: 3
[INFO] [1653561740.002327500] [my_sum_action_client]: Received feedback: 6
[INFO] [1653561740.002761600] [my_sum_action_client]: Result: 6
# in terminal 2
[INFO] [1653561739.988907200] [my_sum_action_server]: Executing goal...
[INFO] [1653561739.989213900] [my_sum_action_server]: Feedback: 1
[INFO] [1653561739.989549000] [my_sum_action_server]: Feedback: 3
[INFO] [1653561739.989855400] [my_sum_action_server]: Feedback: 6
```

Congratulations, you have now created the custom interface type, action
server node, and action client node in the ROS 2 framework!
