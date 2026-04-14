import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from PIL import Image
import os
import pickle

# Dataset path - Update this path after downloading PlantVillage dataset
DATASET_PATH = 'dataset/plantvillage_dataset/color/'
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
NUM_CLASSES = 38  # Adjust based on your dataset classes

class_names = sorted(os.listdir(DATASET_PATH))
print(f"Classes: {class_names}")
print(f"Number of classes: {len(class_names)}")

# Data generators
def load_data():
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_PATH,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE
    )
    
    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_PATH,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE
    )
    
    # Normalize
    normalization_layer = layers.Rescaling(1./255)
    train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))
    
    # Cache and prefetch
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=tf.data.AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=tf.data.AUTOTUNE)
    
    return train_ds, val_ds, class_names

# Build CNN Model
def create_model(num_classes):
    model = keras.Sequential([
        layers.Conv2D(32, 3, padding='same', activation='relu', input_shape=(224, 224, 3)),
        layers.MaxPooling2D(),
        
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        
        layers.Conv2D(128, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        
        layers.Conv2D(256, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.5),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

if __name__ == "__main__":
    train_ds, val_ds, class_names = load_data()
    
    model = create_model(len(class_names))
    model.summary()
    
    # Callbacks
    callbacks = [
        keras.callbacks.ModelCheckpoint('model/best_crop_disease_model.h5', save_best_only=True),
        keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(patience=5)
    ]
    
    # Train
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=50,
        callbacks=callbacks
    )
    
    # Save class names
    with open('model/class_names.pkl', 'wb') as f:
        pickle.dump(class_names, f)
    
    model.save('model/crop_disease_model.h5')
    print("Model saved as model/crop_disease_model.h5")

