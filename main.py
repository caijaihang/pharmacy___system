# -*- mode: python ; coding: utf-8 -*-
"""
药房进货比较系统 - Android 启动入口
在 Android 上启动 Flask 后端 + WebView 前端
"""
import os
import sys
import threading
import socket

def find_free_port(start_port=5000, max_tries=20):
    """查找可用端口"""
    for port in range(start_port, start_port + max_tries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return start_port + max_tries

def start_flask(port):
    """启动 Flask 服务器"""
    # 设置工作目录为 APK 内部 assets 路径
    base_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_path)

    os.environ['PORT'] = str(port)

    # 导入并启动 Flask
    sys.path.insert(0, base_path)
    from app import app as flask_app
    import logging
    logging.getLogger('werkzeug').setLevel(logging.WARNING)

    flask_app.run(
        host='127.0.0.1',
        port=port,
        debug=False,
        use_reloader=False,
        threaded=True
    )

def main():
    """主入口 - 由 android WebView 引导程序调用"""
    port = find_free_port(5000)
    print(f'[启动器] Flask 端口: {port}')

    # 后台启动 Flask
    flask_thread = threading.Thread(target=start_flask, args=(port,), daemon=True)
    flask_thread.start()

    # 返回 URL 给 WebView 加载
    url = f'http://127.0.0.1:{port}/'
    print(f'[启动器] WebView URL: {url}')

    # python-for-android webview 引导程序会自动加载这个 URL
    return url

if __name__ == '__main__':
    main()
