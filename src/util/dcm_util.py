import pydicom
import numpy as np
from PIL import Image, ImageOps
from pydicom.pixel_data_handlers.util import apply_voi_lut

def load_dicom_image(file_path: str):
    loaded_dcm_file = pydicom.dcmread(file_path)

    pixels = apply_voi_lut(loaded_dcm_file.pixel_array, loaded_dcm_file)

    if loaded_dcm_file.get("PhotometricInterpretation") == "MONOCHROME1":
        pixels = np.amax(pixels) - pixels

    return pixels


def normalize_to_8bit(pixels_array):
    p_min, p_max = np.min(pixels_array), np.max(pixels_array)

    if p_max == p_min:
        return np.zeros(pixels_array.shape, dtype=np.uint8)

    pixels_scaled = ((pixels_array - p_min) / (p_max - p_min)) * 255.0
    return pixels_scaled.astype(np.uint8)


def resize_with_padding(uint8_array, size=(224, 224)):
    image = Image.fromarray(uint8_array)

    image.thumbnail(size, Image.Resampling.LANCZOS)

    dw = size[0] - image.size[0]
    dh = size[1] - image.size[1]

    padding = (dw // 2, dh // 2, dw - (dw // 2), dh - (dh // 2))

    return ImageOps.expand(image, padding, fill=0)


def get_suffix(dcm_file) -> str:
    ds = pydicom.dcmread(dcm_file)

    view = str(ds.get("ViewPosition", "")).upper()
    desc = str(ds.get("SeriesDescription", "")).upper()

    if view == "PA" or "PA" in desc:
        return "PA"
    elif view == "LAT" or "PERFIL" in desc or "LATERAL" in desc:
        return "PERFIL"
    else:
        return "IGNORADO"
