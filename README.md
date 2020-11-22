# 智能浇花系统实践分享

## 整体原理

![image-20201122112242854](/Users/clevercong/OneDrive/11、树莓派/PIC/image-20201122112206604.png)

- 温度传感器 + 湿度传感器 + 土壤传感器 = 决定是否浇水
- 继电器 + 水泵 = 控制浇水
- HiLens + 模型 = 判断花的种类
- HiLens + 树莓派 = 数据上传与命令下发

## 准备工作

1. Huawei HiLens *1
2. 树莓派4B *1
3. 土壤传感器+水泵+继电器+电池盒浇花套装，淘宝13块钱有售，不含邮费 *1
4. 空气温湿度压强环境传感器（BME280） *1

## 步骤一：模型训练与转换

1. 首先在网上随意下载一个flowers的数据集，5分类，17分类，102分类的都可以，这里为了训练方便，选择了5分类的：http://download.tensorflow.org/example_images/flower_photos.tgz

2. 上传到OBS上。这里我是用**OBS Brower +**上传的，详见：https://support.huaweicloud.com/browsertg-obs/obs_03_1003.html

   ![image-20201122115205144](/Users/clevercong/OneDrive/11、树莓派/PIC/image-20201122115205144.png)

3. 进入**ModelArts-北京四**控制台，点击**数据管理** - **数据集** - **创建数据集**

   ![image-20201122114400448](/Users/clevercong/OneDrive/11、树莓派/PIC/image-20201122114400448.png)

4. 名称自定义，标注场景选择**图片**，标注类型选择**图像分类**，输入OBS的**输入位置**与**输出位置**，点击创建。

   > 注意这里数据集输入位置，放一个空文件夹（/empty），不要放上一步导入的文件夹（/input）。

   ![image-20201122115707242](/Users/clevercong/OneDrive/11、树莓派/PIC/image-20201122115707242.png)

5. 回到数据集管理界面，进入刚创建的数据集，点击右上角的**导入**，选择从OBS导入。这样导入的数据就是自动标注的了。

   ![image-20201122115903496](/Users/clevercong/OneDrive/11、树莓派/PIC/image-20201122115903496.png)

6. 标注进行中：

   ![image-20201122120013534](/Users/clevercong/OneDrive/11、树莓派/PIC/image-20201122120013534.png)

7. 标注完成，记得点击**发布**按钮，否则一会训练的时候找不到：

   ![image-20201122155257030](/Users/clevercong/OneDrive/11、树莓派/PIC/image-20201122155257030.png)

8. 进入AI市场：

   ![image-20201122114227297](/Users/clevercong/OneDrive/11、树莓派/PIC/image-20201122114227297.png)

9. 找到**图像分类**-**ResNet_V1_50**，点击订阅：

   ![image-20201122155402840](/Users/clevercong/OneDrive/11、树莓派/PIC/image-20201122155402840.png)

10. 订阅后进入控制台，点击**创建训练作业**：

   ![image-20201122155554424](/Users/clevercong/OneDrive/11、树莓派/PIC/image-20201122155554424.png)

11. 选择数据来源，选择刚创建的数据集；模型输出地址选择一个空白的文件夹即可；资源池选个免费的就行：

    ![image-20201122160319034](/Users/clevercong/OneDrive/11、树莓派/PIC/image-20201122160319034.png)

12. 点击下一步，提交即可。等待一段时间。

    ![image-20201122160442368](/Users/clevercong/OneDrive/11、树莓派/PIC/image-20201122160442368.png)

13. 可以看到训练速度非常的快，3分多钟就训练好了：

    ![image-20201122161827798](/Users/clevercong/OneDrive/11、树莓派/PIC/image-20201122161827798.png)

14. 接下来进入到ModelArts控制台，点击模型管理，压缩/转换，新建任务：

    ![image-20201122162229880](/Users/clevercong/OneDrive/11、树莓派/PIC/image-20201122162229880.png)

15. 转换输入目录选择11.中**指定的目录/frozen_graph/**，输出目录指定一个新的空目录，输入框架选择**TensorFlow**，输出框架选择**MindSpore**，转换模板选择**TF-FrozenGraph-To-Ascend-HiLens**，输入张量形状 **images:1,224,224,3**，转换输出节点  **logits:0**。详见下图：

    ![image-20201122163417914](/Users/clevercong/OneDrive/11、树莓派/PIC/image-20201122163417914.png)

16. 进入HiLens控制台，**技能开发** - 模型管理，点击右上角的**导入（转换）模型**。选择刚才转换后的模型。

    ![image-20201122164230902](/Users/clevercong/OneDrive/11、树莓派/PIC/image-20201122164230902.png)

17. 接下来就可以使用这个模型了。具体如何在HiLens中使用，讲解稍后继续。

## 步骤二：树莓派数据采集



## 步骤三：树莓派控制水泵浇水



## 步骤四：树莓派与HiLens通信



## 步骤五：HiLens控制树莓派实现智能浇花



## 未来演进方向

