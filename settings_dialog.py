"""
设置对话框模块
包含系统设置对话框的类
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QComboBox, QCheckBox, QMessageBox,
                               QFileDialog, QLineEdit, QSpinBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon


class SettingsDialog(QDialog):
    """
    系统设置对话框类
    提供应用程序的各种设置选项
    """
    
    def __init__(self, parent=None):
        """
        初始化设置对话框
        
        Args:
            parent: 父窗口对象
        """
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setWindowIcon(QIcon("app.ico"))
        self.setGeometry(300, 300, 400, 500)
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
        
        # 添加设置项：保存路径
        save_path_label = QLabel("保存路径:")
        save_path_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(save_path_label)
        
        # 创建保存路径的横向布局
        path_layout = QHBoxLayout()
        
        self.save_path_edit = QLineEdit()
        self.save_path_edit.setPlaceholderText("选择保存路径...")
        self.save_path_edit.setText("./photos")  # 默认保存路径
        path_layout.addWidget(self.save_path_edit)
        
        browse_button = QPushButton("浏览...")
        browse_button.clicked.connect(self.browse_save_path)
        browse_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 15px;
                font-size: 11px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        path_layout.addWidget(browse_button)
        
        layout.addLayout(path_layout)
        
        # 添加设置项：摄像头1照片尺寸
        camera1_label = QLabel("摄像头1照片尺寸 (Camera 1 Photo Size):")
        camera1_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(camera1_label)
        
        # 创建摄像头1尺寸的横向布局
        camera1_size_layout = QHBoxLayout()
        
        width1_label = QLabel("宽度:")
        self.camera1_width_spin = QSpinBox()
        self.camera1_width_spin.setMinimum(320)
        self.camera1_width_spin.setMaximum(3840)
        self.camera1_width_spin.setValue(1920)
        self.camera1_width_spin.setSuffix(" px")
        camera1_size_layout.addWidget(width1_label)
        camera1_size_layout.addWidget(self.camera1_width_spin)
        
        height1_label = QLabel("  高度:")
        self.camera1_height_spin = QSpinBox()
        self.camera1_height_spin.setMinimum(240)
        self.camera1_height_spin.setMaximum(2160)
        self.camera1_height_spin.setValue(1080)
        self.camera1_height_spin.setSuffix(" px")
        camera1_size_layout.addWidget(height1_label)
        camera1_size_layout.addWidget(self.camera1_height_spin)
        
        layout.addLayout(camera1_size_layout)
        
        # 添加设置项：摄像头2照片尺寸
        camera2_label = QLabel("摄像头2照片尺寸 (Camera 2 Photo Size):")
        camera2_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(camera2_label)
        
        # 创建摄像头2尺寸的横向布局
        camera2_size_layout = QHBoxLayout()
        
        width2_label = QLabel("宽度:")
        self.camera2_width_spin = QSpinBox()
        self.camera2_width_spin.setMinimum(320)
        self.camera2_width_spin.setMaximum(3840)
        self.camera2_width_spin.setValue(1920)
        self.camera2_width_spin.setSuffix(" px")
        camera2_size_layout.addWidget(width2_label)
        camera2_size_layout.addWidget(self.camera2_width_spin)
        
        height2_label = QLabel("  高度:")
        self.camera2_height_spin = QSpinBox()
        self.camera2_height_spin.setMinimum(240)
        self.camera2_height_spin.setMaximum(2160)
        self.camera2_height_spin.setValue(1080)
        self.camera2_height_spin.setSuffix(" px")
        camera2_size_layout.addWidget(height2_label)
        camera2_size_layout.addWidget(self.camera2_height_spin)
        
        layout.addLayout(camera2_size_layout)
        
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
    
    def browse_save_path(self):
        """
        浏览并选择保存路径
        """
        selected_path = QFileDialog.getExistingDirectory(
            self,
            "选择保存路径",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if selected_path:
            self.save_path_edit.setText(selected_path)
    
    def save_settings(self):
        """
        保存设置
        获取所有设置的值并显示保存成功消息
        """
        # 获取所有设置的值
        theme = self.theme_combo.currentText()
        language = self.language_combo.currentText()
        auto_save = self.auto_save_checkbox.isChecked()
        save_path = self.save_path_edit.text().strip()
        camera1_width = self.camera1_width_spin.value()
        camera1_height = self.camera1_height_spin.value()
        camera2_width = self.camera2_width_spin.value()
        camera2_height = self.camera2_height_spin.value()
        auto_start = self.auto_start_checkbox.isChecked()
        show_tips = self.show_tips_checkbox.isChecked()
        
        # 验证保存路径
        if auto_save and not save_path:
            QMessageBox.warning(
                self,
                "路径为空",
                "请选择保存路径！"
            )
            return
        
        # 显示保存成功消息
        QMessageBox.information(
            self, 
            "设置已保存", 
            f"主题: {theme}\n"
            f"语言: {language}\n"
            f"自动保存: {'开启' if auto_save else '关闭'}\n"
            f"保存路径: {save_path}\n"
            f"摄像头1尺寸: {camera1_width} x {camera1_height}\n"
            f"摄像头2尺寸: {camera2_width} x {camera2_height}\n"
            f"开机启动: {'开启' if auto_start else '关闭'}\n"
            f"显示提示: {'开启' if show_tips else '关闭'}"
        )
        
        self.accept()
    
    def get_settings(self):
        """
        获取当前设置值
        
        Returns:
            dict: 包含所有设置的字典
        """
        return {
            'theme': self.theme_combo.currentText(),
            'language': self.language_combo.currentText(),
            'auto_save': self.auto_save_checkbox.isChecked(),
            'save_path': self.save_path_edit.text().strip(),
            'camera1_width': self.camera1_width_spin.value(),
            'camera1_height': self.camera1_height_spin.value(),
            'camera2_width': self.camera2_width_spin.value(),
            'camera2_height': self.camera2_height_spin.value(),
            'auto_start': self.auto_start_checkbox.isChecked(),
            'show_tips': self.show_tips_checkbox.isChecked()
        }
    
    def set_settings(self, settings):
        """
        设置对话框的值
        
        Args:
            settings: 包含设置的字典
        """
        if 'theme' in settings:
            index = self.theme_combo.findText(settings['theme'])
            if index >= 0:
                self.theme_combo.setCurrentIndex(index)
        
        if 'language' in settings:
            index = self.language_combo.findText(settings['language'])
            if index >= 0:
                self.language_combo.setCurrentIndex(index)
        
        if 'auto_save' in settings:
            self.auto_save_checkbox.setChecked(settings['auto_save'])
        
        if 'save_path' in settings:
            self.save_path_edit.setText(settings['save_path'])
        
        if 'camera1_width' in settings:
            self.camera1_width_spin.setValue(settings['camera1_width'])
        
        if 'camera1_height' in settings:
            self.camera1_height_spin.setValue(settings['camera1_height'])
        
        if 'camera2_width' in settings:
            self.camera2_width_spin.setValue(settings['camera2_width'])
        
        if 'camera2_height' in settings:
            self.camera2_height_spin.setValue(settings['camera2_height'])
        
        if 'auto_start' in settings:
            self.auto_start_checkbox.setChecked(settings['auto_start'])
        
        if 'show_tips' in settings:
            self.show_tips_checkbox.setChecked(settings['show_tips'])


if __name__ == "__main__":
    # 测试代码
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    dialog = SettingsDialog()
    dialog.show()
    sys.exit(app.exec())
