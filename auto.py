import autopy
from PIL import ImageGrab
from win32gui import GetWindowText, GetForegroundWindow, GetWindowRect, FindWindowEx



#win2find = input('enter name of window to find')
whnd = FindWindowEx(None, None, None, 'hearthstone')
if not (whnd == 0):
  print('FOUND!')


print(GetWindowRect(whnd))
img = ImageGrab.grab(GetWindowRect(whnd))
img.show()




rect = GetWindowRect(FindWindowEx(None, None, None, 'hearthstone'))
x = rect[0]
y = rect[1]
w = rect[2] - x
h = rect[3] - y
print("Window %s:" % GetWindowText(FindWindowEx(None, None, None, 'hearthstone')))
print("\tLocation: (%d, %d)" % (x, y))
print("\t    Size: (%d, %d)" % (w, h))

#x=0.0
#y=0.0
#print("Returns the scale of the main screen, i.e. how many pixels are in a point.")
#print(autopy.screen.scale()) #→ float
#
#print("Returns a tuple (width, height) of the size of the main screen in points.")
#print(autopy.screen.size()) #-> (float, float)
#
#   
#print("Returns True if the given point is inside the main screen boundaries.")
#print(autopy.screen.is_point_visible(x, y)) #→ bool
#
#    
#print("Returns hexadecimal value describing the color at a given point.")
#
#print(autopy.screen.get_color(x, y)) #-> (int, int, int)



#GetWindowRect(hwnd, &rect)
#DwmGetWindowAttribute(hwnd, DWMWA_EXTENDED_FRAME_BOUNDS, &frame, sizeof(RECT))
#
#border.left = frame.left - rect.left
#border.top = frame.top - rect.top
#border.right = rect.right - frame.right
#border.bottom = rect.bottom - frame.bottom
#
#rect.left -= border.left
#rect.top -= border.top
#rect.right += border.left + border.right
#rect.bottom += border.top + border.bottom


