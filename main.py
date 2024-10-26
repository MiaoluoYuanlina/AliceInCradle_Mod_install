import urllib.request
from urllib.parse import urlparse
from urllib3.util.retry import Retry
import zipfile
import os
import psutil
import sys
import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm
import subprocess
import shutil
import tkinter
import tkinter as tk
from tkinter import messagebox
from tkinter.messagebox import *
import platform
import webbrowser
import time
import colorama
from colorama import Fore, Back, Style
from wcwidth import wcswidth
from colorama import Fore
import re
import hashlib
import socket

# 初始化 colorama
colorama.init()
"""
前景色（Fore）和背景色（Back）：
BLACK: 黑色
RED: 红色
GREEN: 绿色
YELLOW: 黄色
BLUE: 蓝色
MAGENTA: 洋红色（品红色）
CYAN: 青色
WHITE: 白色
RESET: 重置为默认颜色

样式（Style）：
DIM: 暗淡
NORMAL: 正常
BRIGHT: 明亮
RESET_ALL: 重置所有样式
"""


# 日志
Log_M = ""
def print_log(text):
    global Log_M
    Log_M = f"{Log_M}\n{text}"
    print(text)

def print_log_colored_text():
    # 获取终端大小
    columns, rows = shutil.get_terminal_size()

    # 设置颜色
    bg_magenta = Back.WHITE
    reset = Style.RESET_ALL

    # 中间五行的文本
    texts = [f"{Fore.MAGENTA}Py：XiaoMiao_ICa or 苗萝缘莉雫",
             f"{Fore.RED}GPL-3.0 许可证",
             f"{Fore.BLUE}适用于 Alice In Cradle 的 bepinex 框架Mod一键安装程序",
             f"{Fore.BLUE}理论适配游戏全部版本！",
             f"{Fore.RED}本程序仅供学习参考 GitHub项目:repo:MiaoluoYuanlina/AliceinCradle_BepInEx_XiaoMiaoICa-Mod",
             f"{Fore.WHITE}_(‾▿◝_　)ﾉｼ",
             f"{Fore.YELLOW}Mod及游戏本体都是免费的，如果你是购买而来，证明你被骗啦~",
             f"{Fore.RED}本程序会收集你的日志来更好的维护，如果您不同意，请立即关闭此程序。",
             f"{Fore.RED}"]

    # 计算中间五行的起始和结束行
    start_row = (rows // 2) - 4
    end_row = (rows // 2) + 4

    # 生成填满背景颜色的行
    for i in range(rows):
        if start_row <= i <= end_row:
            # 在中间五行打印不同的文本
            text = texts[i - start_row]
            text_width = wcswidth(text)
            #print_log(text)
            text2 = ""
            text3 = ""
            text_length = rows / 2 * 3.5 - len(text) / 2
            #text_length = len(text)
            #print_log(text_length,rows)
            i = 0
            while i < text_length:
                i += 1
                text2 = f"{text2} "

            i = 0
            while i < text_length:
                i += 1
                text3 = f"{text3} "

            #print_log(columns, rows)
            print(f"{text2}{text}{text3}")

            #padding = (columns - text_width) // 2
            #print_log(bg_magenta + " " * 10 + text + bg_magenta + " " * (columns - padding - text_width) + reset)
            #print_log(bg_magenta + " " * padding + text + bg_magenta + " " * (columns - padding - text_width) + reset)
        else:
            print(f"")

    time.sleep(3)

    for i in range(rows):
        text = ""
        while i < rows * 4:
            i += 1
            text = f"{text} "
        # print_log(f"{bg_magenta}{text4}")
        print(f"{text}")

print_log_colored_text()
print_log(f"{Back.RESET}{Fore.RESET}")

# 下载
def download(url, file_path):
    try:
        print_log(f"{Fore.WHITE} URL:{url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 如果响应状态码不是 200，则会引发 HTTPError 异常

        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)

        with open(file_path, "wb") as f:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)

        progress_bar.close()
        print_log(f"{Fore.RESET}")
        return True

    except requests.exceptions.RequestException as e:
        print_log(f"{Fore.RED}下载失败： {e}")
        return False

#解压
def unzip_file(zip_file_path, extract_to_directory):
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to_directory)
        print_log(f"{Fore.GREEN}已解压 {zip_file_path} 到 {extract_to_directory}")
        return True
    except (zipfile.BadZipFile, FileNotFoundError, PermissionError) as e:
        print_log(f"{Fore.RED}解压失败: {e}")
        return False

