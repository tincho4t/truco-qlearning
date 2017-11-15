from Model import Model
import numpy as np
from copy import deepcopy
import tensorflow as tf

# Implementation of a neural network addapted for Q Learning
class QLearningTensorflow(Model):
    
    def __init__(self, n_input, n_hidden_1, outputLayer, existingAlgoPath=None):
        super(QLearningTensorflow, self).__init__()
        self.lr_drop_rate = 0.992
        self.current_lr = 0.01
        self.n_hidden_1 = n_hidden_1
        self.outputLayer = outputLayer
        self.n_input = n_input
        self.X = tf.placeholder("float", [None, n_input])
        self.Y = tf.placeholder("float", [None, outputLayer])
        self.prob = tf.placeholder_with_default(1, shape=())

        self.Q = self.Q_model()
        self.QTarget = self.Q + 0
        self.cost = tf.nn.l2_loss(self.Q-self.Y)
        self.optimizer = tf.train.GradientDescentOptimizer(self.current_lr).minimize(self.cost)
        # gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.2)
        config = tf.ConfigProto(
            device_count = {'GPU': 0}
        )
        self.tfsession = tf.Session(config=config)
        # self.tfsession = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
        self.init = tf.global_variables_initializer()
        self.tfsession.run(self.init)
        self.initial_fit()
        self.saver = tf.train.Saver()

        if existingAlgoPath is not None:
            self.saver.restore(self.tfsession, existingAlgoPath)

    def Q_model(self):
        self.dense = tf.layers.dense(inputs=self.X, units=self.n_hidden_1, activation=tf.nn.relu)
        self.dropout = tf.layers.dropout(inputs=self.dense, rate=self.prob)
        # self.dense_1 = tf.layers.dense(inputs=self.dropout, units=self.n_hidden_1, activation=tf.nn.relu)
        # self.dropout_1 = tf.layers.dropout(inputs=self.dense_1, rate=self.prob)
        # self.dense_2 = tf.layers.dense(inputs=self.dropout_1, units=self.n_hidden_1, activation=tf.nn.relu)
        self.out_layer = tf.layers.dense(inputs=self.dropout, units=self.outputLayer, activation=tf.nn.tanh)
        return self.out_layer

    def QTarget(self):
        self.Target_dense = tf.layers.dense(inputs=self.X, units=self.n_hidden_1, activation=tf.nn.relu)
        self.Target_dropout = tf.layers.dropout(inputs=self.Target_dense, rate=self.prob)
        # self.Target_dense_1 = tf.layers.dense(inputs=self.Target_dropout, units=self.n_hidden_1, activation=tf.nn.relu)
        # self.Target_dropout_1 = tf.layers.dropout(inputs=self.Target_dense_1, rate=self.prob)
        # self.Target_dense_2 = tf.layers.dense(inputs=self.Target_dropout_1, units=self.n_hidden_1, activation=tf.nn.relu)
        self.Target_out_layer = tf.layers.dense(inputs=self.Target_dropout, units=self.outputLayer, activation=tf.nn.tanh)
        return self.Target_out_layer
    
    def predict(self, X, target=False):
        if target:
            return self.tfsession.run(self.QTarget, feed_dict = {self.X:X})
        else:
            return self.tfsession.run(self.Q, feed_dict = {self.X:X})

    def updateLR(self):
        if self.current_lr > 0.00001:
            self.current_lr*=self.lr_drop_rate
    
    def updateTarget(self):
        self.optimizer = tf.train.GradientDescentOptimizer(self.current_lr).minimize(self.cost)
        self.QTarget = self.Q + 0
        print("TARGET UPDATED")
        print("Current LR is",self.current_lr)
    
    def learn(self, X_in, ACTION_in, Y_in):
        Y_LEARN = self.getYOnlyForActionTaken(X_in, ACTION_in, Y_in)
        self.tfsession.run(self.optimizer, feed_dict={self.X: X_in, self.Y: Y_LEARN, self.prob: 0.8})
    
    def getYOnlyForActionTaken(self, X, ACTION, Y):
        allActionPredictions = self.tfsession.run(self.Q, feed_dict={self.X: X, self.prob: 1})
        for i in range(X.shape[0]):
            allActionPredictions[i, int(ACTION[i])] = Y[i] # Only change the prediction for the action that was taken to the expected Y value
        return allActionPredictions

    def initial_fit(self):
        n = 32
        X = np.ones((n,self.n_input))
        y = np.zeros((n,self.outputLayer))
        for i in range(150):
            self.tfsession.run(self.optimizer, feed_dict={self.X: X, self.Y: y})
            allActionPredictions = self.tfsession.run(self.Q, feed_dict={self.X: X})

    def save(self, path):
        save_path = self.saver.save(self.tfsession, path)