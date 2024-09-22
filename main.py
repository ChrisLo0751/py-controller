import adbutils
import uiautomator2 as u2
import time
import os

def initDevice():
    # 获取已连接的设备列表
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    devices = adb.device_list()

    if not devices:
        print("没有检测到连接的设备")
    else:
        for device in devices:
            print(f"正在为设备 {device.serial} 配置 Wi-Fi ADB...")

            # 通过 USB 执行 adb tcpip 5555
            device.shell("adb tcpip 5555")

            # 获取设备的 IP 地址
            ip_info = device.shell("ip addr show wlan0")

            # 从命令结果中提取 IP 地址
            ip_address = None
            for line in ip_info.split("\n"):
                if "inet " in line:
                    ip_address = line.strip().split(" ")[1].split("/")[0]
                    print(f"设备 {device.serial} 的 IP 地址为: {ip_address}")
                    break

            if ip_address:
                # 通过本地电脑执行 adb connect 命令
                connect_cmd = f"adb connect {ip_address}:5555"
                print(f"执行命令: {connect_cmd}")
                result = os.system(connect_cmd)  # 使用 os.system 执行命令

                if result == 0:
                    print(f"设备 {device.serial} 已成功通过 Wi-Fi 连接")
                    d = u2.connect(f"{ip_address}:5555")  # 连接到指定的设备
                    print(f"{d.info}")
                else:
                    print(f"设备 {device.serial} 连接失败")
            else:
                print(f"未能获取设备 {device.serial} 的 IP 地址")


def main():
    initDevice()


if __name__ == '__main__':
    main()
