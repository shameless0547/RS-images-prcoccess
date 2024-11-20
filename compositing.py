import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal
from main import load_image, main  

def apply_false_color(data):
    ##"""伪彩色,波段4、3、2."""##
    if data.ndim < 3 or data.shape[0] < 4:
        print("数据必须至少包含四个波段用于伪彩色合成。")
        return None
    
    near_infrared_band = data[3]   # 波段4
    red_band = data[2]             # 波段3
    green_band = data[1]           # 波段2
    
    false_color_image = np.zeros((data.shape[1], data.shape[2], 3), dtype=np.uint8)
    false_color_image[..., 0] = near_infrared_band  # 红色通道，近红外
    false_color_image[..., 1] = red_band            # 绿色通道，红
    false_color_image[..., 2] = green_band          # 蓝色通道，绿
    
    return false_color_image

def apply_true_color(data):
    ##"""应用真彩色映射，使用波段3、2、1."""##
    if data.ndim < 3 or data.shape[0] < 3:
        print("数据必须至少包含三个波段用于真彩色合成。")
        return None
    
    red_band = data[2]   # 波段3
    green_band = data[1] # 波段2
    blue_band = data[0]  # 波段1
    
    true_color_image = np.zeros((data.shape[1], data.shape[2], 3), dtype=np.uint8)
    true_color_image[..., 0] = red_band   # 红色通道
    true_color_image[..., 1] = green_band # 绿色通道
    true_color_image[..., 2] = blue_band   # 蓝色通道
    
    return true_color_image

def display_false_color(data):
    """显示伪彩色合成图像并保存。"""
    false_color_image = apply_false_color(data)
    if false_color_image is not None:
        plt.imshow(false_color_image)
        plt.title('False Color Composite (Band 4, 3, 2)')
        plt.axis('off')
        plt.show()
        plt.imsave("false_color_composite.png", false_color_image)

def display_true_color(data):
    """显示真彩色合成图像并保存。"""
    true_color_image = apply_true_color(data)
    if true_color_image is not None:
        plt.imshow(true_color_image)
        plt.title('True Color Composite (Band 3, 2, 1)')
        plt.axis('off')
        plt.show()
        plt.imsave("true_color_composite.png", true_color_image)


if __name__ == "__main__":
    dataset, band_count = load_image(r"D:\360MoveData\Users\32843\Desktop\work_img_processing\Data\can_tmr_v1.tif")

    if not dataset or band_count < 4:
        print("无法加载数据或波段数量不足。")
    else:
        print(f"影像已成功加载，波段数量: {band_count}")

        # 读取前4个波段
        data = np.array([dataset.GetRasterBand(i + 1).ReadAsArray() for i in range(4)])

        while True:
            user_choice = input("请输入 'false' 查看伪彩色合成，'true' 查看真彩色合成，'exit' 退出程序: ").strip().lower()
            
            if user_choice == 'false':
                display_false_color(data)
            elif user_choice == 'true':
                display_true_color(data)
            elif user_choice == 'exit':
                print("程序已退出。")
                break
            else:
                print("无效输入，请重新输入。")