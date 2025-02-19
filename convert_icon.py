from PIL import Image

# Convert PNG to ICO
img = Image.open('assets/icon.png')
img.save('assets/icon.ico', sizes=[(256, 256)])
