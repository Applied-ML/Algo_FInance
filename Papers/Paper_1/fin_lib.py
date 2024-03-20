import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
import xgboost as xgb


def target_creation(df,beta):
    df["Tomorrow"] = df["Close"].shift(-1)
    df["Target"] = (df["Tomorrow"] > df["Close"]*(1+beta)).astype(int)
    df = df.iloc[:-1]
    df = df.drop(columns=['Tomorrow'])
    df = df.dropna()
    return df

def create_sequences(data, seq_length):
    sequences = []
    for i in range(len(data) - seq_length + 1):
        sequence = data[i:i + seq_length]
        sequences.append(sequence)
    return np.array(sequences)

def preprocessing(df,past_days):
    X = df.drop(columns=['Target']).values  
    y = df['Target'].values

    X_sequences = create_sequences(X, past_days)
    X_flattened = X_sequences.reshape(-1, past_days * X.shape[1])

    y_resized = y[past_days - 1:]
    X_train, X_test, y_train, y_test = train_test_split(X_flattened, y_resized, test_size=0.2, random_state=42,shuffle=False)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled,X_test_scaled,y_train,y_test


class Models:

    def MLP(X_train_scaled,X_test_scaled,y_train,y_test):
        model = MLPClassifier(hidden_layer_sizes=(16,8,4,2), activation='relu', random_state=42,shuffle=False,learning_rate='constant',learning_rate_init=10e-3,max_iter=1000,validation_fraction=0.5)

        model.fit(X_train_scaled, y_train)

        pred = model.predict(X_test_scaled)

        precision = precision_score(y_test,pred)
        return pred,precision
    
    def XGBOOST(X_train_scaled,X_test_scaled,y_train,y_test,parameters):
        model = xgb.XGBClassifier(**parameters,objective='binary:logistic')
        model.fit(X_train_scaled,y_train)
        pred = model.predict(X_test_scaled)
        precision = precision_score(y_test,pred)
        return pred,precision






