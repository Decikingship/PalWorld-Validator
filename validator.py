import os
import re
import socket
import psutil
import subprocess
import requests


# Function to parse the configuration file
def parse_config(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract the OptionSettings part using regex
    match = re.search(r'OptionSettings=\((.*?)\)', content, re.DOTALL)
    if not match:
        return None

    # Split the settings into a dictionary
    settings_str = match.group(1)
    settings_parts = settings_str.split(',')
    settings = {}
    for part in settings_parts:
        if '=' in part:
            key, value = part.split('=', 1)
            settings[key.strip()] = value.strip()

    return settings


def is_port_open(ip, port):
    # This is platform dependent. The following command works on Windows.
    command = f"netstat -an | findstr {port}"
    try:
        output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
        return f"{ip}:{port}" in output
    except subprocess.CalledProcessError as e:
        # If the command failed, it might mean the port is not open/listening.
        return False


# Function to validate the configuration
def validate_config(settings):
    errors = []

    # Check CPU and Memory requirements
    cpu_count = psutil.cpu_count()
    memory = psutil.virtual_memory().total / (1024 ** 3)  # Convert bytes to GB

    if cpu_count < 4:
        errors.append(f'CPU核心数需要至少为4,当前核心数: {cpu_count}')
    if memory < 8:
        errors.append(f'内存至少需要8GB,当前内存: {memory:.2f}GB')

    # Check each setting
    for key, value in settings.items():
        if value in ['True', 'False']:
            if value not in ['True', 'False']:
                errors.append(f'{key} 的值只能是 True 或者 False.')
        elif key == 'ServerPlayerMaxNum':
            max_players = min(cpu_count * 2.5, memory * 1.5)
            if not (0 < float(value) <= max_players):
                errors.append(f'根据你当前的配置, {key} 的值不应超过 {max_players}.')
        elif key == 'PublicPort':
            if value != '8211':
                errors.append(f'{key} 建议设置为 8211.')
        elif key == 'ServerPassword':
            if value != '':
                errors.append('你已设置了ServerPassword,在这种情况下是不能通过IP连接游戏的')
        elif key == 'PublicIP':
            if value == '':
                errors.append('请填写PublicIP')

    # Check if the port is open using the command-line tool
    port_is_open = is_port_open('0.0.0.0', settings['PublicPort'])
    if not port_is_open:
        public_port = settings['PublicPort']
        errors.append(f'没有程序在监听{public_port}端口,要么是你的PalServer没有启动,要么是你的配置文件没有生效,重启服务器让其生效.')

    return errors


# Main function
def main(config_file_path):
    settings = parse_config(config_file_path)
    if settings is None:
        print('无法解析配置文件.')
        return

    errors = validate_config(settings)
    if errors:
        print('发现一些配置问题:')
        for error in errors:
            print(f'- {error}')
    else:
        print('没有发现配置文件有问题,如果还是不能通过IP连接,请检查防火墙端口是否已开,或者重启PalServer.')


config_file_path = ""
while 'PalWorldSettings.ini' not in config_file_path:
    config_file_path = input('输入你的配置文件(PalWorldSettings.ini)路径:').replace('\"', '')
    if 'PalWorldSettings.ini' not in config_file_path:
        print('路径错误,请重新输入')
    elif not os.path.isfile(config_file_path):
        print('文件不存在,请重新输入')
main(config_file_path)
input('按回车退出')
