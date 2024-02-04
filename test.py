import pytest
import glob
import cat_detect
# from cat_detect import *
model = cat_detect.CatDetector()

IMAGES = glob.glob('./images/cat/*.jpg')
@pytest.mark.parametrize('image_path',IMAGES)
def test_cat_images(image_path):
    image = cat_detect.image_from_path(image_path)
    cat_in_image = model.detect_cat(image)
    assert cat_in_image

def test_images(image_path, cat_in_image):
    image = cat_detect.image_from_path(image_path)
    


IMAGES = glob.glob('./images/dog/*.jpg')
@pytest.mark.parametrize('image_path',IMAGES)
def test_dog_images(image_path):
    image = cat_detect.image_from_path(image_path)
    cat_in_image = model.detect_cat(image)
    assert not cat_in_image

def test_get_remote_image():
    cam = cat_detect.RemoteCameraClient()
    image = cam.get_image()
    breakpoint()

IMAGES = glob.glob('./images/rpi0/image*')
@pytest.mark.parametrize('image_path',IMAGES)
def test_resize_image(image_path):
    image = cat_detect.image_from_path(image_path)
    image_resized = cat_detect.resize(image,(300,300))
    assert image.shape[-2] > image_resized.shape[-2]
    assert image.shape[-1] > image_resized.shape[-1]
    assert image_resized.shape[-2] == image_resized.shape[-1] == 300

    # assert all([])

# def test_detect_dog('image')
# IMAGES = glob.glob('./images/cat/*.jpg')
@pytest.mark.parametrize('animal',['dog','cat'])
def test_detect(animal):
    IMAGES = glob.glob(f'./images/{animal}/*.jpg')
    for image_path in IMAGES:
        image = cat_detect.image_from_path(image_path)
        animal_in_image = model.detect(image, animal)
        assert animal_in_image