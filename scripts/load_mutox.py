import requests
import pandas as pd
from pydub import AudioSegment
from tqdm import trange
import os

N_SAMPLES = 200
VERBOSE = False

df = pd.read_csv("data/mutox/mutox.tsv", delimiter='\t')

def return_info_from_str(info_str):
    return_dict = dict()
    location_list = info_str.split(' ')
    return_dict['public_url'] = location_list[0]
    return_dict['start'] = int(location_list[1])
    return_dict['end'] = int(location_list[2])
    return return_dict

for i in trange(N_SAMPLES):
    sample_id = df['id'][i]
    info_str = df['public_url_segment'][i]
    info_dict = return_info_from_str(info_str)
    if VERBOSE:
        print(info_dict)
    audio_resp = requests.get(info_dict['public_url'])

    with open('tmp.mp3', 'wb') as f:
        f.write(audio_resp.content)

    audio = AudioSegment.from_mp3('tmp.mp3')
    cropped_audio = audio[info_dict['start']:info_dict['end']]
    cropped_audio.export(f'data/mutox/Data/mutox-{sample_id}.wav',format='wav')
    
    os.remove('tmp.mp3')
    
