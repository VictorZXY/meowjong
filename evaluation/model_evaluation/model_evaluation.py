import argparse
import os

import joblib
import tensorflow as tf
from tensorflow import keras

assert tf.__version__ >= "2.0"

# To make the output stable across runs
tf.random.set_seed(42)


def load_data(dataset_path, filename):
    with open(os.path.join(dataset_path, filename), 'rb') as fread:
        X_test = joblib.load(fread)
        y_test = joblib.load(fread)

        return X_test, y_test


if __name__ == '__main__':
    # Parse the args
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path', action='store', type=str,
                        required=True)
    parser.add_argument('--model_path', action='store', type=str, required=True)

    args = parser.parse_args()
    dataset_path = args.dataset_path
    models_path = args.model_path

    # Test whether there are GPUs available
    assert len(tf.config.experimental.list_physical_devices('GPU')) > 0

    kernel_size = {
        'discard': '45',
        'pon': '54',
        'kan': '23',
        'kita': '32',
        'riichi': '34'
    }

    for action in 'discard', 'pon', 'kan', 'kita', 'riichi':
        for scaled in '', '_scaled':
            print('=================================================================')
            print(' ' + action + scaled + ' model evaluation')
            print('=================================================================')

            dataset_name = action + '_tensors_2020' + scaled + '.joblib'

            # Load dataset
            X_test, y_test = load_data(dataset_path, dataset_name)
            print(action + scaled, 'X_test shape:', X_test.shape)
            print('y_test.shape:', y_test.shape)
            print()

            # load model
            keras.backend.clear_session()

            model_name = action + '_cnn_' + kernel_size[action] + scaled + '.h5'
            model = keras.models.load_model(os.path.join(dataset_path,
                                                         model_name))

            # evaluation on test set
            eval_test = model.evaluate(X_test, y_test)
            print(action + scaled, 'test loss:', eval_test[0])
            print(action + scaled, 'test accuracy:', eval_test[1])
