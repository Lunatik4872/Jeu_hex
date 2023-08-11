import tensorflow as tf
import numpy as np
import os

class NN_CNN :

    def __init__(self, taille) :
        self.taille = taille

        self.enter_NN = self.taille
        self.hidden_NN = 20
        self.pooling_NN = tf.keras.layers.MaxPooling1D()
        self.hidden2_NN = 10
        self.out_NN = self.taille**2

        self.W = {}
        self.tmp = 0
        self.load()

        self.optimizer = tf.keras.optimizers.Adam()
    
    def forward(self, X):
        X = tf.convert_to_tensor(X, dtype=tf.float32)
        self.a = {}

        self.a['Z1'] = tf.matmul(X, self.W['W1'])
        self.a['A1'] = tf.nn.relu(self.a['Z1'])
        self.a['A1'] = tf.expand_dims(self.a['A1'], axis=0)

        self.a['pooling'] = self.pooling_NN(self.a['A1'])
        self.a['A1'] = tf.squeeze(self.a['pooling'], axis=0)

        self.a['Z2'] = tf.matmul(self.a['A1'], self.W['W2'])
        self.a['A2'] = tf.nn.relu(self.a['Z2'])

        self.a['Z3'] = tf.matmul(self.a['A2'], self.W['W3'])
        self.output = tf.nn.relu(self.a['Z3'])


        return self.output
    
    def backward(self, X, reward) :
        X = tf.convert_to_tensor(X, dtype=tf.float32)
        reward = tf.convert_to_tensor(reward, dtype=tf.float32)

        with tf.GradientTape() as tape:
            predictions = self.forward(X)
            self.tmp += reward
            loss = tf.reduce_mean(tf.square(reward - predictions))

        grads = tape.gradient(loss, self.W.values())
        self.optimizer.apply_gradients(zip(grads, self.W.values()))
    
    def save(self):
        poids_a_sauvegarder = {
            'W1': self.W['W1'].numpy(),
            'W2': self.W['W2'].numpy(),
            'W3': self.W['W3'].numpy()
        }
        np.save("IA_W.npy", poids_a_sauvegarder)
        np.save('tmp.npy', self.tmp)
    
    def load(self) :
        if os.path.exists("AI_W.npy") and os.path.exists("tmp.npy"):
            poids_charges = np.load("AI_W.npy", allow_pickle=True).item()
            self.W['W1'].assign(poids_charges['W1'])
            self.W['W2'].assign(poids_charges['W2'])
            self.W['W3'].assign(poids_charges['W3'])
            tmp = np.load("tmp.npy")
            self.tmp = tmp
        else :
            self.tmp = 0

            self.W = {'W1': tf.Variable(tf.random.normal((self.enter_NN, self.hidden_NN))),
                    'W2': tf.Variable(tf.random.normal((self.hidden_NN, self.hidden2_NN))),
                    'W3': tf.Variable(tf.random.normal((self.hidden2_NN, self.out_NN)))}
            
        
