import time
import os
import pandas as pd
from Configs import input_data_dir, streaming_data_dir

streaming_file = pd.read_csv(input_data_dir + '\\portugal_listinigs.csv', low_memory=False, encoding='utf-8')

for i in range(0, len(streaming_file), 10):
    batch = streaming_file.iloc[i:i + 10]
    batch_file = os.path.join(streaming_data_dir, f'batch_{int(time.time())}.json')
    batch.to_json(batch_file, orient='records', lines=True, force_ascii=False)
    time.sleep(1)