# 创建目录
def create_directory(directory_path):
    try:
        os.makedirs(directory_path, exist_ok=True)
        print_log(f"{Fore.GREEN}目录 '{directory_path}' 创建成功.")
    except OSError as error:
        print_log(f"{Fore.RED}创建目录出错  '{directory_path}': {error}")

# 获取github地址
def get_GitHub_download_url(url):  # 获取 GitHub 地址
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 会抛出 HTTPError 异常
        if response.status_code == 200:
            return response.url
    except requests.RequestException as e:
        print_log(f"{Fore.RED}无法获取文件直链，错误信息：{e}")

    return None

#获取PID路径
def get_process_info(process_name):
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            if proc.info['name'] == process_name:
                pid = proc.info['pid']
                exe_path = proc.info['exe']
                return pid, exe_path
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None, None

# 结束PID
def terminate_process(pid):
    try:
        # 获取进程对象
        process = psutil.Process(pid)
        # 终止进程
        process.terminate()
        # 等待进程终止
        process.wait()
        print_log(f"{Fore.GREEN}已经终止PID:{pid}")
    except psutil.NoSuchProcess:
        print_log(f"{Fore.RED}没有此PID: {pid}.")
    except psutil.AccessDenied:
        print_log(f"{Fore.RED}结束此PID被拒绝:{pid}.")
    except psutil.ZombieProcess:
        print_log(f"{Fore.RED}此PID为僵尸进程:{pid}")

# 链接访问
def is_url_accessible(url):
    try:
        print_log(f"{Fore.CYAN}正在尝试访问：" + url)

        # 创建一个请求会话，设置重试机制
        session = requests.Session()
        retry = Retry(total=5, backoff_factor=0.1)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        # 发送请求
        response = session.head(url, timeout=10)
        print_log(f"{url} 状态码: {response.status_code}")
        return response.status_code

    except requests.RequestException as e:
        # 捕捉请求异常并打印错误信息
        print_log(f"{Fore.RED}访问 {url} 时发生错误: {e}")
        return 1

#获取系统信息
def get_system_info():
    # 获取操作系统信息
    os_info = platform.uname()

    # 获取CPU信息
    cpu_info = {
        'Physical cores': psutil.cpu_count(logical=False),
        'Total cores': psutil.cpu_count(logical=True),
        'Max Frequency': f"{psutil.cpu_freq().max:.2f}Mhz",
        'Min Frequency': f"{psutil.cpu_freq().min:.2f}Mhz",
        'Current Frequency': f"{psutil.cpu_freq().current:.2f}Mhz",
        'CPU Usage': f"{psutil.cpu_percent()}%"
    }

    # 获取内存信息
    svmem = psutil.virtual_memory()
    memory_info = {
        'Total': f"{svmem.total / (1024 ** 3):.2f} GB",
        'Available': f"{svmem.available / (1024 ** 3):.2f} GB",
        'Used': f"{svmem.used / (1024 ** 3):.2f} GB",
        'Percentage': f"{svmem.percent}%"
    }

    # 获取磁盘信息
    disk_info = []
    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        disk_info.append({
            'Device': partition.device,
            'Mountpoint': partition.mountpoint,
            'File System Type': partition.fstype,
            'Total Size': f"{usage.total / (1024 ** 3):.2f} GB",
            'Used': f"{usage.used / (1024 ** 3):.2f} GB",
            'Free': f"{usage.free / (1024 ** 3):.2f} GB",
            'Percentage': f"{usage.percent}%"
        })

    # 获取网络信息
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    net_info = psutil.net_if_addrs()

    return {
        'Operating System': os_info.system,
        'Node Name': os_info.node,
        'Release': os_info.release,
        'Version': os_info.version,
        'Machine': os_info.machine,
        'Processor': os_info.processor,
        'CPU Info': cpu_info,
        'Memory Info': memory_info,
        'Disk Info': disk_info,
        'Hostname': hostname,
        'IP Address': ip_address,
        'Network Info': net_info
    }

#获取一个编号
def gitID(type: int) -> str:
    BASE_URL = "https://api.xiaomiao-ica.top/AIC/log/exe/"

    if type == 0:
        url = f"{BASE_URL}ID_normalcy/?gain="
    else:
        url = f"{BASE_URL}ID_error/?gain="

    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            response = requests.get(url, verify=False)  # 忽略 SSL 验证
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"尝试 {attempt + 1} 失败: {e}")  # 打印错误信息以供调试
            if attempt < max_attempts - 1:
                continue  # 尝试下一次
            return f"请求出错: {e}，已重试 {max_attempts} 次。"

