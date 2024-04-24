#!/usr/bin/env python

import os
import sys
import subprocess
import argparse
import datetime
import pandas as pd
import re
import os.path


#from pytablewriter import UnicodeTableWriter
from pytablewriter import MarkdownTableWriter

############################################################ Drug coverage evaluation ##################################################################
#### read lines of a file
file1 = open('./input/tool_output_template.csv')
file2 = open('./BK_DR/drugs.csv')
content1 = file1.readlines()
content2 = file2.readlines()

#### read 1st line from the file
#print(content2[0])

#### split by comma
list1=content1[0].strip().split(",")
list1_lower=[x.lower() for x in list1]

list2=content2[0].strip().split(",")
list2_lower=[x.lower() for x in list2]
#print(list2)

#### match two lists
matches = []
for ref_drug in list2_lower:
    if ref_drug in list1_lower:
        matches.append('Yes')
        #print(ref_drug)
    else:
        matches.append('No')
#print(len(matches))
#for x in matches:
#   print(x)

#### how many Benchmark drugs are available in the tested tool
drug_coverage=matches.count('Yes')/len(matches)
drug_coverage_percent_str=str(round(drug_coverage*100,2))
#print(matches.count(1))
#print(drug_coverage)   

#### The drugs in the tested tool that are not in the Benchmark drugs list
uncovered_drug = [] 
for test_drug in list1:
    if test_drug.lower()  not in list2_lower:
        uncovered_drug.append(test_drug)
        #print(test_drug)
        
#### create output file
with open("Benchmark_report.txt", "w") as f:
        f.write("########## Drug coverage evaluation ##########"+"\n\n")
        f.write("1.The percentage of benchmark drugs available in your tool:  "+drug_coverage_percent_str+"%\n\n")
if len(uncovered_drug) != 0:
   aline = ",".join(uncovered_drug)
   with open("Benchmark_report.txt", "a") as f:
        f.write("2.The drugs in your tool that do not exist in benchmark drug list:  "+aline+"\n\n")
else:
   with open("Benchmark_report.txt", "a") as f:
        f.write("2.The drugs in your tool that do not exist in benchmark drug list:  None\n\n")

##### create a matrix with 2 cols and 21 rows
matrix = []
for i in range(21):
    row=[]
    row.append(list2[i])
    row.append(matches[i])
    matrix.append(row)

#### output drug coverage table
def drug():
    writer = MarkdownTableWriter(
        #table_name="3. Drug coverage in your tool",
        headers=["Benchmark drugs", "Is it in your tool?"],
        value_matrix=matrix,
    )
    #writer.write_table()        
    #### change the output stream to a file
    with open("Benchmark_report.txt", "a") as f:
        f.write("3.Drug coverage in your tool\n\n")
        writer.stream = f
        writer.write_table()

if __name__ == "__main__":
    drug()

################################ Gene coverage evaluation ################################################################################
df=pd.read_csv('./BK_DR/WHO_TB_mutations.csv', header=0)
#print(df.head()) 
gene_catalogue=df["final_annotation.Gene"].drop_duplicates()
#print(gene_catalogue)
gene_catalogue_lower=gene_catalogue.str.lower().tolist()
list3=content1[1].strip().split(",")
list3_lower=[x.lower() for x in list3]

#### which gene in your tool can be matched to WHO-gene-mutaiton catalogue
gene_matches = []
for agene in gene_catalogue_lower:
    if agene in list3_lower:
        gene_matches.append('Yes')
    else:
        gene_matches.append('No')
#print(gene_matches)
#### the gene coverage percentage in your tool
gene_coverage=gene_matches.count('Yes')/len(gene_matches)
gene_coverage_percent_str=str(round(gene_coverage*100,2))

#### which gene in your tool can not be found in WHO-gene-mutaiton catalogue
unfound_gene=[]
for agene in list3:
    if agene.lower() not in gene_catalogue_lower:
        unfound_gene.append(agene)
        #print(agene.lower().strip())
#print(gene_catalogue_lower)
#print(unfound_gene)
   
#### output to file
with open("Benchmark_report.txt", "a") as f:
        f.write("\n\n########## Gene coverage evaluation ##########"+"\n\n")
        f.write("1.The percentage of the genes from WHO-gene-mutaiton catalogue available in your tool:  "+gene_coverage_percent_str+"%\n\n")

if len(unfound_gene) != 0:
   aline = ",".join(unfound_gene)
   with open("Benchmark_report.txt", "a") as f:
        f.write("2.The genes in your tool that do not exist in WHO-gene-mutaiton catalogue:  "+aline+"\n\n")
