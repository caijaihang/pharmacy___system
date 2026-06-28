#!/usr/bin/env bash
# 将 Python 文件复制到 Chaquopy 的 python 源码目录

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_SRC="$SCRIPT_DIR/android/app/src/main/python"
mkdir -p "$PYTHON_SRC"

# 复制主应用文件
cp "$SCRIPT_DIR/app.py" "$PYTHON_SRC/"
cp "$SCRIPT_DIR/android_server.py" "$PYTHON_SRC/"

# 复制 static 目录
cp -r "$SCRIPT_DIR/static" "$PYTHON_SRC/"

# 复制模板（如果有）
if [ -d "$SCRIPT_DIR/templates" ]; then
    cp -r "$SCRIPT_DIR/templates" "$PYTHON_SRC/"
fi

echo "Python files copied to $PYTHON_SRC"
ls -la "$PYTHON_SRC/"
