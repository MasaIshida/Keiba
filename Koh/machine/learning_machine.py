from tensorflow.keras.layers import Activation, Dense, Dropout, Conv2D, Flatten, MaxPool2D
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.optimizers import Adam


class DeepLearningMachine(object):

    def __init__(self, x_train, x_test, y_train, y_test):
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test

    # Override
    def learning_model(self, **args):
        """
        学習モデル設計
        :param args:
        :return:
        """
        pass

    # Override
    def start_fit(self, **args):
        """
        学習開始
        :param args:
        :return: 学習経過
        """
        pass

    # Override
    def start_pre(self, **args):
        """
        予測開始
        :param args:
        :return: 予測結果
        """
        pass


class Kho(DeepLearningMachine):

    def __init__(self, x_train, x_test, y_train, y_test):
        super(DeepLearningMachine, self).__init__(x_train, x_test, y_train, y_test)
        self.koh = Sequential()

    # Override
    def learning_model(self):
        self.koh.add(Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(80, 18, 28)))
        self.koh.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
        self.koh.add(MaxPool2D(pool_size=(2, 2)))
        self.koh.add(Dropout(0.25))

        self.koh.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
        self.koh.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
        self.koh.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
        self.koh.add(MaxPool2D(pool_size=(2, 2)))
        self.koh.add(Dropout(0.5))

        self.koh.add(Flatten())
        self.koh.add(Dense(512, activation='relu'))
        self.koh.add(Dense(512, activation='relu'))
        self.koh.add(Dense(19, activation='softmax'))
        self.koh.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.0001), metrics=['acc'])

    # Override
    def start_fit(self, learning_data, label_data):
        self.fit_history = self.koh.fit(learning_data, label_data, batch_size=256, epochs=100, validation_split=0.2)
        return self.fit_history

    def start_pre(self, pre_data):

        return self.koh.predit(pre_data)
