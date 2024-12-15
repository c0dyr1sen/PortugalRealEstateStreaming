import os
import json
import time
from datetime import datetime
from Configs import streaming_data_dir, aggregated_data_dir

#Функция комбинирования файлов из потоковой директории
def combine_json_files(input_dir: str, output_dir: str):
    files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
    combined_data = []

    for file in files:
        file_path = os.path.join(input_dir, file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            data = json.loads(line)
                            combined_data.append(data)
                        except json.JSONDecodeError as e:
                            print(f'Error decoding JSON in file {file}: {e}')

            os.remove(file_path)
        except Exception as e:
            print(f'Error processing a file {file}: {e}')

    if combined_data:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(output_dir, f'combined_{timestamp}.json')

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(combined_data, f, ensure_ascii=False, indent=4)
            print(f'File {output_file} saved.')
        except Exception as e:
            print(f'Error saving a file: {e}')



# --- Main ---

while True:
    combine_json_files(streaming_data_dir, aggregated_data_dir)
    time.sleep(30)
