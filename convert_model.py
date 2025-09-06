import tensorflow as tf

# Load your existing .h5 model
model = tf.keras.models.load_model("glaucoma_detection_model.h5", compile=False)

# Save it in the new .keras format
model.save("glaucoma_detection_model.keras")
