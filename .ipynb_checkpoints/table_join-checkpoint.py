import pandas as pd
import os

output_path = 'output/seqsero'
output_folders = os.listdir(output_path)

def listResultFiles():
    sistr_lst, seqsero_lst = [], []
    
    for sample in output_folders:
        for root, directories, files in os.walk(os.path.join(output_path, sample)):
            for file in files:
                if file.endswith('.tab'):
                    sistr_lst.append(f'{output_path}/{sample}/{file}')
                elif file == 'SeqSero_result.tsv':
                    seqsero_lst.append(f'{output_path}/{sample}/{file}')
    return sistr_lst, seqsero_lst

sistr_out, seqsero_out = listResultFiles()

def appendDataFrames(lst):
    df = pd.DataFrame()
    for element in lst:
        df_temp = pd.read_csv(element, delimiter='\t')
        df = df.append(df_temp)
    return df

seqsero_df = appendDataFrames(seqsero_out)
sistr_df = appendDataFrames(sistr_out)

seqsero_df['Sample name'] = seqsero_df['Sample name'].apply(lambda x: re.split("\.", x, 1)[0])
seqsero_df.drop(columns=['Output directory', 'Input files', 'Note'], inplace=True)

sistr_df.rename(columns={'genome':'Sample name'}, inplace=True)
sistr_df.drop(columns=['fasta_filepath'], inplace=True)

summary_df = seqsero_df.set_index('Sample name').join(sistr_df.set_index('Sample name'))

summary_df.to_csv('seqsero_sistr_summary.csv', index=True)