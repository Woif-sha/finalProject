# Git
1.git clone速度慢

git clone命令中将添加 gitclone.com, eg:

> _git clone https://gitclone.com/github.com/Woif-sha/finalProject.git_

2.配置ssh

https://blog.csdn.net/weixin_42310154/article/details/118340458

ssh-keygen -t rsa -C "liang---y@outlook.com"

3.基本指令

    git config --global user.name "Woif_sha"
    git config --global user.email "liang---y@outlook.com"

    设置忽略的文件格式：touch .gitignore   --/.idea/  /__pycache__/
    清除已上传无用文件：git rm -r --force __pycache__
                      git rm -r --force .idea

    链接远程仓库：git remote add origin ......

    git add -A

    git commit -m "first commit"

    git pull origin master

    git push origin master

# 桶形畸变处理

CSDN：https://blog.csdn.net/u010607947/article/details/80510939

平面->球坐标投影 https://blog.csdn.net/qq_43474959/article/details/108394740


# ReSpeaker 4 Mic Array

1.安装驱动

https://github.com/respeaker/seeed-voicecard

2.声源定位、语音交互（google assistant）

https://github.com/respeaker/mic_array/tree/master?tab=readme-ov-file

3.csdn 例程

https://blog.csdn.net/Unibug/article/details/126067050

# Snowboy

树莓派snowboy唤醒+百度语音识别

https://www.cnblogs.com/lovesKey/p/11080448.html

snowboy教程：

https://blog.csdn.net/directorhy/article/details/131276364

snowboy在线录音：

https://snowboy.hahack.com/

# Sound

百度终端控制台

https://console.bce.baidu.com/ai/#/ai/speech/app/detail~appId=6087467

# Problem

完美解决E: Unable to lock directory /var/lib/apt/lists/方案

https://blog.csdn.net/qq_43332010/article/details/108911126

snowboy make报错解决：

https://blog.csdn.net/ABC__xiaoming/article/details/107512931

解决import跨级导入报错：

https://blog.csdn.net/m0_56190554/article/details/134573180

Grove接口：

https://blog.csdn.net/suyong_yq/article/details/108639824

# 算法层：

1.gcc-phat

知乎：https://zhuanlan.zhihu.com/p/340631844
https://zhuanlan.zhihu.com/p/255037076
CSDN:https://blog.csdn.net/pk296256948/article/details/116294055