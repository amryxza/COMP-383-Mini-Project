import os
#makes results directories for produced results
os.system("mkdir results")
os.system("mkdir results/spades")
os.system("vdb-config -i")

def get_reads():
    #use sra toolkit's fastq-dump to retrieve Illumina reads
    os.system("fastq-dump SRR8185310 --outdir ~/results")

def run_spades():

    #use spades to assemble genome
    #-s selects the fastq file we retrieved in get_reads()
    #-o writes the assembly to spadesresults
    os.system("~/SPAdes-3.15.4-Linux/bin/spades.py -s ~/results/SRR8185310.fastq -o ~/results/spades")


def produce_new_fasta(file):
    #open spades result + account for fasta format
    records = open(file).read().split(">")
    #initialize variables for bp count and contig count
    count=0
    num_contigs=0
    #open new fasta file to contain only contigs > 1000
    new_result = open("new_results.fasta","w")
    #loop through the fasta file
    for i in records:
        #account for the first line being empty
        if i != "":
            temp = i
            #split to find number of bp per contig
            temp = temp.split("_")

            #identify contigs > 1000
            if int(temp[3]) >1000:
                #add number of bp together
                count+=int(temp[3])
                #increment number of contigs
                num_contigs+=1
                #write contigs > 1000 to new result fasta
                new_result.write(">"+i)
    #close new fasta file
    new_result.close()
    #return bp count and contig count
    return count,num_contigs

def predict_proteins():
    #use gms2 to predict proteins from the new fasta file
    #--seq <filename> --genome-type auto --faa <output title>
    os.system("~/gms2_linux_64/gms2.pl --seq ~/results/new_results.fasta --genome-type auto --faa ~/results/gms2_result")

def retrieve_database():
    #make the E.coli fasta a database
    os.system("makeblastdb -in Ecoli.fasta -dbtype prot")

def produce_blast():
    #use blastp to perform a local blast
    #-query <result of gms2> -db Ecoli.fasta
    #-culling_limit 1    ensures that only the best result is published for each predicted sequence
    #-outfmt '10         separates values with commas (csv)
    #qseqid              query sequence ID
    #sseqid              subject sequence ID
    #pident              percent identity
    #qcovs               percent query coverage
    #-out <results in csv format>
    os.system('''blastp -query ~/results/gms2_result -db Ecoli.fasta -culling_limit 1 
    -outfmt '10 qseqid sseqid pident qcovs' -out ~/results/predicted_functionality.csv''')
    
def count_csd():
    records = open("results/gms2_result").read().split(">")
    last_record = records[-1]
    last_record=last_record.split(" ")
    return int(last_record[0]-4140)


def main():
    

    #open log file where results will be printed
    result = open("results/miniproject.log","w")

    #retrieve reads for Illumina from NCBI
    get_reads()

    #run SPAdes to assemble genome
    run_spades()

    #write SPADes command to log file
    result.write("SPAdes command: ~/SPAdes-3.15.4-Linux/bin/spades.py -s ~/results/SRR8185310.fastq -o ~/results/spades")


    #calculate number of contigs and base pairs in spades result
    count,numcontigs=produce_new_fasta("results/spades/contigs.fasta")

    #write bp count and contig count to log file
    result.write("There are "+ str(numcontigs) +" contigs > 1000 in the assembly.")
    result.write("There are " +str(count)+" bp in in the assembly.")

    # use gms2 to predict protein sequences for the genes we have found
    predict_proteins()

    #make the E.coli database
    retrieve_database()

    #blast contigs against the E.coli database and produce a csv 
    produce_blast()

    discrepancy = str(count_csd())

    #write discrepancy in CDS in the csv file compared to the RefSeq
    result.write("GeneMarkS found "+ discrepancy+ " additional CDS than the RefSeq.")

    result.close() 

if __name__ == "__main__":
    main()



