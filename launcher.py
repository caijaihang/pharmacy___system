"""
药房进货比较系统 - 桌面启动器
将 Flask 后端 + PyQt5 WebEngine 前端整合为桌面应用
打包后无需 Python 环境、无需浏览器，双击 EXE 即可运行
"""
import sys
import os
import threading
import time
import socket

# ============================================================
# 路径处理：兼容 PyInstaller 打包后的资源路径
# ============================================================
def get_base_path():
    """获取应用根目录（兼容开发环境和打包后的环境）"""
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后，_MEIPASS 是临时解压目录
        # 可执行文件所在目录用于存放数据库等可写文件
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()

def get_resource_path(relative_path):
    """获取资源文件绝对路径（打包后的资源在 _MEIPASS 内）"""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(BASE_PATH, relative_path)

# ============================================================
# 端口检测：自动选择可用端口
# ============================================================
def find_free_port(start_port=5000, max_tries=20):
    """从 start_port 开始查找可用端口"""
    for port in range(start_port, start_port + max_tries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return start_port + max_tries  # 兜底

# ============================================================
# Flask 后端启动（后台线程）
# ============================================================
def start_flask(port):
    """在后台线程启动 Flask 服务器"""
    # 设置工作目录，确保数据库等路径正确
    os.chdir(BASE_PATH)

    # 设置端口环境变量
    os.environ['PORT'] = str(port)

    # 导入并启动 Flask
    from app import app as flask_app

    # 关闭 Flask 日志（桌面应用不需要看到 HTTP 请求日志）
    import logging
    logging.getLogger('werkzeug').setLevel(logging.WARNING)

    flask_app.run(
        host='127.0.0.1',
        port=port,
        debug=False,
        use_reloader=False,
        threaded=True
    )

# ============================================================
# PyQt5 桌面窗口（主线程）
# ============================================================
def create_window(port):
    """创建 PyQt5 桌面窗口，内嵌浏览器访问 Flask"""
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QProgressBar, QMessageBox,
        QVBoxLayout, QWidget, QLabel
    )
    from PyQt5.QtCore import QUrl, QTimer
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from PyQt5.QtGui import QIcon

    class PharmacyApp(QMainWindow):
        def __init__(self):
            super().__init__()
            self.port = port
            self.init_ui()

        def init_ui(self):
            """初始化界面"""
            self.setWindowTitle('药房进货比较系统')
            self.resize(1400, 900)
            self.setMinimumSize(1024, 700)

            # 设置窗口图标
            icon_path = get_resource_path('static/images/icon.ico')
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))

            # 中央部件
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            # 加载提示
            self.loading_label = QLabel('正在启动系统，请稍候...')
            self.loading_label.setAlignment(
                __import__('PyQt5.QtCore', fromlist=['Qt']).Qt.AlignCenter
            )
            self.loading_label.setStyleSheet(
                'font-size: 18px; color: #409EFF; padding: 40px;'
            )
            layout.addWidget(self.loading_label)

            # 进度条
            self.progress = QProgressBar()
            self.progress.setRange(0, 100)
            self.progress.setValue(10)
            self.progress.setFixedHeight(4)
            self.progress.setTextVisible(False)
            self.progress.setStyleSheet(
                'QProgressBar { background: #EBEEF5; border: none; }'
                'QProgressBar::chunk { background: #409EFF; }'
            )
            layout.addWidget(self.progress)

            # 模拟启动进度
            self.progress_timer = QTimer()
            self.progress_timer.timeout.connect(self.update_progress)
            self.progress_timer.start(200)
            self.progress_value = 10

            # 延迟加载浏览器（等 Flask 启动完成）
            self.load_timer = QTimer()
            self.load_timer.timeout.connect(self.try_load_web)
            self.load_timer.start(500)
            self.retry_count = 0

        def update_progress(self):
            """更新进度条（视觉效果）"""
            if self.progress_value < 85:
                self.progress_value += 2
                self.progress.setValue(min(self.progress_value, 85))

        def try_load_web(self):
            """尝试连接 Flask 并加载网页"""
            import urllib.request
            import urllib.error

            self.retry_count += 1
            try:
                url = f'http://127.0.0.1:{self.port}/'
                req = urllib.request.Request(url, method='HEAD')
                urllib.request.urlopen(req, timeout=2)

                # Flask 已就绪，加载浏览器
                self.load_timer.stop()
                self.progress_timer.stop()
                self.progress.setValue(100)

                # 移除加载提示
                central = self.centralWidget()
                layout = central.layout()
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()

                # 创建 WebEngine 视图
                self.web_view = QWebEngineView()
                self.web_view.load(QUrl(url))
                layout.addWidget(self.web_view)

            except (urllib.error.URLError, urllib.error.HTTPError, OSError):
                if self.retry_count > 30:  # 15秒超时
                    self.load_timer.stop()
                    self.progress_timer.stop()
                    self.progress.setValue(0)
                    self.loading_label.setText(
                        f'系统启动失败，请检查端口 {self.port} 是否被占用后重试'
                    )
                    self.loading_label.setStyleSheet(
                        'font-size: 16px; color: #F56C6C; padding: 40px;'
                    )

        def closeEvent(self, event):
            """关闭窗口时确保应用完全退出"""
            event.accept()
            QApplication.instance().quit()

    return PharmacyApp()

# ============================================================
# 主入口
# ============================================================
def main():
    # 查找可用端口
    port = find_free_port(5000)
    print(f'[启动器] 使用端口: {port}')

    # 后台启动 Flask
    flask_thread = threading.Thread(target=start_flask, args=(port,), daemon=True)
    flask_thread.start()

    # 启动 Qt 应用（必须在主线程）
    from PyQt5.QtWidgets import QApplication
    qt_app = QApplication(sys.argv)

    # 设置应用信息
    qt_app.setApplicationName('药房进货比较系统')
    qt_app.setApplicationVersion('1.0.0')

    # 高 DPI 支持
    qt_app.setAttribute(__import__('PyQt5.QtCore', fromlist=['Qt']).Qt.AA_EnableHighDpiScaling)
    qt_app.setAttribute(__import__('PyQt5.QtCore', fromlist=['Qt']).Qt.AA_UseHighDpiPixmaps)

    # 创建主窗口
    window = create_window(port)
    window.show()

    # 运行 Qt 事件循环
    sys.exit(qt_app.exec_())


if __name__ == '__main__':
    main()
