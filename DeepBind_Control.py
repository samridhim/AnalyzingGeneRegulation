#imports
import numpy as np
import pandas as pd
import keras
import warnings
import import_ipynb
import Pipeline_Control as pp2
import json
    
warnings.filterwarnings("ignore")




'''function to one hot encode the DNA sequence'''

def one_hot_encode(s):
    i=0
    
    dict_i = {"A" : 0, "C": 1, "G": 2, "T" : 3,"a":0, "c":1, "g":2, "t":3}
    ohe = np.zeros((len(s), 4))
    
    for k in s:
        
        if k=='N' or k=='n':
            ohe[i,0] = 0.25
            ohe[i,1] = 0.25
            ohe[i,2] = 0.25
            ohe[i,3] = 0.25
            
        else:
            ohe[i,dict_i[k]] = 1
        i+=1
    return ohe




'''the main deepbind function which is making the CNN model, and training and testing it on the dataframes passed'''

def deepbind1(df_train, df_test,f):
    
    
    print("Shape is: ",df_train.shape)
    print ("Shape test :", df_test.shape)
    

	#extracting the training data
    temp_sequences=df_train['seq']
    temp_target=df_train['target']
    
    
	#one hot encoding the training dna sequences
    ohe_sequences = np.array([one_hot_encode(s) for s in temp_sequences])
    print ohe_sequences
    print "shape of train is: " , ohe_sequences.shape
    

	#keras imports for the CNN
    from keras.models import Sequential
    from keras.layers import Dense
    from keras.layers import Conv1D
    from keras.layers import MaxPooling1D
    from keras.layers import Dropout,Flatten
    from sklearn.utils import shuffle
    from sklearn.model_selection import train_test_split


    model = Sequential()

	#adding 1D convolution layer with ReLU activation
    model.add(Conv1D(filters=10, kernel_size=20, activation='relu', input_shape=(410,4)))
    model.summary()


	#adding max pooling layer
    model.add(MaxPooling1D(pool_size=10, strides=10))
    model.add(Flatten())
    

	#adding 2 fully connected layers
    model.add(Dense(200,  activation='relu'))
    
    model.add(Dense(1, activation = "sigmoid"))
    
    model.summary()
    

	#compiling the models/ making the model/ training the model on the training data
    model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])
    
    data_train, data_test, labels_train, labels_test = train_test_split(ohe_sequences, temp_target, test_size=0, random_state=42, shuffle=True)
    
    model.fit(data_train, labels_train, epochs=5, verbose=1)
    
    
    #extracting the testing data
    temp_sequences_test=df_test['seq']
    temp_target_test=df_test['target']
    

	#one hot encoding the testing dna sequences
    ohe_sequences_test = np.array([one_hot_encode(s) for s in temp_sequences_test])
    print ohe_sequences_test
    print "shape of test is : " , ohe_sequences_test.shape
    
   
    #evaluating the model on the testing data
    scores = model.evaluate(ohe_sequences_test, temp_target_test)
    print ("Test loss ", scores[0])
    print ("Test acc ", scores[1])


	'''getting a scores array where every entry in this array is the probability predicted for each test sequence. hence, size of scores array is same as size of testing dataset''' 
    scores_array= model.predict(ohe_sequences_test, batch_size=None, verbose=1, steps=None)
    print scores_array
    

	#saving the model in the form of a json, and the model/CNN weights in a weights.h5 file
    model.save_weights("modelweights/model_"+str(f)+"_weights.h5")
    my_json_string = model.to_json()
    jsonData = json.loads(my_json_string)
    print jsonData["config"]
    with open("models/model_"+str(count)+".json", "w") as json_file:
        json_file.write(my_json_string)


	#instead of using the inbuilt keras prediction/evaulation accuracy, we are calculating the roc_auc accuracy
    from sklearn.metrics import roc_curve
    keras_model= model
    y_pred_keras = keras_model.predict(ohe_sequences_test).ravel()
    fpr_keras, tpr_keras, thresholds_keras = roc_curve(temp_target_test, y_pred_keras)
    
    print "FPR, TPR", fpr_keras, tpr_keras
    from sklearn.metrics import auc
    auc_keras = auc(fpr_keras, tpr_keras)
    
    print "auc accuracy", auc_keras


    return auc_keras,scores_array

