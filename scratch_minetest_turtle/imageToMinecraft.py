import pycraft_minetest as pcmt
import pycraft_minetest.blocklist as blocklist
import PIL as pl

""" 
   converte immagini jpg/png/gif in minetest usando blocchi di lana colorata come pixel 
   crea immagine in verticale a posizione assoluta
"""

# https://stackoverflow.com/questions/1109422/getting-list-of-pixel-values-from-pil

from PIL import Image

def distance(woolrgb, cpixel):
    """ ricerca il blocco di lana colorata piu' vicino al colore del pixel """
    r = cpixel[0]
    g = cpixel[1]
    b = cpixel[2]
    did = 0
    dmin = 255*255*3
    for i in woolrgb:
        dr = r - woolrgb[i][0]
        dg = g - woolrgb[i][1]
        db = b - woolrgb[i][2]
        d = dr*dr+dg*dg+db*db
        if d < dmin:
            dmin = d
            did = i
    return did

def imageToMinecraftColor(fname):
    im = Image.open(fname)
    print(im.size)
    #gray = im.convert('1')
    #bw = gray.point(lambda x: 0 if x < 128 else 255, '1')
    bw = im
    pixels = bw.load()  # this is not a list, nor is it list()'able
    width, height = bw.size
    bw.show()
    woolrgb, woolnames = minecraftrgbColors()
    for x in range(width):
        print (x)
        for y in range(height):
            cpixel = pixels[x, y]
            xc = x
            yc = (height-y)+8
            zc = 0
            matId = distance(woolrgb, cpixel)
            #if matId==0:
            #    mat=pcmt.air
            #else:
            mat = woolnames[matId]

            pcmt.block(mat, x=xc, y=yc, z=zc, absolute=True)

def imageToMinecraftBW(fname):
    im = Image.open(fname)
    print(im.size)
    gray = im.convert('1') # L opzione punteggiata
    bw = gray.point(lambda x: 0 if x < 128 else 255, '1')
    pixels = bw.load()  # this is not a list, nor is it list()'able
    width, height = bw.size
    bw.show()
    for x in range(width):
        print (x)
        for y in range(height):
            cpixel = pixels[x, y]
            xc = x
            yc = (height-y)+10
            zc = 0
            if cpixel > 0:
                mat = pcmt.glowstone
            else:
                mat = pcmt.ice
            pcmt.block(mat, x=xc, y=yc, z=zc, absolute=True)

def minecraftrgbColors():
    """
    codici colori dei blocchi wool
    https://minecraft.gamepedia.com/Wool
    """
    wool={  0:  '#E9ECEC',
            1:  '#F07613',
            2:  '#BD44B3',
            3:  '#3AAFD9',
            4:  '#F8C627',
            5:  '#70B919',
            6:  '#ED8DAC',
            7:  '#3E4447',
            8:  '#8E8E86',
            9:  '#158991',
            10: '#792AAC',
            11: '#35399D',
            12: '#724728',
            13: '#546D1B',
            14: '#A12722',
            15: '#141519'}
    woolrgb={}
    w = ['WOOL_WHITE',
     'WOOL_ORANGE',
     'WOOL_MAGENTA',
     'WOOL_LIGHT_BLUE',
     'WOOL_YELLOW',
     'WOOL_LIME',
     'WOOL_PINK',
     'WOOL_GRAY',
     'WOOL_LIGHT_GRAY',
     'WOOL_CYAN',
     'WOOL_PURPLE',
     'WOOL_BLUE',
     'WOOL_BROWN',
     'WOOL_GREEN',
     'WOOL_RED',
     'WOOL_BLACK']
    i = 0
    woolnames={}
    for id in wool:
        col = wool[id]
        r = int('0x'+col[1:3], 0)
        g = int('0x'+col[3:5], 0)
        b = int('0x'+col[5:7], 0)
        woolrgb[id] = [r, g, b]

        woolblock = getattr(blocklist, w[i])
        woolnames[id] = woolblock
        i = i + 1

    return woolrgb, woolnames

def colors():
    col=['WOOL_WHITE',
    'WOOL_ORANGE',
    'WOOL_MAGENTA',
    'WOOL_LIGHT_BLUE',
    'WOOL_YELLOW',
    'WOOL_LIME',
    'WOOL_PINK',
    'WOOL_GRAY',
    'WOOL_LIGHT_GRAY',
    'WOOL_CYAN',
    'WOOL_PURPLE',
    'WOOL_BLUE',
    'WOOL_BROWN',
    'WOOL_GREEN',
    'WOOL_RED',
    'WOOL_BLACK']

    for i in range(0,len(col)):
        c = getattr(blocklist,col[i])
        pcmt.block(c, i, 0, 0)

#colors()
imageToMinecraftColor("c:\\temp\\scratch.png")
#minecraftrgbColors()