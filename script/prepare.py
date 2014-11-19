# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 17:17:54 2014

@author: babou
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 08:33:40 2014

@author: Babou
"""
import cv2
import glob, random, os


size = 50

# remove old info.dat
try:
    os.remove('model/info.dat')
except:
    pass

# remove old bg.dat
try:
    os.remove('model/bg.dat')
except:
    pass

# remove old learning images
try:
    #os.remove('data/learning_images/positive/*')
    os.system("rm data/learning_images/positive/*")
except:
    pass

# remove old learning images
try:
    #os.remove('data/learning_images/negative/*')
    os.system("rm data/learning_images/negative/*")
except:
    pass

info = open("model/info.dat","w")

# resizing positive images
for filename in glob.glob("Image/positive2/*.jpg"):
    try:
        img = cv2.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #height,width,channel  = img.shape
        resized_image = cv2.resize(gray, (size, size)) 
        elements = filename.split("/")
        new_filename = "data/learning_images/positive/" + elements[-1].split(".")[0] + ".pgm"
        new_filename_bis = "../" + new_filename # TO CHANGE
        cv2.imwrite(new_filename, resized_image)

        info.write("%s 1 0 0 %d %d\n" % (new_filename_bis, size, size))
    except:
        print "Error file : %s" % (filename)

info.close()
print "Number of files in positive: %s" % str(len(glob.glob("data/learning_images/positive/*.pgm")))


bg = open("model/bg.dat","w")
# cutting pieces of size*size to make the background

i = 0

for filename in glob.glob("Image/negative/*.jpg"):
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height,width,channel  = img.shape
    #elements = filename.split("\\")
    for j in range(2000):
        try:
            random_size = random.randint(size/2, size + (size/2))
            x = random.randint(0,height-random_size)
            y = random.randint(0,width-random_size)
            croped = gray[x:x+random_size, y:y+random_size]
            croped_filename = "data/learning_images/negative/" + str(i) + "_" + str(j) +".pgm" 
            croped_filename_bis = "../" + croped_filename
            cv2.imwrite(croped_filename, croped)
            bg.write("%s\n" % (croped_filename_bis))
            #bg.write("%s 1 0 0 %d %d\n" % (croped_filename_bis, size, size))
        except:
            print "Error file : %s : %d" % (filename, j)
    i+= 1

bg.close()

print "Number of files in negative: %s" % str(len(glob.glob("data/learning_images/negative/*.pgm"))) 



"""
opencv_createsamples -info info.dat -num 131 -w 24 -h 24 -vec node.vec 

opencv_createsamples -info info.dat -num 131 -maxyangle 1.1 maxzangle 0.75 -maxidev 40 -w 24 -h 24 -vec node.vec 
opencv_traincascade -data test3 -vec node.vec -bg bg.dat -numStages 10 -precalcValBufSize 1024 -precalcIdxBufSize 1024 -numPos 1692 -numNeg 2000 -w 24 -h 24

opencv_traincascade -data test5 -vec node.vec -bg bg.dat -numStages 10 -precalcValBufSize 1024 -precalcIdxBufSize 1024 -minhitrate 0.999 -maxfalsealarm 0.5 -numPos 52 -numNeg 200 -w 24 -h 24

opencv_traincascade -data test3 -vec node.vec -bg bg.dat -numStages 10 -precalcValBufSize 1024 -precalcIdxBufSize 1024 -nsplits 2 -minhitrate 0.99 -maxfalsealarm 0.5 -numPos 1200 -numNeg 2000 -w 24 -h 24
"""


