import json
import os
from abc import ABC, abstractmethod
from PyQt6.QtWidgets import QWidget

class BaseAlgorithm(ABC):
    def __init__(self, config_path):
        """
        :param config_path: 该算法专属的配置文件路径
        """
        self.config_path = config_path
        self.config = {}
        self.load_config()

    @abstractmethod
    def calculate_control(self, current_pos, current_step, trajectory_sequence):
        """
        [核心接口] 计算控制量
        :param current_pos: 当前物理坐标 (x, y) tuple
        :param current_step: 当前时间步 k (int)
        :param trajectory_sequence: 完整的参考轨迹列表 [(x0,y0), (x1,y1), ...]
        :return: 控制增量 (delta_x, delta_y) tuple
        """
        pass

    @abstractmethod
    def get_settings_widget(self) -> QWidget:
        """
        [核心接口] 获取参数设置界面
        算法模块需要在这里构建自己的 QWidget，并在内部处理 UI 交互和配置更新
        :return: QWidget 实例
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """返回算法名称"""
        pass

    @abstractmethod
    def reset(self):
        """
        [核心接口] 重置内部状态
        在每次开始追踪前被调用，用于清空积分项、历史误差等
        """
        pass

    def load_config(self):
        """通用加载逻辑"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"[{self.get_name()}] 配置加载失败: {e}")
        else:
            self.save_config() # 如果不存在，保存默认值

    def save_config(self):
        """通用保存逻辑"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            print(f"[{self.get_name()}] 配置已保存")
        except Exception as e:
            print(f"[{self.get_name()}] 配置保存失败: {e}")