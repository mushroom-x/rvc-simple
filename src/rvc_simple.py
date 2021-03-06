'''
如本工业深度摄像头 Python SDK 简化版
@作者: 阿凯爱玩机器人
@微信: xingshunkai
@邮箱: xingshunkai@qq.com
@B站: https://space.bilibili.com/40344504
'''
import os
import yaml
import numpy as np
import cv2
import open3d as o3d
import PyRVC as RVC

class RVCSimple:
	'''如本深度摄像头-简化版Python SDK
	接口 : GigE 以太网接口
	颜色 : BGR 彩图 
	'''
	def __init__(self, config_path="config/default.yaml") -> None:
		# 加载配置文件
		# 载入配置文件
		with open(config_path, 'r', encoding='utf-8') as f:
			self.config = yaml.load(f.read(), Loader=yaml.SafeLoader)
		# 创建相机
		ret, self.cam = self.get_cam()
		if ret:
			# 配置相机参数
			self.opt = self.get_opt()
		else:
			exit(-1)
	
	def get_cam(self):
		'''获取设备'''
		# 系统初始化
		RVC.SystemInit()
		# 选择设备类型
		opt = RVC.SystemListDeviceTypeEnum.GigE
		# 扫描所有设备
		ret, devices = RVC.SystemListDevices(opt)
		print("RVC X GigE Camera devices number:%d" % len(devices))
		# 判断设备是否连接
		if len(devices) == 0:
			print("Can not find any RVC X GigE Camera!")
			RVC.SystemShutdown()
			return False, None
		print("devices size =%d" % len(devices))
		# 创建设备 使用双目
		cam = RVC.X2.Create(devices[0])
		# 测试设备是否正常
		if cam.IsValid() == True:
			print("RVC X Camera is valid!")
		else:
			print("RVC X Camera is not valid!")
			RVC.X2.Destroy(cam)
			RVC.SystemShutdown()
			return False, None
		# 打开设备
		ret1 = cam.Open()
		# 测试设备是否打开
		if ret1 and cam.IsOpen() == True:
			print("RVC X Camera is opened!")
		else:
			print("RVC X Camera is not opened!")
			RVC.X2.Destroy(cam)
			RVC.SystemShutdown()
			return False, None
		return True, cam
	
	def get_opt(self):
		# 设置相机参数
		cap_opt = RVC.X2_CaptureOptions()
		# 选择点云映射的坐标系
		# 选择转换到左侧相机坐标系
		cap_opt.transform_to_camera = RVC.CameraID_Left
		# 配置曝光时间 取值范围 (3~100) ms
		cap_opt.exposure_time_2d = self.config["exposure_time_2d"]
		cap_opt.exposure_time_3d = self.config["exposure_time_3d"]
		# 配置 增益
		cap_opt.gain_2d = self.config["gain_2d"]
		cap_opt.gain_3d = self.config["gain_3d"] 
		# 配置 Gamma
		cap_opt.gamma_2d = self.config["gamma_2d"]
		cap_opt.gamma_3d = self.config["gamma_3d"]
		# 光强对比度阈值
		cap_opt.light_contrast_threshold = self.config["light_contrast_threshold"]
		# 边缘去噪阈值, 取值范围 [0, 10]
		cap_opt.edge_noise_reduction_threshold = self.config["edge_noise_reduction_threshold"]
		# 配置投影的颜色为蓝色
		color_dict = {
			"red": RVC.ProjectorColor_Red,
			"green": RVC.ProjectorColor_Green, 
			"blue": RVC.ProjectorColor_Blue,
			"white": RVC.ProjectorColor_White
		}
		cap_opt.projector_color = color_dict[self.config["projector_color"]]
		return cap_opt
	
	def capture(self):
		'''拍摄图像'''
		self.cam.Capture(self.opt)
		# 获取左侧相机的BGR彩图
		img = np.array(self.cam.GetImage(RVC.CameraID_Left), copy=False)
		# 如果是灰度相机，为了保证接口统一
		# 将灰度图转换为BGR图
		if self.config["type"] == "gray":
			img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
		# 获取点云映射图
		pmap = np.array(self.cam.GetPointMap(), copy=False)
		return img, pmap
	
	def get_pcd(self, img, pmap, img_mask=None):
		'''将彩图与点云映射转换为PCD格式'''
		print(f"img shape:  {img.shape}")
		print(f"pmap shape: {pmap.shape}")
		if img_mask is None:
			h, w, _ = img.shape
			valid_pixel_index = np.bool8(np.ones((h, w)).reshape(-1))
		else:
			valid_pixel_index = (img_mask != 0).reshape(-1)
		# 将图像转换RGB色彩空间， 并将数值缩放到[0, 1]之间
		# 并转换为列向量
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).reshape(-1, 3) /255.0
		# 将点云映射转换为列向量
		pmap = pmap.reshape(-1, 3)
		# 有效点索引
		valid_pt_index = np.bitwise_and(~np.isnan(pmap[:, -1]), valid_pixel_index)
		# 获取有效点云与像素
		pmap_valid = pmap[valid_pt_index]
		img_valid = img[valid_pt_index] 
		# 创建pcd对象
		pcd = o3d.geometry.PointCloud()
		pcd.points = o3d.utility.Vector3dVector(pmap_valid)
		pcd.colors = o3d.utility.Vector3dVector(img_valid)
		return pcd
	
	def release(self):
		'''设备释放'''
		# Close RVC X Camera.
		self.cam.Close()
		# Destroy RVC X Camera.
		RVC.X2.Destroy(self.cam)
		# Shutdown RVC X System.
		RVC.SystemShutdown()