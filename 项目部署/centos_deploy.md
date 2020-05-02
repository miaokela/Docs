
## Centos6下Django环境部署
- `-1.离线依赖软件安装`
  ```
  yum install -y --downloadonly --downloaddir=./packages/ openssl-devel
  yum localinstall -y --nogpgcheck ./packages/*rpm
  ```


- `0.Centos源修改(先确定是否已装wget)`
    ```
    mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
    wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo
    yum makecache
    yum update -y
    ```

- `1.Python环境部署`
    + 1.1 安装Python3.5
         ```
        # 安装依赖
        yum -y groupinstall "Development tools"
        yum install openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel gcc gcc-c++ -y

        # 解压
        tar -zxvf Python-3.5.4.tgz

        cd /Python-3.5.4
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
         ``` 
- `2.安装Redis`
	+ 2.1 下载安装包
        ```
        wget http://download.redis.io/releases/redis-3.2.1.tar.gz  
        wget http://downloads.sourceforge.net/tcl/tcl8.6.1-src.tar.gz
        ``` 
	+ 2.2 安装redis与tcl
        ```
        sudo tar xzvf tcl8.6.1-src.tar.gz -C /usr/local/  
        cd  /usr/local/tcl8.6.1/unix/  
        sudo ./configure  
        sudo make  
        sudo make install   
        ```
        ```
        1.解压
        cd /opt/
        tar zxvf ...tar.gz
        3.进入redis目录
        cd /opt/redis-3.2.1
        4.编译安装
        make
        cd src
        make install
        5.测试(对make做检测)
        make test
        7.配置文件
        配置文件目录为/usr/local/redis/redis.conf
        mkdir /etc/redis/ -p
        >> 配置内容：
        >> bind:127.0.0.1
        >> daemonize yes
        >> requirepass tesunet
        >> protected-mode no
        cp /opt/redis-3.2.1/redis.conf /etc/redis/6379.conf
        8.配置服务，开机自启
        # redis默认不支持chconfig
        # edis服务必须在运行级2，3，4，5下被启动或关闭，启动的优先级是90，关闭的优先级是10。
        # 头部添加：
        #!/bin/sh
        # chkconfig: 2345 90 10

        vi /opt/redis-3.2.1/utils/redis_init_script

        cp /opt/redis-3.2.1/utils/redis_init_script /etc/init.d/redis
        chmod +x /etc/init.d/redis
        chkconfig redis on

        9.redis服务的启动与关闭
        service redis start
        service redis stop
        # 强制杀进程
        ps -ef|grep redis | grep -v grep|cut -c 9-15|xargs kill -9
        ps -ef|grep nginx | grep -v grep|cut -c 9-15|xargs kill -9
        ps -ef|grep celery | grep -v grep|cut -c 9-15|xargs kill -9
        ```

