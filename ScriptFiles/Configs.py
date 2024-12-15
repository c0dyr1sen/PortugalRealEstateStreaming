from pathlib import Path

#Директория проекта с данными
root_path = str(Path(__file__).resolve().parents[1]) + '\\DataFiles'

#Директории, для хранения различных типов данных
streaming_data_dir = root_path + '\\StreamingData'
aggregated_data_dir = root_path + '\\CombinedData'
input_data_dir = root_path + '\\InputData'