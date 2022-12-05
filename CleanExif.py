'''
 # @ Author: starrysky
 # @ Create Time: 2022-12-05 15:52:10
 # @ Modified by: starrysky
 # @ Modified time: 2022-12-05 16:01:22
 # @ Description: 清除文件夹下所有图片的exif信息,如果未成功,导出文件路径.
 '''

from PIL import Image
import os,time
import sys
import threading
#countNums = 1
#photoDir = 'D:/W300218/202006'
#outDir = 'D:/W300218/202006a'
photoDir = 'E:/image/original'
outDir = 'E:/image/cleaned'
 
def clearExifInfo(photoAddress, outPhotoAddress,semaphore): #, currentNum
    semaphore.acquire()
    try: 
        image = Image.open(photoAddress)
    except:
        print("FileError:{0}".format(photoAddress))
        semaphore.release()
        return
    #data = list(image.getdata())
    
    try: 
        data = list(image.getdata())
    
    except:
        print("FileError:{0}".format(photoAddress))
        semaphore.release()
        return
    
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)          
    try:
        image_without_exif.save(outPhotoAddress)   
    except:
        print("Error:{0}".format(photoAddress))
        image_without_exif=image_without_exif.convert('RGB')
        image_without_exif.save(outPhotoAddress)
    #print("End:{0}  --{1}\n".format(currentNum, outPhotoAddress))
    semaphore.release()
    return

'''
def clearExifInfoPNG(photoAddress, outPhotoAddress, currentNum,semaphore):
    semaphore.acquire()
    image = Image.open(photoAddress)
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)          
    image_without_exif.save(outPhotoAddress)   

    print("End:{0}  --{1}\n".format(currentNum, outPhotoAddress))
    semaphore.release()
    return
'''

def clearExif(path):
    startTime = time.time()       
    semaphore = threading.BoundedSemaphore(30)
    for root, dirs, files in os.walk(path):
        outRoot = root.replace(path, outDir)
        if not os.path.exists(outRoot):
            os.makedirs(outRoot)
        for name in files:
            if name.endswith(".JPG") or name.endswith(".jpg") or name.endswith(".png") or name.endswith(".PNG"):
                photoAddress = os.path.join(root,name)
                outPhotoAddress= os.path.join(outRoot,name)
                #如果文件已经存在，则不再重复处理
                if os.path.exists(outPhotoAddress):
                    #print("{0} is exists".format(outPhotoAddress))
                    continue
                #global countNums
                #currentNum = countNums
                #print("Start:{0}  --{1}\n".format(currentNum, photoAddress))                
                #countNums = countNums + 1
                t=threading.Thread(target=clearExifInfo,args=(photoAddress,outPhotoAddress,semaphore)) #,currentNum
                t.start()
            '''
            elif name.endswith(".PNG") or name.endswith(".png"):
                photoAddress = os.path.join(root,name)
                outPhotoAddress= os.path.join(outRoot,name)
                global countNums
                currentNum = countNums
                print("Start:{0}  --{1}\n".format(currentNum, photoAddress))                
                countNums = countNums + 1
                t=threading.Thread(target=clearExifInfo,args=(photoAddress,outPhotoAddress,currentNum,semaphore))
                t.start()
            '''
    return 
 
 
 
# cmd: python CleanExif.py E:\SB_PHOTO
if __name__ == '__main__':
#    photoDir = sys.argv[1]
#     photoDir = '/home/W300218'
    
    clearExif(photoDir)
    print("End")
