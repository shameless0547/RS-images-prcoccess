from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import cv2  # 使用 OpenCV 进行腐蚀和膨胀操作
from main import main

def read_first_band(image_path):
    """
    使用 GDAL 读取图像并提取第一个波段
    :param image_path: 图像的文件路径
    :return: 第一个波段的数据
    """
    # 打开图像
    dataset = gdal.Open(image_path)

    if dataset is None:
        print(f"无法打开图像: {image_path}")
        return None
    
    band = dataset.GetRasterBand(1)  
    band_data = band.ReadAsArray()  
    dataset = None

    return band_data

def plot_image(image_data):


    if image_data is not None:
        plt.imshow(image_data, cmap='gray')
        plt.colorbar()
        plt.title("First Band of Image")
        plt.show()
    else:
        print("没有数据可显示。")

def compute_statistics(image_data):
    """
    计算图像数据的统计信息：最大值、最小值、均值
    :param image_data: 图像数据（numpy 数组）
    """
    if image_data is not None:
        max_value = np.max(image_data)
        min_value = np.min(image_data)
        mean_value = np.mean(image_data)

        print(f"最大值: {max_value}, 最小值: {min_value}, 平均值: {mean_value}")
    else:
        print("没有数据可计算。")

def apply_morphological_operations(image_data, operation='erosion', kernel_size=3, iterations=1):

    kernel = np.ones((kernel_size, kernel_size), np.uint8)  # 创建结构元素（3x3的全1核）


    if operation == 'erosion':
        processed_image = cv2.erode(image_data, kernel, iterations=iterations)  # 腐蚀操作
    elif operation == 'dilation':
        processed_image = cv2.dilate(image_data, kernel, iterations=iterations)  # 膨胀操作
    else:
        raise ValueError("Unsupported operation. Use 'erosion' or 'dilation'.")
    
    return processed_image

def get_iterations():
    while True:
        try:
            iterations = int(input("请输入迭代次数 (整数): "))
            if iterations < 1:
                print("迭代次数必须是正整数，请重新输入。")
            else:
                return iterations
        except ValueError:
            print("无效输入，请输入一个整数。")

def get_operation():
    """
    让用户选择形态学操作（腐蚀或膨胀）
    :return: 用户选择的操作类型
    """
    while True:
        operation = input("请选择形态学操作 (erosion / dilation): ").strip().lower()
        if operation in ['erosion', 'dilation']:
            return operation
        else:
            print("无效输入，请选择 'erosion' 或 'dilation'。")




if __name__ == "__main__":
    # 调用 other_script.py 中的 main() 函数来获取图像路径
    image_path = main()  # 获取图像路径

    if image_path is not None:
        band_data = read_first_band(image_path)
        
        # 获取用户输入的迭代次数
        iterations = get_iterations()
        
        # 选择形态学操作类型
        operation = get_operation()

        # 应用形态学操作
        processed_image = apply_morphological_operations(band_data, operation=operation, iterations=iterations)
        
        # 显示处理后的图像
        plot_image(processed_image)
    else:
        print("无法获取图像路径。")