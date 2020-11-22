# 智能浇花系统实践分享

## 整体原理

![image-20201122112242854](https://github.com/cleverchap/Flower/blob/main/pic/chapter1/image-20201122112206604.png)

- 温度传感器 + 湿度传感器 + 土壤传感器 = 决定是否浇水
- 继电器 + 水泵 = 控制浇水
- HiLens + 模型 = 判断花的种类
- HiLens + 树莓派 = 数据上传与命令下发

## 准备工作

1. Huawei HiLens *1（假设已经完成HiLens设备的初始化工作，包括连接WIFI，注册设备等等）
2. 树莓派4B *1（假设已经完成树莓派设备的初始化工作，包括连接WIFI，设置用户名密码等等）
3. 树莓派其他配件，包括电源线、扩展排线、面包板、杜邦线、散热片、散热风扇等等 *1
4. 土壤传感器+水泵+继电器+电池盒浇花套装，淘宝13块钱有售，不含邮费 *1
5. 空气温湿度压强环境传感器（BME280） *1
6. 剪刀、电工胶布

## 步骤一：模型训练与转换

1. 首先在网上随意下载一个flowers的数据集，5分类，17分类，102分类的都可以，这里为了训练方便，选择了5分类的：http://download.tensorflow.org/example_images/flower_photos.tgz

2. 上传到OBS上。这里我是用**OBS Brower +**上传的，详见：https://support.huaweicloud.com/browsertg-obs/obs_03_1003.html

   ![image-20201122115205144](https://github.com/cleverchap/Flower/blob/main/pic/chapter1/image-20201122115205144.png)

3. 进入**ModelArts-北京四**控制台，点击**数据管理** - **数据集** - **创建数据集**

   ![image-20201122114400448](https://github.com/cleverchap/Flower/blob/main/pic/chapter1/image-20201122114400448.png)

4. 名称自定义，标注场景选择**图片**，标注类型选择**图像分类**，输入OBS的**输入位置**与**输出位置**，点击创建。

   > 注意这里数据集输入位置，放一个空文件夹（/empty），不要放上一步导入的文件夹（/input）。

   ![image-20201122115707242](https://github.com/cleverchap/Flower/blob/main/pic/chapter1/image-20201122115707242.png)

5. 回到数据集管理界面，进入刚创建的数据集，点击右上角的**导入**，选择从OBS导入。这样导入的数据就是自动标注的了。

   ![image-20201122115903496](https://github.com/cleverchap/Flower/blob/main/pic/chapter1/image-20201122115903496.png)

6. 标注进行中：

   ![image-20201122120013534](https://github.com/cleverchap/Flower/blob/main/pic/chapter1/image-20201122120013534.png)

7. 标注完成，记得点击**发布**按钮，否则一会训练的时候找不到：

   ![image-20201122155257030](https://github.com/cleverchap/Flower/blob/main/pic/chapter1/image-20201122155257030.png)

8. 进入AI市场：

   ![image-20201122114227297](https://github.com/cleverchap/Flower/blob/main/pic/chapter1/image-20201122114227297.png)

9. 找到**图像分类**-**ResNet_V1_50**，点击订阅：

   ![image-20201122155402840](https://github.com/cleverchap/Flower/blob/main/pic/chapter1/image-20201122155402840.png)

10. 订阅后进入控制台，点击**创建训练作业**：

   ![image-20201122155554424](https://github.com/cleverchap/Flower/blob/main/pic/chapter1/image-20201122155554424.png)

11. 选择数据来源，选择刚创建的数据集；模型输出地址选择一个空白的文件夹即可；资源池选个免费的就行：

    ![image-20201122160319034](https://github.com/cleverchap/Flower/blob/main/pic/chapter1/image-20201122160319034.png)

12. 点击下一步，提交即可。等待一段时间。

    ![image-20201122160442368](https://github.com/cleverchap/Flower/blob/main/pic/chapter1/image-20201122160442368.png)

13. 可以看到训练速度非常的快，3分多钟就训练好了：

    ![image-20201122161827798](https://github.com/cleverchap/Flower/blob/main/pic/chapter1/image-20201122161827798.png)

14. 接下来进入到ModelArts控制台，点击模型管理，压缩/转换，新建任务：

    ![image-20201122162229880](https://github.com/cleverchap/Flower/blob/main/pic/chapter1/image-20201122162229880.png)

15. 转换输入目录选择11.中**指定的目录/frozen_graph/**，输出目录指定一个新的空目录，输入框架选择**TensorFlow**，输出框架选择**MindSpore**，转换模板选择**TF-FrozenGraph-To-Ascend-HiLens**，输入张量形状 **images:1,224,224,3**，转换输出节点  **logits:0**。详见下图：

    ![image-20201122163417914](https://github.com/cleverchap/Flower/blob/main/pic/chapter1/image-20201122163417914.png)

16. 进入HiLens控制台，**技能开发** - 模型管理，点击右上角的**导入（转换）模型**。选择刚才转换后的模型。

    ![image-20201122164230902](https://github.com/cleverchap/Flower/blob/main/pic/chapter1/image-20201122164230902.png)

17. 接下来就可以使用这个模型了。具体如何在HiLens中使用，稍后继续讲解。

## 步骤二：树莓派数据采集与控制水泵浇水

### 树莓派连接

首先将树莓派跟传感器连接好，这里建议单独购买一个扩展排线+面包板，要不然不够连的。

这里我是把BME280连接到了物理引脚1、3、5、9。**土壤湿度传感器DO口**连接到了物理引脚12（BCM编码18，代码`shumeipai/settings.py/sensor_channel=18`），**继电器IN口**连接到了物理引脚18（BCM编码24，代码`shumeipai/settings.py/power_channel=24`），**继电器COM端**连接**水泵正极**，**继电器NO端**连接**单独供电电源的正极**（防止电压不足），**继电器VCC端**连接3.3V（物理引脚17），**水泵负极**接**单独供电电源的负极**。其他正常接地、接电源即可。

![image-20201122173258026](https://github.com/cleverchap/Flower/blob/main/pic/chapter2/image-20201122173258026.png)

### 土壤干湿度数据采集

在土壤传感器上有四个口，分别是AO/DO/VCC/GND，VCC/GND是电源和接地不用说了，AO是模拟信号，DO是数字信号。模拟信号可以输出电压值，可以转换成干湿度，但是需要单独购买一个转换器；数字信号输出高低电平，灵敏度可以使用小螺丝刀通过传感器上的一个旋钮调节。这里以数字信号为例，模拟信号可以参考这篇博客：https://bbs.huaweicloud.com/blogs/178706

用螺丝刀调节好灵敏度后，就可以直接运行代码了，代码非常简单。土壤干湿度数据采集详见代码：`shumeipai/soil_sensor.py/get_result_from_sensor()`

### 空气温湿度压强数据采集

这里使用了微雪BME280集成扩展板，使用起来比较简单，厂家提供现成的`C`代码和详细的指导。需要先开启`I2C`和`SPI`，具体步骤详见：https://www.waveshare.net/wiki/BME280_Environmental_Sensor

连接好以后，输入`i2cdetect -y 1`，如果全都是`--`的话，说明没有连接好，或者电压不足。如果显示`77`或者`76`的话，说明连接成功了。Python代码详见：`shumeipai/bme280.py`。如果要修改是`77`还是`76`，修改`DEVICE = 0x77`字段即可。

![BME280-Environmental-Sensor-user-manual-4.png](https://www.waveshare.net/w/upload/d/d8/BME280-Environmental-Sensor-user-manual-4.png)

###  树莓派控制水泵浇水

树莓派控制水泵浇水，是通过`GPIO24`口的高低电平实现的。首先设置`Mode`为`OUT`，设置低电平代表出水，设置高电平代表停止出水。

代码详见：`shumeipai/power_control.py`。    

## 步骤三：HiLens编码与调试

1. 首先进入HiLens控制台，点击左侧**技能开发** - **HiLens Studio(Beta**)。

![image-20201122194121874](https://github.com/cleverchap/Flower/blob/main/pic/chapter3/image-20201122194121874.png)

2. 创建一个新的工程，可以选择一个已有的技能模板二次开发，这里我们选择了**Heart_Shape_Detection**。

3. 工程生成的代码文件主要是两个：`main.py`和`utils.py`。其中代码部分已经有相当详细的注释。可以参考。

4. 第一步我们先把加载的模型换掉。`HiLens Studio`模型文件放在`/model`下面。我们先把之前训练的模型上传。

   ![image-20201122194830852](https://github.com/cleverchap/Flower/blob/main/pic/chapter3/image-20201122194830852.png)

5. 第二步把代码里加载模型的地方，修改成我们自己的模型的名字：

   ```python
       # 初始化模型
       model_path = os.path.join(work_path, 'model/heart-det.om') // 'model/heart-det.om'->'model/xxxx.om' 
       cls_model = hilens.Model(model_path)
   ```

6. 第三步按照自己的代码逻辑，试着编写一部分代码。比如说我们这里打算在屏幕左上角显示花的种类，以及当前的温度、湿度等信息。我们通过注释看到2.4是用来展示结果的地方。我们重点改这里。核心代码如下：

   ```python
   # 输出分类结果、温湿度、及其他处理结果
   def process_predict_result(outputs, input_rgb):
       # 预测结果
       predict = softmax(outputs[0])
       # 得到花的种类
       max_inx = np.argmax(predict)
       # 得到花的名称
       text = get_english_flower_name_by_index(max_inx)
       # 绘制结果
       font = cv2.FONT_HERSHEY_SIMPLEX
       font_scale = 2
       thickness = 2
       # 花的种类显示在屏幕左上角
       cv2.putText(input_rgb, text, (50, 50), font, font_scale, (255, 0, 0), thickness)
       temp, hpa, humi, dry_or_humid = get_temperature_and_humidity_from_sensor()
       # 当前温度、湿度显示在种类下面
       string = "%s C, %s RH, %s hPa, %s" % (temp, humi, hpa, dry_or_humid)
       cv2.putText(input_rgb, string, (50, 100), font, font_scale, (255, 0, 0), thickness)
       return max_inx
   ```

7. `HiLens Studio`提供了在线`Debug`的方式，不依赖`HiLens`硬件。但是和树莓派通信。前期调试`HiLens`识别花的种类的代码的时候，可以试试这个`Debug`功能。

   ![image-20201122200334816](https://github.com/cleverchap/Flower/blob/main/pic/chapter3/image-20201122200334816.png)

   这里预置了一小段视频，在`/test`文件夹下，文件名固定为`camera0.mp4`。预置的这个视频不能满足我们调试花种类判断的诉求。因此我们需要录一小段（10s）左右的视频，然后上传到这里，名字改成一样的。

   ![image-20201122200519731](https://github.com/cleverchap/Flower/blob/main/pic/chapter3/image-20201122200519731.png)

   但是执行代码，并不会成功。因为原视频是`1280x720`的，我用手机录的是`540x960`的，中心点不一样。需要修改`preprocess()`函数。相关代码如下：

   ```python
   # 对输入图像进行预处理——画框、截图
   def preprocess(input_nv21):
       input_rgb = cv2.cvtColor(input_nv21, cv2.COLOR_YUV2RGB_NV21)
   
       radius = 240  # 240
       if USING_HILENS:
           img_center = [640, 360]  # 画面(1280x720)中心点
       else:
           img_center = [270, 480]  # 画面(540x960)中心点
       // ...
   ```

   不要问我怎么知道的...`HiLens`相当难调试，不像写`App`那样可以在线看`log`，只能各种猜测和加`log`了。

## 步骤四：树莓派与HiLens通信

1. 可以看到，我们上面的`get_temperature_and_humidity_from_sensor()`是用来获取温湿度等信息的。单靠`HiLens`是没有办法连接那些传感器的，必须靠树莓派中转一下。这里我们通过局域网`IP`直连的方式（最简单），没有继续去挖掘。

2. 树莓派（`Client`端）代码：`shumeipai/client.py`，`Client`端需要知道`Server`端的`IP`地址。

3. `HiLens`（`Server`端）代码：`HiLens/server.py`

4. 最后，由于`HiLens`视频捕捉是一个`while(1)`的死循环，`Socket`通信又是一个`while(1)`的死循环，因此需要启两个线程来完成各自的工作。

   ```python
   def run(work_space):
       hilens.error("start!!!!!!!!!!!!!!")
       # 创建两个线程
       try:
           _thread.start_new_thread(run_inner, (work_space,))
           _thread.start_new_thread(start_listen, ())
       except:
           print("Error: 无法启动线程")
       while 1:
           pass
       hilens.error("end!!!!!!!!!!!!!!")
   ```

## 步骤五：HiLens控制树莓派实现智能浇花

1. `Client`端发给`Server`端的数据是一个字符串，按照固定的格式，包括温度、湿度、压强、土壤干湿情况；如果`Server`端回复的字符串以`Watching`开头，后面跟随要浇花的秒数。

   ```python
   tcpCliSock = socket(AF_INET, SOCK_STREAM)
   tcpCliSock.connect(ADDR)
   
   while True:
       sleep(3)
       t1, t2, temperature, pressure, humidity = get_temp_pressure_humidity_from_sensor()
       dry_or_humid = get_result_from_sensor(sensor_channel)
       data1 = ("%.2f,%.2f,%.2f,%s" % (temperature, pressure, humidity, dry_or_humid))
       if not data1:
           break
       tcpCliSock.send(data1.encode())
       data1 = tcpCliSock.recv(BUFSIZ)
       if not data1:
           break
       command = data1.decode('utf-8')
       if command.startswith("Watering"):
           time = command[8:]
           blink(int(float(time)))
   tcpCliSock.close()
   ```

2. `Server`端根据`Client`端提供的数据，加上当前花的种类，以及上次浇水时间，综合判断是否需要浇水以及浇水时长。

   ```python
   def start_listen():
       // ...
       try:
           while True:
   								// ...
                   # 接收传感器数据，温度、湿度、压强、土壤干湿情况
                   set_temperature_and_humidity(split_data[0], split_data[1], split_data[2], split_data[3])
                   command = get_command(time()) # 综合计算是否需要浇花,具体代码详见utils.py/get_prinkling_norm()
                   if command is not None:
                       tcpCliSock.send(('%s' % command).encode()) # 需要浇花
                   else:
                       tcpCliSock.send(('[%s] %s' % (ctime(), data)).encode()) # 不需要浇花
               tcpCliSock.close()
       finally:
           tcpSerSock.close()
   ```

## 未来演进方向

1. 增加光照传感器，已经预留了相关代码，没有调过。
2. 给树莓派装上轮子变成小车，让小车走起来；装上机械臂操控土壤传感器，主动量每一盆花的土壤湿度。

## 遇到的问题和解决方案

1. Q：hilens新建技能，不管是从空模板，还是已有技能新建，都失败。

   A：这个问题是因为之前用`OBS`欠费了，一两天后就把`OBS`所有的桶都删了，包括`HiLens`依赖的桶。而`HiLens`依赖的桶名字是固定的，再新建一个同名的也不行。最后是提了一个工单，找华为的工程师给解决的。所以在调试的时候，尽量避免欠费。


