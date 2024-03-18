import requests
import pandas as pd
from pydub import AudioSegment
from tqdm import trange
import os
import threading
from io import BytesIO

N_SAMPLES = 1000
VERBOSE = False

df = pd.read_csv("data/mutox/mutox.tsv", delimiter='\t')
df = df[df['lang']=='eng']
df = df[df['partition']=='devtest']

print(df.head)

def return_info_from_str(info_str):
    return_dict = dict()
    location_list = info_str.split(' ')
    return_dict['public_url'] = location_list[0]
    return_dict['start'] = int(location_list[1])
    return_dict['end'] = int(location_list[2])
    return return_dict

def crop_and_save(df,i,return_info_from_str):
    sample_id = df['id'][i]
    info_str = df['public_url_segment'][i]
    info_dict = return_info_from_str(info_str)
    if VERBOSE:
        print(info_dict)
    try:
        audio_resp = requests.get(info_dict['public_url'],timeout=10)
    except requests.exceptions.Timeout:
        print(f'skipped {sample_id} due to timeout')

    '''
    with open('tmp.mp3', 'wb') as f:
        f.write(audio_resp.content)
    '''
    try:
        audio_data = BytesIO(audio_resp.content)
        audio = AudioSegment.from_file(audio_data, format='mp3')
        cropped_audio = audio[info_dict['start']:info_dict['end']]
        cropped_audio.export(f'data/mutox/Data/mutox-{sample_id}.wav',format='wav')
    except IndexError:
        print(f'skipped {sample_id} due to error')

  

for j in trange(0,N_SAMPLES):
    i = df.index[j]
    t = threading.Thread(target=crop_and_save, args=(df,i,return_info_from_str,))
    t.start()
    t.join(timeout=5)
