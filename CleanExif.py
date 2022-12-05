'''
 # @ Author: starrysky
 # @ Create Time: 2022-06-25 14:26:10
 # @ Modified by: starrysky
 # @ Modified time: 2022-12-05 16:29:05
 # @ Description: 多线程批量删除图片exif信息
 '''


from PIL import Image
import os,time
import sys
import threading

# 如果需要统计数据，打开countNums
# countNums = 1 

# 图片路径
photoDir = 'E:/image/original'
# 清理后的图片保存路径
outDir = 'E:/image/cleaned'

# 多线程，最大线程数
THREADING_LIMIT = 30
 
def clearExifInfo(photoAddress, outPhotoAddress,semaphore): #, currentNum
    semaphore.acquire()
    try: 
        image = Image.open(photoAddress)
    except:
        print("FileError:{0}".format(photoAddress))
        semaphore.release()
        return  

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
# 清理png格式的图片
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

# 多线程处理图片
def clearExif(path):
    startTime = time.time()       
    semaphore = threading.BoundedSemaphore(THREADING_LIMIT)  
    for root, dirs, files in os.walk(path):
        outRoot = root.replace(path, outDir)
        if not os.path.exists(outRoot):
            os.makedirs(outRoot)
        for name in files:
            if name.endswith(".JPG") or name.endswith(".jpg") or name.endswith(".png") or name.endswith(".PNG"):
                photoAddress = os.path.join(root,name)
                outPhotoAddress= os.path.join(outRoot,name)
                # 为防止意外中断，重复处理文件：如果文件已经存在，则不再重复处理。
                if os.path.exists(outPhotoAddress):
                    #print("{0} is exists".format(outPhotoAddress))
                    continue
                '''
                # 如果需要统计数据，打开这里
                global countNums
                currentNum = countNums
                print("Start:{0}  --{1}\n".format(currentNum, photoAddress))                
                countNums = countNums + 1
                '''
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
 
 
 

if __name__ == '__main__':
# 如果使用命令行：
# cmd: python CleanExif.py photoDir
#    photoDir = sys.argv[1]
    
    clearExif(photoDir)
    print("End")
