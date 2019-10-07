# Oracle DataGuard

## 1.Oracle 11g安装
```
1.1 关闭selnux
    vi /etc/selinux/config
    # 修改SELINUX=disabled
1.2 关闭防火墙
    chkconfig iptables off
    service iptables stop
1.3 修改参数内核
    vi /etc/sysctl.conf
    fs.aio-max-nr = 1048576
    fs.file-max = 6815744
    kernel.shmall = 2097152
    kernel.shmmax = 536870912
    kernel.shmmni = 4096
    kernel.sem = 250 32000 100 128
    net.ipv4.ip_local_port_range = 9000 65500
    net.core.rmem_default = 262144
    net.core.rmem_max = 4194304
    net.core.wmem_default = 262144
    net.core.wmem_max = 1048586
    
    sysctl -p
1.4 修改/etc/pam.d/login，# vi /etc/pam.d/login,在文本末尾加上：
    session    required /lib64/security/pam_limits.so
    session    required pam_limits.so
1.5 创建oracle用户与用户组
    groupadd oinstall
    groupadd dba
    useradd -g oinstall -G dba oracle
    # 设置oracle用户密码
    passwd oracle
1.6 修改oracle最大进程数
    vi /etc/profile
    if [ $USER = "oracle" ]; then 
    if [ $SHELL = "/bin/ksh" ]; then 
        ulimit -p 16384 
        ulimit -n 65536 
    else 
        ulimit -u 16384 -n 65536 
    fi
    fi
    # 保存退出后，令其生效
    source /etc/profile
1.7 限制用户资源
    vi /etc/security/limits.conf
    oracle  soft  nproc 2047
    oracle  hard  nproc 16384
    oracle  soft  nofile  1024
    oracle  hard  nofile  65536
    oracle  hard  stack 10240
1.8 配置环境变量
    # 创建oracle目录
    mkdir -p /u01/app/oracle
    chown -R oracle:oinstall /u01/app/
    chmod -R 775 /u01/app/
1.9 配置oracle环境
    su - oracle
    vi .bash_profile
    export ORACLE_BASE=/u01/app/oracle
    export ORACLE_HOME=/u01/app/oracle/product/11.2.0/dbhome_1
    export ORACLE_SID=orcl
    export PATH=$ORACLE_HOME/bin:$PATH:$HOME/bin
    export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/usr/lib
    
    source .bash_profile

1.10 安装依赖软件包
    yum -y install  binutils
    yum -y install  compat-libstdc++
    yum -y install  glibc*
    yum -y install  elfutils-libelf
    yum -y install  elfutils-libelf-devel
    yum -y install  libaio
    yum -y install  libgcc
    yum -y install  libstdc++*
    yum -y install  make
    yum -y install  compat-libcap1
    yum -y install  gcc
    yum -y install  gcc-c++
    yum -y install  glibc-devel
    yum -y install  libaio-devel
    yum -y install  libstdc++-devel
    yum -y install  sysstat
    yum -y install  unixODBC*

1.11 安装oracle数据库
    1.11.1 解压两个压缩包之后的database目录下执行./runInstaller
        # 不设置邮箱
        # 仅安装数据库软件
        # 单实例安装
        # 选择简体中文/繁体中文
        # 选择企业版
        # 其他均下一步
    1.11.2
        netca
        dbca
```


## 2.搭建OracleDG
```
参考博客：https://www.cnblogs.com/pymkl/articles/11340694.html
```





































