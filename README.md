## Project Description
The influence of genomic sequence on patterns of histone modification associated with gene expression and chromatin programming is called sequence bias, and it suggests that the mechanisms responsible for global histone modifications may interpret genomic sequence in various ways. 

In this research project we undertake the task of finding such sequence biases using Deep Learning. Specifically, we train a Convolutional Neural Network to detect patterns in DNA Sequences which are underlying certain histone marks. 

For more information, link to our final presentation: https://bit.ly/2Y2a4L4

## Requirements
Project is done in Python 3 environment.

Open Source Libraries used - 
1. Keras - https://github.com/keras-team/keras
2. Numpy - https://github.com/numpy/numpy
3. Pandas - https://github.com/pandas-dev/pandas
5. ucsc-twobittofa - https://anaconda.org/bioconda/ucsc-twobittofa
6. bedtools - https://github.com/arq5x/bedtools2
7. DeepLift - https://github.com/kundajelab/deeplift


## Description of Important Files 

1. `Main_Latest.py` - The main processing file which takes the FASTA / CSV files for training and passesd them through the pipeline for training.

2. `Pipeline_Control.py` - The pipeline control file which is responsible for removing intersections of overlapping DNA sequences within two files and also refactoring them according to the file type required by the tools - twoBitToFa and bedtools. 

3. `DeepBind_Control.py` - This file is the heart of the project. This is where the training & testing logic is embedded. We have used Keras to train the model. 

4. `DeepLift_Latest.py` - DeepLift is a tool which allows computation and visualisation of important scores of bases within DNA sequences that are trained with the help of deep neural networks. 

5. `Creating_Class0.py` - Helper class which enables us to create the control sequences, i.e. the sequences which become the negative set throughout the training process. 


##  Steps to run on Local Machine
1. Extract the different `ENCFF*.bed.gz` files

2. Make sure the paths are configured to your local device

3. Run the run.sh file using `sh run.sh`. Wait for the training to finish. 

4. Model info (accuracy, probability scores) will be available in `ENCFF*.bed.csv` files

5. To view on DeepLift change the model and the h5 file names accordingly
