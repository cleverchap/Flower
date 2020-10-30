# -*- coding: utf-8 -*-
# !/usr/bin/python3
# SkillFramework 1.0.0 python demo

import os
import cv2
import hilens
import _thread

from HiLens.server import start_listen
from HiLens.utils import load_assets
from HiLens.utils import preprocess
from HiLens.utils import process_predict_result
from HiLens.utils import logd, logi

net_size = 224


def run_inner(work_path):
    # 系统初始化，参数要与创建技能时填写的检验值保持一致
    hilens.init("heart")
    hilens.error("run !!!!!!!!!! " + work_path)

    # 初始化摄像头与显示器
    camera = hilens.VideoCapture()
    display = hilens.Display(hilens.HDMI)

    # 初始化模型
    # model_path = os.path.join(work_path, 'model/heart-det.om')
    model_path = os.path.join(work_path, 'model/convert-6ecb.om')
    cls_model = hilens.Model(model_path)
    logi("model_path:")
    logi(model_path)
    logi("cls_modem")
    logi(cls_model)

    # 加载图片资源文件
    img_heart, img_cover = load_assets(work_path)
    logd("img_heart")
    logd(img_heart)

    index = 0
    while True:
        try:
            # 2.1 读取摄像头数据
            input_nv21 = camera.read()
            logd("input_nv21")
            logd(input_nv21)

            # 2.2 截取出一个正方形区域作为手势识别输入并做预处理
            input_rgb, gesture_area = preprocess(input_nv21)
            logd("input_rgb")
            logd(input_rgb)
            logd("gesture_area")
            logd(gesture_area)
            input_resized = cv2.resize(gesture_area, (net_size, net_size))
            logd("input_resized")
            logd(input_resized)

            # 2.3 模型推理
            outputs = cls_model.infer([input_resized.flatten()])
            logd("outputs")
            logd(outputs)

            # 2.4 结果展示
            index = process_predict_result(outputs, input_rgb)
            logd("index")
            logd(index)
            logd("input_rgb")
            logd(input_rgb)
            output_nv21 = hilens.cvt_color(input_rgb, hilens.RGB2YUV_NV21)
            display.show(output_nv21)
        except Exception as e:
            print(e)
            break


def run(work_space):
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
    run(work_space=os.getcwd())
