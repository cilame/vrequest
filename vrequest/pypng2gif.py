# 通过生成的png生成gif图片

import os
from PIL import Image

def create_gif(filepathname,filedir,size=None,scale=None,step=1):
    d = []
    for i in os.listdir(filedir):
        if i.endswith('.png'):
            d.append(os.path.join(filedir,i))
    func = lambda i: int(os.path.split(i)[-1].rsplit('.')[0])
    r = []
    for i in sorted(d,key=func):
        r.append(Image.open(i))
    q = []
    for i in r[::step]:
        if size is not None:
            q.append(i.resize(size))
        elif scale is not None:
            width = int(i.width/scale)
            height = int(i.height/scale)
            q.append(i.resize((width,height)))
        else:
            q.append(i)
    q[0].save(
        filepathname,
        save_all=True,
        append_images=q[1:],
        loop=0,
        duration=120,
        comment=b"aaabb"
    )
    return q[0].size

if __name__ == '__main__':
    filedir = r'C:\Users\Administrator\Desktop\_temp'
    filepathname = r'C:\Users\Administrator\Desktop\gif.gif'
    create_gif(filepathname,filedir,step=2)
