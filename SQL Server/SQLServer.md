## 使用SQLServer作为Django的Backend

- 1.安装SQLServer 2012  
    > 参考博文：https://blog.csdn.net/u013162035/article/details/78567389  
    > 新增用户 >> 取消强制密码过期 >> 新增数据库datacenter(权限)
    + 1.1 开启1433端口  
        > 参考博文：https://www.cnblogs.com/daqi-work/archive/2019/07/19/11214165.html  
        > 我的电脑-管理-SQL Server网络配置-SQLEXPRESS的协议-双击，修改TCP端口(win2012搜索SQL Server配置管理器)
        > 需要重启SQL Server  
        
- 2.安装/更新相关版本模块
    > 针对django版本安装对应的django-pyodbc-azure  
    > 由于django-pyodbc-azure没有django 1.9.7版本，故重新选择安装django==1.9.12，  
    > 并安装django-pyodbc-azure==1.9.12  
    
- 3.配置Django项目settings.py  
    ```
    DATABASES = {
        'default': {
            'ENGINE': 'sql_server.pyodbc',
            'NAME': 'datacenter',
            'USER': 'miaokela',
            'PASSWORD': 'Passw0rD',
            'HOST': '127.0.0.1',
            'PORT': '1433',
            'OPTIONS': {
                'driver': 'SQL Server Native Client 11.0',  # Windows管理工具>>ODBC源数据>>点击添加即可查看驱动
            },
        },
    }
    ```

- 4.迁移Migrate  
    > python manage.py migrate  

- 5.导入数据文件  
    + 5.1 数据为MySQL数据库  
        > 参考博文：https://www.cnblogs.com/Wolfmanlq/p/6109731.html  
        > 注意将MySQL数据库名修改成dbo
    
    + 5.2 数据为SQLServer数据库
        > 参考博文：https://blog.csdn.net/qq_36923376/article/details/83420751  
        > 分离-关闭远程SQL Server服务-覆盖两个文件-启动
    
- 6.问题解决  
    + 6.1 MySQL数据库导入SQL Server  
        ```
        Django Migrate在SQL Server中生成的表以用户拥有名称dbo.开头，而MySQL数据直接迁移至SQL Server
        以MySQL数据库名开头，故将MySQL表名修改成dbo，再做导入
        ```
    + 6.2 SQL Server数据库中唯一索引null重复也算  
        > 注意SQL Server中一对一外键的使用，不要出现空的情况  
        > 故，在导入数据时UserInfo表出现问题，在程序中org组织新增时，添加无用用户，设置is_active=0、is_staff=0
    






































