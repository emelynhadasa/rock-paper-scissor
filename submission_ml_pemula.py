# -*- coding: utf-8 -*-
"""submission_ml_pemula

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MKhmqa_iquyFT6nI40mvjlvas7YD4HJd

#Biodata
Nama: Emelyn Hadasa

Email: emelyndhadasa@gmail.com

Phone: 087879530678
"""

import tensorflow as tf

!wget --no-check-certificate \
  https://github.com/dicodingacademy/assets/releases/download/release/rockpaperscissors.zip \
  -O /tmp/final.zip

# Ekstraksi file zip
import zipfile,os
local_zip = '/tmp/final.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/tmp')
zip_ref.close()

base_dir = '/tmp/rockpaperscissors'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'val')

os.listdir('/tmp/rockpaperscissors/train')

os.listdir('/tmp/rockpaperscissors/val')

from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_data = ImageDataGenerator( rescale = 1.0/255,
                                          rotation_range=20,
                                          width_shift_range=0.2,
                                          height_shift_range=0.2,
                                          shear_range=0.2,
                                          zoom_range=0.2,
                                          horizontal_flip=True,
                                          fill_mode='nearest',
                                          validation_split=0.4
                                  )

validation_data = ImageDataGenerator(rescale = 1.0/255,
                                        validation_split=0.4)

train_generator = train_data.flow_from_directory(train_dir,
                                                  batch_size=32,
                                                  class_mode='categorical',
                                                  target_size=(60, 40),
                                                  subset='training')

validation_generator = validation_data.flow_from_directory(train_dir,
                                                          batch_size=32,
                                                          class_mode='categorical',
                                                          target_size=(60, 40),
                                                          subset='validation')

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(64, (5,5), activation=tf.nn.relu,input_shape=(60, 40, 3)),
    tf.keras.layers.BatchNormalization(),

    tf.keras.layers.Conv2D(64, (3,3), activation=tf.nn.relu,padding = 'Same'),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Conv2D(128, (3,3), activation=tf.nn.relu,padding = 'Same'),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Flatten(),

    tf.keras.layers.Dense(256, activation=tf.nn.relu),
    tf.keras.layers.Dense(3, activation = tf.nn.softmax)
])

model.summary()

from keras.callbacks import ReduceLROnPlateau

learning_rate_reduction = ReduceLROnPlateau(monitor='val_acc',
                                            patience=2,
                                            verbose=1,
                                            factor=0.5,
                                            min_lr=0.000003)

model.compile(loss = 'categorical_crossentropy', optimizer= tf.keras.optimizers.Adam(), metrics=['acc'])

history = model.fit(train_generator,
                    epochs = 10,
                    verbose = 1,
                    validation_data = validation_generator,
                    callbacks=[learning_rate_reduction])

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from google.colab import files
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline

uploaded = files.upload()

for fn in uploaded.keys():

  path = fn
  img = image.load_img(path, target_size=(60,40))

  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
  images = np.vstack([x])

  classes = model.predict(images, batch_size=10)
  print(fn)

  if classes[0,1] !=0:
    print('batu')
  elif classes[0,0] !=0:
    print('kertas')
  else:
    print('gunting')