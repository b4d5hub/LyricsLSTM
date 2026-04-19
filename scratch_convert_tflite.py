import tensorflow as tf

print("Loading Keras model...")
model = tf.keras.models.load_model('taylor_swift_lstm.keras')

print("Converting to TFLite...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# For LSTM models we might need to enable Select TF ops and lower precision to save space
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS,
    tf.lite.OpsSet.SELECT_TF_OPS
]

tflite_model = converter.convert()

with open('taylor_swift_lstm.tflite', 'wb') as f:
    f.write(tflite_model)
    
print("Conversion complete.")
