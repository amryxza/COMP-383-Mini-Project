# COMP-383-Mini-Project

## Introduction
The purpose of this Python wrapper can be summarized in distinct steps:
  1. To retrieve and assemble fastq files containing single unpaired reads
  2. To predict a protein sequence based on contigs > 100 bp
  3. To BLAST the predicted protein sequences against an existing database

## Required Tools
The following tools are required in order for this code to function.

### SRA Toolkit
The documentation can be found here: https://github.com/ncbi/sra-tools
SRA Toolkit is used for its fastq-dump functionality. In order to install SRA Toolkit, the following code can be run in Ubuntu.
>wget --output-document sratoolkit.tar.gz http://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/current/sratoolkit.current-ubuntu64.tar.gz
>tar -vxzf sratoolkit.tar.gz
>export PATH=$PATH:$PWD/sratoolkit.2.11.2-ubuntu64/bin

### SPAdes
The documentation can be found here: https://github.com/ablab/spades
SPAdes is used in order to assemble the reads retrieved using SRA Toolkit. In order to install SPAdes, the following code can be run in Ubuntu.
>wget http://cab.spbu.ru/files/release3.15.4/SPAdes-3.15.4-Linux.tar.gz
>tar -xzf SPAdes-3.15.4-Linux.tar.gz

### GeneMarkS-2
This software can be downloaded here: http://exon.gatech.edu/GeneMark/license_download.cgi
GeneMarkS-2 is used to predict protein sequences from the the genes identified by SPAdes. 
Both the gz files (the code and the key) must be downloaded. Move the code into your home directory. Unpack it using:
>tar -xf gms2_linux_64.tar.gz

The key must be unzipped and copied to your home directory using:

>gunzip gm_key_64.gz
>cp gm_key_64 ~/.gmhmmp2_key

## mini project.py
This was coded using Python 3 and contains the wrapper. Be sure to change the repository to the user repository before running through data. Results from the code (including the number of contigs longer than 1000 bps, the total number of bps in those contigs, and the difference between the CSD produced by GeneMarks and the CSD in the RefSeq) will be summarized in /files/miniproject.log
Additional files in /files will include:
1. the fastq file from SRAtoolkit
2. files from SPAdes (including contigs.fasta)
3. the fasta file with contigs > 1000 bp (new_results.fasta)
4. the protein predictions from GMS-2
5. the results of the BLAST (predicted_functionality.csv). This will include the query sequence ID, subject sequence ID, % identity, and %query coverage  
