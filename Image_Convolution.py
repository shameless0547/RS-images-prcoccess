from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
from main import main  # 导入 main 函数，获取图像路径
import cv2  # 用于卷积操作

# 定义卷积核作为全局变量
SOBEL_X = np.array([[1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]], dtype=np.float32)

SOBEL_Y = np.array([[1, 2, 1],
                    [0, 0, 0],
                    [-1, -2, -1]], dtype=np.float32)

# 中值滤波器并不使用传统的卷积核，直接使用 OpenCV 函数
MEDIAN_FILTER = None  # 用特殊标记表示中值滤波器

# 读取图像并提取第一个波段
def load_and_floatify_image(image_path):
    # 使用 GDAL 打开 TIFF 图像
    dataset = gdal.Open(image_path)
    
    if not dataset:
        raise FileNotFoundError(f"无法打开图像文件：{image_path}")
    
    # 获取图像的第一个波段
    band = dataset.GetRasterBand(1)  # 获取第1个波段
    image = band.ReadAsArray()  # 读取波段数据为 NumPy 数组
    
    # 转换为浮动型并归一化到 [0, 1]
    image = np.array(image, dtype=np.float32) / 255.0
    return image

# 卷积运算
def apply_convolution(image, kernel):
    if kernel is not None:
        # 使用 OpenCV 的 filter2D 函数进行卷积运算
        return cv2.filter2D(image, -1, kernel)
    else:
        # 中值滤波处理
        return cv2.medianBlur(image, 3)  # 中值滤波，3表示3x3的邻域

# 使用 matplotlib 输出图像
def display_output_image(convolved_image):
    # 转换为 [0, 255] 范围的整数，便于显示
    convolved_image_display = np.uint8(convolved_image * 255)
    plt.imshow(convolved_image_display, cmap='gray')  # 显示灰度图像
    plt.title("Convolved Image")  # 设置图像标题
    plt.axis('off')  # 不显示坐标轴
    plt.show()  # 显示图像

# 用户输入自定义卷积核
def get_custom_kernel():
    print("请输入一个 3x3 卷积核的数字，按行输入，每行三个数字，使用空格分隔：")
    custom_kernel = []
    
    for i in range(3):
        while True:
            try:
                row = list(map(float, input(f"请输入第{i+1}行卷积核（3个数字，用空格分隔）：").split()))
                if len(row) != 3:
                    print("每行必须输入 3 个数字，请重新输入。")
                else:
                    custom_kernel.append(row)
                    break
            except ValueError:
                print("请输入有效的数字！")
    
    return np.array(custom_kernel, dtype=np.float32)

# 主程序逻辑
def main_convolution():
    image_path = main()  # 从 main.py 获取图像路径
    print(f"获取的图像路径：{image_path}")  # 输出路径用于调试
    image = load_and_floatify_image(image_path)  # 读取并浮动化图像
    
    # 提供用户选择卷积核的功能
    print("请选择卷积核：")
    print("1. 锐化核 [[1, 0, 1], [-2, 0, 2], [-1, 0, 1]]")
    print("2. Sobel算子 [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]")
    print("3. 中值滤波核 (3x3)")
    print("4. 自定义卷积核（3x3)")
    
    kernel_choice = int(input("请输入卷积核的编号 (1, 2, 3 或 4): "))
    
    if kernel_choice == 1:
        kernel = SOBEL_X
    elif kernel_choice == 2:
        kernel = SOBEL_Y
    elif kernel_choice == 3:
        kernel = MEDIAN_FILTER
    elif kernel_choice == 4:
        kernel = get_custom_kernel()  # 调用自定义卷积核输入函数
    else:
        raise ValueError("无效的卷积核选择！")
    
    convolved_image = apply_convolution(image, kernel)  # 应用卷积运算
    display_output_image(convolved_image)  # 使用 matplotlib 显示卷积结果

if __name__ == "__main__":
    main_convolution()