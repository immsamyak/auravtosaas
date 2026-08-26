from PIL import Image

img_light = Image.open('backend/screenshots/light_mode_toggle_test.png')
img_dark = Image.open('backend/screenshots/dark_mode_toggle_test.png')

print("Light mode top-left pixel:", img_light.getpixel((0,0)))
print("Dark mode top-left pixel:", img_dark.getpixel((0,0)))
print("Light mode center pixel:", img_light.getpixel((640,400)))
print("Dark mode center pixel:", img_dark.getpixel((640,400)))
