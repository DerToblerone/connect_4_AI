import tensorflow as tf
from tensorflow import keras

import sys

sys.path.append('.')
import test_network
from util import time2str


try:
    model_1 = keras.models.load_model('./model_generated_data')
    model_2 = keras.models.load_model('./parameters')
    print("load complete")
except:
    exit()

date_str =  time2str()
print(date_str)
input("enter to start testing")

test_network.main(model_2,50,'{0}_t_TD.txt'.format(date_str))

date_str =  time2str()

test_network.main(model_1,50, '{0}_t_gen_data.txt'.format(date_str))
input("testing done")
