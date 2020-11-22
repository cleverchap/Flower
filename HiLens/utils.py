import cv2
import numpy as np

DBG = False
INFO = False
USING_HILENS = True
IS_DEMO = True

current_temp = ""
current_humidity = ""
current_pressure = ""
current_dry_or_humid = ""
current_illumination = ""
last_watering_time = 0


# softmax
def softmax(x):
    x = x - np.max(x, axis=0)
    ex = np.exp(x)
    return ex / np.sum(ex, axis=0)


# 画矩形框的四个角
def draw_square(img_data, left_top, right_bot, line_len, color):
    cv2.line(img_data, (left_top[0], left_top[1]),
             (left_top[0] + line_len, left_top[1]), color, 2)
    cv2.line(img_data, (left_top[0], left_top[1]),
             (left_top[0], left_top[1] + line_len), color, 2)
    cv2.line(img_data, (left_top[0], right_bot[1]),
             (left_top[0] + line_len, right_bot[1]), color, 2)
    cv2.line(img_data, (left_top[0], right_bot[1]),
             (left_top[0], right_bot[1] - line_len), color, 2)
    cv2.line(img_data, (right_bot[0], left_top[1]),
             (right_bot[0] - line_len, left_top[1]), color, 2)
    cv2.line(img_data, (right_bot[0], left_top[1]),
             (right_bot[0], left_top[1] + line_len), color, 2)
    cv2.line(img_data, (right_bot[0], right_bot[1]),
             (right_bot[0] - line_len, right_bot[1]), color, 2)
    cv2.line(img_data, (right_bot[0], right_bot[1]),
             (right_bot[0], right_bot[1] - line_len), color, 2)


# 矩形框四周模糊化
def blur(img_data, left_top, right_bot, k):
    img_data[:left_top[1] - 5, :, :] = \
        cv2.blur(img_data[:left_top[1] - 5, :, :], ksize=(k, k))
    img_data[:, :left_top[0] - 5, :] = \
        cv2.blur(img_data[:, :left_top[0] - 5, :], ksize=(k, k))
    img_data[right_bot[1] + 5:, :, :] = \
        cv2.blur(img_data[right_bot[1] + 5:, :, :], ksize=(k, k))
    img_data[:, right_bot[0] + 5:, :] = \
        cv2.blur(img_data[:, right_bot[0] + 5:, :], ksize=(k, k))


# 对输入图像进行预处理——画框、截图
def preprocess(input_nv21):
    input_rgb = cv2.cvtColor(input_nv21, cv2.COLOR_YUV2RGB_NV21)

    radius = 240  # 240
    if USING_HILENS:
        img_center = [640, 360]  # 画面(1280x720)中心点
    else:
        img_center = [270, 480]  # 画面(540x960)中心点
    left_top = [img_center[0] - radius, img_center[1] - radius]
    right_bot = [img_center[0] + radius, img_center[1] + radius]

    line_len = 40
    color = (255, 255, 255)
    kernel_size = 20
    draw_square(input_rgb, left_top, right_bot, line_len, color)
    blur(input_rgb, left_top, right_bot, kernel_size)

    # 截取出一个正方形区域作为识别区域
    gesture_area = input_rgb[img_center[1] - radius: img_center[1] + radius,
                   img_center[0] - radius: img_center[0] + radius,
                   :]
    return input_rgb, gesture_area


# 输出分类结果、温湿度、及其他处理结果
def process_predict_result(outputs, input_rgb):
    # 预测结果
    predict = softmax(outputs[0])
    # 得到花的种类
    max_inx = np.argmax(predict)
    logi(max_inx)
    # 得到花的名称
    text = get_english_flower_name_by_index(max_inx)
    logi(text)
    # 绘制结果
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    thickness = 2
    logd("before" + str(input_rgb))
    # 花的种类显示在屏幕左上角
    cv2.putText(input_rgb, text, (50, 50), font, font_scale, (255, 0, 0), thickness)
    temp, hpa, humi, dry_or_humid = get_temperature_and_humidity_from_sensor()
    # 当前温度、湿度显示在种类下面
    string = "%s C, %s RH, %s hPa, %s" % (temp, humi, hpa, dry_or_humid)
    cv2.putText(input_rgb, string, (50, 100), font, font_scale, (255, 0, 0), thickness)
    logi(string)
    logd("after" + str(input_rgb))
    return max_inx


def get_chinese_flower_name_by_index(index):
    # {“labels_list”：[“雏菊”，“蒲公英”，“玫瑰”，“向日葵”，“郁金香”]，“ismultilabel”：错误}
    switch = {0: "雏菊", 1: "蒲公英", 2: "玫瑰", 3: "向日葵", 4: "郁金香"}
    return switch.get(index, "Not Found")


def get_english_flower_name_by_index(index):
    # {"labels_list": ["daisy", "dandelion", "roses", "sunflowers", "tulips"], "is_multilabel": false}
    switch = {0: "daisy", 1: "dandelion", 2: "roses", 3: "sunflowers", 4: "tulips"}
    return switch.get(index, "Not Found")


def get_temperature_and_humidity_from_sensor():
    return current_temp, current_pressure, current_humidity, current_dry_or_humid


def set_temperature_and_humidity(temp, pressure, humid, dry_or_humid, illumination=""):
    global current_pressure, current_temp, current_humidity, current_dry_or_humid, current_illumination
    current_temp = temp
    current_pressure = pressure
    current_humidity = humid
    current_dry_or_humid = dry_or_humid
    current_illumination = illumination


def get_command(current_time):
    global last_watering_time
    if last_watering_time == 0:
        print("first time, return")
        last_watering_time = current_time
        return None
    # 60 = 1min; 3600 = 1h(Dry); 10800 = 3h(Humid)
    # 根据土壤干湿度决定是否浇花
    waiting_time = 3600
    if current_dry_or_humid == "Humid":
        waiting_time *= 3  # 10800
    if IS_DEMO:
        waiting_time /= 300  # 18s for dry or 54s for humid
    if current_time - last_watering_time > waiting_time:
        last_watering_time = current_time
        return "Watering" + str(get_prinkling_norm())
    return None


def get_prinkling_norm():
    base = 1.0
    # 根据光照调整浇水量
    try:
        if float(current_illumination) > 2000:
            base *= 3
        elif float(current_illumination) > 1500:
            base *= 2
        elif 500 > float(current_illumination) > 0:
            base *= 0.8
    except ValueError:
        print("value error for illumination: " + current_illumination)
    # 根据空气温度调整浇水量
    if float(current_temp) > 30:
        base *= 3.2
    elif float(current_temp) > 25:
        base *= 1.6
    elif float(current_temp) < 5:
        base *= 0.4
    # 根据空气湿度调整浇水量
    if float(current_humidity) < 10:
        base *= 2.4
    elif float(current_humidity) < 20:
        base *= 1.2
    elif float(current_humidity) > 60:
        base *= 0.8
    # MAX is 23.04; MIN is 0.256
    base = min(base, 5)
    base = max(base, 0.5)
    return base * 5


def logd(content):
    if DBG:
        print(str(content))


def logi(content):
    if INFO:
        print(str(content))
