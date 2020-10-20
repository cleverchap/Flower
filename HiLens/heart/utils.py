import os
import cv2
import numpy as np

threshold = 0.99


# softmax
def softmax(x):
    x = x-np.max(x, axis=0)
    ex = np.exp(x)
    return ex/np.sum(ex, axis=0)


# 画矩形框的四个角
def draw_square(img_data, left_top, right_bot, line_len, color):
    cv2.line(img_data, (left_top[0], left_top[1]),
             (left_top[0] + line_len, left_top[1]), color, 2)
    cv2.line(img_data, (left_top[0], left_top[1]),
             (left_top[0], left_top[1]+line_len), color, 2)
    cv2.line(img_data, (left_top[0], right_bot[1]),
             (left_top[0]+line_len, right_bot[1]),  color, 2)
    cv2.line(img_data, (left_top[0], right_bot[1]),
             (left_top[0], right_bot[1]-line_len),  color, 2)
    cv2.line(img_data, (right_bot[0], left_top[1]),
             (right_bot[0]-line_len, left_top[1]),  color, 2)
    cv2.line(img_data, (right_bot[0], left_top[1]),
             (right_bot[0], left_top[1]+line_len),  color, 2)
    cv2.line(img_data, (right_bot[0], right_bot[1]),
             (right_bot[0]-line_len, right_bot[1]), color, 2)
    cv2.line(img_data, (right_bot[0], right_bot[1]),
             (right_bot[0], right_bot[1]-line_len), color, 2)


# 矩形框四周模糊化
def blur(img_data, left_top, right_bot, k):
    img_data[:left_top[1] - 5, :, :] = \
        cv2.blur(img_data[:left_top[1] - 5, :, :],  ksize=(k, k))
    img_data[:, :left_top[0] - 5, :] = \
        cv2.blur(img_data[:, :left_top[0] - 5, :],  ksize=(k, k))
    img_data[right_bot[1] + 5:, :, :] = \
        cv2.blur(img_data[right_bot[1] + 5:, :, :], ksize=(k, k))
    img_data[:, right_bot[0] + 5:, :] = \
        cv2.blur(img_data[:, right_bot[0] + 5:, :], ksize=(k, k))


# 对输入图像进行预处理——画框、截图
def preprocess(input_nv21):
    input_rgb = cv2.cvtColor(input_nv21, cv2.COLOR_YUV2RGB_NV21)

    radius = 240
    img_center = [640, 360]  # 画面(1280x720)中心点
    left_top = [img_center[0]-radius, img_center[1]-radius]
    right_bot = [img_center[0]+radius, img_center[1]+radius]

    line_len = 40
    color = (255, 255, 255)
    kernel_size = 20
    draw_square(input_rgb, left_top, right_bot, line_len, color)
    blur(input_rgb, left_top, right_bot, kernel_size)

    # 截取出一个正方形区域作为手势识别输入
    gesture_area = input_rgb[img_center[1] - radius: img_center[1] + radius,
                             img_center[0] - radius: img_center[0] + radius,
                             :]
    return input_rgb, gesture_area


# 加载资源图像——透明心形图与封面图
def load_assets(work_path):
    img_heart = cv2.imread(os.path.join(work_path, 'test/heart.png'))
    img_heart = cv2.cvtColor(img_heart, cv2.COLOR_BGR2RGB)

    img_cover = cv2.imread(os.path.join(work_path, 'test/cover.jpg'))
    img_cover = cv2.cvtColor(img_cover, cv2.COLOR_BGR2RGB)
    img_cover = cv2.resize(img_cover, (1280, 720))
    return img_heart, img_cover


# 结果展示——若检测到心形手势显示简单的动画特效
def show_result(index, input_rgb, outputs, img_heart, img_cover):
    predict = softmax(outputs[0])
    max_inx = np.argmax(predict)
    img_heart_flip = cv2.flip(img_heart, 1)
    h_heart, w_heart, _ = img_heart.shape
    h_input, w_input, _ = input_rgb.shape

    font_scale = 2
    thickness = 2
    font = cv2.FONT_HERSHEY_SIMPLEX
    if max_inx == 2 and predict[max_inx] > threshold:
        index += 1
        y = h_input - h_heart - index*3
        if y <= 0:
            y = 0
            input_rgb = img_cover
        else:
            input_rgb[y:y+h_heart, 128:128+w_heart, :] = \
                cv2.addWeighted(input_rgb[y:y+h_heart, 128:128+w_heart, :],
                                1, img_heart_flip, 0.5, 0)
            input_rgb[y:y+h_heart, 128+w_heart:128+2*w_heart, :] = \
                cv2.addWeighted(input_rgb[y:y+h_heart,
                                          128+w_heart:128+2*w_heart,
                                          :],
                                1, img_heart, 0.5, 0)
            cv2.putText(input_rgb, 'Heart', (550, 100), font,
                        font_scale, (255, 0, 0), thickness)
    else:
        index = 0
    return index, input_rgb