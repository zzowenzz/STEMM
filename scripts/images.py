import os
import random
from PIL import Image

# Paths to images (update these paths based on your folder structure)
KOALA_IMAGE_PATH = './images/'
koala_classes = ["DES_alana", "DES_alex", "DES_ally", "DES_anke"]  # Koala classes

# Get shuffled reference images for a koala class
def get_reference_images(koala_class):
    images_path = os.path.join(KOALA_IMAGE_PATH, koala_class)
    reference_images = [os.path.join(images_path, img) for img in os.listdir(images_path) if 'reference' in img]
    random.shuffle(reference_images)  # Shuffle the order of reference images
    return reference_images

# Get a random unseen image for a quiz (we will pick a random unseen image for each user)
def get_quiz_image(koala_class):
    images_path = os.path.join(KOALA_IMAGE_PATH, koala_class)
    unseen_images = [os.path.join(images_path, img) for img in os.listdir(images_path) if 'unseen' in img]
    return random.choice(unseen_images)  # Randomly select one unseen image for the quiz

# Get all koala classes
def get_koala_classes():
    return koala_classes

# Resize images to a uniform size
def resize_image(image_path, size=(50, 50)):
    img = Image.open(image_path)
    return img.resize(size)