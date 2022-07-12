'''
点云动态刷新窗口
----------------------------------------------
@作者: 阿凯爱玩机器人
@QQ: 244561792
@微信: xingshunkai
@邮箱: xingshunkai@qq.com
@B站: https://space.bilibili.com/40344504
'''
import copy
import numpy as np
import open3d as o3d

class PCDVisualizer():
    '''点云可视化窗口'''
    def __init__(self, window_name="PCD") -> None:
        # 窗口名字
        self.window_name = window_name
        # 可视化窗口
        self.visualizer = o3d.visualization.Visualizer()
        # 点云数据
        self.pcd = o3d.geometry.PointCloud()
        # 是否添加了Geometry
        self.add_geomery = False
    
    def create_window(self):
        '''创建窗口'''
        # 创建窗口
        self.visualizer.create_window(self.window_name, width=1280, height=720)
    
    def destroy_window(self):
        '''销毁窗口'''
        self.visualizer.destroy_window()
    
    def reset_pcd(self):
        '''重置点云数据'''
        self.pcd.clear()
    
    def update_pcd(self, pcd, is_reset=True):
        '''更新点云数据'''
        if is_reset:
            self.reset_pcd()
        # 添加新的PCD
        self.pcd += copy.deepcopy(pcd)
        if not self.add_geomery:
            self.visualizer.add_geometry(self.pcd)
            self.add_geomery = True
        # 可视化窗口更新
        self.visualizer.update_geometry(self.pcd)
    
    def step(self):
        '''更新一步'''
        # 接收事件
        self.visualizer.poll_events()
        # 渲染器需要更新
        self.visualizer.update_renderer()