import rasterio
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# === 参数配置 ===
extract_dir = r"D:\360MoveData\Users\32843\Desktop\自然地理实习\原始数据\光谱曲线\data"
wavelengths = [0.44, 0.48, 0.56, 0.65, 0.86, 1.6, 2.2]  # Landsat 9 OLI 波长
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# === 读取TIF波段文件 ===
tif_files = sorted(glob.glob(os.path.join(extract_dir, "*_B[1-7].TIF")),
                   key=lambda x: int(os.path.basename(x).split('_B')[1].split('.')[0]))

if len(tif_files) != 7:
    raise ValueError("未正确读取7个波段，当前读取数: " + str(len(tif_files)))

band_data_list = []
for path in tif_files:
    with rasterio.open(path) as src:
        band_data_list.append(src.read(1).astype(float))

print(f"读取波段数: {len(band_data_list)}, 图像大小: {band_data_list[0].shape}")

# === 显示 B4 波段（索引为3） ===
fig, ax = plt.subplots(figsize=(8, 8))
b4_display = np.clip(band_data_list[3] / 10000.0, 0, 1)  # B4是红色波段
im = ax.imshow(b4_display, cmap='gray')
ax.set_title("点击像素点查看光谱曲线和指数")

# === 鼠标点击事件 ===
def onclick(event):
    if event.inaxes != ax:
        return
    col = int(event.xdata)
    row = int(event.ydata)
    print(f"\n>>> 选中像素点: Row={row}, Col={col}")

    # 提取该像素在所有波段的反射率（DN值除以10000）
    spectral_values = []
    for data in band_data_list:
        val = data[row, col] / 10000.0
        val = np.clip(val, 0, 1)
        spectral_values.append(val)

    # 命名各波段
    B1, B2, B3, B4, B5, B6, B7 = spectral_values

    # === 指数计算 ===
    NDVI = (B5 - B4) / (B5 + B4) if (B5 + B4) else np.nan
    NDWI = (B2 - B5) / (B2 + B5) if (B2 + B5) else np.nan
    NDBI = (B6 - B5) / (B6 + B5) if (B6 + B5) else np.nan
    MNDWI = (B3 - B6) / (B3 + B6) if (B3 + B6) else np.nan
    SAVI = ((B5 - B4) / (B5 + B4 + 0.5)) * 1.5 if (B5 + B4 + 0.5) else np.nan
    ClayIndex = B7 / B5 if B5 else np.nan
    BrightnessIndex = np.sqrt(B6**2 + B7**2) / np.sqrt(2)

    # 输出指标
    print(f"NDVI: {NDVI:.4f}")
    print(f"NDWI: {NDWI:.4f}")
    print(f"NDBI: {NDBI:.4f}")
    print(f"MNDWI: {MNDWI:.4f}")
    print(f"SAVI: {SAVI:.4f}")
    print(f"Clay Index: {ClayIndex:.4f}")
    print(f"Brightness Index: {BrightnessIndex:.4f}")
    print(f"B6 Reflectance: {B6:.4f}")
    print(f"B7 Reflectance: {B7:.4f}")

    # === 绘制光谱曲线 ===
    plt.figure(figsize=(8, 5))
    plt.plot(wavelengths, spectral_values, color='gray', linestyle='-')
    for i, (wl, val) in enumerate(zip(wavelengths, spectral_values)):
        plt.scatter(wl, val, color=colors[i % len(colors)], s=80, label=f'Band {i+1}')
    plt.title(f"光谱曲线 - 像素({row}, {col})")
    plt.xlabel("波长 (μm)")
    plt.ylabel("反射率")
    plt.ylim(0, 1)
    plt.grid(True)
    plt.legend()
    plt.show()

fig.canvas.mpl_connect('button_press_event', onclick)
plt.tight_layout()
plt.show()