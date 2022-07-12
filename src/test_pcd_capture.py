'''
如本工业深度摄像头Open3D示例
- 读取图像与点云映射， 并转换为open3d的pcd格式
@作者: 阿凯爱玩机器人
@微信: xingshunkai
@邮箱: xingshunkai@qq.com
@B站: https://space.bilibili.com/40344504
'''
import numpy as np
import cv2
import open3d as o3d
from rvc_simple import RVCSimple

# 相机的配置文件 YAML格式
# 根据不同的工件特性，设置不同的参数
# 默认配置为RVC-X Mini彩色相机的配置文件
# 需要根据RVCManager调整相机参数，并保存到YAML配置文件中
config_path = "config/default.yaml"
# 创建设备
rvc = RVCSimple(config_path=config_path)
# 获取图像与点云映射
img, pmap = rvc.capture()
# 获取PCD点云
pcd = rvc.get_pcd(img, pmap)

# 保存2D图像
cv2.imwrite("./data/test.png", img)
# 保存点云映射 单位m
np.savetxt("./data/test.xyz", pmap.reshape(-1, 3), delimiter=",", fmt="%.4f")
# 保存PCD点云
o3d.io.write_point_cloud("./data/test.pcd", pcd)

# Open3D点云可视化
o3d.visualization.draw_geometries([pcd])

# 释放设备
rvc.release()