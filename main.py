import sys
import cv2
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                               QLabel, QPushButton, QLineEdit, QMessageBox, 
                               QSpinBox, QFileDialog, QDialog, QHBoxLayout,
                               QComboBox, QCheckBox, QMenuBar, QMenu, QToolButton)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QImage, QPixmap, QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("工程摄像拍照")
        self.setGeometry(100, 100, 400, 300)
        
        # 设置窗口图标
        self.setWindowIcon(QIcon("app.ico"))
        
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
        modules_menu.addAction("摄像头控制")
        modules_menu.addAction("计算器")
        modules_menu.addAction("问候功能")
        
        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建布局
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        # 创建输入框
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("请输入您的名字")
        self.layout.addWidget(self.name_input)
        
        # 创建问候按钮
        self.greet_button = QPushButton("点击问候")
        self.greet_button.clicked.connect(self.on_greet_clicked)
        self.greet_button.setStyleSheet("""
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
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.layout.addWidget(self.greet_button)
        
        # 创建标签显示问候语
        self.greeting_label = QLabel("")
        self.greeting_label.setAlignment(Qt.AlignCenter)
        self.greeting_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.greeting_label)
        
        # 创建跳转到第二个界面的按钮
        self.switch_button = QPushButton("进入界面二")
        self.switch_button.clicked.connect(self.open_second_window)
        self.switch_button.setStyleSheet("""
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
            QPushButton:pressed {
                background-color: #0a5bb5;
            }
        """)
        self.layout.addWidget(self.switch_button)
        
        # 添加弹性空间
        self.layout.addStretch()
        
        # 状态栏
        self.statusBar().showMessage("界面一 - 就绪")
        
        # 第二个窗口的引用
        self.second_window = None
    
    def show_menu(self):
        # 获取菜单按钮的全局位置
        button_rect = self.menu_button.rect()
        button_pos = self.menu_button.mapToGlobal(button_rect.bottomLeft())
        
        # 显示菜单在按钮下方
        self.menu.exec(button_pos)
    
    def on_greet_clicked(self):
        name = self.name_input.text()
        if name.strip():
            self.greeting_label.setText(f"你好, {name}!")
            self.statusBar().showMessage(f"已问候: {name}")
        else:
            QMessageBox.warning(self, "提示", "请先输入您的名字!")
            self.statusBar().showMessage("等待输入...")
    
    def open_second_window(self):
        if self.second_window is None:
            self.second_window = SecondWindow(self)
        self.hide()
        self.second_window.show()
    
    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()
    
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, '确认退出',
            '确定要退出程序吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
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


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setWindowIcon(QIcon("app.ico"))
        self.setGeometry(300, 300, 400, 350)
        self.setModal(True)
        
        # 创建主布局
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 创建标题
        title_label = QLabel("系统设置")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 添加分隔线
        separator = QLabel()
        separator.setFrameStyle(QLabel.HLine | QLabel.Sunken)
        layout.addWidget(separator)
        
        # 添加设置项：界面主题
        theme_label = QLabel("界面主题:")
        theme_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(theme_label)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["浅色主题", "深色主题", "系统默认"])
        layout.addWidget(self.theme_combo)
        
        # 添加设置项：语言
        language_label = QLabel("语言 / Language:")
        language_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(language_label)
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(["简体中文", "English"])
        layout.addWidget(self.language_combo)
        
        # 添加设置项：自动保存
        self.auto_save_checkbox = QCheckBox("自动保存照片")
        self.auto_save_checkbox.setChecked(True)
        layout.addWidget(self.auto_save_checkbox)
        
        # 添加设置项：开机启动
        self.auto_start_checkbox = QCheckBox("开机启动应用")
        self.auto_start_checkbox.setChecked(False)
        layout.addWidget(self.auto_start_checkbox)
        
        # 添加设置项：显示提示
        self.show_tips_checkbox = QCheckBox("显示操作提示")
        self.show_tips_checkbox.setChecked(True)
        layout.addWidget(self.show_tips_checkbox)
        
        # 添加弹性空间
        layout.addStretch()
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        # 创建保存按钮
        save_button = QPushButton("保存")
        save_button.clicked.connect(self.save_settings)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 30px;
                font-size: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        button_layout.addWidget(save_button)
        
        # 创建取消按钮
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px 30px;
                font-size: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        button_layout.addWidget(cancel_button)
    
    def save_settings(self):
        # 这里可以添加保存设置的逻辑
        theme = self.theme_combo.currentText()
        language = self.language_combo.currentText()
        auto_save = self.auto_save_checkbox.isChecked()
        auto_start = self.auto_start_checkbox.isChecked()
        show_tips = self.show_tips_checkbox.isChecked()
        
        # 显示保存成功消息
        QMessageBox.information(
            self, 
            "设置已保存", 
            f"主题: {theme}\n"
            f"语言: {language}\n"
            f"自动保存: {'开启' if auto_save else '关闭'}\n"
            f"开机启动: {'开启' if auto_start else '关闭'}\n"
            f"显示提示: {'开启' if show_tips else '关闭'}"
        )
        
        self.accept()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
