## B站搜索
介绍可以参见[博客](http://www.kylen314.com/archives/6670)

关键字：`bl` (喂，`bl`是`b`i`l`i的简写啊！)

选中搜索结果中的视频回车即可直接在浏览器中打开；

<img src = "http://www.kylen314.com/wp-content/uploads/2014/08/QQ20140831-10.png" />


> 如按下文配置好[biligrab-danmaku2ass](https://github.com/m13253/biligrab-danmaku2ass)及[you-get](https://github.com/soimort/you-get)，选中搜索结果中的视频，按住`cmd`然后回车即可使用mpv本地播放视频，按住`ctrl`再回车可以查看高清视频；【因为macbook观看弹幕视频发热太过严重，这个方法不仅可以有效解决这个问题，并且新番可以**跳广告**！！】,按住`alt`再回车可以下载视频【如果可以的话】；

## B站新番
介绍可以参见[博客](http://www.kylen314.com/archives/6670)

关键字：`bgm`

食用方法：
* 直接输入`bgm`可以查看最近更新的二次元新番
* 后面加`t`可以查看今天会更新的新番
* 输入`wn`可以查看`周n`更新的视频，比如`bgm w3`就是查看周三更新的视频
* 前面的各种命令前面加个`3`可以查看三次元新番

<img src = "http://www.kylen314.com/wp-content/uploads/2014/08/QQ20140831-11.png" />
<img src = "http://www.kylen314.com/wp-content/uploads/2014/08/QQ20140831-13.png" />
<img src = "http://www.kylen314.com/wp-content/uploads/2014/08/QQ20140831-14.png" />
<img src = "http://www.kylen314.com/wp-content/uploads/2014/08/QQ20140831-15.png" />

> 比较讨厌的有两点，一是这些更新顺序我代码中明明是按和现在接近程序顺序输出的，但是显示出来却不全是，貌似跟你最近点击有关。。
>还有一点，获取到的新番信息里面包含封面的URL的，但是好像Alfred列表的每个选项前面的图标只能是本地icon，不然不显示。。
 

## B站排行
介绍可以参见[博客](http://www.kylen314.com/archives/6670)

关键字：`bhot`

食用方法：
* 查看热门视频只要输入`bhot`即可[默认返回的是`全站`   `3天`内`除了新番区`以外`点击量`最高的`20`个视频；]
* 选择分区，后面加上：
	*  动画区:`dh`
	* 音乐舞蹈区:`yy`
	* 游戏区:`yx`
	* 娱乐区:`yl`
	* 科学与技术:`kj`
* 设置天数范围只要加个`dx`就可以返回`x天`内排名最高的；
* 排名方式默认点击量，也可以选择:
	* 按弹幕数排:`dm`
	* 收藏数:`sc`
	* 评论数:`pl`
	* 硬币数:`yb`

<img src = "http://www.kylen314.com/wp-content/uploads/2014/08/QQ20140831-16.png" />

> 举个例子，你想查看`60天`内`音乐区` `硬币数`最高的视频：那么输入`bhot d60ybyy`【参数顺序随便写，比如`bhot ybyyd60`也可以】


<img src = "http://www.kylen314.com/wp-content/uploads/2014/08/QQ20140831-17.png" />

> 如按下文配置好[biligrab-danmaku2ass](https://github.com/m13253/biligrab-danmaku2ass)及[you-get](https://github.com/soimort/you-get)，选中搜索结果中的视频，按住`cmd`然后回车即可使用mpv本地播放视频，按住`ctrl`再回车可以查看高清视频；【因为macbook观看弹幕视频发热太过严重，这个方法不仅可以有效解决这个问题，并且新番可以**跳广告**！！】,按住`alt`再回车可以下载视频【如果可以的话】；

## 配合使用的系统设置
首先完成以下三项配置：
* [you-get](https://github.com/soimort/you-get)
* [biligrab-danmaku2ass](https://github.com/m13253/biligrab-danmaku2ass)
* [danmaku2ass](https://github.com/m13253/danmaku2ass)

目标：
* 可以使用`you-get http://www.bilibili.com/video/avXXXX`下载B站视频
* 假设cd到[biligrab-danmaku2ass](https://github.com/m13253/biligrab-danmaku2ass)所放的路径，可以使用`./bilidan.py http://www.bilibili.com/video/avXXX/`在MPV中本地播放视频

然后：
在'\usr\bin'中建立一个名为`bili`的文本文件，内容如下：
```
#!/bin/bash
xxxxxxx/bilidan.py $@
```
其中前面`xxxxxxx`表示`bilidan.py`路径，然后添加执行权限`sudo chmod +x bili`后便可以随时随地在任意路径下终端使用`bili http://www.bilibili.com/video/avXXX/`播放视频了！！
当然你也可以设置默认配置，比如弹幕透明度：
```
#!/bin/bash
~/danmaku2ass/bilidan.py --d2aflags 'text_opacity=0.5' $@
```
完成以上配置即可！！
