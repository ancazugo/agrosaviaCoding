import pandas as pd
import re

ariba = pd.read_csv('exercise_2/ariba_amr_output.csv')
metadata = pd.read_csv('exercise_2/ncbi_acquired_genes_metadata.csv')

refseqs_df = metadata[((metadata['subclass'] == 'CARBAPENEM') | (metadata['subclass'] == 'CEPHALOSPORIN')) & (metadata['refseq_nucleotide_accession'].str.startswith('NG_'))]
refseqs = list(refseqs_df['refseq_nucleotide_accession'])

index = 1
loci =[]
while index < 200:
    locus = list(ariba.columns)[index].replace('.assembled', '')
    loci.append(locus)
    index += 4
    
def isResistant():
    
    samples_lst, loci_lst, antibiotics_lst, refseqs_lst = [], [], [], []
    
    for row in range(len(ariba)):
        for locus in loci:
                       
            sample = ariba.loc[row]
            name = sample['name']
            assembled = sample[locus + '.assembled']
            ctg = sample[locus + '.ctg_cov']
            
            refseq = str(sample[locus + '.ref_seq'])
            ref_seq_format = re.split("\.", refseq, 1)[-1]
            
            if assembled.startswith('yes') and (ctg >= 10) and (ref_seq_format in refseqs):
                
                antibiotic = refseqs_df[refseqs_df['refseq_nucleotide_accession'] == ref_seq_format]['subclass'].iloc[0]               
                samples_lst.append(name)
                loci_lst.append(locus)
                antibiotics_lst.append(antibiotic)
                refseqs_lst.append(ref_seq_format)
                
    df = pd.DataFrame({'Sample': samples_lst, 'Locus': loci_lst, 'Antibiotic': antibiotics_lst, 'RefSeq_Accession': refseqs_lst})
    return df

ans = isResistant()
ans.to_csv('resistant_samples.csv', index=False)