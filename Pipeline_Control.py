#pipe function is used to remove intersections between 2 files f1 & f2
def pipe(f1,f2):
    
    import sys
    import os
    import subprocess
    
    #f1 and f2 have 1,8,21 removed
    
    print("in pipeline: f1",f1)            #f1= 1 file
    print("in pipeline: f2",f2)            #f2 = 11 files
    

	#initializing filenames and file paths
    filename1, file_extension1 = os.path.splitext(f1)
    filename2, file_extension2 = os.path.splitext(f2)
    filename1=filename1.split("/")
    filename2=filename2.split("/")
    
    print("Filename 1 in pipe:",filename1)
    print("Filename 2 in pipe:",filename2)

    
    intermediate_file1= "inter_bed/"+filename1[1]+"_without_intersection.bed"
    intermediate_file2= "inter_bed/"+filename2[1]+"_without_intersection.bed"

    fasta_file1 = "inter_fa/"+filename1[1]+".fa"      #class1_IFF_test.fa
    fasta_file2 = "inter_fa/"+filename2[1]+".fa"      #class0_overall_test.fa



    #converting bed file of 10 columns to 4 column file, with 100 upstream/downstream
    command=''' echo "$(awk '{print $1, $2+$10-100, $2+$10+100, $4}' ''' + f1 + ''' )" > ''' + f1
    subprocess.call(command, shell=True)
    command=''' echo "$(awk '{print $1, $2+$10-100, $2+$10+100, $4}' ''' + f2 + ''' )" > ''' + f2
    subprocess.call(command, shell=True)


    #dropping peak info column and storing only 1st 3 columns
    command=''' echo "$(awk '{print $1, $2, $3}' ''' + f1 + ''' )" > ''' + f1
    subprocess.call(command, shell=True)
    command=''' echo "$(awk '{print $1, $2, $3}' ''' + f2 + ''' )" > ''' + f2
    subprocess.call(command, shell=True)


    #replacing spaces with tabs
    command=''' echo "$(tr ' ' \\\\t < '''+ f1 + ''' )" > ''' + f1
    subprocess.call(command, shell=True)
    command=''' echo "$(tr ' ' \\\\t < '''+ f2 + ''' )" > ''' + f2
    subprocess.call(command, shell=True)


    #finding intersections and storing a file w/o intersections in intermediate file
    command= ''' bedtools intersect -v -a ''' + f1 + ''' -b ''' + f2 + ''' > ''' + intermediate_file1
    subprocess.call(command, shell=True)
    command= ''' bedtools intersect -v -a ''' + f2 + ''' -b ''' + f1 + ''' > ''' + intermediate_file2
    subprocess.call(command, shell=True)


    #appending a random 4th column to prepare the file for twoBitToFa 
    command=''' echo "$(awk '{print $1, $2, $3,100}' ''' + intermediate_file1 + ''' )" > ''' + intermediate_file1
    subprocess.call(command, shell=True)
    command=''' echo "$(awk '{print $1, $2, $3,100}' ''' + intermediate_file2 + ''' )" > ''' + intermediate_file2
    subprocess.call(command, shell=True) 


    #converting bed to fasta
    command=''' twoBitToFa hg19.2bit -bed=''' + intermediate_file1 + ''' ''' + fasta_file1
    subprocess.call(command, shell=True)
    command=''' twoBitToFa hg19.2bit -bed=''' + intermediate_file2 + ''' ''' + fasta_file2
    subprocess.call(command, shell=True)
    
    
    
    #finding intersection count of the files
    command=''' echo "$(tr ' ' \\\\t < '''+ intermediate_file1 + ''' )" > ''' + intermediate_file1
    subprocess.call(command, shell=True)
    command=''' echo "$(tr ' ' \\\\t < '''+ intermediate_file2 + ''' )" > ''' + intermediate_file2
    subprocess.call(command, shell=True)
    command='''bedtools intersect -a '''+intermediate_file1+''' -b '''+intermediate_file2+''' | wc -l'''
    count=subprocess.check_output(command, shell=True)
    count= int(count)
    print count
    

    
    #finding number of rows in class 1 
    command= ''' awk 'END {print NR}' '''+intermediate_file1
    num_in_class1=subprocess.check_output(command, shell=True)
    num_in_class1= int(num_in_class1)
    

    #finding number of rows in class 0
    command= ''' awk 'END {print NR}' '''+intermediate_file2
    num_in_class0=subprocess.check_output(command, shell=True)
    num_in_class0= int(num_in_class0)

    #count = intersection count of file1_30 & file2_30  
    #num_in_class0 = total in class 0 file1_30
    #num_in_class1 = total in class 1 file2_30
    return count, num_in_class0, num_in_class1