# 正常结束程序
def program_END(intdata):  # 正常结束程序
    #上传日志
    system_info = get_system_info()
    ID1=gitID(intdata)
    print_log(f"{Fore.MAGENTA}")
    print_log(f"程序为你在本次运行分配的ID：{ID1}")
    print_log(f"出现问题时，可以把这段ID复制下来发给本苗(程序作者)，本苗会帮助你解决问题！")
    print_log(f"")
    print_log(f"{Fore.RESET}")
    print_log("————————————————————————————————————————————————————————————————————————————————————————")
    print_log(f"系统信息:")
    # 打印系统信息
    for key, value in system_info.items():
        print_log(f"{key}: {value}")
    print_log("————————————————————————————————————————————————————————————————————————————————————————")

    # 上传日志
    send_data_to_server(Log_M,intdata)

    if intdata != 0 :
        window = tkinter.Tk()
        window.withdraw()  # 退出默认 tk 窗口

        result = messagebox.askokcancel(title="欧尼酱~有一件问题想要问您~", message=f'程序非正常退出，是否联系本苗呢？\n\n为你分配的错误编号:{ID1}\n可以把这个编号发给本苗，本苗会帮助你！')
        print_log(result)
        if result == True:
            webbrowser.open("https://xiaomiao-ica.top")

    print_log(f"{Fore.CYAN}10秒后程序将退出")
    time.sleep(10)
    sys.exit(intdata)

# 调用微软商店
def open_microsoft_store(app_name):
    url = f"ms-windows-store://pdp/?productid={app_name}"
    webbrowser.open(url)

#网络访问
def read_text_from_url(url):
    response = requests.get(url)
    content = response.text
    return content

#删空行
def remove_empty_lines_from_string(text):
    # 将字符串按行分割
    lines = text.split("\n")
    # 去除空行
    non_empty_lines = [line for line in lines if line.strip() != ""]
    # 将非空行重新组合成一个字符串
    return "\n".join(non_empty_lines)

#检测文本中文
def contains_chinese(text):
    # 使用正则表达式匹配中文字符的范围
    pattern = re.compile(r'[\u4e00-\u9fff\u3040-\u30ff\u31f0-\u31ff\u3400-\u4dbf\uac00-\ud7af]')
    return bool(pattern.search(text))

#上传日志
def send_data_to_server(text, data):
    # 定义要发送的文本和数据
    url = 'https://api.xiaomiao-ica.top/AIC/log/exe/index.php'  # 替换为实际的PHP文件URL

    # 构造POST请求的数据
    payload = {
        'text': text,
        'data': data
    }

    # 发送POST请求到PHP服务器，忽略SSL验证
    try:
        response = requests.post(url, data=payload, verify=False)
        # 输出服务器响应内容
        print(f"{Fore.CYAN}{response.text}")
    except requests.RequestException as e:
        print(f"{Fore.RED}请求出错: {e}")

#获取文件哈希值
def file_hash(file_path: str, hash_method) -> str:
    if not os.path.isfile(file_path):
        print_log('文件不存在。')
        return ''
    h = hash_method()
    with open(file_path, 'rb') as f:
        while b := f.read(8192):
            h.update(b)
    return h.hexdigest()
def str_hash(content: str, hash_method, encoding: str = 'UTF-8') -> str:
    return hash_method(content.encode(encoding)).hexdigest()
def file_md5(file_path: str) -> str:
    return file_hash(file_path, hashlib.md5)
def file_sha256(file_path: str) -> str:
    return file_hash(file_path, hashlib.sha256)
def file_sha512(file_path: str) -> str:
    return file_hash(file_path, hashlib.sha512)
def file_sha384(file_path: str) -> str:
    return file_hash(file_path, hashlib.sha384)
def file_sha1(file_path: str) -> str:
    return file_hash(file_path, hashlib.sha1)
def file_sha224(file_path: str) -> str:
    return file_hash(file_path, hashlib.sha224)
def str_md5(content: str, encoding: str = 'UTF-8') -> str:
    return str_hash(content, hashlib.md5, encoding)
def str_sha256(content: str, encoding: str = 'UTF-8') -> str:
    return str_hash(content, hashlib.sha256, encoding)
def str_sha512(content: str, encoding: str = 'UTF-8') -> str:
    return str_hash(content, hashlib.sha512, encoding)
