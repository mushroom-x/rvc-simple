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
# 保存点云映射
np.savetxt("./data/test.xyz".format(), pmap.reshape(-1, 3))
# 保存PCD点云
o3d.io.write_point_cloud("./data/test.pcd", pcd)

# Open3D点云可视化
o3d.visualization.draw_geometries([pcd])

# 释放设备
rvc.release()