## Oracle相关知识

- 1.Oracle的关闭与开启
    ```
    数据库 >> 监听 >> isqlplus/OEM
    ```
    + 1.1 关闭isqlplusctl
        > netstat -tulnp|grep 5560  
        > isqlplusctl stop
    + 1.2 关闭OEM
        > emctl status dbconsole/netstat -tulnp|grep 1158  
        > emctl stop dbconsole
    + 1.3 关闭监听
        > lsnrctl status/netstat -tulnp|grep 1521  
        > lsnrctl stop  
    + 1.4 关闭数据库
        > sqlplus / as sysdba  
        > shutdown immediate;  
        > ps -ef|grep oracle

    + 1.5 启动监听
        > lsnrctl start
    + 1.6 启动数据库
        > sqlplus / as sydba  
        > startup
    + 1.7 启动isqlplusctl
        > isqlplusctl start
    + 1.8 启动OEM
        > emctl start dbconsole  
        > `EM一旦建立就不要修改主机名，否则EM无法启动`   
        > 访问：(https://localhost:5500/em/console/aboutApplication)
        > EM修改时区:

- 2.Oracle体系结构
    + 2.1 Oracle数据库
        ```
        1) 控制文件
        2) 数据文件
        3) 日志文件

        4) 内存结构
            共享池
            重做日志缓冲区
            Buffer缓冲区
        ```


































