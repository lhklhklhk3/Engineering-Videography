"""
配置管理模块
处理应用程序配置的加载和保存
"""

import json
import os
from pathlib import Path


class ConfigManager:
    """
    配置管理器类
    负责配置文件的读取、写入和管理
    """
    
    def __init__(self, config_file="config.json"):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件名（默认为 config.json）
        """
        self.config_file = config_file
        self.default_config = {
            'theme': '浅色主题',
            'language': '简体中文',
            'auto_save': True,
            'save_path': './photos',
            'camera1_width': 1920,
            'camera1_height': 1080,
            'camera2_width': 1920,
            'camera2_height': 1080,
            'auto_start': False,
            'show_tips': True
        }
        self.config = self.load_config()
    
    def get_config_path(self):
        """
        获取配置文件的完整路径
        
        Returns:
            str: 配置文件的完整路径
        """
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), self.config_file)
    
    def load_config(self):
        """
        从文件加载配置
        
        Returns:
            dict: 配置字典
        """
        config_path = self.get_config_path()
        
        # 如果配置文件不存在，返回默认配置
        if not os.path.exists(config_path):
            print(f"配置文件不存在: {config_path}")
            print("使用默认配置")
            return self.default_config.copy()
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                print(f"配置加载成功: {config_path}")
                return config
        except json.JSONDecodeError as e:
            print(f"配置文件格式错误: {e}")
            print("使用默认配置")
            return self.default_config.copy()
        except Exception as e:
            print(f"加载配置失败: {e}")
            print("使用默认配置")
            return self.default_config.copy()
    
    def save_config(self, config=None):
        """
        保存配置到文件
        
        Args:
            config: 要保存的配置字典，如果为None则保存当前配置
        
        Returns:
            bool: 保存成功返回True，失败返回False
        """
        if config is None:
            config = self.config
        
        config_path = self.get_config_path()
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            print(f"配置保存成功: {config_path}")
            self.config = config
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False
    
    def get(self, key, default=None):
        """
        获取配置项
        
        Args:
            key: 配置键
            default: 默认值
        
        Returns:
            配置值或默认值
        """
        return self.config.get(key, default)
    
    def set(self, key, value):
        """
        设置配置项
        
        Args:
            key: 配置键
            value: 配置值
        """
        self.config[key] = value
    
    def update(self, new_config):
        """
        更新配置
        
        Args:
            new_config: 新的配置字典
        """
        self.config.update(new_config)
    
    def reset_to_default(self):
        """
        重置为默认配置
        """
        self.config = self.default_config.copy()
    
    def delete_config_file(self):
        """
        删除配置文件
        
        Returns:
            bool: 删除成功返回True，失败返回False
        """
        config_path = self.get_config_path()
        
        if os.path.exists(config_path):
            try:
                os.remove(config_path)
                print(f"配置文件已删除: {config_path}")
                return True
            except Exception as e:
                print(f"删除配置文件失败: {e}")
                return False
        else:
            print("配置文件不存在")
            return False


# 全局配置管理器实例
config_manager = ConfigManager()


if __name__ == "__main__":
    # 测试代码
    print("=== 配置管理器测试 ===\n")
    
    # 创建配置管理器
    cm = ConfigManager("test_config.json")
    
    # 测试加载配置
    print("1. 加载配置:")
    print(f"   当前配置: {cm.config}\n")
    
    # 测试修改配置
    print("2. 修改配置:")
    cm.set('theme', '深色主题')
    cm.set('language', 'English')
    cm.config['camera1_width'] = 2560
    print(f"   修改后: {cm.config}\n")
    
    # 测试保存配置
    print("3. 保存配置:")
    success = cm.save_config()
    print(f"   保存结果: {success}\n")
    
    # 测试重新加载
    print("4. 重新加载配置:")
    cm2 = ConfigManager("test_config.json")
    print(f"   加载结果: {cm2.config}\n")
    
    # 清理测试文件
    cm.delete_config_file()
    print("5. 清理测试文件完成")
