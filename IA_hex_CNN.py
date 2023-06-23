import numpy as np

class NN_CNN :

    def __init__(self, taille) :

        self.taille = taille

        self.enter_NN = self.taille
        self.hidden_NN = 20
        self.pooling_NN = 5
        self.hidden2_NN = 10
        self.out_NN = self.taille

        self.tmp = 0

        self.W = {'W1': np.random.randn(self.enter_NN,self.hidden_NN), 
                  'W2': np.random.randn(self.hidden_NN,self.pooling_NN),
                  'W3': np.random.randn(self.pooling_NN,self.hidden2_NN),
                  'W4': np.random.randn(self.hidden2_NN,self.out_NN)} 
    
    def forward(self,X) :
        X = np.array(X)
        self.A = {}

    def softmax(self, Z):
        e_x = np.exp(Z - np.max(Z, axis=0))
        return e_x / np.sum(e_x, axis=0)

    def softmax_derivative(self, Z):
        softmax_output = self.softmax(Z)
        return softmax_output * (1 - softmax_output)
    
    def back_prop(self, X) :
        ...
    
    def update(self) :
        ...
    
    def predict(X) :
        ...