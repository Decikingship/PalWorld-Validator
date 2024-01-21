# PalWorld-Validator
这个项目用于检测PalWorld的服务端配置文件是否有错,它会检测以下内容:
1. 你的服务器配置是否满足运行服务端的最低要求
2. 你的配置文件格式是否有问题
3. 你的配置文件的字段值是否正确
4. 如果你已经运行了PalServer,它会检测内网对应的端口是否生效,也就是说你的PalServer有没有跑在你指定的端口上
5. 你设置的最大人数是否超过了你的服务器可承载的最大人数
## 使用方法
###  方法一:使用exe文件
直接下载并使用该文件,这个程序会被WindowsDefender判定为病毒,如果不放心请直接使用源代码:

https://github.com/Decikingship/PalWorld-Validator/releases/tag/Windows
###  方法二:使用源代码
1. 安装Python3.x(如已安装请跳过): https://www.python.org/downloads/
2. 安装git(如已安装请跳过): https://git-scm.com/downloads
3. 克隆本项目: `git clone https://github.com/Decikingship/PalWorld-Validator.git`
4. 使用cmd进入项目目录。
5. cmd执行安装依赖: `pip install -r requirements.txt`
6. 运行本项目: `python validator.py`
7. 输入你的配置文件(`PalWorldSettings.ini`)绝对路径并回车。

## License
本项目基于Apache-2.0协议开源,可以随意修改。
