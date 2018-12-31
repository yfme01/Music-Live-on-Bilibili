# Music-Live-on-Bilibili

运行于服务器上的Bilibili直播点歌台

原版[https://github.com/chenxuuu/24h-raspberry-live-on-bilibili](https://github.com/chenxuuu/24h-raspberry-live-on-bilibili)

原版说很乱，我看了下，的确很乱，有强迫症的我发现了下面这个：  
[https://github.com/fhyuncai/24h-server-live-on-bilibili](https://github.com/fhyuncai/24h-server-live-on-bilibili)  
所以我就基于这个修改了以下，并跟进了原版的新功能

预览地址：[https://live.bilibili.com/8712608](https://live.bilibili.com/8712608)


本人没学过Python，只是心血来潮想弄一个点歌台，所以才稍微弄了一下，有不对的地方请指正

-------
### 修改内容：
- 跟进原版新功能：点播mv，并适配到服务器
- 跟进原版新功能：点播B站视频，并适配到服务器（受原版“此版本的功能”内的`接口失效`说 明影响）
- 修复强行适配后无法读取瓜子
- 去掉了一个会导致弹幕无法运行的依赖调用，下方也除去了该依赖的安装步骤（其实我也不知道干嘛用的）
- 增加了指定用户不需要送礼物点歌设置（在`/service/PostDanmu.py`里面，可以自己修改）
- 去掉了旁边的歌曲封面图（个人爱好）
- 其他的不知道...
-------
### 注意：
- 使用`腾讯云`服务器的：
	下方`安装依赖`部分需要root用户，而腾讯云给`Ubuntu-server16.04`的默认用户是  		`ubuntu`，解决方法：
	```Bash  
	$ sudo passwd root
	```
	输入两次要设置的root密码  
	```Bash 
	$ su root
	```
	发现命令行前的`$`变成`#`就已经是`root`了
- 使用较低配的机子（本人使用的机子是`1H1G1M`）出现`偶尔`卡顿是正常情况。  
	若卡顿十分频繁，可能出现以下情况（本人遇到与猜测）
	- 看直播的人网速不够（废话）
	- 图片分辨率过大，推荐使用`1280×720`，此分辨率CPU使用量一般为60-70%，实测`1920×1080`图片CPU使用量99%以上
	- 点`mv`等视频会卡，故我将点`mv`的“价格”设置得特别高，若配置足够可改回正常
- 如果想自己研究的，可以看下下面的技巧（我查了好久才知道的，大神可略过）
	- 如果直播没运行成功或者弹幕没回应，可以用
	```Bash
	$ screen -ls
	```

	查看`Push`（直播）和`Danmu`	（弹幕）是否运行，也可以获取screen的`id`

	```Bash
	$ screen -r id  #id换成screen的id
	``` 

	可以进入screen查看输出进行调试

-------

此版本的功能：

- 弹幕点歌
- 弹幕点MV
- 弹幕反馈（发送弹幕）
- 旧版实现的视频推流功能
- 自定义介绍字幕
- 歌词滚动显示，同时滚动显示翻译歌词
- 切歌
- 显示排队播放歌曲，渲染视频
- 闲时随机播放预留歌曲
- 播放音乐时背景图片随机选择
- ~~可点播b站任意视频（会员限制除外，番剧根据b站规定，禁止点播）~~（接口暂时失效）
- 已点播歌曲、视频自动进入缓存，无人点播时随机播放
- 存储空间达到设定值时，自动按点播时间顺序删除音乐、视频来释放空间`（这个没测试过）`
- 实时显示歌曲/视频长度
- 根据投喂礼物的多少来决定是否允许点播

已知问题：

- 换歌、视频时会闪断

## 安装说明：

此版本仅在Ubuntu16.04测试通过，其它系统请自测

## 安装依赖：

```Bash
sudo apt-get update
sudo apt-get -y install autoconf automake build-essential libass-dev libfreetype6-dev libtheora-dev libtool libvorbis-dev pkg-config texinfo wget zlib1g-dev
```

libmp3lame：
```Bash
sudo apt-get install -y libmp3lame-dev
```

libopus:
```Bash
sudo apt-get install -y libopus-dev
```

libvpx:
```Bash
sudo apt-get install -y libvpx-dev
```

libomxil-bellagio:
```Bash
sudo apt-get install -y libomxil-bellagio-dev
```

ffmpeg、x264编码器：
```Bash
sudo apt-get install -y ffmpeg
```

x264、x265编码器：
```Bash
sudo apt-get install -y x264 x265 libx264 libx265
```

安装python3：

```Bash
sudo apt-get install -y python3
```

安装pip3：
```Bash
sudo apt-get install -y python3-pip
```

安装python3的mutagen库：
```Bash
sudo pip3 install mutagen
```

安装python3的moviepy库：
```Bash
sudo pip3 install moviepy
```

安装python3的numpy需要的库：
```Bash
sudo apt-get install libatlas-base-dev
```

安装python3的requests库：
```Bash
sudo pip3 install requests
```

安装screen:
```Bash
sudo apt-get install -y screen
```

安装中文字体（此方法可能不适用你的服务器，如果无法安装请自行百度）：
```Bash
sudo apt install fontconfig
sudo apt-get install ttf-mscorefonts-installer
sudo apt-get install -y --force-yes --no-install-recommends fonts-wqy-microhei
sudo apt-get install -y --force-yes --no-install-recommends ttf-wqy-zenhei
#可能有装不上的，应该问题不大

# 查看中文字体 --确认字体是否安装成功
fc-list :lang=zh-cn
```

（字体安装来自[ubuntu下 bilibili直播推流 ffmpeg rtmp推送](https://ppx.ink/2.ppx)）

下载本项目：
```Bash
git clone https://github.com/yfme01/Music-Live-on-Bilibili.git
```

配置项说明：
```Json
{
	"path": "/root/24h-server-live-on-bilibili", //文件所在目录
	"musicapi": "https://api.yuncaioo.com/bililive/", //API地址，用的修改的人的
	"freespace": "15360", //允许下载和缓存文件夹占用空间大小，超过时自动按时间顺序删除音乐，单位：MiB
	"gift": "0", //设定是否使用投礼物才能点歌，0为关闭，1为开启
	"rtmp": {
		"url": "", //rtmp地址
		"code": "", //直播码
		"bitrate": "192" //推流码率，单位k
	},
	"danmu": {
		"cookie": "", //发送弹幕用的cookie
		"token": "", //发送弹幕用的csrf_token
		"roomid": "8712608", //直播间ID
		"size": "20" //每段弹幕的最大长度（20级以后可发30字）
	},
	"nightvideo": {
		"use": "1" //设定是否播放晚间专属视频，0为关闭，1为开启
	}
}
```

请修改`Config.json`文件中的各种选项
其中，`cookie`请尽量使用小号，在直播间，打开浏览器审查元素，先发一条弹幕，再查看`network`选项卡，找到`name`为`send`的项目，`Request head`中的`Cookie`即为`cookie`变量的值。注意设置后，账号不能点击网页上的“退出登陆”按键，换账号请直接清除当前Cookie再刷新

`token`请填写`Request head`中的`csrf_token`

`service/PostDanmu.py`文件的`yfme001`请改为你的机器人的名字，`yfme01`请改为你的名字

如有条件，请`务必`自己搭建php的下载链接解析服务，源码都在`tools/php`文件夹内（需要修改，请等待更新）

`resource/music`文件夹内放入mp3格式的音乐，在无人点歌时播放

`resource/img`文件夹内放入jpg格式的图片，用于做为放音乐时的背景，请尽量保证文件名全英文，分辨率推荐统一处理为1280x720

所有配置完成后，开启直播，然后启动脚本即可：
```Bash
sh start.sh
```

### 其他命令

停止：
```Bash
sh stop.sh
```

重启：
```Bash
sh restart.sh
```

如有出错的地方，请提交issue，也欢迎各位改进脚本并pr

本程序协议为GPL
