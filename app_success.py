from pix2text import Pix2Text

img_fp = './uploads/congthuc.png'
p2t = Pix2Text.from_config()
outs = p2t.recognize_formula(img_fp)
print(outs)