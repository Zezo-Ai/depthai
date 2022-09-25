import depthai as dai
from typing import Union, Tuple, Optional, Dict, Any, Type


def rgbResolution(resolution: Union[None, str, dai.ColorCameraProperties.SensorResolution]) -> dai.ColorCameraProperties.SensorResolution:
    """
    Parses Color camera resolution based on the string
    """
    if isinstance(resolution, dai.ColorCameraProperties.SensorResolution) or resolution is None:
        return resolution

    resolution = str(resolution).upper()
    if resolution == '3120' or resolution == '13MP':
        return dai.ColorCameraProperties.SensorResolution.THE_13_MP
    elif resolution == '3040' or resolution == '12MP':
        return dai.ColorCameraProperties.SensorResolution.THE_12_MP
    elif resolution == '2160' or resolution == '4K':
        return dai.ColorCameraProperties.SensorResolution.THE_4_K
    # elif resolution == '1920' or resolution == '5MP':
    #     return dai.ColorCameraProperties.SensorResolution.THE_5_MP
    elif resolution == '800' or resolution == '800P':
        return dai.ColorCameraProperties.SensorResolution.THE_800_P
    elif resolution == '720' or resolution == '720P':
        return dai.ColorCameraProperties.SensorResolution.THE_720_P
    else:  # Default
        return dai.ColorCameraProperties.SensorResolution.THE_1080_P

def monoResolution(resolution: Union[None, str, dai.MonoCameraProperties.SensorResolution]) -> dai.MonoCameraProperties.SensorResolution:
    """
    Parses Mono camera resolution based on the string
    """
    if isinstance(resolution, dai.MonoCameraProperties.SensorResolution) or resolution is None:
        return resolution

    resolution = str(resolution).upper()
    if resolution == '800' or resolution == '800P' or resolution == '1MP':
        return dai.MonoCameraProperties.SensorResolution.THE_800_P
    elif resolution == '720' or resolution == '720P':
        return dai.MonoCameraProperties.SensorResolution.THE_720_P
    elif resolution == '480' or resolution == '480P':
        return dai.MonoCameraProperties.SensorResolution.THE_480_P
    else: # Default
        return dai.MonoCameraProperties.SensorResolution.THE_400_P

def parseResolution(
    camera: Union[dai.node.ColorCamera, dai.node.MonoCamera, Type],
    resolution: Union[str, dai.ColorCameraProperties.SensorResolution, dai.MonoCameraProperties.SensorResolution]
    ):
    if isinstance(camera, dai.node.ColorCamera) or camera == dai.node.ColorCamera:
        return rgbResolution(resolution)
    elif isinstance(camera, type(dai.node.MonoCamera)) or camera == dai.node.ColorCamera:
        return monoResolution(resolution)
    else:
        raise ValueError("camera must be either MonoCamera or ColorCamera!")

def parse_bool(value: str) -> bool:
    if value.upper() in ['1', 'TRUE', 'ON', 'YES']:
        return True
    elif value.upper() in ['0', 'FALSE', 'OFF', 'NO']:
        return False
    else:
        raise ValueError(f"Couldn't parse '{value}' to bool!")

def parse_usb_speed(speed: Union[None, str, dai.UsbSpeed]) -> Optional[dai.UsbSpeed]:
    if speed is None:
        return None
    elif isinstance(speed, dai.UsbSpeed):
        return speed
    elif isinstance(speed, str):
        if speed.upper() in ['HIGH', '2', 'USB2']:
            return dai.UsbSpeed.HIGH
        elif speed.upper() in ['SUPER', '3', 'USB3']:
            return dai.UsbSpeed.SUPER
    raise ValueError(f"Could not parse USB speed '{speed}' to dai.UsbSpeed!")

def parse_median_filter(filter: Union[int, dai.MedianFilter]) -> dai.MedianFilter:
    if isinstance(filter, dai.MedianFilter):
        return filter

    if filter == 3:
        return dai.MedianFilter.KERNEL_3x3
    elif filter == 5:
        return dai.MedianFilter.KERNEL_5x5
    elif filter == 7:
        return dai.MedianFilter.KERNEL_7x7
    else:
        return dai.MedianFilter.MEDIAN_OFF

def parseOpenVinoVersion(version: Union[None, str, dai.OpenVINO.Version]) -> Optional[dai.OpenVINO.Version]:
    if version is None:
        return None
    if isinstance(version, str):
        vals = None
        if '.' in version:
            vals = version.split('.')
        elif '_' in version:
            vals = version.split('_')
        if vals is None:
            return None
        version = getattr(dai.OpenVINO.Version, f"VERSION_{vals[0]}_{vals[1]}")
    return version

def parseSize(size: Union[str, Tuple[int, int]]) -> Tuple[int, int]:
    if isinstance(size, Tuple):
        return size
    elif isinstance(size, str):
        vals = size.split('x')
        if len(vals) != 2: raise ValueError("Size must be in format '[width]x[height]'!")
        return Tuple[int(vals[0]), int(vals[1])]
    else:
        raise ValueError("Size typle not supported!")


def parseColorCamControl(options: Dict[str, Any], cam: dai.node.ColorCamera):
    from .camera_helper import setCameraControl
    setCameraControl(cam.initialControl,
                     options.get('manualFocus', None),
                     options.get('afMode', None),
                     options.get('awbMode', None),
                     options.get('sceneMode', None),
                     options.get('antiBandingMode', None),
                     options.get('effectMode', None),
                     options.get('sharpness', None),
                     options.get('lumaDenoise', None),
                     options.get('chromaDenoise', None),
                     )


def parseEncode(encode = Union[str, bool, dai.VideoEncoderProperties.Profile]
                ) -> dai.VideoEncoderProperties.Profile:
    if isinstance(encode, dai.VideoEncoderProperties.Profile):
        return encode
    elif isinstance(encode, bool) and encode:
        return dai.VideoEncoderProperties.Profile.MJPEG  # MJPEG by default
    elif isinstance(encode, str):
        encode = encode.upper()
        if encode in ['MJPEG', 'JPEG', 'JPG', '.MJPEG', '.JPEG', '.JPG']:
            return dai.VideoEncoderProperties.Profile.MJPEG
        elif encode in ['H265', '.H265', 'H.265', 'HEVC', '.HEVC']:
            return dai.VideoEncoderProperties.Profile.H265_MAIN
        elif encode in ['H264', '.H264', 'H.264', 'MPEG-4', 'MPEG', 'AVC']:
            return dai.VideoEncoderProperties.Profile.H265_MAIN
    raise ValueError(f"Parsing user-defined encode value '{encode}' failed!")

def parse_cam_socket(socket = Union[str, dai.CameraBoardSocket]) -> dai.CameraBoardSocket:
    if isinstance(socket, dai.CameraBoardSocket):
        return socket
    elif isinstance(socket, str):
        socket = socket.upper()
        if socket in ['RGB', 'COLOR']:
            return dai.CameraBoardSocket.RGB
        elif socket == 'RIGHT':
            return dai.CameraBoardSocket.RIGHT
        elif socket == 'LEFT':
            return dai.CameraBoardSocket.LEFT
    raise ValueError(f"Parsing user-defined camera board socket value '{socket}' failed!")