- `3.安装MySQL`
    >>>
    `3.1 免编译方式安装：(方便)`
    ```
    # 解压
    tar xvf mysql-5.6.46-linux-glibc2.12-x86_64.tar.gz
    mv mysql-5.6.46-linux-glibc2.12-x86_64 /usr/local/mysql

    # 安装
    /usr/local/mysql/scripts/mysql_install_db --user=mysql --basedir=/usr/local/mysql --datadir=/usr/local/mysql/data

    # 复制mysql配置文件
    cd /usr/local/mysql/support-files
    cp my-default.cnf /etc/my.cnf

    # 添加系统服务
    cp mysql.server /etc/init.d/mysql
    chkconfig mysql on

    # 添加环境变量
    vim /etc/profile
    >>
    export MYSQL_HOME="/usr/local/mysql"
    export PATH="$PATH:$MYSQL_HOME/bin"
    >>
    source /etc/profile

    # 配置
    vim /etc/my.cnf
    >>
    [mysql]
    default-character-set=utf8

    [mysqld]
    basedir=/usr/local/mysql
    datadir=/usr/local/mysql/data
    port=3306
    server_id=1
    socket=/tmp/mysql.sock
    symbolic-links=0
    character-set-server=utf8
    default-storage-engine=INNODB

    [mysqld_safe]
    log-error=/var/log/mysqld.log
    pid-file=/var/run/mysqld/mysqld.pid

    # 启动mysql
    service mysql start

    # 设置密码
    mysqladmin -u root password 'password'

    # 令所有用户可以访问
    GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'password' WITH GRANT OPTION;
    FLUSH PRIVILEGES;
    ```
    #
    `3.2 cmake编译方式安装：`
    >>>
  + 0.检查系统是否安装其他版本的MYSQL数据
    ```
    yum list installed | grep mysql
    yum -y remove mysql-libs.x86_64
    ```

  + 1.检查Linux版本(忽略)
    ```
    [root@mysqlcmake ~]# cat /etc/redhat-release 
    CentOS release 6.10 (Final)
    [root@mysqlcmake ~]# uname -r  # 内核
    2.6.32-754.17.1.el6.x86_64
    [root@mysqlcmake ~]# uname -m  # 系统版本
    x86_64
    ```
  + 2.安装cmake
    ```
    # cmake下载地址:https://cmake.org/files/v2.8/
    tar xzf cmake-2.8.8.tar.gz 
    cd cmake-2.8.8  # >> CMake has bootstrapped.  Now run gmake.
    ./configure --prefix=/opt/cmake
    gmake
    make&&make install
    cd ..
    ln -s /opt/cmake/bin/cmake /usr/local/bin/cmake
    ```
  + 3.安装依赖包
    ```
    yum install ncurses-devel -y
    ```
  + 4.添加用户和组(忽略)
    ```
    groupadd mysql
    useradd mysql -s /sbin/nologin -M -g mysql
        -s表示指定用户所用的shell，此处为/sbin/nologin，表示不登录。
        -M表示不创建用户主目录。
        -g表示指定用户的组名为mysql。
    ```
  + 4.安装MySQL
    ```
    tar xzf mysql-5.5.62.tar.gz 
    cd mysql-5.5.62

    cmake . -DCMAKE_INSTALL_PREFIX=/opt/mysql \
    -DMYSQL_DATADIR=/opt/mysql/data \
    -DMYSQL_UNIX_ADDR=/opt/mysql/tmp/mysql.sock \
    -DWITH_EXTRA_CHARSETS=gbk,gb2312,utf8,ascii \
    -DENABLED_LOCAL_INFILE=ON \
    -DWITH_INNOBASE_STORAGE_ENGINE=1 \
    -DWITH_FEDERATED_STORAGE_ENGINE=1 \
    -DWITH_BLACKHOLE_STORAGE_ENGINE=1 \
    -DWITHOUT_EXAMPLE_STORAGE_ENGINE=1 \
    -DWITHOUT_PARTITION_STORAGE_ENGINE=1 \
    -DWITH_FAST_MUTEXES=1 \
    -DWITH_ZLIB=bundled \
    -DENABLED_LOCAL_INFILE=1 \
    -DWITH_READLINE=bundled \
    -DWITH_EMBEDDED_SERVER=1 \
    -DWITH_DEBUG=0 \
    
    -DDEFAULT_CHARSET=utf8 \
    -DDEFAULT_COLLATION=utf8_general_ci
    
    make&&make install
    ```
  + 5.创建MySQL数据库配置文件并对数据库目录授权
    ```
    # MySQL5.5数据库默认为用户提供了多个配置文件模板，但是MySQL5.6的support-files目录下已经没有配置文件模板了
    cd /root/Downloads/mysql-5.5.62
    cp support-files/my-small.cnf /etc/my.cnf  # 用最小的文件，生产可以根据硬件选择：my-innodb-heavy-4G.cnf
    ```
  + 6.配置环境变量
    ```
    echo 'export PATH=/opt/mysql/bin:$PATH' >> /etc/profile
    tail -l /etc/profile
    source /etc/profile
    echo $PATH
    ```
  + 7.初始化数据库文件
    ```
    chown -R mysql.mysql /opt/mysql/
    chown -R 1777 /tmp/  # 1777 粘贴位，作用是让用户无法删除文件，只可以进行读写
    
    cd /opt/mysql/scripts/
    ./mysql_install_db --basedir=/opt/mysql/ --datadir=/opt/mysql/data --user=mysql

    # --basedir=/opt/mysql/为MySQL的安装路径，--datadir为数据文件目录。
    # 另，注意mysql_install_db和MySQL5.1的路径不同，MySQL5.1不在MySQL bin路径下了
    ```
  + 8.配置并启动MySQL数据库
    ```
    cd /root/Downloads/mysql-5.5.62
    cp support-files/mysql.server   /etc/init.d/mysqld
    chmod +x /etc/init.d/mysqld
    /etc/init.d/mysqld start
    # 解决错误
    #  mysqld_safe Directory '/opt/mysql-5.5.62/tmp' for UNIX socket file don't exists.
    mkdir /opt/mysql-5.5.62/tmp
    chown -R mysql.mysql /opt/mysql/
    ```
  + 9.初始化密码
    ```
    /opt/mysql/bin/mysqladmin -u root password 'password'
    ```
  + 10.删除无用配置
    ```
    select user,host from mysql.user;  
    delete from mysql.user where user='';  
    delete from mysql.user where host='mysqlcmake';  # 可能是你设置的host  
    delete from mysql.user where host='::1';  
    剩下：  
    +------+-----------+
    | user | host      |
    +------+-----------+
    | root | 127.0.0.1 |
    | root | localhost |
    +------+-----------+
    ```
  + 11.开机自启
    ```
    chkconfig mysqld on
    chkconfig --list mysqld
    ```
  + 12.查看系统安装语言
    ```
    cat /etc/sysconfig/i18n
    # 如果没有，则添加LANG="en_US.UTF-8"
    ```

