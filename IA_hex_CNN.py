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
    
    def forward(self,X) :
        