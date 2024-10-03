import os
import random

# Paths to images (update these paths based on your folder structure)
KOALA_IMAGE_PATH = './images/'
koala_classes = ["Koala_1", "Koala_2"]

# Get reference images for a koala class
def get_reference_images(koala_class):
    images_path = os.path.join(KOALA_IMAGE_PATH, koala_class)
    return [os.path.join(images_path, img) for img in os.listdir(images_path) if 'reference' in img]

# Get a random unseen image for a quiz
def get_quiz_image(koala_class):
    images_path = os.path.join(KOALA_IMAGE_PATH, koala_class)
    unseen_images = [img for img in os.listdir(images_path) if 'unseen' in img]
    return os.path.join(images_path, random.choice(unseen_images))

# Get all koala classes
def get_koala_classes():
    return koala_classes
