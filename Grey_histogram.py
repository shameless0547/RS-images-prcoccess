import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
from main import load_image,main,display_image

def compute_histogram(data):
    """计算灰度直方图。"""
    histogram = np.zeros(256, dtype=int)
    rows, cols = data.shape
    for i in range(rows):
        for j in range(cols):
            pixel_value = data[i, j]
            if pixel_value >= 0 and pixel_value < 256:
                histogram[pixel_value] += 1
    return histogram

def plot_histogram(histogram):
    """绘制灰度直方图。"""
    plt.bar(range(256), histogram, color='gray', alpha=0.7)
    plt.title('Gray Level Histogram')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.xlim([0, 255])
    plt.grid()

def generate_histogram(image_path):
    dataset, band_count = load_image(image_path)

    if dataset:
        print(f"影像已成功加载，波段数量: {band_count}")
        
        # 读取第一个波段的数据
        band = dataset.GetRasterBand(1)
        data = band.ReadAsArray()
        print(f"第一个波段的数据形状: {data.shape}")
        
        # 计算灰度直方图
        histogram = compute_histogram(data)
        
        # 打印直方图数据
        print("灰度直方图数据:")
        print(histogram)
        
        # 绘制影像和直方图
        plt.figure(figsize=(12,6))


        # 灰度直方图
        plt.subplot(1,1,1)
        plot_histogram(histogram)

        plt.tight_layout()
        plt.show()

        return histogram  # 返回直方图以便在主函数中使用

if __name__ == "__main__":
    image_path = r"D:\360MoveData\Users\32843\Desktop\work_img_processing\Data\can_tmr_v1.tif"
    histogram = generate_histogram(image_path)  # 生成并返回直方图