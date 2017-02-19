import numpy as np
import random
import tensorflow as tf
import tensorflow.contrib.layers as layers

map_fn = tf.python.functional_ops.map_fn


################################################################################
##                           GRAPH DEFINITION                                 ##
################################################################################

INPUT_SIZE = 2       # 2 bits per timestep
OUTPUT_SIZE = 1       # 1 bit per timestep
RNN_HIDDEN = 20
BATCH_SIZE = 16
TINY = 1e-6    # to avoid NaNs in logs
LEARNING_RATE = 0.01
DTYPE = tf.float32

inputs  = tf.placeholder(DTYPE, (None, None, INPUT_SIZE))  # (time, batch, in)
outputs = tf.placeholder(DTYPE, (None, None, OUTPUT_SIZE)) # (time, batch, out)

cell = tf.nn.rnn_cell.BasicGRUCell(RNN_HIDDEN)

initial_state = cell.zero_state(BATCH_SIZE, DTYPE)

# Given inputs (time, batch, input_size) outputs a tuple
#  - outputs: (time, batch, output_size)  [do not mistake with OUTPUT_SIZE]
#  - states:  (time, batch, hidden_size)
rnn_outputs, rnn_states = tf.contrib.static_rnn(cell, inputs, initial_state=initial_state)

# project output from rnn output size to OUTPUT_SIZE. Sometimes it is worth adding
# an extra layer here.
final_projection = lambda x: layers.linear(x, num_outputs=OUTPUT_SIZE, activation_fn=tf.nn.sigmoid)

# apply projection to every timestep.
predicted_outputs = map_fn(final_projection, rnn_outputs)

# compute elementwise cross entropy.
error = -(outputs * tf.log(predicted_outputs + TINY) + (1.0 - outputs) * tf.log(1.0 - predicted_outputs + TINY))
error = tf.reduce_mean(error)

# optimize
train_fn = tf.train.AdamOptimizer(learning_rate=LEARNING_RATE).minimize(error)

# assuming that absolute difference between output and correct answer is 0.5
# or less we can round it to the correct output.
accuracy = tf.reduce_mean(tf.cast(tf.abs(outputs - predicted_outputs) < 0.5, DTYPE))


################################################################################
##                           TRAINING LOOP                                    ##
################################################################################

NUM_BITS = 10
ITERATIONS_PER_EPOCH = 100

session = tf.Session()
# For some reason it is our job to do this:
session.run(tf.initialize_all_variables())

for epoch in range(1000):
    epoch_error = 0
    for _ in range(ITERATIONS_PER_EPOCH):
        # here train_fn is what triggers backprop. error and accuracy on their
        # own do not trigger the backprop.
        epoch_error += session.run([error, train_fn], {
            inputs: x,
            outputs: y,
        })[0]
    epoch_error /= ITERATIONS_PER_EPOCH
    valid_accuracy = session.run(accuracy, {
        inputs:  valid_x,
        outputs: valid_y,
    })
    print("Epoch %d, train error: %.2f, valid accuracy: %.1f %%" % (epoch, epoch_error, valid_accuracy * 100.0))
