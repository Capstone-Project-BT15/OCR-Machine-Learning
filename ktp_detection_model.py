import urllib.request
import zipfile
import tensorflow as tf
import os
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image
import matplotlib.pyplot as plt

def model():
    #data_url = 'https://github.com/Capstone-Project-BT15/OCR-Machine-Learning/ktp_and_nonktp.zip'
    #urllib.request.urlretrieve(data_url, 'ktp_and_nonktp.zip')
    local_file = 'ktp_and_notktp.zip'
    zip_ref = zipfile.ZipFile(local_file, 'r')
    zip_ref.extractall('data/')
    zip_ref.close()

    BASE_DIR = 'data/ktp_and_notktp'
    train_dir = os.path.join(BASE_DIR, 'train')
    validation_dir = os.path.join(BASE_DIR, 'val')


    train_datagen = ImageDataGenerator(rescale=1.0 / 255.0,
                                       rotation_range=40,
                                       width_shift_range=0.2,
                                       height_shift_range=0.2,
                                       shear_range=0.2,
                                       zoom_range=0.2,
                                       horizontal_flip=True,
                                       fill_mode='nearest')

    # YOUR IMAGE SIZE SHOULD BE 150x150
    # Make sure you used "binary"
    train_generator = train_datagen.flow_from_directory(directory=train_dir,
                                                        batch_size=16,
                                                        class_mode='binary',
                                                        target_size=(150, 150)) # YOUR CODE HERE

    val_datagen = ImageDataGenerator(rescale=1 / 255.0)
    val_generator = val_datagen.flow_from_directory(directory=validation_dir,
                                                    batch_size=16,
                                                    class_mode='binary',
                                                    target_size=(150, 150))

    model = tf.keras.models.Sequential([
        # YOUR CODE HERE, end with a Neuron Dense, activated by 'sigmoid'
        tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(150, 150, 3)),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.summary()
    model.compile(loss='binary_crossentropy', optimizer=RMSprop(learning_rate=0.001), metrics=['acc'])
    history = model.fit(train_generator, validation_data=val_generator, epochs=500)


    return model, history

ktp_detection, history = model()
ktp_detection.save("ktp_detection_model.h5")


plt.plot(history.history['acc'], label='Training Accuracy')
plt.plot(history.history['val_acc'], label='Validation Accuracy')

# Adding labels and title
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Model Accuracy Over Training Epochs')

# Adding a legend
plt.legend()

# Display the plot
plt.show()