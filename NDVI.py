from main import load_image, main  # 从 main.py 中导入 load_image 和 main 函数
import numpy as np
import matplotlib.pyplot as plt

def calculate_ndvi(band4, band3):
    """
    计算 NDVI 指数。
    NDVI = (Band4 - Band3) / (Band4 + Band3)
    """
    # 使用 numpy 避免分母为 0 的情况
    ndvi = np.where((band4 + band3) == 0, 0, (band4 - band3) / (band4 + band3))
    print(ndvi)
    return ndvi



def main_ndvi():

    # 加载影像数据集（此时图像路径已在 main 函数中指定）
    image_path = r"D:\360MoveData\Users\32843\Desktop\work_img_processing\Data\can_tmr_v1.tif"
    dataset, band_count = load_image(image_path)

    if dataset and band_count >= 4:  # 检查是否至少有 4 个波段
        # 提取 Band 4 和 Band 3 数据
        band4 = dataset.GetRasterBand(4).ReadAsArray()
        band3 = dataset.GetRasterBand(3).ReadAsArray()

        # 计算 NDVI
        ndvi = calculate_ndvi(band4, band3)

        # 显示 NDVI 结果

        plt.imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
        plt.colorbar(label='NDVI')
        plt.title('NDVI Index')
        plt.axis('off')
        plt.show()
    else:
        print("数据集无效或波段不足。")

if __name__ == "__main__":
    main_ndvi()