- `4.安装Nginx`
    ```
   # nginx前置库
    yum install -y gcc pcre pcre-devel openssl openssl-devel gd gd-devel
    # 在/home目录下
    wget http://nginx.org/download/nginx-1.13.7.tar.gz

    # 解压/配置
    tar -zxvf nginx-1.13.7.tar.gz
    cd nginx-1.13.7
    ./configure
    make
    make install

    # 备份nginx配置文件
    cd /usr/local/nginx/conf/
    cp nginx.conf nginx.conf.bak

    # 修改nginx配置(删除原有的)
    worker_processes  1;
    events {
        worker_connections  1024;
    }
    http {
        include       mime.types;
        default_type  application/octet-stream;
        sendfile        on;
        server {
            listen       80;
            server_name  localhost;
            charset utf-8;
            location / {
                include uwsgi_params;
                uwsgi_pass 0.0.0.0:8007;
                uwsgi_param UWSGI_SCRIPT TSDRM.wsgi;
                uwsgi_param UWSGI_CHDIR /var/www/html/TSDRM;
            }
            location /static/ {
                alias /var/www/html/TSDRM/static/;
            }
        }
    }

    # 启动nginx
    /usr/local/nginx/sbin/nginx
    # /usr/local/nginx/sbin/nginx -t 检查
    # /usr/local/nginx/sbin/nginx -s reload 重启nginx 
    ```
- `5.配置运行uwsgi`
    ```
    # 复制项目至/opt/   创建TSDRM_ADG,unzip TSDRM_ADG
    pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
    pip3 install uwsgi -i https://pypi.tuna.tsinghua.edu.cn/simple/
    ln -s /usr/local/python3/bin/uwsgi /usr/bin/uwsgi

    # pyodbc另外装
    yum install unixODBC unixODBC-devel -y
    pip3 install pyodbc -i https://pypi.tuna.tsinghua.edu.cn/simple/
    
    # 配置uwsgi
    # 在项目目录下创建uwsgi.ini
    [uwsgi]
    socket=0.0.0.0:8007 # 配置nginx代理时使用
    #http=0.0.0.0:8000
    chdir=/opt/TSDRM_ADG
    #module=TSDRM.wsgi:application
    wsgi-file=/opt/TSDRM_ADG/TSDRM/wsgi.py
    master=True
    process=4
    pidfile=/opt/TSDRM_ADG/TSDRM-master.pid
    vacuum=True
    max-requests=5000
    daemonize=/opt/TSDRM_ADG/log/wsgi.log
    static-map=/static=/opt/TSDRM_ADG/static

    
    uwsgi --ini uwsgi.ini
    # 重启uwsgi
    uwsgi --reload TSDRM-master.pid

    # 重启nginx
    # 此时项目就可以访问了，只是静态文件未读取？？？

    # 解决静态文件问题
    # settings.py文件中写入静态文件物理路径(已经写了)
    SITE_ROOT=os.path.join(os.path.abspath(os.path.dirname(__file__)),'..')
    STATIC_ROOT = os.path.join(SITE_ROOT,'static')

    # 添加静态文件访问逻辑路径
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static')
    ]

    # 收集静态文件
    python3 manage.py collectstatic

    # 注销掉物理路径
    # STATIC_ROOT,SITE_ROOT

    # 重新启动nginx与uwsgi
    ```

- `8.wkhtmltopdf安装`
  ```
  	# 注意：要安装带有qt的软件，不然会报错
    cd ~
    wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.3/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
    tar vxf wkhtmltox-0.12.3_linux-generic-amd64.tar.xz 
    cp wkhtmltox/bin/wk* /usr/local/bin/

    # 下载中文字体simsun.ttc复制到 linux系统 /usr/share/fonts
    docker cp /root/Downloads/simsun.ttc 容器ID:/usr/share/fonts
    测试使用：
    wkhtmltopdf http://www.baidu.com ./test.pdf
  ```
