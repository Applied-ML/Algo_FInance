import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def target_creation(df,beta):
    if beta == 'default':
    
        df["Tomorrow"] = df["Close"].shift(-1)
        df["Target"] = (df["Tomorrow"] > df["Close"]).astype(int)
        df = df.iloc[:-1]
        df = df.drop(columns=['Tomorrow'])
        return df
    else:
        df["Tomorrow"] = df["Close"].shift(-1)
        df["Target"] = (df["Tomorrow"] > df["Close"]*(1+beta)).astype(int)
        df = df.iloc[:-1]
        df = df.drop(columns=['Tomorrow'])
        return df


def create_sequences(data, seq_length):
    sequences = []
    for i in range(len(data) - seq_length + 1):
        sequence = data[i:i + seq_length]
        sequences.append(sequence)
    return np.array(sequences)


class Models():
    def __init__(self,alpha,model_name):
        self.alpha = alpha
        self.model = model_name


    def preprocessing(self,df,past_days):
        X = df.drop(columns=['Target']).values  
        y = df['Target'].values

        X_sequences = create_sequences(X, past_days)
        X_flattened = X_sequences.reshape(-1, past_days * X.shape[1])

        y_resized = y[past_days - 1:]
        X_train, X_test, y_train, y_test = train_test_split(X_flattened, y_resized, test_size=0.333, random_state=42,shuffle=False)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled,X_test_scaled,y_train,y_test

    def Model(self,df):
        
        past_days = self.alpha


        X_train_scaled,X_test_scaled,y_train,y_test = self.preprocessing(df,past_days)

        
        if self.model == 'mlp':
            model = MLPClassifier(hidden_layer_sizes=(16,8,4,2), activation='relu', random_state=42,shuffle=False,learning_rate='constant',learning_rate_init=10e-3,max_iter=1000,validation_fraction=0.5)

            model.fit(X_train_scaled, y_train)

            y_pred_train = model.predict(X_train_scaled)
            y_pred_test = model.predict(X_test_scaled)
            train_accuracy = accuracy_score(y_train, y_pred_train)
            test_accuracy = accuracy_score(y_test, y_pred_test)

            return train_accuracy,test_accuracy,len(X_train_scaled),y_pred_test