def str_sha384(content: str, encoding: str = 'UTF-8') -> str:
    return str_hash(content, hashlib.sha384, encoding)
def str_sha1(content: str, encoding: str = 'UTF-8') -> str:
    return str_hash(content, hashlib.sha1, encoding)
def str_sha224(content: str, encoding: str = 'UTF-8') -> str:
    return str_hash(content, hashlib.sha224, encoding)



if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    PC_system = platform.system()  # 获取系统信息
    PC_release = platform.release()
    PC_version = platform.version()

    # 取进程信息
    Gamepid, Gamepath = None, None
    pidI=9
    while Gamepid is None or Gamepath is None:
        Gamepid, Gamepath = get_process_info("AliceInCradle.exe")
        if Gamepid is None or Gamepath is None:
            pidI=pidI+1
            if pidI==10:
                pidI =0
                print_log(f"{Fore.RED}请现在开启游戏！！！")
            time.sleep(1)

    if Gamepid and Gamepath:
        print_log(f"{Fore.GREEN}游戏PID PID: {Gamepid}")
        print_log(f"{Fore.GREEN}游戏路径 Path: {Gamepath}")
        terminate_process(Gamepid)  # 结束进程
    else:
        print_log(f"{Fore.RED}没有找到游戏！")
        program_END(3)
        messagebox.showerror("欧尼酱~出错啦~","没有找到你的游戏信息，这是不寻常的问题，可以尝试联系本苗。\n记得一定要带上控制台的截图，要不本苗也帮助不你了~")

    if contains_chinese(Gamepath):
        print_log(f"{Fore.RED}你的游戏路径有中文！BepEx不可有中文路径！ 路径：{Gamepath}")
        messagebox.showerror("欧尼酱~出错啦~",
                             f"你的游戏目录有中文，请将游戏目录移动到没有中文日文韩文等特殊文字的目录。\n当前目录{Gamepath}")
        program_END(9)

    def get_user_input():
        while True:
            try:
                print_log(f"{Fore.YELLOW}请输入1~2")
                print_log(f"{Fore.YELLOW}1.{Fore.MAGENTA}使用国际站点下载(你可能需要较好的网络)")
                print_log(f"{Fore.YELLOW}2.{Fore.MAGENTA}使用国内代理站点下载(本苗的自建站点如果无法访问可以尝试更改DNS)")
                user_input = int(input(f"{Fore.YELLOW}请输入1或2：{Fore.CYAN}"))
                if user_input in [1, 2]:
                    return user_input
                else:
                    print_log(f"{Fore.RED}请输入无效")
            except ValueError:
                print_log(f"{Fore.RED}输入无效 {Fore.YELLOW}请输入数字1或2。")
    result = get_user_input()
    print_log(f"你输入了：{result}")
    download_url_1 = "https://builds.bepinex.dev/projects/bepinex_be/571/BepInEx_UnityMono_x64_3a54f7e_6.0.0-be.571.zip"
    HaXiMD5_BepEx = "d42de011d504ea560cbb940318403489"
    download_url_2 = "https://github.xiaomiao-ica.top/AIC/Mod/Latest_version_URL.txt"
    HaXiMD5_Mod_url = "https://github.xiaomiao-ica.top/AIC/Mod/MD5.txt"
    Download_method = 1
    if (result == 1):
        # 尝试访问 github
        Download_method = 1
        status_code = is_url_accessible("https://github.com/")
        if status_code == 200:
            print_log(f"{Fore.GREEN}成功访问 GitHub ！")
        elif status_code == 201:
            print_log(f"{Fore.GREEN}成功访问 GitHub!")
        elif status_code == 202:
            print_log(f"{Fore.YELLOW}成功访问 GitHub 但是未能返回正确的值。")
        elif status_code == 200:
            print_log(f"{Fore.YELLOW}成功访问 GitHub 但是未能返回正确的值。")
        elif status_code == 200:
            print_log(f"{Fore.YELLOW}成功访问 GitHub 但是未能返回正确的值。")
        elif status_code == 403:
            print_log(f"{Fore.YELLOW}成功访问 GitHub 但是未能返回正确的值，你的访问被拒绝你可能无法正常下载。")
        else:
            print_log(f"{Fore.RED}无法访问 GitHub ！")
            messagebox.showerror("欧尼酱~出错啦~","你无法链接到GitHub请尝试使用加速器！\n 推荐使用 Watt Toolkit 加速器 https://steampp.net")
            root.destroy()
            print_log(f"推荐使用加速器 Watt Toolkit https://steampp.net")
            if 1 == 1 and (PC_release == "10" or PC_release == "11"):
                open_microsoft_store("9mtcfhs560ng")
            else:
                webbrowser.open("https://steampp.net")
            program_END(1)

        # 尝试访问 bepinex.dev
        status_code = is_url_accessible(download_url_1)
        if status_code == 200:
            print_log(f"{Fore.GREEN}成功访问 bepinex 官网！")
        elif status_code == 201:
            print_log(f"{Fore.GREEN}成功访问 bepinex 官网！")
        elif status_code == 202:
            print_log(f"{Fore.YELLOW}成功访问 bepinex 官网但是未能返回正确的值。")
        elif status_code == 200:
            print_log(f"{Fore.YELLOW}成功访问 bepinex 官网但是未能返回正确的值。")
        elif status_code == 200:
            print_log(f"{Fore.YELLOW}成功访问 bepinex 官网但是未能返回正确的值。")
        elif status_code == 403:
            print_log(f"{Fore.YELLOW}成功访问 bepinex 官网但是未能返回正确的值，你的访问被拒绝你可能无法正常下载。")
        else:
            print_log(f"{Fore.RED}吗无法访问 bepinex 官网！")

            messagebox.showerror("欧尼酱~出错啦~",
                                 "你可以尝试使用代理服务器！\n 推荐使用 Clash进行代理！ https://clashcn.com")
            webbrowser.open("https://clashcn.com/clashdownload")
            program_END(2)
    elif (result == 2):
        Download_method = 2
        #https://api.xiaomiao-ica.top/AIC/file/AliceInCradle_Miaoo_Mod_1.1.dll
        download_url_1 = f"https://api.xiaomiao-ica.top/agent/?fileUrl={download_url_1}"
        download_url_2 = f"https://api.xiaomiao-ica.top/agent/?fileUrl={download_url_2}"
        HaXiMD5_Mod_url = f"https://api.xiaomiao-ica.top/agent/?fileUrl={HaXiMD5_Mod_url}"
        # 尝试访问 api.xiaomiao-ica.top
        status_code = is_url_accessible(download_url_1)
        if status_code == 200:
            print_log(f"{Fore.GREEN}成功访问 本苗自建站点 官网！")
        elif status_code == 201:
            print_log(f"{Fore.GREEN}成功访问 本苗自建站点 官网！")
        elif status_code == 202:
            print_log(f"{Fore.YELLOW}成功访问 本苗自建站点 官网但是未能返回正确的值。")
        elif status_code == 200:
            print_log(f"{Fore.YELLOW}成功访问 本苗自建站点 官网但是未能返回正确的值。")
        elif status_code == 200:
            print_log(f"{Fore.YELLOW}成功访问 本苗自建站点 官网但是未能返回正确的值。")
        elif status_code == 403:
            print_log(f"{Fore.YELLOW}成功访问 本苗自建站点 官网但是未能返回正确的值，你的访问被拒绝你可能无法正常下载。")
        else:
            print_log(f"{Fore.RED}无法访问 本苗自建站点 官网！")

            messagebox.showerror("欧尼酱~出错啦~","你可以尝试更改DNS")
            program_END(2)

    else:
        sys.exit(-1)


    # 下载 BepInEx
    create_directory(fr"{os.getcwd()}\temp")
    if (download(download_url_1,fr"{os.getcwd()}\temp\BepInEx_UnityMono_x64_3a54f7e_6.0.0-be.571.zip")):
        print_log(f"{Fore.GREEN}下载完成！")

        MD5=file_md5(fr"{os.getcwd()}\temp\BepInEx_UnityMono_x64_3a54f7e_6.0.0-be.571.zip")
        print_log(f"{Fore.GREEN}MD5哈希:{MD5}")

        if MD5 == HaXiMD5_BepEx:
            print_log("MD5哈希校验成功！")
        else:
            print_log(f"{Fore.RED}MD5哈希值错误！")
            messagebox.showerror("欧尼酱~出错啦~",
                                 f"MD5哈希值校验失败！\n这有可能是因为网络波动等原因造成的文件损坏，可以尝试程序运行程序。\n获取到的哈希值:{MD5}\n正确哈希值:{HaXiMD5_BepEx}")
            program_END(11)
    else:
        print_log(f"{Fore.RED}下载BepInEx失败！")
        messagebox.showerror("欧尼酱~出错啦~","下载BepInEx时出现错误！\n这可能是偶尔的问题，你可以尝试重新运行本程序。\n如果一直无法访问可以尝试联系本苗\n记得一定要带上控制台的截图，要不本苗也帮助不你了~")
        program_END(4)

    # 解压 BepInEx
    if (unzip_file(fr"{os.getcwd()}\temp\BepInEx_UnityMono_x64_3a54f7e_6.0.0-be.571.zip",
                   fr"{os.path.dirname(Gamepath)}")):
        print_log(f"{Fore.GREEN}解压完成！")
    else:
        print_log(f"{Fore.RED}解压失败！")
        messagebox.showerror("欧尼酱~出错啦~","解压BepInEx时出现错误！\n这可能是偶尔的问题，你可以尝试重新运行本程序。\n如果一直无法访问可以尝试联系本苗\n记得一定要带上控制台的截图，要不本苗也帮助不你了~")
        program_END(5)


    # 动态获取github链接 获取下载地址
    Mod_url = read_text_from_url(download_url_2)#动态获取地址
    Mod_url = remove_empty_lines_from_string(Mod_url)#去空行
    print_log(f"使用域名{urlparse(Mod_url).netloc}")
    if urlparse(Mod_url).netloc == "github.com" and result == 1:
        # 解析github链接
        print_log(f"正在尝试解析github下载地址:{Mod_url}")
        print_log(f"{Fore.CYAN}此过程如果超过一分钟可以尝试重新运行。")
        download_url = get_GitHub_download_url(Mod_url)#解析GitHub地址
        if download_url:
            print_log(f"{Fore.GREEN}解析到github地址:" + download_url)
            Mod_url = download_url
        else:
            print_log(f'{Fore.RED}解析到github地址失败！')
            messagebox.showerror("欧尼酱~出错啦~","你无法解析到github地址！\n你可以尝试联系本苗！\n记得一定要带上控制台的截图，要不本苗也帮助不你啦~")
            program_END(6)
    else:
        Mod_url = f"https://api.xiaomiao-ica.top/agent/?fileUrl={Mod_url}"


    # 下载mod
    create_directory(fr"{os.path.dirname(Gamepath)}\BepInEx\plugins\XiaoMiao_ICa")#创建目录
    if (download(f"{Mod_url}",fr"{os.path.dirname(Gamepath)}\BepInEx\plugins\XiaoMiao_ICa\AliceInCradle_Miaoo_Mod_1.0.dll")):
        print_log(f"{Fore.GREEN}下载完成！")
        MD5=file_md5(f"{os.path.dirname(Gamepath)}\BepInEx\plugins\XiaoMiao_ICa\AliceInCradle_Miaoo_Mod_1.0.dll")
        print_log(f"{Fore.GREEN}MD5哈希:{MD5}")

        URL_HaXiMD5 = read_text_from_url(HaXiMD5_Mod_url)  # 动态获取MOD哈希
        URL_HaXiMD5 = remove_empty_lines_from_string(URL_HaXiMD5)  # 去空行
        if MD5 == URL_HaXiMD5:
            print_log("MD5哈希校验成功！")
        elif URL_HaXiMD5 == "":
            print_log(f"{Fore.RED}未能从URL获取哈希值")
        else:
            print_log(f"{Fore.RED}MD5哈希值错误！")
            messagebox.showerror("欧尼酱~出错啦~",f"MD5哈希值校验失败！\n这有可能是因为网络波动等原因造成的文件损坏，可以尝试程序运行程序。\n获取到的哈希值:{MD5}\n正确哈希值:{URL_HaXiMD5}")
            program_END(10)
    else:
        print_log(f"{Fore.RED}下载Mod失败！")
        messagebox.showerror("欧尼酱~出错啦~","下载Mod失败！！\n有可能是你的网络波动问题可以尝试重新运行本程序\n如果无法解决可以尝试联系本苗！\n记得一定要带上控制台的截图，要不本苗也帮助不你了~")
        program_END(7)

    # 删除缓存
    temp_directory = fr"{os.getcwd()}\temp"
    try:
        shutil.rmtree(temp_directory)
        print_log(f"{Fore.GREEN}目录 '{temp_directory}' 及其所有内容已删除")
    except OSError as e:
        print_log(f"{Fore.RED}删除目录时出错: {e}")

    print_log(f"{Fore.CYAN}启动游戏...")
    subprocess.Popen(Gamepath, shell=True)

    program_END(0)
