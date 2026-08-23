import tensorflow as tf
import os

# Disable tensorflow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Disable eager execution (needed for TF1.x graph compatibility)
tf.compat.v1.disable_eager_execution()

# Paths
image_path = r"C:\Users\alain\OneDrive\Pictures\test dataset\non pd\_MPR_Thick_Range[1]__002.png"


label_path = r"C:\Users\isasu\Music\project\web\D_daignosis\myapp\new_logs\output_labels.txt"
graph_path = r"C:\Users\isasu\Music\project\web\D_daignosis\myapp\new_logs\output_graph.pb"

def check(image_path):
    # Read image bytes
    image_data = tf.io.gfile.GFile(image_path, 'rb').read()

    # Load labels
    label_lines = [line.strip() for line in tf.io.gfile.GFile(label_path)]

    # Load frozen graph (.pb)
    with tf.io.gfile.GFile(graph_path, 'rb') as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    # Run session
    with tf.compat.v1.Session() as sess:
        # Tensor names must match your graph
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

        # Sort predictions by confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            print('%s (score = %.5f)' % (human_string, score))

        # Best prediction
        nid = top_k[0]
        print("\nBest Prediction →", label_lines[nid], "with score =", predictions[0][nid])
        return label_lines[nid], predictions[0][nid]

# # Run check
# check(image_path)