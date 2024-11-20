import matplotlib.pyplot as plt
from osgeo import gdal

def load_image(image_path):
    """加载影像并返回数据集和波段数量。"""
    dataset = gdal.Open(image_path)
    if dataset is None:
        print(f"无法打开影像文件: {image_path}")
        return None, 0
    
    band_count = dataset.RasterCount
    return dataset, band_count

def display_image(image_path):
    dataset, band_count = load_image(image_path)

    if dataset:
        print(f"影像已成功加载，波段数量: {band_count}")

        while True:
            band_number = input(f"请输入要显示的波段编号（1 到 {band_count}），或输入 'exit' 退出: ")

            if band_number.lower() == 'exit':
                break

            try:
                band_number = int(band_number)
                if 1 <= band_number <= band_count:
                    # 读取指定波段的数据
                    band = dataset.GetRasterBand(band_number)
                    data = band.ReadAsArray()
                    print(f"第 {band_number} 波段的数据形状: {data.shape}")

                    # 显示原始影像
                    plt.imshow(data, cmap='gray')
                    plt.title(f'Original Image - Band {band_number}')
                    plt.axis('off')
                    plt.show()
                else:
                    print(f"无效的波段编号，请输入范围内的数字（1 到 {band_count}）。")
            except ValueError:
                print("请输入有效的数字或 'exit' 以退出。")

def main():
    image_path = r"Data\can_tmr_v1.tif"  ##将图片放入DATA文件夹，可以修改你自己需要的数据
    print("success")
    return image_path

if __name__ == "__main__":
    main()
