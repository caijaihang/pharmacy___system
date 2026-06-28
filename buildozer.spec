[app]

# 应用信息
title = PharmacyCompare
package.name = pharmacycompare
package.domain = caijaihang

# 版本
version = 1.0.0

# 源码配置
source.dir = .
source.include_exts = py,html,js,db,json
source.include_patterns = static/**,templates/**

# Python 依赖（版本号不要写在 python3 后面）
requirements = python3,flask,flask-cors,requests,beautifulsoup4,lxml,pandas,numpy,openpyxl,xlrd,certifi,charset-normalizer,idna,urllib3,jinja2,markupsafe,itsdangerous,click

# Android 配置
android.api = 30
android.minapi = 24
android.ndk = 28c
android.arch = arm64-v8a

# WebView 引导程序
android.bootstrap = webview

# Web 服务器端口
android.port = 5000

# 权限
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# 屏幕方向
orientation = all

# 日志级别
log_level = 2
