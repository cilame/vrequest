canread = ['.bmp', '.dib', '.jpeg', '.jpg', '.jpe', '.jp2', '.png', '.webp', '.pbm', '.pgm', '.ppm', '.pxm', '.pnm', '.sr', '.ras', '.tiff', '.tif', '.exr', '.hdr', '.pic']

import cv2

def canny(filepathname, left=70, right=140):
    v = cv2.imread(filepathname)
    s = cv2.cvtColor(v, cv2.COLOR_BGR2GRAY)
    s = cv2.Canny(s, left, right)
    cv2.imshow('nier',s)
    return s

    # 圈出最小方矩形框，这里Canny算法后都是白色线条，所以取色范围 127-255 即可。
    # ret, binary = cv2.threshold(s,127,255,cv2.THRESH_BINARY) 
    # contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # for c in contours:
    #     x,y,w,h = cv2.boundingRect(c)
    #     if w>5 and h>10: # 有约束的画框
    #         cv2.rectangle(v,(x,y),(x+w,y+h),(155,155,0),1)
    # # cv2.drawContours(s,contours,-1,(0,0,255),3) # 画所有框
    # cv2.imshow('nier2',v)

    # cv2.waitKey()
    # cv2.destroyAllWindows()


def laplacian(filepathname):
    v = cv2.imread(filepathname)
    s = cv2.cvtColor(v, cv2.COLOR_BGR2GRAY)
    s = cv2.Laplacian(s, cv2.CV_16S, ksize=3)
    s = cv2.convertScaleAbs(s)
    cv2.imshow('nier',s)
    return s

    # ret, binary = cv2.threshold(s,40,255,cv2.THRESH_BINARY)
    # contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # for c in contours:
    #     x,y,w,h = cv2.boundingRect(c)
    #     if w>5 and h>10:
    #         cv2.rectangle(v,(x,y),(x+w,y+h),(155,155,0),1)
    # cv2.imshow('nier2',v)

    # cv2.waitKey()
    # cv2.destroyAllWindows()


def sobel(filepathname):
    v = cv2.imread(filepathname)
    s = cv2.cvtColor(v,cv2.COLOR_BGR2GRAY)
    x, y = cv2.Sobel(s,cv2.CV_16S,1,0), cv2.Sobel(s,cv2.CV_16S,0,1)
    s = cv2.convertScaleAbs(cv2.subtract(x,y))
    s = cv2.blur(s,(9,9))
    cv2.imshow('nier',s)
    return s

    # ret, binary = cv2.threshold(s,40,255,cv2.THRESH_BINARY)
    # contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # for c in contours:
    #     x,y,w,h = cv2.boundingRect(c)
    #     if w>5 and h>10:
    #         cv2.rectangle(v,(x,y),(x+w,y+h),(155,155,0),1)
    # cv2.imshow('nier2',v)

    # cv2.waitKey()
    # cv2.destroyAllWindows()


def findmatchtemplate(filepathname, befindimage):
    # 从 befindimage 中找到 filepathname，（befindimage 是大图，filepathname 是小图）
    img1 = cv2.imread(filepathname)
    img2 = cv2.imread(befindimage)
    w, h = img1.shape[:2]
    v = cv2.matchTemplate(img2,img1,cv2.TM_CCOEFF)
    a, b, c, top_left = cv2.minMaxLoc(v)
    bot_right = top_left[0]+h, top_left[1]+w
    img3 = cv2.rectangle(img2, top_left, bot_right, (155,155,0), 1)
    cv2.imshow('nier', img3)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    return top_left[0], top_left[1], w, h