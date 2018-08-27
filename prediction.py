import datetime
import json
import time
from flask import Flask, request
import os
import uuid

def predict(filename):

    data = {
        'disease':{
            'name'  : 'Apple random name',
            'description' : 'Disease description goes here'
            },
        'remedy':{
            'medicine': 'medicine name',
            'dose': 'dosage',
            'remarks': 'remarks about remedy'
            }
    }
    
    return data
