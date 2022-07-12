'''
PCD点云动态可视化
从RVC 3D相机动态读取图片与点云, 
并动态的在Open3D的窗口中刷新点云。
----------------------------------------------
@作者: 阿凯爱玩机器人
@QQ: 244561792
@微信: xingshunkai
@邮箱: xingshunkai@qq.com
@B站: https://space.bilibili.com/40344504
'''
import numpy as np
import cv2
import open3d as o3d
import time
import threading
# 自定义库
from rvc_simple import RVCSimple
from pcd_visualizer import PCDVisualizer

# 相机的配置文件 YAML格式
# 根据不同的工件特性，设置不同的参数
# 默认配置为RVC-X Mini彩色相机的配置文件
# 需要根据RVCManager调整相机参数，并保存到YAML配置文件中
config_path = "config/default.yaml"
# 创建设备
rvc = RVCSimple(config_path=config_path)

# 创建可视化窗口
visualizer = PCDVisualizer()
visualizer.create_window()

img = None 	# 彩图
pmap = None # 点云映射
pcd = None 	# PCD点云
is_pcd_update = False
stop_flag = False

def capture_image():
	'''定义图像采集线程函数'''
	global img, pmap, pcd
	global is_pcd_update
	global stop_flag
	while True:
		# 退出程序
		if stop_flag:
			break
		# 获取图像与点云映射
		img, pmap = rvc.capture()
		# 获取PCD点云
		pcd = rvc.get_pcd(img, pmap)
		is_pcd_update = True
		print("获取PCD点云")
		# 延时一段时间
		time.sleep(1.0)

# 创建获取图像线程
capture_image_thread = threading.Thread(target=capture_image, \
	name='capture_image_thread')

# 开启线程
capture_image_thread.start()
try:
	while True:
		# 更新PCD点云
		if is_pcd_update:
			# 重置标志位
			is_pcd_update = False
			print("更新PCD点云")
			visualizer.update_pcd(pcd)
		# 可视化器迭代
		visualizer.step()
except KeyboardInterrupt as e:
	print("程序终止")
	stop_flag = True
	# 等待线程结束
	capture_image_thread.join()
	# 关闭窗口
	visualizer.destroy_window()
	# 释放相机
	rvc.release()