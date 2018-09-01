from keras.models import Model, load_model
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
from skimage.transform import resize
from imageio import imread
import numpy as np
import csv
import os
import tensorflow as tf
import time
import logging

log = logging.getLogger(__name__) 

class Predict:
    def __init__(self, model_path, label_path):
        """
        load the model and the label names
        model_path: string contaning path to model.h5 file
        label_path: string contaning path to label.csv file
        Returns: None
        """
        # load the model
        self.model = load_model(model_path)
        self.model._make_predict_function()
        self.graph = tf.get_default_graph()

        # load labels
        self.label_names = {}
        with open(label_path) as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                self.label_names[int(line[1])] = line[0]

    def make_prediction(self, filepath):
        """
        pass the input to the model for prediction
        Returns: list containing top 3 predictions along with percentage probability
        """
        x = self.load_img_from_path(filepath)
        x = np.expand_dims(x, axis=0)
        s1 = time.time()
        with self.graph.as_default():
            preds = self.model.predict(x)
        
        log.debug('make_prediction: ' +  str(time.time() - s1))
        idx = np.argsort(preds)[0][-3:][::-1]
        percent = preds[0][idx]*100
        out = [self.label_names[i] for i in idx]        
        return list(zip(out,percent))

    def load_img_from_path(self, filepath):
        '''
        load the image from the given path and convert it to numpy array
        Returns: numpy array
        '''
        x = resize(imread(filepath), (224, 224)).astype(np.float32)
        x = image.img_to_array(x)
        return x        