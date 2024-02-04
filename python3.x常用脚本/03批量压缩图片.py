from PIL import Image
from os import path,listdir,mkdir
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES=True
Image.MAX_IMAGE_PIXELS=None


root=r"D:\图纸"
save_path=r"D:\图纸"


for pics in listdir(root):
    img=Image.open(path.join(root,pics))
    cp_img=img.copy()
    cp_img.save(path.join(save_path,pics),quality=33)
    print(pics)

# root=r"D:\图纸"
# save_root=r"D:\图纸压缩后"

# for jieZhen in listdir(root):
#     mkdir(path.join(save_root,jieZhen)) if not path.exists(path.join(save_root,jieZhen)) else None
#     img_path=path.join(root,jieZhen)
#     for pics in listdir(img_path):
#         pics_path=path.join(img_path,pics)
#         P=Image.open(pics_path)
#         cp_p=P.copy()
#         save_path=path.join(save_root,jieZhen,pics)
#         cp_p.save(save_path,quality=5)
#         print(save_path)




# print(listdir(root))

# img=Image.open(pth)

# cp_img=img.copy()

# save_pth="D:\图纸压缩后"

# cp_img.save(path.join(save_pth,path.basename(pth)),quality=5)