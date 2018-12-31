#coding:utf-8
import os
import sys
import time
import random
from mutagen.mp3 import MP3
import json
#import Config
import shutil
import _thread
import service.AssMaker

config = json.load(open('./Config.json', encoding='utf-8'))
path = config['path']
rtmp = config['rtmp']['url']
live_code = config['rtmp']['code']
nightvideo = bool(int(config['nightvideo']['use']))

#格式化时间，暂时没啥用，以后估计也没啥用
def convert_time(n):
    s = n%60
    m = int(n/60)
    return '00:'+"%02d"%m+':'+"%02d"%s

#移动放完的视频到缓存文件夹
def remove_v(filename):
    try:
        #shutil.move(path+'/resource/playlist/'+filename,path+'/resource/music/')
        os.remove(path+'/resource/playlist/'+filename)
    except Exception as e:
        print(e)
    try:
        os.remove(path+'/resource/playlist/'+filename.replace(".flv",'')+'ok.ass')
        os.remove(path+'/resource/playlist/'+filename.replace(".flv",'')+'ok.info')
    except Exception as e:
        print(e)
        print('delete error')

while True:
    try:
        if (time.localtime()[3] <= 5) and nightvideo: #time.localtime()[3] >= 23 or 
            print('night is comming~')  #晚上到咯~
            night_files = os.listdir(path+'/resource/night') #获取所有缓存文件
            night_files.sort()    #排序文件
            night_ran = random.randint(0,len(night_files)-1)    #随机抽一个文件
            # if(night_files[night_ran].find('.flv') != -1):  #如果为flv视频
                # #直接暴力推流
                # print('ffmpeg -threads 1 -re -i "'+path+"/resource/night/"+night_files[night_ran]+'" -vcodec copy -acodec copy -f flv "'+rtmp+live_code+'"')
                # os.system('ffmpeg -threads 1 -re -i "'+path+"/resource/night/"+night_files[night_ran]+'" -vcodec copy -acodec copy -f flv "'+rtmp+live_code+'"')
            if(night_files[night_ran].find('.mp3') != -1):  #如果为mp3
                pic_files = os.listdir(path+'/resource/img') #获取准备的图片文件夹中的所有图片
                pic_files.sort()    #排序数组
                pic_ran = random.randint(0,len(pic_files)-1)    #随机选一张图片
                audio = MP3(path+'/resource/night/'+night_files[night_ran])    #获取mp3文件信息
                seconds=audio.info.length   #获取时长
                print('mp3 long:'+convert_time(seconds))
                if not os.path.isfile(path+'/resource/night/'+night_files[night_ran]+'.ass'):
                    service.AssMaker.make_ass(path+'/night/'+night_files[night_ran].replace('.mp3',''),'当前是晚间专属时间哦~时间范围：凌晨0-5点\\N大家晚安哦~做个好梦~\\N当前文件名：'+night_files[night_ran],path)
                print('ffmpeg -threads 1 -re -loop 1 -r 15 -t '+str(int(seconds))+' -f image2 -i "'+path+'/resource/img/'+pic_files[pic_ran]+'" -i "'+path+'/resource/night/'+night_files[night_ran]+'" -vf ass="'+path+'/resource/night/'+night_files[night_ran]+'.ass" -x264-params "profile=high:level=5.1" -pix_fmt yuv420p -b '+config['rtmp']['bitrate']+'k -vcodec libx264 -acodec copy -f flv "'+rtmp+live_code+'"')
                os.system('ffmpeg -threads 1 -re -loop 1 -r 15 -t '+str(int(seconds))+' -f image2 -i "'+path+'/resource/img/'+pic_files[pic_ran]+'" -i "'+path+'/resource/night/'+night_files[night_ran]+'" -vf ass="'+path+'/resource/night/'+night_files[night_ran].replace('.mp3','')+'.ass" -x264-params "profile=high:level=5.1" -pix_fmt yuv420p -b '+config['rtmp']['bitrate']+'k -vcodec libx264 -acodec copy -f flv "'+rtmp+live_code+'"')
            continue
        
        files = os.listdir(path+'/resource/playlist')   #获取文件夹下全部文件
        files.sort()    #排序文件，按文件名（点播时间）排序
        count=0     #总共匹配到的点播文件统计
        for f in files:
            if((f.find('.mp3') != -1) and (f.find('.download') == -1)): #如果是mp3文件
                print(path+'/resource/playlist/'+f)
                seconds = 600
                bitrate = 0
                try:
                    audio = MP3(path+'/resource/playlist/'+f)   #获取mp3文件信息
                    seconds=audio.info.length   #获取时长
                    bitrate=audio.info.bitrate  #获取码率
                    print(audio.info.length)
                except Exception as e:
                    print(e)
                    bitrate = 99999999999
                
                print('mp3 long:'+convert_time(seconds))
                if((seconds > 600) | (bitrate > 400000)):  #大于十分钟就不播放/码率限制400k以下
                    print('too long/too big,delete')
                else:
                    pic_files = os.listdir(path+'/resource/img') #获取准备的图片文件夹中的所有图片
                    pic_files.sort()    #排序数组
                    pic_ran = random.randint(0,len(pic_files)-1)    #随机选一张图片
                    #推流
                    print('ffmpeg -threads 1 -re -loop 1 -r 15 -t '+str(int(seconds))+' -f image2 -i "'+path+'/resource/img/'+pic_files[pic_ran]+'" -i "'+path+'/resource/playlist/'+f+'" -vf ass="'+path+"/resource/playlist/"+f.replace(".mp3",'')+'.ass'+'" -x264-params "profile=high:level=5.1" -pix_fmt yuv420p -b '+config['rtmp']['bitrate']+'k -vcodec libx264 -acodec copy -f flv "'+rtmp+live_code+'"')
                    os.system('ffmpeg -threads 1 -re -loop 1 -r 15 -t '+str(int(seconds))+' -f image2 -i "'+path+'/resource/img/'+pic_files[pic_ran]+'" -i "'+path+'/resource/playlist/'+f+'" -vf ass="'+path+"/resource/playlist/"+f.replace(".mp3",'')+'.ass'+'" -x264-params "profile=high:level=5.1" -pix_fmt yuv420p -b '+config['rtmp']['bitrate']+'k -vcodec libx264 -acodec copy -f flv "'+rtmp+live_code+'"')
                    try:    #放完后删除mp3文件、删除字幕、删除点播信息
                        shutil.move(path+'/resource/playlist/'+f,path+'/resource/music/')
                        shutil.move(path+'/resource/playlist/'+f.replace(".mp3",'')+'.ass',path+'/resource/music/')
                        #os.remove(path+'/resource/playlist/'+f)
                        #os.remove(path+'/resource/playlist/'+f.replace(".mp3",'')+'.ass')
                    except Exception as e:
                        print(e)
                try:
                    os.remove(path+'/resource/playlist/'+f.replace(".mp3",'')+'.info')
                    os.remove(path+'/resource/playlist/'+f)
                    os.remove(path+'/resource/playlist/'+f.replace(".mp3",'')+'.ass')
                except:
                    print('delete error')
                count+=1    #点播统计加一
                break
            if((f.find('ok.flv') != -1) and (f.find('.download') == -1) and (f.find('rendering') == -1)):   #如果是有ok标记的flv文件
                print('flv:'+f)
                #直接推流
                print('ffmpeg -threads 1 -re -i "'+path+"/resource/playlist/"+f+'" -vcodec copy -acodec copy -f flv "'+rtmp+live_code+'"')
                os.system('ffmpeg -threads 1 -re -i "'+path+"/resource/playlist/"+f+'" -vcodec copy -acodec copy -f flv "'+rtmp+live_code+'"')
                os.rename(path+'/resource/playlist/'+f,path+'/resource/playlist/'+f.replace("ok",""))   #修改文件名，以免下次循环再次匹配
                _thread.start_new_thread(remove_v, (f.replace("ok",""),))   #异步搬走文件，以免推流卡顿
                count+=1    #点播统计加一
                break
        if(count == 0):     #点播统计为0，说明点播的都放完了
            print('no media')
            mp3_files = os.listdir(path+'/resource/music') #获取所有缓存文件
            mp3_files.sort()    #排序文件
            mp3_ran = random.randint(0,len(mp3_files)-1)    #随机抽一个文件
            
            if(mp3_files[mp3_ran].find('.mp3') != -1):  #如果是mp3文件
                pic_files = os.listdir(path+'/resource/img') #获取准备的图片文件夹中的所有图片
                pic_files.sort()    #排序数组
                pic_ran = random.randint(0,len(pic_files)-1)    #随机选一张图片
                audio = MP3(path+'/resource/music/'+mp3_files[mp3_ran])    #获取mp3文件信息
                seconds=audio.info.length   #获取时长
                print('mp3 long:'+convert_time(seconds))
                #推流
                if(os.path.isfile(path+'/resource/music/'+mp3_files[mp3_ran].replace(".mp3",'')+'.ass')):
                    if os.path.isfile(path+"/resource/music/"+mp3_files[mp3_ran].replace(".mp3",'')+'.jpg'):
                        print('ffmpeg -threads 0 -re -loop 1 -r 2 -t '+str(int(seconds))+' -f image2 -i "'+path+'/resource/img/'+pic_files[pic_ran]+'" -i "'+path+"/resource/music/"+mp3_files[mp3_ran].replace(".mp3",'')+'.jpg'+'" -filter_complex "[0:v][1:v]overlay=30:390[cover];[cover]ass='+path+"/resource/music/"+mp3_files[mp3_ran].replace(".mp3",'')+'.ass'+'[result]" -i "'+path+'/resource/music/'+mp3_files[mp3_ran]+'" -map "[result]" -map 2,0 -pix_fmt yuv420p -preset ultrafast -maxrate '+config['rtmp']['bitrate']+'k -acodec copy -c:v libx264 -f flv "'+rtmp+live_code+'"')
                        os.system('ffmpeg -threads 0 -re -loop 1 -r 2 -t '+str(int(seconds))+' -f image2 -i "'+path+'/resource/img/'+pic_files[pic_ran]+'" -i "'+path+"/resource/music/"+mp3_files[mp3_ran].replace(".mp3",'')+'.jpg'+'" -filter_complex "[0:v][1:v]overlay=30:390[cover];[cover]ass='+path+"/resource/music/"+mp3_files[mp3_ran].replace(".mp3",'')+'.ass'+'[result]" -i "'+path+'/resource/music/'+mp3_files[mp3_ran]+'" -map "[result]" -map 2,0 -pix_fmt yuv420p -preset ultrafast -maxrate '+config['rtmp']['bitrate']+'k -acodec copy -c:v libx264 -f flv "'+rtmp+live_code+'"')
                    else:
                        print('ffmpeg -threads 0 -re -loop 1 -r 2 -t '+str(int(seconds))+' -f image2 -i "'+path+'/resource/img/'+pic_files[pic_ran]+'" -i "'+path+'/resource/music/'+mp3_files[mp3_ran]+'" -vf ass="'+path+"/resource/music/"+mp3_files[mp3_ran].replace(".mp3",'')+'.ass'+'" -pix_fmt yuv420p -preset ultrafast -maxrate '+config['rtmp']['bitrate']+'k -acodec copy -c:v libx264 -f flv "'+rtmp+live_code+'"')
                        os.system('ffmpeg -threads 0 -re -loop 1 -r 2 -t '+str(int(seconds))+' -f image2 -i "'+path+'/resource/img/'+pic_files[pic_ran]+'" -i "'+path+'/resource/music/'+mp3_files[mp3_ran]+'" -vf ass="'+path+"/resource/music/"+mp3_files[mp3_ran].replace(".mp3",'')+'.ass'+'" -pix_fmt yuv420p -preset ultrafast -maxrate '+config['rtmp']['bitrate']+'k -acodec copy -c:v libx264 -f flv "'+rtmp+live_code+'"')
                else:
                    print('ffmpeg -threads 0 -re -loop 1 -r 2 -t '+str(int(seconds))+' -f image2 -i "'+path+'/resource/img/'+pic_files[pic_ran]+'" -i "'+path+'/resource/music/'+mp3_files[mp3_ran]+'" -vf ass="'+path+'/default.ass" -pix_fmt yuv420p -preset ultrafast -maxrate '+config['rtmp']['bitrate']+'k -acodec copy -c:v libx264 -f flv "'+rtmp+live_code+'"')
                    os.system('ffmpeg -threads 0 -re -loop 1 -r 2 -t '+str(int(seconds))+' -f image2 -i "'+path+'/resource/img/'+pic_files[pic_ran]+'" -i "'+path+'/resource/music/'+mp3_files[mp3_ran]+'" -vf ass="'+path+'/default.ass" -pix_fmt yuv420p -preset ultrafast -maxrate '+config['rtmp']['bitrate']+'k -acodec copy -c:v libx264 -f flv "'+rtmp+live_code+'"')
            if(mp3_files[mp3_ran].find('.flv') != -1):  #如果为flv视频
                #直接推流
                print('ffmpeg -threads 0 -re -i "'+path+"/resource/music/"+mp3_files[mp3_ran]+'" -vcodec copy -acodec copy -f flv "'+rtmp+live_code+'"')
                os.system('ffmpeg -threads 0 -re -i "'+path+"/resource/music/"+mp3_files[mp3_ran]+'" -vcodec copy -acodec copy -f flv "'+rtmp+live_code+'"')
    except Exception as e:
        print(e)

