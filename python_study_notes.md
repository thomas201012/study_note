# python语法学习笔记
## 学习目标
+ 熟悉并理解python的五种变量类型
+ 学会使用python常用语句
+ 理解try...except..的语法使用
+ asyncio的理解和使用
+ python代码启动和运行顺序和逻辑
+ 什么是类的单例设计？例子
---
## 变量类型
### Numbers（数字）
    在python3.x版本后支持3种不同的数据类型
        - int（整形）
        - float（浮点型）
        - complex（复数）
### tring（字符串）
    python的字串列表有2种取值顺序:
        - 从左到右索引默认0开始的，最大范围是字符串长度少1
        - 从右到左索引默认-1开始的，最大范围是字符串开头

    python中没有单字符类型，单字符也包含在字符串内
### List（列表）
    列表可以完成大多数集合类的数据结构实现。它支持字符，数字，字符串甚至可以包含列表（即嵌套）。

    列表用 [ ] 标识，是 python 最通用的复合数据类型。
### Tuple（元组）
    元组用 () 标识。内部元素用逗号隔开。但是元组不能二次赋值，相当于只读列表。
### Dictionary（字典）：
    字典(dictionary)是除列表以外python之中最灵活的内置数据结构类型。列表是有序的对象集合，字典是无序的对象集合。

    两者之间的区别在于：字典当中的元素是通过键来存取的，而不是通过偏移存取。

    字典用"{ }"标识。字典由索引(key)和它对应的值value组成
### 总结
    在Python中，对象可以分为可变对象和不可变对象。
    其中列表和字典为可变对象，数字、字符串、元组为不可变对象。
    在可变对象中，重新赋值可以直接改变对象指向的地址中的值。
    而不可变对象中，对于一些可重新赋值的对象，重新赋值是将之前对象指向的地址直接删除，重新指向新赋值的地址。
---
## 类
+ 在Python中，类是一种面向对象编程的核心概念。类是对象的蓝图，它定义了对象的属性（变量）和方法（函数）。通过类，我们可以创建多个相似的对象，并使用它们的属性和方法。
+ 下面是一个简单的示例，展示了如何定义和使用一个类：
```
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say_hello(self):
        print(f"Hello, my name is {self.name} and I'm {self.age} years old.")

# 创建对象
person1 = Person("Alice", 25)
person2 = Person("Bob", 30)

# 访问对象的属性
print(person1.name)  # 输出: Alice
print(person2.age)   # 输出: 30

# 调用对象的方法
person1.say_hello()  # 输出: Hello, my name is Alice and I'm 25 years old.
person2.say_hello()  # 输出: Hello, my name is Bob and I'm 30 years old.
```
+ 在上面的例子中，我们定义了一个名为 Person 的类。它有两个属性：name 和 age，以及一个方法 say_hello()。通过 __init__() 方法，我们可以在创建对象时为属性赋值。say_hello() 方法用于打印出对象的属性。

+ 通过使用 Person 类，我们创建了两个不同的对象 person1 和 person2。我们可以通过点操作符来访问对象的属性，例如 person1.name 和 person2.age。同样，我们可以通过调用对象的方法来执行特定的操作，例如 person1.say_hello() 和 person2.say_hello()。

+ 类是面向对象编程的基础，它提供了一种组织和封装代码的方式，使得代码更具可读性、可维护性和可扩展性。通过定义类和创建对象，我们可以利用面向对象的思想来构建复杂的程序和系统。
## 常用语句
### if
+ Python 编程中 if 语句用于控制程序的执行，下面是一个简单的if语句的例子：
```
# 定义一个变量
x = 10

# 使用 if 语句进行条件判断
if x > 0:
    print("x 是一个正数")
```   
+ 除了基本的if语句，还可以使用else和elif（即else if）来处理多个条件。下面是一个包含else和elif的例子：
```
# 定义一个变量
x = 0

# 使用 if-else 语句进行条件判断
if x > 0:
    print("x 是一个正数")
elif x < 0:
    print("x 是一个负数")
else:
    print("x 是零")
``` 
+ if语句可以根据条件的真假执行不同的代码块，这使得我们能够根据不同的情况采取不同的行动。根据具体的需求，可以使用多个条件和嵌套的if语句来实现更复杂的逻辑。 
### for
+ 在Python中，for循环是一种常用的循环结构，用于迭代遍历一个可迭代对象（如列表、元组、字符串等）中的元素。下面是一些for循环的例子：

