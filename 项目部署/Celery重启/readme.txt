# celery在windows下重启自动启动
    进入文件夹:
    win7: C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
    win10 &&win server2016: C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
    放入python脚本(beat脚本需要删除pid文件):