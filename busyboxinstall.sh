#!/bin/bash

# 检查ADB是否安装
if ! command -v adb &> /dev/null
then
    echo "ADB命令未找到，请先安装ADB工具"
    exit 1
fi

# 检查设备是否连接
adb devices | grep -w "device" &> /dev/null
if [ $? -ne 0 ]; then
    echo "没有检测到连接的设备，请确保设备已连接并开启了USB调试"
    exit 1
fi

# 检查是否root权限
adb root &> /dev/null
if [ $? -ne 0 ]; then
    echo "设备没有root权限，无法执行安装busybox的操作"
    exit 1
fi

# 下载busybox二进制文件（如果已经有了可以跳过这步）
echo "下载busybox二进制文件..."
curl -L -o busybox https://github.com/steveloughran/busybox-android/releases/download/v1.30.1/busybox-android-armv7

# 给busybox文件添加执行权限
chmod +x busybox

# 推送busybox到设备的系统路径
echo "正在将busybox推送到设备..."
adb push busybox /data/local/tmp/

# 在设备上执行busybox
echo "安装busybox..."
adb shell "chmod +x /data/local/tmp/busybox"
adb shell "ln -s /data/local/tmp/busybox /system/bin/busybox"

# 检查是否安装成功
adb shell "busybox --help" &> /dev/null
if [ $? -eq 0 ]; then
    echo "busybox安装成功！"
else
    echo "busybox安装失败，请检查错误信息"
    exit 1
fi

echo "安装完成，可以通过'adb shell busybox'命令来使用busybox工具"
