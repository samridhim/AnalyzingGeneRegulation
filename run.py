
#to be run as python run.py *filename*
#it runs all the files one at a time. Eg: it will first take IFF as class1 and run that with premade class0, in the next iteration it will #run UBP as class1 along with the premade class0 file

import Main_Latest as main
import sys
import pandas as pd
import json
import pickle

#filenames1 = ['ENCFF127XXD_H3K4me3.bed','ENCFF099LMD_H3K4me2.bed', 'ENCFF139CKE_H4K20me1.bed', 'ENCFF183UQD_H3K4me1.bed','ENCFF322IFF_H3K27me3.bed','ENCFF498CMP_H3K36me3.bed', 'ENCFF578UBP_H3K27ac.bed', 'ENCFF624XRN_H2AFZ.bed', 'ENCFF737AMS_H3K4me3.bed', 'ENCFF894VEM_H3K9me3.bed']

df_final = pd.DataFrame(columns=['File1','File2','Accuracy', 'Scores_Array'])
count = 0
#for f in filenames1:
#	accuracy, scores = main.classify(f)
#	df_final.loc[count,['File1']] = f
#   	df_final.loc[count, ['File2']] = 'class0.bed'
#    	df_final.loc[count, ['Accuracy']] = accuracy
#    	df_final.loc[count, ['Scores_Array']] = str(scores)
#	count+=1

#	df_final.loc[count,['File1']] = f
#   	df_final.loc[count, ['File2']] = 'class0.bed'
#    	df_final.loc[count, ['Accuracy']] = accuracy
#    	df_final.loc[count, ['Scores_Array']] = str(scores)
accuracy,scores = main.classify(sys.argv[1])
df_final.loc[count,['File1']] = sys.argv[1]
df_final.loc[count, ['File2']] = 'class0.bed'
df_final.loc[count, ['Accuracy']] = accuracy
print type(scores)
df_final.loc[count, ['Scores_Array']] = str(scores)
df_final.to_csv(str(sys.argv[1])+".csv")
with open(str(sys.argv[1])+".pkl", 'wb') as f:
    pickle.dump(scores.tolist(), f)



