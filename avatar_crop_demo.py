"""Rizline的头像截取demo,与游戏内尚有一定差距.
    Rizline的头像截取以右上角为原点,玩家截取所能到达的最左侧坐标为(1,0),最下侧为(0,1),
    Rizline的z为背景的放大倍率."""

from PIL import Image,ImageDraw

AVATAR_PATH = "illustration.BRAVEROAD.umavsMorimoriAtsushi.0.png"  # 这里要填写头像的路径

AVATAR_POS = {  # 对应存档文件的"rizcard"中的"avatarPos"
    "x": 0.22031038999557495,
    "y": 0.25898006558418274,
    "z": 3
}

bg = Image.open(AVATAR_PATH,"r")  # 读取曲绘图片
bg = bg.resize((int(1080*AVATAR_POS["z"]),int(1080*AVATAR_POS["z"])))  # 将曲绘放大
w = int(1080*AVATAR_POS["z"]) - 960 - 120  # 计算出实际在屏幕上可移动的px数(曲绘放大后大小-中心圆直径960px-两边保护px共120) 

circle_img = Image.new("RGBA", bg.size, (0, 0, 0, 0))  # 创建一个画布用以生成圆形模板
draw = ImageDraw.Draw(circle_img)
x = (1-AVATAR_POS["x"]) * w + 480 + 60  # PIL以左上角为原点,而截取图像以右上角为原点 因此需要对x坐标进行一次反转
y = AVATAR_POS["y"] * w + 480 + 60  # +480是圆形半径 +60是加上一边的保护px数
draw.circle((x,y), radius=480, fill=(255, 255, 255, 255))  # 绘制圆形~
avatar_image = Image.composite(bg, circle_img, circle_img)  # 将蒙板套入曲绘
avatar_image = avatar_image.crop((x-480,y-480,x+480,y+480))  # 对结果进行裁切

avatar_image.save("demo.png")