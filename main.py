import os
import cv2
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import pandas as pd
import numpy as np
import subprocess
from moviepy.editor import *
import gtts
data=np.array(pd.read_csv('slide.csv',encoding='latin-1'))
data1=np.array(pd.read_csv('video_information.csv',encoding='latin-1'))
image_folder = '.'
images = [img for img in os.listdir(image_folder)
if img.endswith(".ttf")]
count=0
path=[]
color_count=0
store1=0
store2=0
store3=0
c_store1=0
c_store2=0
c_store3=0
def fun(u):
  up=0
  first=0
  second=0
  third=0   
  for i in data1[u][4]:
    if i==',':
        
        store1=int(data1[u][4][1:up])
        first=up+1
        up=up+1
        break
    else:
        up=up+1
  for i in data1[u][4][first:]:
    if i==',':
        
        store2=int(data1[u][4][first+1:up])
        second=up+1
        up=up+1
         
        break
    else:
      up=up+1   
  for i in data1[u][4][second:]:
    if i==')':
       
        store3=int(data1[u][4][second+1:up])
        break
    else:
      up=up+1
  return store1,store2,store3;       
information=[]
col_count = data.shape[1]
col_count1=data1.shape[1]
for i in range(len(data1)):
    col=[]
    for j in range(col_count1):
        col.append(data1[i][j])
    information.append(col)

def generate_video(i):
    
    array_data=[]
    for j in range(col_count):
       array_data.append(data[i][j])
    for t in range(col_count):
        tts1 = gtts.gTTS(data[i][t],slow=True)
        tts1.save('welcome'+str((t+1))+'.mp3')
    c=[]
    for gh in range(col_count):
      audio_clip = AudioFileClip('welcome'+str((gh+1))+'.mp3')
      if gh!=0:
       image_clip = ImageClip(str((gh+1))+'.jpg')
      else:
        image_clip = ImageClip(str((i+1))+'_'+str((gh+1))+'.jpg')
      video_clip = image_clip.set_audio(audio_clip)
      video_clip.duration = audio_clip.duration
      video_clip.write_videofile('output_path'+str((gh+1))+'.mp4',fps = 60)
      os.remove('welcome'+str((gh+1))+'.mp3')
      if gh!=0:
       os.remove(str((gh+1))+'.jpg')
      else:
            pass
    for jh in range(col_count):
      video_1 = VideoFileClip('output_path'+str((jh+1))+'.mp4')
      c.append(video_1)
      
    final_video= concatenate_videoclips(c)
    final_video.write_videofile('final_video'+str((i+1))+'.mp4',fps = 60)
    video_name = 'final_video'+str((i+1))+'.mp4'
    path.append("D:/Python/youtube_client/"+video_name)
    
    for ghq in range(col_count):
     os.remove('output_path'+str((ghq+1))+'.mp4')

for i in range(len(data)):
    for j in range(col_count):
      l1,l2,l3=fun(i)
      img1 = Image.new('RGB', (2560,1440), color = (l1,l2,l3))
      I1 = ImageDraw.Draw(img1)
      fontsize = 1 
      img_fraction = 0.50
      font = ImageFont.truetype('C:/Windows/Fonts/'+(information[i][7]+'.ttf'), fontsize)
     
      while font.getsize(data[i][j])[0] < img_fraction*img1.size[0]:
        fontsize += 1
        font = ImageFont.truetype(('C:/Windows/Fonts/'+(information[i][7]+'.ttf')), fontsize)
      l=len(data[i][j])
      k=data[i][j]
      count=1
      if l>40:
        fontsize=70
      if l>63:
        l=l/2
        count=count+1
        while l>63:
          l=l/2
          count=count+1
      chunks, chunk_size = len(k), len(k)//count
      hj=58
      hj1=0
      list_line=[]
      fgh=0
      if count!=1:
        for u in range(count):
          c=0
          kj=0
          if (u+1)!=count:
            t=True
            while t:
              if k[hj]==' ':
                if len(k[hj1:hj])<=56:
                 list_line.append(k[hj1:hj])
                else:
                     kj=len(k[hj1:hj])-56
                     while k[hj-kj]!=' ':
                         kj=kj+1
                         c=c+1
                     hj=hj-kj
                     list_line.append(k[hj1:hj])
                hj=hj+53
                hj1=hj1+58-c
                t=False
              else:
                hj=hj-1 
                c=c+1
          else:
            hj=hj-53
            
            if len(k[hj:])<=56:
              list_line.append(k[hj:])
            else:
              
              kj=len(k[hj1:hj+1])-56
              
              while k[hj-kj]!=' ':
                kj=kj+1
                c=c+1
              lu=hj
              hj=hj-kj
              list_line.append(k[lu:hj+1])
              list_line.append(k[hj:])
              fgh=1
      else:
        list_line.append(k)
                 
             
     
      fontsize -= 1
      if count<2:
        if j==0:
           fontsize=140
        else: 
          fontsize=85
        font = ImageFont.truetype('C:/Windows/Fonts/'+(information[i][7]+'.ttf'), fontsize)
        w,h=font.getsize(data[i][j])
        
        I1.text((((2560-w)/2),((1440-h)/2)), data[i][j], font=font,fill=information[i][6])
      else:
         c=0
         temp=count+fgh
         height=2560
         width=1440
         while temp>0:
          fontsize=85
          font = ImageFont.truetype('C:/Windows/Fonts/'+(information[i][7]+'.ttf'), fontsize)
          w,h=font.getsize(list_line[c])
          I1.text((((height-w)/2),((width-h)/2)), list_line[c], font=font,fill=information[i][6])
          c=c+1
          temp=temp-1
          height=height+20
          width=width+170
         
      if j!=0:
       img1.save(str(j+1)+".jpg")
      else:
       img1.save(str(i+1)+'_'+str(j+1)+".jpg")
    generate_video(i)
k=0
for i in path:
 name=information[k][0]
 description1=information[k][1]
 tag=information[k][2]
 age=information[k][3]
 schedule=information[k][5]
 k=k+1 
 action1="set"
 value="0"
 play_list="PLQ_BzM_Cvnku-SA2R31DT09fSYvoRAp07"
 subprocess.Popen(['python', 'upload_videos_1.py', '--file',
 i, '--action',action1,'--playlist_id',play_list,'--c',value,
 '--title',name,'--description',description1,'--publishedAt',
 schedule,'--publishAt',schedule,'--keywords',tag,'--n_v',str(k),'--category',str(age)])
 