else:
   with open("Benchmark_report.txt", "a") as f:
        f.write("2.The genes in your tool that do not exist in WHO-gene-mutaiton catalogue:  None\n\n")

##### output gene coverage table
gene_matrix = []
for i in range(85):
    row=[]
    row.append(str(gene_catalogue.values[i]))
    #print(str(gene_catalogue.values[i]))
    row.append(gene_matches[i])
    gene_matrix.append(row)

def gene():
    writer = MarkdownTableWriter(
        headers=["Genes in WHO-TB-mutaiton-catalogue", "Is it in your tool?"],
        value_matrix=gene_matrix,
    )
    #writer.write_table()        
    #### change the output stream to a file
    with open("Benchmark_report.txt", "a") as f:
        f.write("3.Gene coverage in your tool\n\n")
        writer.stream = f
        writer.write_table()

if __name__ == "__main__":
    gene()


####### Mutations evaluation ###############################################################################
#print(list(df))
#print(df.dtypes)
#### get the third row in your tool data file
list4=content1[2].strip().split(",")
list4_lower=[x.lower() for x in list4]

#### get WHO mutation positions, genes and nucleotides.
mutation_pos=list(df["final_annotation.Position"])
mutation_gene=list(df["final_annotation.Gene"])
mutation_gene_lower=list(df["final_annotation.Gene"].str.lower())
mutation_nuc=list(df["final_annotation.TentativeHGVSNucleotidicAnnotation"])
mutation_nuc_lower=list(df["final_annotation.TentativeHGVSNucleotidicAnnotation"].str.lower())

#ref_nuc=list(df["final_annotation.ReferenceNucleotide"])
#ref_nuc_lower=list(df["final_annotation.ReferenceNucleotide"].str.lower())

#alt_nuc=list(df["final_annotation.AlternativeNucleotide"])
#alt_nuc_lower=list(df["final_annotation.AlternativeNucleotide"].str.lower())



#print(mutation_pos)
#print(type(mutation_pos[0]))

#### evaluate mutations found in your tool 
num=len(mutation_pos)
num_x=len(list4_lower)
found_in_WHO=[None]*num_x
i=0
for aset in list4_lower:
   items=aset.strip().split("|")
   for idx in range(num):
       if int(items[0])==mutation_pos[idx] and items[1]==mutation_gene_lower[idx] and items[2] in mutation_nuc_lower[idx]:
       #if int(items[0])==mutation_pos[idx] and items[1]==mutation_gene_lower[idx] and items[2]==ref_nuc_lower[idx] and items[3]==alt_nuc_lower[idx]:
          found_in_WHO[i]="Yes"
          #print(items[2])
          break          
   if found_in_WHO[i]==None:
      found_in_WHO[i]="No"
   i += 1
#### output 
num_detected=found_in_WHO.count('Yes')
detection_percent=str(round((num_detected/len(found_in_WHO))*100,2))
num_undetected=found_in_WHO.count('No')
undetection_percent=str(round((num_undetected/len(found_in_WHO))*100,2))

with open("Benchmark_report.txt", "a") as f:
   f.write("\n\n########## Mutation evaluation ##########"+"\n\n")
   f.write("1.How many of the mutations found by your tool can be confirmed in WHO TB mutation catalogue:  "+detection_percent+"%\n\n")
   if num_undetected == 0:
       f.write("1.How many of the mutations found by your tool can not be confirmed in WHO TB mutation catalogue:  None"+"\n\n")
   else:
       f.write("1.How many of the mutations found by your tool can not be confirmed in WHO TB mutation catalogue:  "+undetection_percent+"%\n\n")

### output table
mutation_matrix = []
for i in range(num_x):
    row=[]
    items=list4[i].strip().split("|")

    row.append(str(items[0]))
    row.append(str(items[1]))
    row.append(str(items[2]))
    #row.append(str(items[3]))
    row.append(found_in_WHO[i])
    mutation_matrix.append(row)

def mutation():
    writer = MarkdownTableWriter(
        headers=["Mutation positions reported by your tool", "Mutation genes reported by your tool", "Nucleotide changes reported by your tool", "Is it in WHO-TB-mutaiton-catalogue?"],
        value_matrix=mutation_matrix,
    )
    #writer.write_table()        
    #### change the output stream to a file
    with open("Benchmark_report.txt", "a") as f:
        f.write("3.Mutations in your tool\n\n")
        writer.stream = f
        writer.write_table()

if __name__ == "__main__":
    mutation()

################################ Figures #####################################################################
