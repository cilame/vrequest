# 处理简单的截图以及截图录制的功能

import zlib
import ctypes
from struct import pack, calcsize, unpack
GetWindowDC             = ctypes.windll.user32.GetWindowDC
GetSystemMetrics        = ctypes.windll.user32.GetSystemMetrics
SelectObject            = ctypes.windll.gdi32.SelectObject
DeleteObject            = ctypes.windll.gdi32.DeleteObject
BitBlt                  = ctypes.windll.gdi32.BitBlt
GetDIBits               = ctypes.windll.gdi32.GetDIBits
CreateCompatibleDC      = ctypes.windll.gdi32.CreateCompatibleDC
CreateCompatibleBitmap  = ctypes.windll.gdi32.CreateCompatibleBitmap

def desktop_ltwh():
    return (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))

def screenshot(shape:'left,top,width,height'=None):
    def png_bit(data, size, level=6):
        width, height = size
        line = width * 3
        png_filter = pack(">B", 0)
        scanlines = b"".join(
            [png_filter + data[y * line : y * line + line] for y in range(height)][::-1]
        )
        magic = pack(">8B", 137, 80, 78, 71, 13, 10, 26, 10)
        ihdr = [b"", b"IHDR", b"", b""]
        ihdr[2] = pack(">2I5B", width, height, 8, 2, 0, 0, 0)
        ihdr[3] = pack(">I", zlib.crc32(b"".join(ihdr[1:3])) & 0xFFFFFFFF)
        ihdr[0] = pack(">I", len(ihdr[2]))
        idat = [b"", b"IDAT", zlib.compress(scanlines, level), b""]
        idat[3] = pack(">I", zlib.crc32(b"".join(idat[1:3])) & 0xFFFFFFFF)
        idat[0] = pack(">I", len(idat[2]))
        iend = [b"", b"IEND", b"", b""]
        iend[3] = pack(">I", zlib.crc32(iend[1]) & 0xFFFFFFFF)
        iend[0] = pack(">I", len(iend[2]))
        return magic + b"".join(ihdr + idat + iend)

    left, top, width, height = shape if shape else desktop_ltwh()
    bmi      = pack('LHHHH', calcsize('LHHHH'), width, height, 1, 32)
    srcdc    = GetWindowDC(0)
    memdc    = CreateCompatibleDC(srcdc)
    svbmp    = CreateCompatibleBitmap(srcdc, width, height)
    SelectObject(memdc, svbmp); BitBlt(memdc, 0, 0, width, height, srcdc, left, top, 13369376)
    _data    = ctypes.create_string_buffer(height * width * 4)
    got_bits = GetDIBits(memdc, svbmp, 0, height, _data, bmi, 0)
    DeleteObject(memdc)
    data = bytes(_data)
    rgb = bytearray(width * height * 3)
    rgb[0::3],rgb[1::3],rgb[2::3] = data[2::4],data[1::4],data[0::4]
    size = (width, height)
    return png_bit(rgb, size) # 全屏截图 png bit 数据

def create_png_pixel_tobytes(png_bit, shapelimit=None):
    left, top, width, height = [0,0,10000000,10000000] if shapelimit is None else shapelimit
    b = png_bit.find(b'IHDR')
    q = calcsize(">2I")
    w, h = unpack(">2I", png_bit[b+4:b+4+q])
    b = png_bit.find(b'IDAT')
    q = calcsize(">I")
    v = unpack(">I", png_bit[b-q:b])[0]
    v = png_bit[b+4:b+4+v]
    z = zlib.decompress(v[2:-4], -15)
    l, p = w * 3 + 1, []
    for i in range(h):
        if i >= top and i < top + height:
            li = z[i*l:(i+1)*l][1:]
            for j in range(w):
                if j >= left and j < left + width:
                    p.append(sum(li[(j)*3 : (j+1)*3])//3)
    w, h = (w, h) if shapelimit is None else (width, height)
    p = [255 if i > 123 else 0 for i in p] # 人工二值化
    return bytes(p), w, h



import tkinter
# 主要的截图处理工具，用于快速截图或者鼠标框选部分进行定位处理的工具
class PicCapture:
    def __init__(self, root, png):
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        self.top = tkinter.Toplevel(root, width=sw, height=sh)
        self.top.overrideredirect(True)
        self.canvas = tkinter.Canvas(self.top, bg='white', width=sw, height=sh)
        self.image  = tkinter.PhotoImage(file=png)
        self.canvas.create_image(sw//2, sh//2, image=self.image)
        self.fin_draw = None
        def btndown(event):
            self.X.set(event.x)
            self.Y.set(event.y)
            self.sel = True
        self.canvas.bind('<Button-1>', btndown)
        def btnmove(event):
            if not self.sel:
                return
            try:
                self.canvas.delete(self.fin_draw)
            except Exception as e:
                pass
            self.fin_draw = self.canvas.create_rectangle(
                                    self.X.get(), 
                                    self.Y.get(), 
                                    event.x, 
                                    event.y, 
                                    outline='red')
            
        self.canvas.bind('<B1-Motion>', btnmove)
        def btnup(event):
            self.sel = False
            try:
                self.canvas.delete(self.fin_draw)
            except Exception as e:
                pass
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])
            self.rect = (left, top, right, bottom)
            self.top.destroy()
        self.canvas.bind('<ButtonRelease-1>', btnup)
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)

