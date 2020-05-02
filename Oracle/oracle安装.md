## Oracle 11g安装(Centos6.8)

- 1.系统条件
    + 1.1 硬件需求
        ```
        1) 内存
            RAM:2G以上
            查看：grep MemTotal /proc/meminfo
            swap：RAM 4G以内时，是RAM的两倍，>4G就等于RAM
            查看：grep SwapTotal /proc/meminfo
        ```
    + 1.2 软件需求
        ```
        1) 内核需求
            Oracle Linux4 and Red Hat Enterprise Linux4
            2.6.9 or later

            查看： uname -r (2.6.32-642.el6.x86_64)需要升级内核
            >> mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
            >> wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo
            >> yum makecache
            >> yum update nss
            >> rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
            >> rpm -Uvh https://www.elrepo.org/elrepo-release-6-8.el6.elrepo.noarch.rpm
            >> yum --enablerepo=elrepo-kernel -y install kernel-lt
            >> vi /etc/grub.conf 修改default为0
            >> reboot
        2) 包依赖
            yum -y install  binutils
            yum -y install  compat-libstdc++
            yum -y install  glibc*
            yum -y install  expat
            yum -y install  elfutils-libelf
            yum -y install  elfutils-libelf-devel
            yum -y install  libaio
            yum -y install  libgcc
            yum -y install  libstdc++*
            yum -y install  make
            yum -y install  numactl
            yum -y install  compat-libcap1
            yum -y install  pdksh
            yum -y install  gcc
            yum -y install  gcc-c++
            yum -y install  glibc-devel
            yum -y install  libaio-devel
            yum -y install  libstdc++-devel
            yum -y install  sysstat
            yum -y install  unixODBC*
        ```
    + 1.3 扩大系统限制  
        ```
        1) 最大进程
            vi /etc/profile
            if [ $USER = "oracle" ]; then 
            if [ $SHELL = "/bin/ksh" ]; then 
                ulimit -p 16384 
                ulimit -n 65536 
            else 
                ulimit -u 16384 -n 65536 
            fi
            fi
            >> source /etc/profile
        2) 资源限制
            vi /etc/security/limits.conf
            oracle  soft  nproc 2047
            oracle  hard  nproc 16384
            oracle  soft  nofile  1024
            oracle  hard  nofile  65536
            oracle  hard  stack 10240
        3) 内核参数
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
            >> /sbin/sysctl -p
        4) 要使 limits.conf 文件配置生效，必须要确保 pam_limits.so 文件被加入到启动文件中
            >> vi /etc/pam.d/login
            session    required /lib64/security/pam_limits.so
        ```
    + 1.4 关闭防火墙
        ```
        # chkconfig iptables off
        # service iptables stop
        ```
    + 1.5 /etc/hosts文件添加ip 主机名

- 2.创建用户/用户组/文件目录
    ```
    groupadd oinstall 
    groupadd dba
    useradd -g oinstall -G dba oracle
    passwd oracle

    mkdir -p /u01/app/oracle
    chown -R oracle:oinstall /u01/app/
    chmod -R 775 /u01/app/

    >> su - oracle
    >> vi .bash_profile
    export ORACLE_BASE=/u01/app/oracle
    export ORACLE_HOME=/u01/app/oracle/product/11.2.0/dbhome_1
    export ORACLE_SID=orcl
    export PATH=$ORACLE_HOME/bin:$PATH:$HOME/bin
    ```

- 3.Oracle安装  
    ```
    cd /database   
    ./runInstaller  
    netca  
    dbca  
    ```




