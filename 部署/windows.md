## Windows下django+apache+mysql+redis项目部署

#### 1.Python3.54安装
```text
1.从官网下载可执行安装文件
    https://www.python.org/downloads/windows/
    选择Windows x86-64 executable installer
    # 预安装基础模块
2.添加系统环境
    如:C:\Python\python27和C:\Python\python27\Scripts
3.更新pip3
    python -m pip install --upgrade pip --force-reinstall
4.安装项目依赖
    # 先安装tornado
    pip3 install tornado-5.1.1-cp35-cp35m-win_amd64.whl
    pip3 install -r requirements.txt
5.手动下载并安装mod_wsgi    
    pip3 install mod_wsgi-4.5.24+ap24vc14-cp35-cp35m-win_amd64.whl
    
6.没网的情况下安装依赖包
    # 下载
    pip3 download -d C:\Users\Administrator\Desktop\package -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
    # 安装
    pip3 install --no-index --find-links=d:\python27\packs\ pandas （-r requirements.txt）
    
    
```

#### 2.MySQL5.6安装
```text
1.添加mysql的bin目录至系统环境
    C:\Application\MySQL\mysql-5.6.45-winx64\bin
2.创建一个my.ini的文件，放在bin目录里面，内容如下
    [mysql]
    # 设置mysql客户端默认字符集
    default-character-set=utf8 
    [mysqld]
    #设置3306端口
    port = 3306 
    # 设置mysql的安装目录
    basedir=E:/mysql-5.7.12-winx64
    # 设置mysql数据库的数据的存放目录
    datadir=E:/mysql-5.7.12-winx64/data
    # 允许最大连接数
    max_connections=200
    # 服务端使用的字符集默认为8比特编码的latin1字符集
    character-set-server=utf8
    # 创建新表时将使用的默认存储引擎
    default-storage-engine=INNODB
3.初始化数据库、安装并启动服务
    mysqld --initialize-insecure  
    mysqld -install # 如果已存在，则删除：sc delete mysql  或者 mysql -remove
    net start mysql 
4.初始化登录密码
    mysqladmin -u root password *******
5.删除无用配置
    delete from mysql.user where user='';  
    delete from mysql.user where host='::1';
6.令所用用户可以访问
    update user set host='%' where user ='root';
    flush privileges;
7.导入项目数据库(先创建数据库)
    mysql -uroot -p jx_tesudrm < jx_tesudrm.sql
```

#### 3.Redis3.2.1安装
```text
# 官网下载地址：http://redis.io/download
# github下载地址：https://github.com/MSOpenTech/redis/tags |Redis-x64-3.2.100
# 1.解压
# 2.启动:
    redis-server redis.windows.conf # 指定配置文件开启
# 3.设置redis服务(开机自启):
redis-server --service-install redis.windows.conf --loglevel verbose
# 4.常用命令:
#     卸载服务：redis-server --service-uninstall
#     开启服务：redis-server --service-start
#     停止服务：redis-server --service-stop
# 5.测试:
    redis-cli.exe -h 127.0.0.1 -p 6379
    >> ping
    >> pong
```


#### 4.Apache安装
```text
1.解压下载的压缩包：
    httpd-2.4.41-o102s-x64-vc14-r2.zip
    # 将解压出的apache24移植指定位置
2.修改配置文件
    C:\Application\Apache24\conf\httpd.conf
    
    Define SRVROOT "C:\Apache24"  #Apache24文件的路径，其余不用改。
    Listen 192.168.184.146:8000 #此处为你要发布的网站ip地址，此处我用我电脑的ip和端口，你也可以用127.0.0.1:8000用于本地测试；80端口自己设置
    ServerName 192.168.184.146:8000
3.创建apache服务(管理员权限开启终端)   
    httpd.exe -k install -n "apache2.4"  #apache2.4是所创建服务器名称，可更改。
    # 重启apache命令：httpd.exe -k restart
4.访问测试：192.168.184.146:8000
5.配置mod_wsgi
    5.1 查看mod_wsgi路径
        mod_wsgi-express module-config
        >> 记录下来
        LoadFile "c:/application/python35/python35.dll"
        LoadModule wsgi_module "c:/application/python35/lib/site-packages/mod_wsgi/server/mod_wsgi.cp35-win_amd64.pyd"
        WSGIPythonHome "c:/application/python35"
    5.2 设置django静态文件路径
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
    
    5.2 修改配置文件httpd.conf
        #安装wsgi模块后，出来的三行字符，直接复制过来
        LoadFile "c:/application/python35/python35.dll"
        LoadModule wsgi_module "c:/application/python35/lib/site-packages/mod_wsgi/server/mod_wsgi.cp35-win_amd64.pyd"
        WSGIPythonHome "c:/application/python35"
        #设置工程中的wsgi路径
        WSGIScriptAlias / C:\Pro\Tools\TSDRM\TSDRM\wsgi.py
        #设置工程路径
        WSGIPythonPath  C:\Pro\Tools\TSDRM
        #设置wsgi路径
        <Directory C:\Pro\Tools\TSDRM\TSDRM>
            <Files wsgi.py>
                Require all granted
            </Files>
        </Directory>
        #设置静态文件路径
        Alias /static C:\Pro\Tools\TSDRM\static
        <Directory C:\Pro\Tools\TSDRM\static>  
            AllowOverride None  
            Options None  
            Require all granted  
        </Directory> 
 6.注意:不要导入	win_unicode_console
 7.将wkhtmltopdf应用软件拷贝至apache目录下
    # 新建文件faconstor
    拷贝static文件夹至faconstor
```