1.遍历列表：
```
fruits = ["apple", "banana", "orange"]

for fruit in fruits:
    print(fruit)
``` 
2.遍历字符串：
```
message = "Hello, World!"

for char in message:
    print(char)
``` 
3.使用range()函数进行迭代：
```
for i in range(1, 5):
    print(i)
``` 
4.嵌套循环：
```
for i in range(1, 4):
    for j in range(1, 4):
        print(i, j)
``` 
+ for循环是一种非常有用的控制结构，可以用于处理可迭代对象中的元素。通过for循环，我们可以重复执行特定的代码块，以便对每个元素执行相同的操作或逻辑。
### while
+ 在Python中，while循环是一种常用的循环结构，用于在满足特定条件的情况下重复执行一段代码块。下面是一些while循环的例子：

1.基本的while循环：
```
count = 0

while count < 5:
    print(count)
    count += 1
``` 
2.使用while循环进行用户输入验证：
```
password = ""

while password != "secret":
    password = input("请输入密码：")

print("密码正确！")
``` 
3.使用while循环实现猜数字游戏：
```
import random

number = random.randint(1, 10)
guess = 0

while guess != number:
    guess = int(input("猜一个1到10之间的数字："))

    if guess < number:
        print("太小了！")
    elif guess > number:
        print("太大了！")
    else:
        print("猜对了！")
``` 
+ while循环提供了一种在满足特定条件时重复执行代码块的方法。通过判断条件的真假，可以控制循环的执行和退出。使用while循环，我们可以实现各种复杂的逻辑和交互。但需要注意的是，要确保循环条件最终会变为假，否则可能导致无限循环。
---
## 异常处理
+ try...except是Python中用于异常处理的语法结构。它允许我们编写代码来捕获和处理可能发生的异常，以便在程序出现错误时进行适当的处理，而不会导致程序崩溃。下面是try...except的语法使用：
```
try:
    # 可能会引发异常的代码块
    # ...
except ExceptionType1:
    # 处理 ExceptionType1 类型的异常
    # ...
except ExceptionType2:
    # 处理 ExceptionType2 类型的异常
    # ...
except:
    # 处理其他异常
    # ...
else:
    # 如果没有发生异常，执行的代码块
    # ...
finally:
    # 无论是否发生异常，都会执行的代码块
    # ...
```
+ try块中的代码是我们希望监视的可能引发异常的代码块。如果在try块中的代码执行过程中引发了异常，那么程序会立即跳转到与异常类型匹配的except块，并执行相应的代码块。如果没有匹配的except块，那么异常会被传递到上一级的调用栈中，直到找到匹配的except块或导致程序终止。

+ 在except块中，我们可以指定要处理的特定异常类型。如果引发的异常与except块中指定的异常类型匹配，那么该except块中的代码将被执行。如果我们省略了异常类型，即使用except而不指定具体的异常类型，那么该except块将捕获所有类型的异常。

+ 除了except块，还可以使用else块和finally块。else块中的代码会在try块中的代码执行完毕且没有引发异常时执行。finally块中的代码无论是否发生异常都会执行，它通常用于释放资源或进行清理操作。

+ 下面是一个具体的例子，演示了try...except的使用：
```
try:
    num1 = int(input("请输入一个整数："))
    num2 = int(input("请输入另一个整数："))
    result = num1 / num2
    print("结果是：", result)
except ValueError:
    print("输入的不是整数！")
except ZeroDivisionError:
    print("除数不能为零！")
except:
    print("发生了其他类型的异常！")
else:
    print("没有发生异常！")
finally:
    print("程序执行完毕！")
```
+ 在上述代码中，我们尝试从用户输入中获取两个整数，并计算它们的商。如果用户输入的不是整数，会引发ValueError异常；如果除数为零，会引发ZeroDivisionError异常；如果发生其他类型的异常，都会被捕获到最后一个except块中。如果没有发生异常，将执行else块中的代码。无论是否发生异常，最后都会执行finally块中的代码。

