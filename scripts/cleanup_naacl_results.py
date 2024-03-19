import pandas as pd

LANG = 'eng'

RESULTS_FILENAME = f'2024-MAR-18-agora-{LANG}-mutox-results-with-gpt-4-0125.csv'
REF_FILENAME = 'data/mutox/mutox.tsv'

def get_info_for_filename(filename, df_results, df_ref):
    return_dict = dict()
    
    file_id = filename.replace('mutox-','').replace('.wav','')
    row = df_ref[df_ref['id']==file_id]

    return_dict['true_label'] = row['contains_toxicity'].values[0]
    return_dict['true_label_detail'] = row['toxicity_types'].values[0]
    return_dict['true_transcript'] = row['audio_file_transcript'].values[0]
    return_dict['file_id'] = file_id
    return return_dict
    
df_results = pd.read_csv(RESULTS_FILENAME)
df_ref = pd.read_csv(REF_FILENAME, delimiter='\t')


for i in range(df_results.shape[0]):
    filename = df_results['filename'][i]
    info_for_filename = get_info_for_filename(filename, df_results, df_ref)
    for key_ in info_for_filename.keys():
        if key_ == 'file_id': break
        df_results.at[i,key_] = info_for_filename[key_]

print(df_results.head())
df_results.to_csv(f'2024-MAR-18-{LANG}-cleaned-gpt-4-0125.csv')
