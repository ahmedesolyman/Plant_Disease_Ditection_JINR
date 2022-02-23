# Plant_Disease_Ditection_JINR
Plant Disease Detection
This repository contains the code for the RFBR project 18-07-00829

"Development of massive parallel approaches for farmers complaints through text and images using high performance computing"

Plants disease detection is very popular field of study. Many promising results were already obtained but it is still only few real-life applications that can make farmer’s life easier. The aim of our research is solving the problem of detection and preventing diseases of agricultural crops with the help of deep learning. We collected a special database of the grapes leaves consisting of four set of images, including healthy, Esca, Black rot and Chlorosis diseases. We reached over 90% accuracy using a deep siamese convolutional network.

Installation
install all required packages;
clone PDD using git:
git clone https://github.com/AlexanderUzhinskiy/pdd_new.git
then, cd to the pdd_new folder and feel free to use it:
cd pdd_new
Getting started
At first, to start training your own model using the PDD dataset, you should download the data. To do that we prepared a special module datasets. We load the dataset with grape's leaves and set the random state for splitting data into train and test subsets. random_state parameter is used for reproducibility.

from pdd.datasets.grape import load_data

train_data_path, test_data_path = load_data(split_on_train_test=True, random_state=13)
In our study we utilized a deep convolutional siamese network to train feature extractor and then applied K-Nearest Neighbours on the top of extracted features. Siamese networks take as input pairs of images with corresponding labels: 0 -- for images from different classes and 1 -- for images from the same class.

For training we are using a strong augmentation including rotations, zooming, flips and channel shifts.

from pdd.utils.training import SiameseBatchGenerator

train_batch_gen = SiameseBatchGenerator.from_directory(dirname=train_data_path, augment=True)
test_batch_gen = SiameseBatchGenerator.from_directory(dirname=test_data_path)

def siams_generator(batch_gen, batch_size=None):
    while True:
        batch_xs, batch_ys = batch_gen.next_batch(batch_size)
        yield [batch_xs[0], batch_xs[1]], batch_ys
As an feature extractor any Keras model with appropriate input layer can be used. But we created a simple one:

from pdd.models import get_feature_extractor

import keras.backend as K
import tensorflow as tf

# set the single session for tensorflow and keras both
sess = tf.Session()
K.set_session(sess)

input_shape = (256, 256, 3)

feature_extractor = get_feature_extractor(input_shape)
To make it possible to train the feature extractor in siamese manner we developed a special helper:

from pdd.models import make_siamese

siams = make_siamese(feature_extractor, dist='l1', loss='cross_entropy')
There are three types of distances:

l1
l2
cosine
But only 'l1' is available for cross-entropy loss.

After that one can train the siams model using keras fit_generator method.

When the feature extractor is trained, it's time to create a TensorFlow graph for KNN algorithm

from pdd.models import TfKNN

tfknn = TfKNN(sess, 
              feature_extractor, 
              (train_images, train_labels))
For prediction TfKNN has special method:

preds = tfknn.predict(test_images, return_dist=True)
And finally, to save the graph for serving:

tfknn.save_graph_for_serving("tfknn_graph")
