import tensorflow as tf
from urllib.request import urlopen
from PIL import Image
import numpy as np
import cv2
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import joblib

# Constants
GENDER_CLASSES = {'Boys': 0, 'Girls': 1, 'Men': 2, 'Unisex': 3, 'Women': 4}

COLOUR_CLASSES = {'Beige': 0, 'Black': 1, 'Blue': 2, 'Brown': 4, 'Bronze': 3, 'Burgundy': 5, 'Charcoal': 6, 'Coffee Brown': 7, 'Copper': 8, 'Cream': 9, 'Gold': 10, 'Green': 11, 'Grey': 12, 'Grey Melange': 13, 'Khaki': 14, 'Lavender': 15, 'Lime Green': 16, 'Magenta': 17, 'Maroon': 18, 'Mauve': 19, 'Metallic': 20, 'Multi': 21,
                  'Mushroom Brown': 22, 'Mustard': 23, 'Navy Blue': 24, 'Nude': 25, 'Off White': 26, 'Olive': 27, 'Orange': 28, 'Peach': 29, 'Pink': 30, 'Purple': 31, 'Red': 32, 'Rose': 33, 'Rust': 34, 'Sea Green': 35, 'Silver': 36, 'Skin': 37, 'Steel': 38, 'Tan': 39, 'Taupe': 40, 'Teal': 41, 'Turquoise Blue': 42, 'White': 43, 'Yellow': 44}

ARTICLE_CLASSES = joblib.load('./models/art.npy')

# Invert the dictionaires
COLOUR_CLASSES = {COLOUR_CLASSES[k]: k for k in COLOUR_CLASSES}

GENDER_CLASSES = {GENDER_CLASSES[k]: k for k in GENDER_CLASSES}

ARTICLE_CLASSES = {ARTICLE_CLASSES[k]: k for k in ARTICLE_CLASSES}

# Load Models
colour_model = load_model('./models/colour.hdf5')
article_model = load_model('./models/article.hdf5')
gender_model = load_model('./models/gender.hdf5')
# Helper Methods


def get_Top3(arr, mode):
    if (mode == 'colour'):
        top3_indices = np.argsort(-arr)[0][:3]
        return [[COLOUR_CLASSES[i], f'{round(arr[0][i]*100,2)}'] for i in top3_indices]

    if (mode == 'article'):
        top3_indices = np.argsort(-arr)[0][:3]
        return [[ARTICLE_CLASSES[i], f'{round(arr[0][i]*100,2)}'] for i in top3_indices]

    if(mode == 'gender'):
        top3_indices = np.argsort(-arr)[0][:3]
        return [[GENDER_CLASSES[i], f'{round(arr[0][i]*100,2)}'] for i in top3_indices]


def predict(img):
    # img = load_img('./temp/'+file_name, target_size=(224, 224, 3))
    img = np.array(img)
    img = preprocess_input(img)
    img = np.array([img])
    pred = {}
    pred['colour'] = get_Top3(colour_model.predict(img), 'colour')
    pred['article'] = get_Top3(article_model.predict(img), 'article')
    pred['gender'] = get_Top3(gender_model.predict(img), 'gender')
    return pred


def predict_from_file(file):
    img = load_img(file, target_size=(224, 224))
    return predict(img)


def predict_from_url(url):
    # img = load_img('./temp/'+file_name, target_size=(224, 224, 3))
    img = load_img(urlopen(url), target_size=(224, 224))
    return predict(img)
