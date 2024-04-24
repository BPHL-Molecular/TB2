# TBx2
**TB** **T**ool **B**enchmarking
## How to use the tool to benchmark your TB tools/pipelines
### 1. Downloading the NGS data from (?????) and using them to feed your TB tool.
### 2. Using the outputs of your TB tool to fill the CSV file "tool_output_template.csv" in the folder "./input".        
   #### Note: 
         1. The file "tool_output_template.csv" has three rows. The first row is drug names covered by your TB tools.For example, Rifampicin,Isoniazid,Ethambutol,Pyrazinamide.      
         2. The names are seperated by the comma ",". The second row is the genes covered by your TB tools. They are also seperated by the comma ",". For example, gyrB,gyrA,fgd1,mshA,ccsA,rpoB,rpoC,mmpL5,mmpS5.         
         3. The third row is the mutation locus information found by your TB tool. The loci are seperated by ",". Each locus includes three information: mutation location, mutation gene, and mutation nucleic acid.For example, 761095|rpoB|T>G,781687|rpsL|A>G,2155168|katG|G>C.          
### 3.Run the tool

1) If pytablewriter is not included in your python3, you need install it first.
```bash
pip install pytablewriter
```   
2) run the tool

```bash
bash benchmark.sh
```

### 4. The result file is "Benchmark_report.txt"   
