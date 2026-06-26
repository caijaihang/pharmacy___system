"""
PyInstaller 运行时钩子 - 处理资源路径
在 EXE 启动前执行，确保数据库和静态文件路径正确
"""
import sys
import os

if getattr(sys, 'frozen', False):
    # 打包后的环境
    # _MEIPASS: PyInstaller 临时解压目录（只读）
    # EXE 所在目录：可写文件存放位置
    exe_dir = os.path.dirname(sys.executable)
    temp_dir = sys._MEIPASS

    # 设置工作目录为 EXE 所在目录（确保数据库可写）
    os.chdir(exe_dir)

    # 如果 EXE 同级目录没有 pharmacy.db，从打包资源中复制一份
    db_path = os.path.join(exe_dir, 'pharmacy.db')
    db_template = os.path.join(temp_dir, 'pharmacy.db')

    if not os.path.exists(db_path) and os.path.exists(db_template):
        import shutil
        shutil.copy2(db_template, db_path)
        print(f'[运行时钩子] 已复制初始数据库到 {db_path}')

    # 如果没有 exports 目录，创建一个
    exports_dir = os.path.join(exe_dir, 'exports')
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)
