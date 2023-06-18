import numpy as np

class Neuron:
    def __init__(self, taille):
        """C'est du classique ici on va initialiser chaque valeur de l'objet Neuron.
        tout d'abord tu y retrouve l'architecture du reseau avec les diférentes couches
        l'entree les cache et la sortis. Tu peus changer le nombre de neurones à ta guise sauf entre et sortie
        eux ils sont bien defini pour une tache la ils savent ce qu'ils doivent recevoire. Note que plus t'as de 
        couche et de neurone plus l'ia est performante mais en contre partie elle va etre plus gourmante 
        en puissance et plus lente (RESTER SUR DU RAISONABLE !!!)
        """
        self.input_neurons = taille
        self.hidden_neurons = 20
        self.hidden_neurons2 = 20
        self.out_neurons = taille

        """Eux c'est pour l'evaluation de l'IA pendant le jeu suivant ce qu'elle fait on lui ajoute ou retire des points
        puis on compare à son meilleur score si on fait pire alors on l'entraine sinon on conserve"""

        self.tmp = 0  
        self.eval = 0
        self.top_reward = 0

        """La c'est la definition des matrices qui vont lui permettre de donner des resultats comme leur num 
        l'indique c'est pour les diferentes zones W1 : (3,20) W2 : (20,20) W3 : (20,3) ils permettent la liaison
        avec modification du resultat comme on le retrouve dans les communcation elec et chimique du cerveau"""

        self.W1 = np.random.rand(self.input_neurons, self.hidden_neurons)
        self.W2 = np.random.rand(self.hidden_neurons, self.hidden_neurons2)
        self.W3 = np.random.rand(self.hidden_neurons2, self.out_neurons)

    def forward(self, X):
        """La forward est le nom qu'on donne a la fonction qui parcoure de maniere naturelle le reseau de gauche 
        a droite. Elle nous donne en sortie une matrice (3,3) de probabilite. Dans le code on conserve uniquement 
        celle avec la plus grande proba (la tu vois sigmoide car je reflechi encore mais c'est la fonction
        softmax qui est implemente la)
        Pour le fonctionnement c'est simple on part des entres qui est le plateau puis on va calculer 
        Z qui represente les calculs de transfert entre chaque couche pour visualiser tire des traits de chaque 
        neurone et met lui un nombre c'est sont poid ce que represente les W et avec ça tu calcul les activations
        soit le nombre qui arrive dans la couche suivante (c'est garce a la fameuse fonction d'activation ici softmax).
        Ces calculs sont realise jusqu'a la sortie du raison (la 2 couches donc j'ai fait a la main mais sinon on generalise)"""
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
        """La backward sont principe est de parcourir le reseau a l'envert on part de la sortie et on va a l'entree
        cela est tres utilse car en faisant cela on marque les erreurs et avec ces erreur on apporte des modifications
        au reseau en modifiant les poids soit les W.
        POur expliquer les calcul c'est pas evident mais en gros la je prend la note compare a la meilleur puis en fonction
        d'elle j'etablis les erreurs avec le out_delta et je remonte le reseau avec les activation inverse donc la derive.
        une fois au bout je me sert de ses calculs pour mettre a jour les poids"""
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
