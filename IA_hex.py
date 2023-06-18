import numpy as np

class Neuron:
    def __init__(self, taille):
        self.input_neurons = taille
        self.hidden_neurons = 20
        self.hidden_neurons2 = 20
        self.out_neurons = taille
        self.tmp = 0  
        self.eval = 0
        self.top_reward = 0

        self.W1 = np.random.rand(self.input_neurons, self.hidden_neurons)
        self.W2 = np.random.rand(self.hidden_neurons, self.hidden_neurons2)
        self.W3 = np.random.rand(self.hidden_neurons2, self.out_neurons)

    def forward(self, X):
        X = np.array(X)
        self.z = np.dot(X, self.W1)
        self.a = self.sigmoide(self.z)
        print(self.a.shape)
        self.z2 = np.dot(self.a,self.W2)
        self.a2 = self.sigmoide(self.z2)
        self.out = self.sigmoide(np.dot(self.a2, self.W3))
        print(self.out)
        return self.out

    def sigmoide(self, Z):
        e_x = np.exp(Z - np.max(Z, axis=0))
        return e_x / np.sum(e_x, axis=0)

    def sigmoide_derivative(self, Z):
        softmax_output = self.sigmoide(Z)
        return softmax_output * (1 - softmax_output)
    
    def backward(self, X, reward):
        X = np.array(X)  # (3,3)
        self.tmp += reward  # (1,)

        if np.any(self.tmp >= self.eval):
            return

        self.top_reward = np.maximum(self.top_reward, reward)  # (1,)
        self.eval = self.top_reward  # (1,)

        self.out_delta = reward * self.sigmoide_derivative(self.out)  # (1,) * (3,3) = (3,3)

        self.a2_error = self.out_delta  # (3,3)
        self.a2_delta = self.a2_error.dot(self.W3.T) * self.sigmoide_derivative(self.a2)  # (3,3) * (3,20) = (3,20)

        self.a_error = self.a2_delta.dot(self.W2.T)  # (3,20) * (20,20) = (3,20)
        self.a_delta = self.a_error * self.sigmoide_derivative(self.a)  # (3,20) * (3,20) = (3,20)

        self.W1 += X.T.dot(self.a_delta)  # (3,3) * (3,20) = (3,20)
        self.W2 += self.a.T.dot(self.a2_delta)  # (20,3) * (3,20) = (20,20)
        self.W3 += self.a2.T.dot(self.out_delta)  # (20,3) * (3,3) = (20,3)

    def save(self):
        np.save('W1.npy', self.W1)
        np.save('W2.npy', self.W2)
        np.save('W3.npy', self.W3)
        np.save('tmp.npy', self.tmp)
        np.save('eval.npy', self.eval)
        np.save('top_reward.npy', self.top_reward)

    def load(self):
        self.W1 = np.load('W1.npy')
        self.W2 = np.load('W2.npy')
        self.W3 = np.load('W3.npy')
        self.tmp = np.load('tmp.npy')
        self.eval = np.load('eval.npy')
        self.top_reward = np.load('top_reward.npy')
