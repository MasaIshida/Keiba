from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import os
import pickle
import numpy as np
import zipfile

from Koh.machine.learning_machine import Kho


def main():
    learning_data = np.zeros([1, 80, 18, 28])
    label_data = np.zeros([1, 1])
    #  ダミー
    pre_data = []
    thaw_zip_data()
    learning_data, label_data = read_data(learning_data, label_data)
    x_train, x_test, y_train, y_test = train_test_split(
        learning_data,
        label_data,
        train_size=0.99,
        random_state=1)
    y_train = to_categorical(y_train, 19)
    y_test = to_categorical(y_test, 19)
    kho = Kho(x_train, x_test, y_train, y_test)
    kho.learning_model()
    kho.start_fit(learning_data, label_data)
    kho.start_pre(pre_data)


def thaw_zip_data():

    with zipfile.ZipFile("../../LeaningJsonData/learning_data.zip") as existing_zip:
        existing_zip.extractall()

    with zipfile.ZipFile("../../LeaningJsonData/label.zip") as existing_zip:
        existing_zip.extractall()


def read_data(learning_data, label_data):

    with open("../../LeaningJsonData/learning_data.binaryfile", "rb") as byn:
        leaning_arr = pickle.load(byn)
        learning_data = np.r_['0, 4', learning_data, leaning_arr]

    with open("../../LeaningJsonData/label.binaryfile", "rb") as byn:
        leaning_arr = pickle.load(byn)
        label_data = np.r_['0, 4', label_data, leaning_arr]

    return learning_data, label_data


if __name__ == "__main__":
    main()