+ try...except提供了一种结构化的方式来处理可能发生的异常，使我们能够优雅地处理错误情况，保证程序的稳定性和可靠性。在python中代码的异常编译器并不会直接报错，而是在运行过程中才会进行代码的检查，使用try...except可以避免一段程序中的错误影响到另一段程序。
---
## asyncio的理解和使用
+ asyncio是Python中用于异步编程的库，它提供了一种基于事件循环的方式来处理并发任务。通过使用asyncio，你可以编写异步代码，以便在执行IO密集型操作（如网络请求、文件读写等）时能够更高效地利用系统资源。
+ 以下是对asyncio的理解和使用的一般步骤：

    - 引入asyncio模块：
    - 在代码的开头，使用import asyncio语句引入asyncio模块。

    - 定义协程函数：
在asyncio中，异步任务通常以协程（coroutine）的形式表示。协程函数使用async def关键字定义，并在其中编写异步操作的逻辑。协程函数可以包含await关键字，用于等待其他协程或异步操作的完成。

    - 创建事件循环：
事件循环（event loop）是asyncio的核心概念，它负责调度和执行协程函数。使用asyncio.get_event_loop()函数来获取默认的事件循环对象，或者使用asyncio.new_event_loop()函数创建一个新的事件循环对象。

    - 调度协程任务：
使用事件循环的run_until_complete()方法来调度和执行协程任务。你可以将需要执行的协程函数作为参数传递给该方法，以启动异步任务的执行。

    - 异步操作的处理：
在协程函数中，可以使用await关键字来等待异步操作的完成。例如，通过调用asyncio.sleep()函数可以模拟一个异步的延迟操作，让协程暂停一段时间。

    - 并发任务的管理：
asyncio提供了一些工具来管理并发任务的执行，例如asyncio.gather()函数可以并发运行多个协程任务，并等待它们全部完成。

    - 运行事件循环：
使用事件循环的run_forever()方法来启动事件循环的持续执行，直到手动停止或遇到异常。

+ 这只是asyncio的基本使用方法，实际上，asyncio还提供了更多的功能和工具，如异步IO、定时器、信号处理等。你可以根据具体的需求和场景，深入学习和探索asyncio的更多特性和用法。
+ 常用API：

		asyncio.run(coroutine, *, debug=False): 运行一个异步函数或协程，并管理事件循环的生命周期。这是启动异步程序的推荐方式。

		asyncio.create_task(coroutine): 创建一个任务（Task）来运行指定的协程。

		asyncio.sleep(delay, result=None, *, loop=None): 暂停当前协程的执行，让出事件循环给其他任务执行。delay 参数指定暂停的时间（以秒为单位）。

		asyncio.wait(tasks, *, loop=None, timeout=None, return_when=ALL_COMPLETED): 等待一组任务完成。tasks 参数是一个任务（Task）对象的集合，return_when 参数指定等待的条件。

		asyncio.gather(*coroutines_or_futures, loop=None, return_exceptions=False): 并行运行多个协程或未来对象，并等待它们全部完成。返回一个包含所有结果的列表。

		asyncio.open_connection(host=None, port=None, *, loop=None, limit=None, ssl=None, family=0, proto=0, flags=0, sock=None, local_addr=None, server_hostname=None, ssl_handshake_timeout=None, happy_eyeballs_delay=None): 打开一个网络连接并返回读写流（StreamReader 和 StreamWriter）。

		asyncio.start_server(client_connected_cb, host=None, port=None, *, loop=None, limit=None, family=socket.AF_UNSPEC, flags=socket.AI_PASSIVE, sock=None, backlog=100, ssl=None, reuse_address=None, reuse_port=None, ssl_handshake_timeout=None, start_serving=True): 创建一个异步服务器，监听指定的主机和端口，并在有新连接时调用 client_connected_cb 回调函数。

		asyncio.run_coroutine_threadsafe(coroutine, loop): 在指定的事件循环中安排一个协程的执行，并返回一个 concurrent.futures.Future 对象。