import os
import tempfile
def screenshot_rect(root):
    filename = os.path.join(os.path.dirname(tempfile.mktemp()), 'temp.png')
    screenshot_bit = screenshot()
    with open(filename,'wb') as f:
        f.write(screenshot_bit)
    picshot = PicCapture(root, filename)
    root.wait_window(picshot.top)
    left, top, right, bottom = picshot.rect
    left, top, width, height = left, top, right-left, bottom-top
    os.remove(filename)
    return screenshot((left, top, width, height))

def screenshot_rect_int(root):
    filename = os.path.join(os.path.dirname(tempfile.mktemp()), 'temp.png')
    screenshot_bit = screenshot()
    with open(filename,'wb') as f:
        f.write(screenshot_bit)
    picshot = PicCapture(root, filename)
    root.wait_window(picshot.top)
    left, top, right, bottom = picshot.rect
    left, top, width, height = left, top, right-left, bottom-top
    os.remove(filename)
    return left, top, width, height

import time
import threading
import shutil
class screenvideo:
    def __init__(self, filepath, rect, dirname='_temp', print=print):
        self.filepath = os.path.join(filepath, dirname)
        self.rect     = rect
        self.cencel   = False
        self.print    = print
        if not os.path.isdir(self.filepath):
            if os.path.isfile(self.filepath):
                os.remove(self.filepath)
            os.mkdir(self.filepath)
        else:
            shutil.rmtree(self.filepath)
            os.mkdir(self.filepath)
    def start_video(self):
        self.print('start.')
        def _():
            idx = 0
            while True:
                time.sleep(1/24)
                filepathname = os.path.join(self.filepath, '{}.png'.format(idx))
                self.print('write in:{}'.format(filepathname))
                idx += 1
                with open(filepathname, 'wb') as f:
                    f.write(screenshot(self.rect))
                if self.cencel:
                    self.print('stop.')
                    break
        threading.Thread(target=_).start()
    def stop_video(self):
        self.cencel = True

sv = None
def _start_video(desktop, rect, dirname, print=print):
    global sv
    sv = screenvideo(desktop, rect, dirname, print)
    sv.start_video()
def _stop_video():
    global sv
    if sv is not None:
        sv.stop_video()

if __name__ == '__main__':
    # 截图存放到桌面
    s = tkinter.Tk()
    def start(*a): 
        desktop = os.path.join(os.path.expanduser("~"),'Desktop')
        rect    = screenshot_rect_int(s)
        _start_video(desktop, rect, '_temp')
    def stop(*a):  
        _stop_video()

    def parse_rect_from_png_bytes(*a):
        dtop = os.path.join(os.path.expanduser("~"),'Desktop')
        dfile = os.path.join(dtop, '_temp.png')
        bitpng = screenshot_rect(s)
        with open(dfile, 'wb') as f:
            f.write(bitpng)
    
    tkinter.Button(s,text='截图获取坐标开始录制',command=start,width=40).pack()
    tkinter.Button(s,text='停止录制',command=stop,width=40).pack()
    tkinter.Button(s,text='普通的截图存放到桌面',command=parse_rect_from_png_bytes,width=40).pack()
    s.mainloop()