- `9.安装cv_Oracle`
    ````
    1.下载oracle Client
    https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html

    2.安装脚本
    #!/bin/bash

    # INSTALL ORACLE INSTANT CLIENT #
    #################################

    # NOTE: Oracle requires at least 1176 MB of swap (or something around there).
    # If you are using CentOS in a VMWare VM, there's a good chance that you don't have enough by default.
    # If this describes you and you need to add more swap, see the
    # "Adding a Swap File to a CentOS System" section, here:
    # http://www.techotopia.com/index.php/Adding_and_Managing_CentOS_Swap_Space

    # Install basic dependencies
    sudo yum -y install libaio bc flex

    echo "Now go get some the following two RPMs ..."
    echo "- basic: oracle-instantclient11.2-basic-11.2.0.3.0-1.x86_64.rpm"
    echo "- SDK/devel: oracle-instantclient11.2-devel-11.2.0.3.0-1.x86_64.rpm"
    echo "... from this URL: http://www.oracle.com/technetwork/topics/linuxx86-64soft-092277.html"
    echo "WARNING: It's pretty annoying, they make you sign up for an Oracle account, etc."
    echo 'I will assume you have put these two files are into ~/Downloads'
    echo "Press any key once you're ready" && read -n 1 -s

    sudo rpm -ivh /opt/oracle-instantclient11.*

    # SET ENVIRONMENT VARIABLES #
    #############################

    # Source for this section: http://cx-oracle.sourceforge.net/BUILD.txt

    # (SIDENOTE: I had to alter it by doing some digging around for where the Oracle RPMs really installed to;
    # if you ever need to do this, do a command like this:
    #     rpm -qlp )

    echo '# Convoluted undocumented Oracle bullshit.' >> $HOME/.bashrc
    echo 'export ORACLE_VERSION="11.1"' >> $HOME/.bashrc
    echo 'export ORACLE_HOME="/usr/lib/oracle/$ORACLE_VERSION/client64/"' >> $HOME/.bashrc
    echo 'export PATH=$PATH:"$ORACLE_HOME/bin"' >> $HOME/.bashrc
    echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:"$ORACLE_HOME/lib"' >> $HOME/.bashrc
    . $HOME/.bashrc

    # INSTALL cx_Oracle #
    #####################

    pip3 install cx_Oracle==5.2 -i https://pypi.tuna.tsinghua.edu.cn/simple/

    ````

- `10.supervisor启动后台进程`
  ```
  pip3 install supervisor -i https://pypi.tuna.tsinghua.edu.cn/simple/

  # 如果在debian系统，已经存在该命令
  ln -s /usr/local/python3/bin/echo_supervisord_conf /usr/bin/echo_supervisord_conf
  ln -s /usr/local/python3/bin/supervisorctl /usr/bin/supervisorctl
  ln -s /usr/local/python3/bin/supervisord /usr/bin/supervisord

  # 生成配置文件
  echo_supervisord_conf > /etc/supervisord.conf

  # 修改配置文件
  [program:uwsgi]        
  command=uwsgi --ini uwsgi.ini
  directory=/TSDRM/

  numprocs=1
  stdout_logfile=/TSDRM/log/spvs_uwsgi_std.log
  stderr_logfile=/TSDRM/log/spvs_uwsgi_err.log
  autostart=true
  autorestart=true
  startsecs=10
  stopwaitsecs=600
  priority=15


  [program:celery.worker]  
  command=python3 manage.py celery -A TSDRM worker -l info --logfile=/TSDRM/log/worker.log
  directory=/TSDRM/

  numprocs=1
  stdout_logfile=/TSDRM/log/spvs_worker_std.log
  stderr_logfile=/TSDRM/log/spvs_worker_err.log
  autostart=true
  autorestart=true
  startsecs=10
  stopwaitsecs=600
  priority=16

  [program:celery.flower]  
  command=python3 manage.py celery -A TSDRM flower -l info --logfile=/TSDRM/log/flower.log
  directory=/TSDRM/

  numprocs=1
  stdout_logfile=/TSDRM/log/spvs_flower_std.log
  stderr_logfile=/TSDRM/log/spvs_flower_err.log
  autostart=true
  autorestart=true
  startsecs=10
  stopwaitsecs = 600
  priority=17

  [program:celery.beat]
  command=python3 manage.py celery -A TSDRM flower -l info --logfile=/TSDRM/log/beat.log
  directory=/TSDRM/

  numprocs=1
  stdout_logfile=/TSDRM/log/spvs_beat_std.log
  stderr_logfile=/TSDRM/log/spvs_beat_err.log
  autostart=true
  autorestart=true
  startsecs=10
  stopwaitsecs = 600
  priority=18

  # 启动
  supervisord -c /etc/supervisord.conf

  ```















