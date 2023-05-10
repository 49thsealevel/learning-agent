import numpy as np
import platform
from PIL import ImageGrab

if platform.system() == "Darwin":
    try:
        import Quartz.CoreGraphics as CG
        import Quartz
    except:
        raise Exception("Unable to perform necessary import for Mac")


class ScreenGrabber:
    def grab_screen(self) -> np.ndarray:
        raise NotImplementedError()


class WindowsScreenGrabber(ScreenGrabber):
    def grab_screen(self):
        img = ImageGrab.grab()
        screen = np.array(img)
        return screen


class MacScreenGrabber(ScreenGrabber):
    def grab_screen(self) -> np.ndarray:
        main_display_id = Quartz.CGMainDisplayID()
        image = CG.CGDisplayCreateImage(main_display_id)
        width = CG.CGImageGetWidth(image)
        height = CG.CGImageGetHeight(image)
        bytesperrow = CG.CGImageGetBytesPerRow(image)

        pixeldata = CG.CGDataProviderCopyData(CG.CGImageGetDataProvider(image))
        image = np.frombuffer(pixeldata, dtype=np.uint8)
        image = image.reshape((height, bytesperrow // 4, 4))
        image = image[:, :width, :]
        return image
