import pytest 
import os
from PIL import Image
import tkinter as tk
from main import ImageReductionApp 

@pytest.fixture
def sample_image():
    test_image = Image.new('RGB', (300, 200), color = 'red')
    test_image_path = 'test_image.png'
    test_image.save(test_image_path)
    yield test_image_path
    if os.path.exists(test_image_path):
        os.remove(test_image_path)

@pytest.fixture
def app():
    root = tk.Tk()
    app = ImageReductionApp(root)
    yield app
    root.destroy()

def test_load_image(app, sample_image):   
    app.original_image = Image.open(sample_image)
    assert app.original_image is not None
    assert app.original_image.size == (300, 200)

def test_reduce_image(app, sample_image):
    app.original_image = Image.open(sample_image)
    app.reduction_factor.set(2)
    app.reduction_method.set('Lanczos')
    app.reduce_image()
    assert app.processed_image is not None
    assert app.processed_image.size == (150, 100)

def test_save_image(app, sample_image, tmp_path):
    app.original_image = Image.open(sample_image)
    app.reduction_factor.set(2)
    app.reduce_image()
    save_path = tmp_path / 'reduced_image.jpg'
    app.processed_image.save(save_path)
    assert os.path.exists(save_path)

def test_invalid_image_loading(app):
    with pytest.raises(Exception):
        app.load_image()

def test_multiple_reductions(app, sample_image):
    app.original_image = Image.open(sample_image)
    reduction_factors = [2, 3, 4]
    for factor in reduction_factors:
        app.reduction_factor.set(factor)
        app.reduce_image()
        expected_width = 300 // factor
        expected_height = 200 // factor
        assert app.processed_image.size == (expected_width, expected_height)

def test_interpolation_methods(app, sample_image):
    methods = ['Nearest', 'Bilinear', 'Bicubic', 'Lanczos']
    
    for method in methods:
        app.original_image = Image.open(sample_image)
        app.reduction_method.set(method)
        app.reduction_factor.set(2)
        app.reduce_image()
        assert app.processed_image is not None
        assert app.processed_image.size == (150, 100)