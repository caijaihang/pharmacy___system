[app]

# 应用信息
title = 药房进货比较系统
package.name = pharmacy
package.domain = caijaihang

# 版本
version = 1.0.0

# 源码配置
source.dir = .
source.include_exts = py,html,js,db,json
source.include_patterns = static/**,templates/**

# Python 依赖
requirements = python3==3.11.6,flask==2.2.5,flask-cors==4.0.0,requests==2.28.2,beautifulsoup4==4.12.2,lxml,pandas==2.0.3,numpy,openpyxl==3.1.2,xlrd==2.0.1,certifi,charset-normalizer==3.1.0,idna==3.4,urllib3==1.26.18,jinja2==3.1.2,markupsafe==2.1.3,itsdangerous==2.1.2,click==8.1.7

# WebView 引导程序（关键：用 webview 而不是 kivy）
p4a.bootstrap = webview

# Web 服务器端口
p4a.port = 5000

# Android 配置
android.api = 30
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# 权限
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# 屏幕方向（auto 自动旋转）
orientation = auto

# 架构（只打 arm64，减小 APK 体积）
android.arch = arm64-v8a

# 日志级别
log_level = 2

# 窗口设置（全屏无状态栏）
fullscreen = 0

# Gradle 依赖
android.gradle_dependencies = compile 'com.android.support:multidex:1.0.3'

# Android 入口
android.entrypoint = org.kivy.android.PythonActivity

# 接受许可
android.accept_sdk_license = True
