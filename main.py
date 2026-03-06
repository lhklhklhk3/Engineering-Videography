import sys
import cv2
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                               QLabel, QPushButton, QLineEdit, QMessageBox, 
                               QSpinBox, QFileDialog, QHBoxLayout,
                               QMenuBar, QMenu)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QImage, QPixmap, QIcon
from settings_dialog import SettingsDialog
from config_manager import config_manager



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("工程摄像拍照")
        self.setGeometry(100, 100, 1400, 900)

        # 设置窗口图标
        self.setWindowIcon(QIcon("app.ico"))

        # 摄像头相关
        self.cap1 = None
        self.cap2 = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frames)

        # 索引编号
        self.photo_index = 0

        # 摄像头状态
        self.camera1_enabled = False
        self.camera2_enabled = False
        self.camera1_error = False
        self.camera2_error = False

        # 应用配置
        self.apply_config()

        # 创建菜单栏
        self.menubar = self.menuBar()

        # 创建菜单按钮作为corner widget
        self.menu_button = QPushButton("菜单 ▼")
        self.menu_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #999;
                border-radius: 4px;
                padding: 5px 15px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #c0c0c0;
            }
        """)
        self.menu_button.clicked.connect(self.show_menu)

        # 将菜单按钮设置为菜单栏的右角widget
        self.menubar.setCornerWidget(self.menu_button, Qt.TopRightCorner)

        # 创建菜单
        self.menu = QMenu(self)

        # 添加"系统设置"菜单项
        settings_action = self.menu.addAction("系统设置")
        settings_action.triggered.connect(self.open_settings)

        # 添加分隔符
        self.menu.addSeparator()

        # 添加"功能模块"子菜单
        modules_menu = self.menu.addMenu("功能模块")
        modules_menu.addAction("计算器")
        modules_menu.addAction("问候功能")

        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建主布局
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # 创建标题标签
        self.title_label = QLabel("双摄像头捕获系统")
        self.title_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        # 创建索引显示
        self.index_label = QLabel(f"当前索引: {self.photo_index}")
        self.index_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.index_label.setAlignment(Qt.AlignCenter)
        self.index_label.setStyleSheet("color: #2196F3; padding: 10px;")
        self.main_layout.addWidget(self.index_label)

        # 创建摄像头显示区域的横向布局
        self.camera_layout = QHBoxLayout()
        self.main_layout.addLayout(self.camera_layout)

        # 创建摄像头1显示区域
        self.camera1_container = self.create_camera_container("摄像头 1")
        self.camera_layout.addLayout(self.camera1_container)

        # 创建摄像头2显示区域
        self.camera2_container = self.create_camera_container("摄像头 2")
        self.camera_layout.addLayout(self.camera2_container)

        # 创建控制按钮布局
        self.control_layout = QHBoxLayout()
        self.main_layout.addLayout(self.control_layout)

        # 创建打开摄像头按钮
        self.open_camera_button = QPushButton("打开摄像头")
        self.open_camera_button.clicked.connect(self.open_cameras)
        self.open_camera_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 30px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.control_layout.addWidget(self.open_camera_button)

        # 创建关闭摄像头按钮
        self.close_camera_button = QPushButton("关闭摄像头")
        self.close_camera_button.clicked.connect(self.close_cameras)
        self.close_camera_button.setEnabled(False)
        self.close_camera_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 12px 30px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #b71c1c;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.control_layout.addWidget(self.close_camera_button)

        # 创建捕获按钮
        self.capture_button = QPushButton("捕获照片")
        self.capture_button.clicked.connect(self.capture_photos)
        self.capture_button.setEnabled(False)
        self.capture_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 12px 30px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.control_layout.addWidget(self.capture_button)

        # 状态栏
        self.statusBar().showMessage("就绪 - 请打开摄像头")

    def create_camera_container(self, title):
        """创建摄像头显示容器"""
        layout = QVBoxLayout()

        # 标题
        label = QLabel(title)
        label.setFont(QFont("Arial", 12, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # 视频显示
        video_label = QLabel("摄像头未开启")
        video_label.setAlignment(Qt.AlignCenter)
        video_label.setMinimumSize(600, 450)
        video_label.setStyleSheet("""
            QLabel {
                border: 3px solid #666;
                background-color: #333;
                color: #fff;
                font-size: 14px;
            }
        """)
        layout.addWidget(video_label)

        # 状态标签
        status_label = QLabel("状态: 未连接")
        status_label.setFont(QFont("Arial", 10))
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(status_label)

        return layout
    
    def show_menu(self):
        # 获取菜单按钮的全局位置
        button_rect = self.menu_button.rect()
        button_pos = self.menu_button.mapToGlobal(button_rect.bottomLeft())

        # 显示菜单在按钮下方
        self.menu.exec(button_pos)

    def get_camera1_label(self):
        """获取摄像头1的视频显示标签"""
        return self.camera1_container.itemAt(1).widget()

    def get_camera2_label(self):
        """获取摄像头2的视频显示标签"""
        return self.camera2_container.itemAt(1).widget()

    def get_camera1_status_label(self):
        """获取摄像头1的状态标签"""
        return self.camera1_container.itemAt(2).widget()

    def get_camera2_status_label(self):
        """获取摄像头2的状态标签"""
        return self.camera2_container.itemAt(2).widget()

    def open_cameras(self):
        """打开两个摄像头"""
        self.camera1_error = False
        self.camera2_error = False

        # 打开摄像头1
        try:
            self.cap1 = cv2.VideoCapture(0)
            if self.cap1.isOpened():
                self.camera1_enabled = True
                self.get_camera1_label().setText("摄像头1 已开启")
                self.get_camera1_status_label().setText("状态: 运行中")
                self.get_camera1_status_label().setStyleSheet("color: #4CAF50; padding: 5px;")
            else:
                raise Exception("无法打开摄像头1")
        except Exception as e:
            self.camera1_error = True
            self.camera1_enabled = False
            self.get_camera1_label().setText("摄像头1 错误")
            self.get_camera1_status_label().setText(f"状态: {str(e)}")
            self.get_camera1_status_label().setStyleSheet("color: #f44336; padding: 5px;")
            QMessageBox.warning(self, "错误", f"无法打开摄像头1: {str(e)}")

        # 打开摄像头2
        try:
            self.cap2 = cv2.VideoCapture(1)
            if self.cap2.isOpened():
                self.camera2_enabled = True
                self.get_camera2_label().setText("摄像头2 已开启")
                self.get_camera2_status_label().setText("状态: 运行中")
                self.get_camera2_status_label().setStyleSheet("color: #4CAF50; padding: 5px;")
            else:
                raise Exception("无法打开摄像头2")
        except Exception as e:
            self.camera2_error = True
            self.camera2_enabled = False
            self.get_camera2_label().setText("摄像头2 错误")
            self.get_camera2_status_label().setText(f"状态: {str(e)}")
            self.get_camera2_status_label().setStyleSheet("color: #f44336; padding: 5px;")
            QMessageBox.warning(self, "错误", f"无法打开摄像头2: {str(e)}")

        # 检查是否有至少一个摄像头可用
        if self.camera1_enabled or self.camera2_enabled:
            self.timer.start(30)  # 30ms更新一次
            self.open_camera_button.setEnabled(False)
            self.close_camera_button.setEnabled(True)
            self.capture_button.setEnabled(True)

            # 更新状态栏
            status_parts = []
            if self.camera1_enabled:
                status_parts.append("摄像头1: 运行")
            if self.camera2_enabled:
                status_parts.append("摄像头2: 运行")
            if self.camera1_error:
                status_parts.append("摄像头1: 错误")
            if self.camera2_error:
                status_parts.append("摄像头2: 错误")

            self.statusBar().showMessage(" | ".join(status_parts))
        else:
            self.statusBar().showMessage("错误: 两个摄像头都无法打开")
            self.open_camera_button.setEnabled(True)
            self.close_camera_button.setEnabled(False)
            self.capture_button.setEnabled(False)

    def close_cameras(self):
        """关闭两个摄像头"""
        self.timer.stop()

        # 关闭摄像头1
        if self.cap1 is not None and self.cap1.isOpened():
            self.cap1.release()
            self.cap1 = None
        self.camera1_enabled = False
        self.get_camera1_label().setText("摄像头未开启")
        self.get_camera1_status_label().setText("状态: 未连接")
        self.get_camera1_status_label().setStyleSheet("color: #666; padding: 5px;")
        self.get_camera1_label().clear()

        # 关闭摄像头2
        if self.cap2 is not None and self.cap2.isOpened():
            self.cap2.release()
            self.cap2 = None
        self.camera2_enabled = False
        self.get_camera2_label().setText("摄像头未开启")
        self.get_camera2_status_label().setText("状态: 未连接")
        self.get_camera2_status_label().setStyleSheet("color: #666; padding: 5px;")
        self.get_camera2_label().clear()

        self.open_camera_button.setEnabled(True)
        self.close_camera_button.setEnabled(False)
        self.capture_button.setEnabled(False)
        self.statusBar().showMessage("摄像头已关闭")

    def update_frames(self):
        """更新两个摄像头的帧"""
        # 更新摄像头1
        if self.cap1 is not None and self.cap1.isOpened():
            ret, frame = self.cap1.read()
            if ret:
                # 将OpenCV图像转换为QImage
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

                # 调整图像大小以适应标签
                scaled_pixmap = QPixmap.fromImage(qt_image).scaled(
                    self.get_camera1_label().size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )

                self.get_camera1_label().setPixmap(scaled_pixmap)
            else:
                self.camera1_error = True
                self.get_camera1_status_label().setText("状态: 无法读取帧")
                self.get_camera1_status_label().setStyleSheet("color: #f44336; padding: 5px;")

        # 更新摄像头2
        if self.cap2 is not None and self.cap2.isOpened():
            ret, frame = self.cap2.read()
            if ret:
                # 将OpenCV图像转换为QImage
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

                # 调整图像大小以适应标签
                scaled_pixmap = QPixmap.fromImage(qt_image).scaled(
                    self.get_camera2_label().size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )

                self.get_camera2_label().setPixmap(scaled_pixmap)
            else:
                self.camera2_error = True
                self.get_camera2_status_label().setText("状态: 无法读取帧")
                self.get_camera2_status_label().setStyleSheet("color: #f44336; padding: 5px;")

    def capture_photos(self):
        """捕获两个摄像头的照片"""
        captured_count = 0
        save_path = config_manager.get('save_path', './photos')

        # 确保保存路径存在
        import os
        os.makedirs(save_path, exist_ok=True)

        # 捕获摄像头1
        if self.cap1 is not None and self.cap1.isOpened() and not self.camera1_error:
            try:
                ret, frame = self.cap1.read()
                if ret:
                    filename = f"{save_path}/camera1_{self.photo_index:04d}.jpg"
                    cv2.imwrite(filename, frame)
                    captured_count += 1
                    self.statusBar().showMessage(f"已捕获摄像头1照片: {filename}")
                else:
                    QMessageBox.warning(self, "警告", "摄像头1 无法捕获图像")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"捕获摄像头1照片失败: {str(e)}")
        else:
            if self.camera1_error:
                QMessageBox.warning(self, "警告", "摄像头1 处于错误状态，无法捕获")

        # 捕获摄像头2
        if self.cap2 is not None and self.cap2.isOpened() and not self.camera2_error:
            try:
                ret, frame = self.cap2.read()
                if ret:
                    filename = f"{save_path}/camera2_{self.photo_index:04d}.jpg"
                    cv2.imwrite(filename, frame)
                    captured_count += 1
                    self.statusBar().showMessage(f"已捕获摄像头2照片: {filename}")
                else:
                    QMessageBox.warning(self, "警告", "摄像头2 无法捕获图像")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"捕获摄像头2照片失败: {str(e)}")
        else:
            if self.camera2_error:
                QMessageBox.warning(self, "警告", "摄像头2 处于错误状态，无法捕获")

        # 更新索引
        if captured_count > 0:
            self.photo_index += 1
            self.index_label.setText(f"当前索引: {self.photo_index}")

            # 显示成功消息
            if captured_count == 2:
                QMessageBox.information(self, "成功",
                    f"成功捕获 2 张照片\n索引: {self.photo_index - 1}\n保存路径: {save_path}")
            else:
                QMessageBox.information(self, "成功",
                    f"成功捕获 {captured_count} 张照片\n索引: {self.photo_index - 1}\n保存路径: {save_path}")
        else:
            QMessageBox.warning(self, "错误", "没有捕获任何照片")

    def open_settings(self):
        dialog = SettingsDialog(self)
        result = dialog.exec()

        # 如果用户保存了设置（返回 QDialog.Accepted）
        if result == dialog.DialogCode.Accepted:
            # 重新加载配置
            config_manager.load_config()
            print("-" * 50)
            print("设置已更新并重新加载")
            print(f"更新后的配置: {config_manager.config}")
            print(f"配置文件: {config_manager.get_config_path()}")
            print("-" * 50)

            # 应用配置到应用程序
            self.apply_config()

    def apply_config(self):
        """
        应用配置到应用程序
        根据配置更新应用程序的各项设置
        """
        config = config_manager.config

        print("-" * 50)
        print("应用配置到应用程序")
        print(f"当前配置: {config}")
        print("-" * 50)

        # 应用主题设置（暂时只是打印，可以根据实际需求实现）
        if 'theme' in config:
            print(f"主题设置为: {config['theme']}")

        # 应用语言设置（暂时只是打印，可以根据实际需求实现）
        if 'language' in config:
            print(f"语言设置为: {config['language']}")

        # 其他配置可以根据需要在这里应用

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, '确认退出',
            '确定要退出程序吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            # 关闭所有摄像头
            self.close_cameras()
            event.accept()
        else:
            event.ignore()


class SecondWindow(QMainWindow):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("工程摄像拍照")
        self.setGeometry(150, 150, 400, 300)
        
        # 设置窗口图标
        self.setWindowIcon(QIcon("app.ico"))
        
        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建布局
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        # 创建标题标签
        self.title_label = QLabel("计算器功能")
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)
        
        # 创建数字输入框
        self.num1_input = QSpinBox()
        self.num1_input.setRange(-1000, 1000)
        self.num1_input.setPrefix("数字1: ")
        self.layout.addWidget(self.num1_input)
        
        self.num2_input = QSpinBox()
        self.num2_input.setRange(-1000, 1000)
        self.num2_input.setPrefix("数字2: ")
        self.layout.addWidget(self.num2_input)
        
        # 创建计算按钮
        self.add_button = QPushButton("加法")
        self.add_button.clicked.connect(lambda: self.calculate("+"))
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                padding: 8px;
                font-size: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7b1fa2;
            }
        """)
        self.layout.addWidget(self.add_button)
        
        self.sub_button = QPushButton("减法")
        self.sub_button.clicked.connect(lambda: self.calculate("-"))
        self.sub_button.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                padding: 8px;
                font-size: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7b1fa2;
            }
        """)
        self.layout.addWidget(self.sub_button)
        
        # 创建结果显示标签
        self.result_label = QLabel("结果: ")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.layout.addWidget(self.result_label)
        
        # 创建返回按钮
        self.back_button = QPushButton("返回界面一")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
            QPushButton:pressed {
                background-color: #cc7a00;
            }
        """)
        self.layout.addWidget(self.back_button)
        
        # 创建跳转到摄像头界面的按钮
        self.camera_button = QPushButton("打开摄像头")
        self.camera_button.clicked.connect(self.open_camera_window)
        self.camera_button.setStyleSheet("""
            QPushButton {
                background-color: #E91E63;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c2185b;
            }
            QPushButton:pressed {
                background-color: #ad1457;
            }
        """)
        self.layout.addWidget(self.camera_button)
        
        # 添加弹性空间
        self.layout.addStretch()
        
        # 状态栏
        self.statusBar().showMessage("界面二 - 就绪")
        
        # 摄像头窗口的引用
        self.camera_window = None
    
    def calculate(self, operation):
        num1 = self.num1_input.value()
        num2 = self.num2_input.value()
        
        if operation == "+":
            result = num1 + num2
            self.result_label.setText(f"结果: {num1} + {num2} = {result}")
            self.statusBar().showMessage(f"加法: {num1} + {num2} = {result}")
        elif operation == "-":
            result = num1 - num2
            self.result_label.setText(f"结果: {num1} - {num2} = {result}")
            self.statusBar().showMessage(f"减法: {num1} - {num2} = {result}")
    
    def go_back(self):
        self.hide()
        if self.parent_window:
            self.parent_window.show()
    
    def open_camera_window(self):
        if self.camera_window is None:
            self.camera_window = CameraWindow(self)
        self.hide()
        self.camera_window.show()
    
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, '确认关闭',
            '确定要关闭此界面吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class CameraWindow(QMainWindow):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("工程摄像拍照")
        self.setGeometry(200, 200, 640, 520)
        
        # 设置窗口图标
        self.setWindowIcon(QIcon("app.ico"))
        
        # 摄像头相关
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        
        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建布局
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        # 创建标题标签
        self.title_label = QLabel("摄像头控制界面")
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)
        
        # 创建视频显示标签
        self.video_label = QLabel("摄像头未开启")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumSize(640, 480)
        self.video_label.setStyleSheet("""
            QLabel {
                border: 2px solid #666;
                background-color: #333;
                color: #fff;
            }
        """)
        self.layout.addWidget(self.video_label)
        
        # 创建按钮布局
        self.button_layout = QVBoxLayout()
        self.layout.addLayout(self.button_layout)
        
        # 创建控制按钮
        self.open_button = QPushButton("打开摄像头")
        self.open_button.clicked.connect(self.open_camera)
        self.open_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.button_layout.addWidget(self.open_button)
        
        self.close_button = QPushButton("关闭摄像头")
        self.close_button.clicked.connect(self.close_camera)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        self.close_button.setEnabled(False)
        self.button_layout.addWidget(self.close_button)
        
        self.capture_button = QPushButton("拍照保存")
        self.capture_button.clicked.connect(self.capture_photo)
        self.capture_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        self.capture_button.setEnabled(False)
        self.button_layout.addWidget(self.capture_button)
        
        # 创建返回按钮
        self.back_button = QPushButton("返回")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
            QPushButton:pressed {
                background-color: #cc7a00;
            }
        """)
        self.layout.addWidget(self.back_button)
        
        # 状态栏
        self.statusBar().showMessage("摄像头控制 - 就绪")
    
    def open_camera(self):
        try:
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                self.timer.start(30)  # 30ms更新一次
                self.video_label.setText("摄像头已开启")
                self.open_button.setEnabled(False)
                self.close_button.setEnabled(True)
                self.capture_button.setEnabled(True)
                self.statusBar().showMessage("摄像头已开启")
            else:
                QMessageBox.warning(self, "错误", "无法打开摄像头!")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"打开摄像头失败: {str(e)}")
    
    def close_camera(self):
        if self.cap is not None and self.cap.isOpened():
            self.timer.stop()
            self.cap.release()
            self.cap = None
            self.video_label.setText("摄像头未开启")
            self.video_label.clear()
            self.open_button.setEnabled(True)
            self.close_button.setEnabled(False)
            self.capture_button.setEnabled(False)
            self.statusBar().showMessage("摄像头已关闭")
    
    def update_frame(self):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # 将OpenCV图像转换为QImage
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                
                # 调整图像大小以适应标签
                scaled_pixmap = QPixmap.fromImage(qt_image).scaled(
                    self.video_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                
                self.video_label.setPixmap(scaled_pixmap)
    
    def capture_photo(self):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # 保存图片
                options = QFileDialog.Options()
                file_path, _ = QFileDialog.getSaveFileName(
                    self, "保存照片", "", 
                    "JPEG Image (*.jpg);;PNG Image (*.png)",
                    options=options
                )
                
                if file_path:
                    cv2.imwrite(file_path, frame)
                    QMessageBox.information(self, "成功", f"照片已保存到: {file_path}")
                    self.statusBar().showMessage(f"照片已保存: {file_path}")
            else:
                QMessageBox.warning(self, "错误", "无法捕获图像!")
    
    def go_back(self):
        # 关闭摄像头
        if self.cap is not None and self.cap.isOpened():
            self.close_camera()
        self.hide()
        if self.parent_window:
            self.parent_window.show()
    
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, '确认关闭',
            '确定要关闭此界面吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            # 窗口关闭时自动关闭摄像头
            if self.cap is not None and self.cap.isOpened():
                self.close_camera()
            event.accept()
        else:
            event.ignore()



def main():
    app = QApplication(sys.argv)
    
    # 应用启动时加载配置
    config_path = config_manager.get_config_path()
    print(f"应用程序启动")
    print(f"配置文件路径: {config_path}")
    print(f"当前配置: {config_manager.config}")
    print("-" * 50)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
