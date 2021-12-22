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

# 创建设备
rvc = RVCSimple()
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