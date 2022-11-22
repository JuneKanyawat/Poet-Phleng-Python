import re,urllib.request,urllib.parse
import pafy

def search(name): # หาลิ้ง youtube จากชื่อ
    query_string = urllib.parse.urlencode({"search_query": name})
    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)

    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
    clip2 =  "{}".format(search_results[0])
    return clip2

def picture(link,name):
    video=pafy.new(link)
    picture_url=video.bigthumbhd #url รูป title ของ video
    path='/Users/Onlyjune/Desktop/untitled folder 4/file_save/'+name+'.jpg' # path ที่ต้องการจะ save + ชื่อไฟล์
    urllib.request.urlretrieve(picture_url,path) #ดาวโหลด 
    print (path)

def name(link):
    video=pafy.new(link)
    name_video=video.title # ชื่อวิดิโอ
    return name_video

user_input = input("Enter : ")

link=search(user_input)

print(link)
print(name(link))
picture(link,name(link))
