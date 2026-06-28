"""
Android Flask 服务器启动入口
由 Chaquopy 调用，在 Android 中启动 Flask 并运行
"""
import sys
import os
import threading
import socket
import sqlite3

def find_free_port(start_port=5000, max_tries=20):
    for port in range(start_port, start_port + max_tries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return start_port + max_tries

def start_server(port):
    """启动 Flask 服务器（由 Java 调用）"""
    # 设置路径
    app_dir = '/data/data/com.caijaihang.pharmacycompare/files/app'
    if not os.path.exists(app_dir):
        # Chaquopy 环境下，app 模块在 assets 中
        app_dir = os.path.dirname(os.path.abspath(__file__))

    os.chdir(app_dir)
    sys.path.insert(0, app_dir)

    # 确保数据库目录可写
    db_path = os.path.join(app_dir, 'pharmacy.db')
    os.environ['DATABASE_PATH'] = db_path

    # 导入并启动 Flask
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
