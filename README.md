代码下载：
https://github.com/cleverchap/Flower.git

查看有同一局域网内有哪些IP
arp -a

OSError: [Errno 48] Address already in use
解决办法：前者很简单，杀死进程．后者更简单把正在run的项目停掉．
lsof -i :5000 # 这个命令针对我用的port 5000

如果是查看本机所有的进行的进程：
ps aux　 #　用ps -A查看所有进程

杀死进程：
kill -9 PID # PID是进程号,查看进程时会显示，比如23645

树莓派云灌溉系统的实现
https://github.com/sogeisetsu/shumeipai

在树莓派上读取土壤湿度传感器读数-python代码实现及常见问题（全面简单易懂）
https://bbs.huaweicloud.com/blogs/178706

树莓派土壤湿度传感器 - 全文
http://www.elecfans.com/yuanqijian/sensor/20180122620414_a.html

自动浇灌系统：
https://make.quwj.com/project/78

树莓派实现自动浇花程序
https://blog.csdn.net/jiaojuan9641/article/details/107510342

BME传感器引脚连接：
http://www.waveshare.net/wiki/BME280_Environmental_Sensor

BME Python代码：
https://www.jianshu.com/p/3eeac8b4123b?utm_campaign=hugo

查询温度湿度压强传感器是否在位：
i2cdetect -y 1

树莓派4B 使用gpio readall无法查询到管脚信息的问题及解决办法
https://blog.csdn.net/SmartTiger_CSL/article/details/102859831