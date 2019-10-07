# Docker

## 1.Linux下使用Docker(CentOS 7)
#### 1.1 安装Docker
```text
1.centos7安装docker ce
  # 安装依赖包
  sudo yum install -y yum-utils device-mapper-persistent-data lvm2
  # 添加软件源
  sudo yum-config-manager --add-repo https://mirrors.ustc.edu.cn/docker-ce/linux/centos/docker-ce.repo
  # 更新缓存/安装docker ce
  sudo yum makecache fast
  sudo yum install docker-ce
2.启动docker ce
  sudo systemctl enable docker
  sudo systemctl start docker
3.将docker加入用户组
  sudo groupadd docker
  sudo usermod -aG docker $USER
4.测试docker
  docker run hello-world
5.镜像加速
  阿里云加速镜像：dev.aliyun.com
  # 修改加速地地址(镜像加速器)
  sudo mkdir -p /etc/docker
  sudo tee /etc/docker/daemon.json <<-'EOF'
  {
    "registry-mirrors": ["https://p731kmg8.mirror.aliyuncs.com"]
  }
  EOF
  sudo systemctl daemon-reload
  sudo systemctl restart docker
  docker info 可以查看是否注册成功！
```

#### 1.2 Docker使用示例
```
***************************** 搭建python环境 **********************************
1.拉取centos:6.8
docker pull centos:6.8

2.创建,并运行容器
docker run -it centos:6.8 /bin/bash

3.在centos:6.8中安装python3.57
  3.1 下载python3.57
  3.2 将python3.57传到容器中
    docker cp /root/Downloads/requirements.txt 05e0:/root/requirements.txt
  3.3 安装python3.57
    一.更新系统软件包
    yum update -y

    二.安装软件管理包和可能使用的依赖
    yum -y groupinstall "Development tools"
    yum install openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel gcc

    三、安装python3(自己手动迅雷下载快)
    wget https://www.python.org/ftp/python/3.5.7/Python-3.5.7.tgz

    # 解压
    tar -zxvf Python-3.5.7.tgz

    cd /Python-3.5.7
    # 编译
    ./configure --prefix=/usr/local/python3
    make
    make install

    # 建立软链接
    ln -s /usr/local/python3/bin/python3.5 /usr/bin/python3
    ln -s /usr/local/python3/bin/pip3.5 /usr/bin/pip3

    # 查看python3与pip3版本
    python3
    pip3 -V

  4.安装项目模块
    4.1 上传requirements.txt文件至docker容器
      docker cp /root/Downloads/requirements.txt 05e0:/root/
    4.2 从清华大学pip源安装项目依赖
      pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

  5.安装wkhtmltox
    在https://github.com/wkhtmltopdf/wkhtmltopdf/releases/ 下载对应的安装包，在这里我选择：wkhtmltox-0.12.5-1.centos6.i686.rpm
    rpm -ivh wkhtmltox-0.12.5-1.centos6.i686.rpm
    报错：
    error: Failed dependencies:
      fontconfig is needed by wkhtmltox-1:0.12.5-1.centos6.x86_64
      freetype is needed by wkhtmltox-1:0.12.5-1.centos6.x86_64
      libX11 is needed by wkhtmltox-1:0.12.5-1.centos6.x86_64
      libXext is needed by wkhtmltox-1:0.12.5-1.centos6.x86_64
      libXrender is needed by wkhtmltox-1:0.12.5-1.centos6.x86_64
      libjpeg is needed by wkhtmltox-1:0.12.5-1.centos6.x86_64
      libpng is needed by wkhtmltox-1:0.12.5-1.centos6.x86_64
      xorg-x11-fonts-75dpi is needed by wkhtmltox-1:0.12.5-1.centos6.x86_64
      xorg-x11-fonts-Type1 is needed by wkhtmltox-1:0.12.5-1.centos6.x86_64
    解决：
      # 通过yum安装
      yum install -y fontconfig freetype libX11 libXext libXrender libjpeg libpng xorg-x11-fonts-75dpi xorg-x11-fonts-Type1

    # 下载中文字体simsun.ttc复制到 linux系统 /usr/share/fonts
    docker cp /root/Downloads/simsun.ttc 05e0:/usr/share/fonts
    # 测试:
    wkhtmltopdf http://www.baidu.com ./test.pdf

  6.打包镜像上传阿里云(注意仓库所在地域)
    # 先关闭容器
    docker stop 05e0
    # 基于当前容器重新创建镜像
    docker commit -m "在centos6.8下搭建python环境" -a "root" -p 05e0 centos_py:3.56
    # -p表示提交时停止容器

    附录：使用第三方容器仓库：阿里云(需要先在阿里云镜像管理https://cr.console.aliyun.com中创建命名空间,一下tp_pro为命名空间)
    $ sudo docker login --username=miaokela registry.cn-qingdao.aliyuncs.com
    $ sudo docker tag [ImageId] registry.cn-qingdao.aliyuncs.com/tesunet/centos_py:[镜像版本号]
    $ sudo docker push registry.cn-qingdao.aliyuncs.com/tesunet/centos_py:[镜像版本号]

  7.从阿里云下载镜像
    # 创建容器,测试
    $ sudo docker pull registry.cn-qingdao.aliyuncs.com/tesunet/centos_py:[镜像版本号]
    docker tag registry.cn-qingdao.aliyuncs.com/tesunet/centos_py:[镜像版本号] centos_py:3.57
    docker run -it centos_py:3.57 /bin/bash
    pip3 list

```
















