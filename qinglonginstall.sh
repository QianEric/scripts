#!/bin/bash

# 青龙面板安装脚本

# 青龙面板的下载链接（可以根据实际需求修改）
QINGLONG_URL="https://github.com/whyour/qinglong/releases/download/v1.15.0/qinglong_v1.15.0_linux_amd64.tar.gz"

# 下载目录
DOWNLOAD_DIR="/data/local/tmp"

# 设备中青龙面板安装路径
INSTALL_DIR="/opt/qinglong"

# ADB命令
ADB="adb shell"

# 准备工作：检查设备是否连接
$ADB get-state
if [ $? -ne 0 ]; then
  echo "设备未连接，请检查ADB连接。"
  exit 1
fi

# 步骤 1: 下载青龙面板
echo "正在下载青龙面板..."
$ADB "curl -L $QINGLONG_URL -o $DOWNLOAD_DIR/qinglong.tar.gz"
if [ $? -ne 0 ]; then
  echo "下载失败，请检查网络连接。"
  exit 1
fi

# 步骤 2: 解压安装包
echo "正在解压青龙面板..."
$ADB "tar -zxvf $DOWNLOAD_DIR/qinglong.tar.gz -C $DOWNLOAD_DIR"
if [ $? -ne 0 ]; then
  echo "解压失败。"
  exit 1
fi

# 步骤 3: 移动到目标安装目录
echo "正在移动青龙面板到安装目录..."
$ADB "mkdir -p $INSTALL_DIR"
$ADB "mv $DOWNLOAD_DIR/qinglong/* $INSTALL_DIR/"
if [ $? -ne 0 ]; then
  echo "安装失败，请检查目录权限。"
  exit 1
fi

# 步骤 4: 设置权限
echo "正在设置文件权限..."
$ADB "chmod +x $INSTALL_DIR/qinglong"

# 步骤 5: 启动青龙面板
echo "正在启动青龙面板..."
$ADB "$INSTALL_DIR/qinglong start"
if [ $? -eq 0 ]; then
  echo "青龙面板安装并启动成功！"
else
  echo "启动失败，请检查日志获取详细信息。"
  exit 1
fi

# 完成
echo "青龙面板安装过程完成。"
