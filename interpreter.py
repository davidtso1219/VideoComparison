import tensorflow as tf

interpreter = tf.lite.Interpreter(model_path='detect.tflite')
interpreter.allocate_tensors()
