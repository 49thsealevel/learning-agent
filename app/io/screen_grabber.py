import numpy as np


class ScreenGrabber:
    def grab_screen(self) -> np.ndarray:
        raise NotImplementedError()


class WindowsScreenGrabber(ScreenGrabber):
    def __init__(self):
        try:
            from win32gui import FindWindow, GetWindowRect
        except:
            raise Exception("Unable to perform necessary import for Windows")

    def grab_screen(self):
        window_handle = FindWindow(None, None)
        window_rect = GetWindowRect(window_handle)
        screen = np.array(ImageGrab.grab(bbox=window_rect))
        return screen


class MacScreenGrabber(ScreenGrabber):
    def __init__(self):
        try:
            import Quartz.CoreGraphics as CG
            import Quartz
        except:
            raise Exception("Unable to perform necessary import for Mac")

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