+ asyncio.run（）就相当于单片机中的死循环，通过asyncio.create_task（）向死循环中添加运行函数。通过await关键字完成程序的阻塞跳转。
+ 在micropython中，asyncio.create_task（）可以先进行任务的添加，之后在进行asyncio.run（）事件的开启，再开启事件后，事件内的任务才会开始运行。
---
## python代码启动和运行顺序和逻辑
###  __ init __.py的理解
+ __ init __.py文件是一个特殊的文件，用于标识一个目录是一个Python包（package）。它可以是一个空文件，也可以包含一些初始化代码。
+ __ init __.py文件只会在第一次导入包或模块时被执行。之后的导入操作会直接使用已加载的模块，不再执行__init__.py文件。
+ __ init __.py文件的执行可以用来进行一些初始化操作，例如设置包的环境、导入必要的模块或定义包的接口。它也可以为空文件，仅用于标识一个目录是一个Python包。
### python代码的运行逻辑
+ 代码的启动和运行顺序可以分为以下几个步骤：

    - 1.解释器加载模块和库：
当你运行一个Python脚本时，解释器会首先加载所需的模块和库。这包括标准库、第三方库和自定义模块。解释器会按照指定的搜索路径查找并加载这些模块。在加载这些库时，会运行当前库下的__init__.py文件。

    - 2.顶层代码执行：
在Python脚本中，顶层代码是不包含在任何函数或类中的代码。解释器会按照从上到下的顺序执行顶层代码。这些代码可以包括变量的定义、函数的定义、类的定义以及其他可执行的语句。

    - 3.函数和类的定义：
在顶层代码执行过程中，如果遇到函数或类的定义，解释器会将它们存储在内存中，以便后续调用和实例化。

    - 4.主程序的执行：
在顶层代码执行完毕后，解释器会查找并执行主程序。主程序通常是通过调用特定的函数或执行特定的语句来定义的。主程序可以包含一系列操作、函数调用、类实例化以及其他逻辑。

    - 5.函数调用和方法调用：
在主程序中，如果遇到函数调用或方法调用的语句，解释器会跳转到相应的函数或方法，并执行其内部的代码。执行完成后，解释器会回到调用处继续执行后续的代码。

    - 6.控制流语句的处理：
在代码的执行过程中，解释器会根据条件判断、循环语句等控制流语句来决定执行路径。例如，if语句根据条件的真假来选择不同的分支执行。

    - 7.异常处理：
在代码执行过程中，如果出现异常，解释器会根据异常处理机制来捕获并处理异常。你可以使用try-except语句来捕获异常，并在except块中定义相应的处理逻辑。
    - 8.代码执行结束：
当代码的执行到达脚本的末尾或遇到sys.exit()等终止语句时，解释器会结束代码的执行，并退出程序。
### _boot.py文件的理解
+ 在MicroPython中，_boot.py是一个特殊的启动文件。它类似于Python中的__init__.py文件，但用于MicroPython的启动过程。

+ 当MicroPython设备启动时，它会在文件系统中查找并执行名为_boot.py的文件（如果存在）。这个文件用于执行一些初始化操作，例如设置默认配置、导入模块或执行自定义的启动代码。

+ _boot.py文件通常用于配置和初始化MicroPython设备的各种设置，例如网络连接、GPIO引脚配置等。它可以根据你的需求进行自定义编写，以适应具体的应用场景。

+ 需要注意的是，_boot.py文件是特定于MicroPython的，不是Python的标准文件。它的具体用法和功能可能会因MicroPython的版本和所在的硬件平台而有所不同。因此，如果你在使用MicroPython时遇到了具体的问题或需要更详细的信息，请参考MicroPython的文档或相关资源。
---
## 什么是类的单例设计？例子
+ 类的单例设计是一种设计模式，它确保一个类只有一个实例，并提供一个全局访问点来访问该实例。这种设计模式通常用于需要共享资源或跨多个部分使用相同状态的情况。
+ 下面是一个简单的例子来说明类的单例设计：
```
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

# 创建实例
s1 = Singleton()
s2 = Singleton()

# 验证实例是否相同
print(s1 is s2)  # 输出: True
```
+ 在上面的例子中，Singleton类使用了一个类变量 _instance 来保存实例。在类的 __new__ 方法中，我们检查 _instance 是否为 None，如果是，则创建一个新的实例并将其赋值给 _instance，否则直接返回 _instance。

+ 当我们创建 s1 和 s2 两个实例时，由于 Singleton 类只有一个实例，因此 s1 和 s2 实际上是同一个对象。因此，s1 is s2 的结果为 True。

+ 这样设计的好处是可以确保在整个程序中只有一个实例存在，从而避免了资源的重复创建和状态的不一致性。类的单例设计模式在需要共享状态或资源的场景中非常有用，例如数据库连接池、日志记录器等。
---