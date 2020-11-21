# -*- coding: utf-8 -*-
# !/usr/bin/python3

import os
import cv2
import hilens
import _thread

from HiLens.server import start_listen
from HiLens.utils import preprocess
from HiLens.utils import process_predict_result

net_size = 224


def run_inner(work_path):
    # 系统初始化，参数要与创建技能时填写的检验值保持一致
    hilens.init("heart")

    # 初始化摄像头与显示器
    camera = hilens.VideoCapture()
    display = hilens.Display(hilens.HDMI)

    # 初始化模型
    model_path = os.path.join(work_path, 'model/convert-6ecb.om')
    cls_model = hilens.Model(model_path)

    while True:
        try:
            # 2.1 读取摄像头数据
            input_nv21 = camera.read()

            # 2.2 截取出一个正方形区域作为手势识别输入并做预处理
            input_rgb, gesture_area = preprocess(input_nv21)
            input_resized = cv2.resize(gesture_area, (net_size, net_size))

            # 2.3 模型推理
            outputs = cls_model.infer([input_resized.flatten()])

            # 2.4 结果展示
            index = process_predict_result(outputs, input_rgb)
            output_nv21 = hilens.cvt_color(input_rgb, hilens.RGB2YUV_NV21)
            display.show(output_nv21)
        except Exception as e:
            print(e)
            break


def run():
    hilens.error("start!!!!!!!!!!!!!!")
    # 创建两个线程
    try:
        _thread.start_new_thread(run_inner, (os.getcwd(),))
        _thread.start_new_thread(start_listen, ())
    except:
        print("Error: 无法启动线程")
    while 1:
        pass
    hilens.error("end!!!!!!!!!!!!!!")


if __name__ == '__main__':
    run()
