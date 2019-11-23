from information import NoteData,ImageData,Information,Data
import os
import pickle

if os.path.exists('database/informations.p'):
    informations = pickle.load(open("database/informations.p", "rb"))

else:
    informations = []