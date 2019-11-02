## Oracle

### 1.物理层面

#### 1.1 查看已安装Oracle的相关信息
```
1) Oracle实例
    select * from v$instance;

2) Oracle安装路径
    Oracle Inventory 目录: 和ORACLE_BASE同级的一个目录。这个目录用来保存本机上所安装的Oracle 软件的目录清单
    Oracle Base 目录: Oracle软件安装的最顶层目录。这个目录下可以安装多个版本的Oracle软件
    Oracle Home 目录: 软件安装位置

3) 控制文件信息
    1.控制文件：
        a.一个非常小的二进制文件；
        b.记录重做日志、数据文件的名字和位置，以及归档重做日志历史等数据库状态信息；
        c.在数据库启动的MOUNT阶段被读取；

    2.数据库启动时读取文件的顺序：
        a.打开参数文件，读取控制文件位置信息；
        b.从控制文件中读取数据库各种文件的位置；
        c.打开数据库；

    3.查看控制文件路径
        select name, status from v$controlfile;
        select value from v$parameter where name='control_files';
        show parameter control_files;
    4.控制文件所存的内容：
        a.数据库名称；
        b.数据库标识符；
        c.数据库创建时间；
        d.表空间信息；
        e.重做日志文件历史；
        f.归档日志文件的位置和状态信息；
        g.备份的状态信息和位置；
        h.当前日志序列号；
        i.检验点信息；
    5.ALTER SYSTEM指令修改SPFILE的参数：
        a.获取控制文件名：
            select * from v$controlfile;
            >>
                STATUS    NAME             IS_ BLOCK_SIZE FILE_SIZE_BLKS
                ------- -------------------- --- ---------- --------------
                    /u01/app/oracle/orad NO       16384           594
                    ata/orcl/control01.c
                    tl

                    /u01/app/oracle/orad NO       16384           594
                    ata/orcl/control02.c
                    tl
        b.使用alter system set指令修改SPFILE中的控制文件名
            alter system set control_files='/.../.../control01.ctl','/.../.../control02.ctl' scope=spfile;
        c.关闭数据库：
            shutdown immediate
        d.将控制文件control01.ctl，control02.ctl复制到更改的目录下。
        e.重启数据库：
            startup
        f.验证是否使用PFILE启动数据库：
            show parameter spfile;
            # value不为空，说明此时使用SPFILE文件启动数据库。
        g.验证控制文件的修改结果：
            select status, name from v$controlfile;

4) 日志/日志组管理
    1.查看日志文件信息
        desc v$logfile;
        Name                       Null?    Type
        ----------------------------------------- -------- ----------------------------
        GROUP#                         NUMBER
        STATUS                         VARCHAR2(7)
        TYPE                            VARCHAR2(7)
        MEMBER                         VARCHAR2(513)
        IS_RECOVERY_DEST_FILE            VARCHAR2(3)

    2.查看当前数据库是否为归档模式
        select name, log_mode from v$database;
        NAME      LOG_MODE
        --------- ------------
        ORCL      ARCHIVELOG  # 表示归档

    3.新增日志文件组
        ALTER DATABASE [database_name] ADD LOGFILE GROUP n filename SIZE m
        # 省略database_name，表示当前数据库
        ALTER DATABASE ADD LOGFILE GROUP 8 '/.../...log' SIZE 15M;
    4.添加日志文件到日志文件组
        ALTER DATABASE [database_name] ADD LOGFILE MEMBER filename TO GROUP n;
        ALTER DATABASE ADD LOGFILE MEMBER '/.../...log' TO GROUP 1;

    5.删除日志组合日志文件
        # 删除日志组
        ALTER DATABASE [database_name] DROP LOGFILE GROUP n;
        ALTER DATABASE DROP LOGFILE GROUP 4;
        # 删除日志文件
        ALTER DATABASE [database_name] DROP LOGFILE MEMBER filename;
        ALTER DATABASE DROP LOGFILE MEMBER '/.../..';

    6.查询日志文件组和日志文件
        # 查看日志组
        SELECT GROUP#, MEMBERS, STATUS FROM V$LOG;
        GROUP#    MEMBERS   STATUS
        ---------- ---------- ----------------
            1        1       INACTIVE
            2        1       CURRENT
            3        1       INACTIVE

        # 查看日志文件
        COL MEMBER FORMAT A150;  # A150表示展示宽度
        SELECT GROUP#, MEMBER FROM V$LOGFILE;
        GROUP#
        ----------
        MEMBER
        --------------------------------------------------------------------------------
            1
        /u01/app/oracle/oradata/orcl/redo01.log

            2
        /u01/app/oracle/oradata/orcl/redo02.log

            3
        /u01/app/oracle/oradata/orcl/redo03.log

5) 重做日志管理
    1.数据库运行过程中，用户更改数据会暂时存放在数据库高速缓冲区，以提高写数据库的速度，
    要等到数据库高速缓冲区中的数据到一定条件，DBWR进程才会将数据提交到数据库中；

    2.日志写优先：
        LGWR进程负责把用户更改的书库优先写到重做日志文件中；

    3.重做日志结构：
        Oracle规定每个数据库实例至少有两个重做日志组，每个重做日志组至少有一个重做日志文件；
    
    4.非归档模式：
        在重新使用新的联机重做日志前，DBWR进程需要将所有数据更改写到数据文件中；

    5.归档模式：
        当前正在使用的重做日志写满后，Oracle会关闭当前日志文件，ARCH进程需要把旧的日志文件中的
        数据移动到归档重做日志文件中；
        如果ARCH进程没有完成，就没有已经归档的联机重做日志可以切换，只有ARCH进程释放了联机重做日志后，
        数据库才可以继续工作；

    6.查看重做日志信息:
        select group#, sequence#, bytes, members, archived, status from v$log;
        >>
            GROUP#  SEQUENCE#       BYTES    MEMBERS ARC STATUS
        ---------- ---------- ---------- ---------- --- ----------------
            1        0            52428800      1     YES UNUSED
            2        0            52428800      1     YES CURRENT
            3        0            52428800      1     YES UNUSED

    7.查看重做日志组的信息：
        col member for a50;
        select group#, status, type, member from v$logfile;
        >>
            GROUP# STATUS  TYPE    MEMBER
        ---------- ------- ------- --------------------------------------------------
            1       ONLINE  /u01/app/oracle/oradata/orcl/redo01.log
            2       ONLINE  /u01/app/oracle/oradata/orcl/redo02.log
            3       ONLINE  /u01/app/oracle/oradata/orcl/redo03.log
            4       STANDBY /u01/app/oracle/oradata/orcl/stdred001.log
            5       STANDBY /u01/app/oracle/oradata/orcl/stdred002.log
            6       STANDBY /u01/app/oracle/oradata/orcl/stdred003.log
            7       STANDBY /u01/app/oracle/oradata/orcl/stdred004.log
        # STATUS参数：
            STALE:      内容不完整
            空白：      日志组正在使用
            INVALID:    文件不能访问
            DELETED:    文件已经不能再使用

    8.判断是否处于归档模式：
        archive log list;
        >>
            Database log mode           Archive Mode
            Automatic archival           Enabled
            Archive destination           /u01/app/oracle/product/11.2.0/dbhome_1/dbs/arch
            Oldest online log sequence     0
            Next log sequence to archive   0
            Current log sequence           0

    9.设置归档模式：
        # 首先要关闭数据库，再启动数据库到mount状态
        shutdown immediate;
        startup nomount;
        alter database mount;
        alter database archivelog;

    10.查看归档文件的存储目录及大小：
        show parameter db_recovery_file_dest;
        >>
            NAME                     TYPE     VALUE
            ------------------------------------ ----------- ------------------------------
            db_recovery_file_dest             string
            db_recovery_file_dest_size         big integer 0

    11.重做日志组管理：
        a.指定group组号添加重做日志组：
            alter database add logfile group 4 ('d:\temp\redo04a.log', 'd:\temp\redo04b.log') size 11M;
        b.验证结果:
            select * from v$logfile;
        c.在原有日志组号基础上添加重做日志组(缺掉group参数)
            alter database add logfile ('d:\temp\redo04a.log', 'd:\temp\redo04b.log') size 11M;
        d.查看当前重做日志组的使用情况
            select group#, sequence#, bytes, members, archived, status from v$log;
            >>
                GROUP#  SEQUENCE#       BYTES    MEMBERS ARC STATUS
            ---------- ---------- ---------- ---------- --- ----------------
                1        0    52428800      1 YES UNUSED
                2        0    52428800      1 YES CURRENT
                3        0    52428800      1 YES UNUSED

    12.删除重做日志组：
        alter database drop logfile group4, group5;
        # 当前的重做日志组和处于ACTIVE状态的日志组都无法删除，如果要删除当前在用的日志组，必须先进行日志切换；
        # 验证日志组成员是否删除
        select * from v$logfile;
        # 验证日志组是否删除
        select group#,sequence#,bytes,members,arachived,status from v$log;
    注意：使用指令删除重做日志组会留下垃圾，也就是说在删除了重做日志组后，作为重做日志组成员的操作系统文件还存在，
        需要手工删除这些垃圾文件；

    13.向重做日志添加重做日志成员：
        alter database add logfile member 'd:\temp\redo01a.log' to group1, 'd:\temp\redo02a.log' to group 2;
        # 验证日志组的成员树结果：
        select group#,sequence#, bytes, members, archived, status from v$log;
        # 验证添加重做日志组以及对应成员信息：
        select * from v$logfile order by group#;

    14.删除重做日志组中的一个日志成员：
        alter database drop logfile member 'd\temp\redo04a.log';
        # 查看指定重做日志组成员信息
        select * from v$logfile where group#=4;

    15.删除日志成员的限制： 
        a.重做日志组最后一个有效成员不能删除；
        b.当前正在使用的日志组，日志切换前不能删除；
        c.ARCHIVELOG模式，并且要删除的日志成员所在日志组没有被归档，不能删除；

    16.日志切换：
        一组重做日志组写满时会触发日志切换，也可以手动触发日志切换：alter database switch logfile;

    17.检查点事件：
        减少数据库实例恢复时间：LGWR进程将重做日志缓冲区中的数据写入重做日志文件中，
        同时通知DBWR进程将数据库告诉缓冲区中已经提交的数据写入数据文件。
        # 先强制日志切换，再强制产生检查点事件：
        alter system switch logfile;
        alter system checkpoint;
        # 检查点事件默认是DBWR进程触发；

    管理归档日志
    18.为了防止由于归档进程与LGWR进程不匹配造成的等待时间，可以启动更多后台归档进程：
        show parameter log_archive_max_processes;
        alter system set log_archive_max_processes=4;

    19.查看归档目录相关参数：
        show parameter log_archive_dest;

    20.设置归档目录：
        alter system set log_archive_dest_1='location=f:\app\archive1\mandatory';
        # 如果是data guard将归档目录设置到远程备库，会使用service参数；
        
    21.查看归档目录：
        show parameter log_archive_dest_1;

```

### 2.逻辑层面








































