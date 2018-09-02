import sys
sys.path.insert(0,'C:\\Users\\Igor\\Documents\\Python\\Projects and Scripts\\IGE\\')
import IGE_API as ige
from IGE_API import ndi, show, get_ssim, sk

#src = 'C:\\Users\\Igor\\Desktop\\scc.png'
#dest = '\\'.join(src.split('\\')[:-1]) + '\\'


i1 = ndi.imread('D:\\1.png',flatten=True)
i1 = i1[i1.shape[0]-168:][:]

i2 = ndi.imread('D:\\2.png',flatten=True)
i2 = i2[i2.shape[0]-168:][:]

i3 = ndi.imread('D:\\3.png',flatten=True)
i3 = i3[i3.shape[0]-168:][:]

i4 = ndi.imread('D:\\4.png',flatten=True)
i4 = i4[i4.shape[0]-168:][:]

i5 = ndi.imread('D:\\5.png',flatten=True)
i5 = i5[i5.shape[0]-168:][:]

pics = [i1, i2, i3, i4, i5]

    

for x in range(5):
    for y in range(5):
        print('Comparing ' + str(x+1) +' with '+ str(y+1))
        get_ssim(pics[x],pics[y],readPaths=False, otsu=100)
        print()
    print('==============================')
    #show(pics[x])
        


#ex.getNameAndPic(src=src, dest=dest,saveAll=True, drawAll=True)

#img = ''
#name = m.getNameAndPic(img)

'''
==========PLAN==========
formats: check by bottom bar (2 versions)
'''
