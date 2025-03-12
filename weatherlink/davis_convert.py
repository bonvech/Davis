##  Based on https://github.com/beamerblvd/weatherlink-python/tree/master
##  The data formats were obtained from Davis WeatherLink documentation:
##  - http://www.davisnet.com/support/weather/download/VantageSerialProtocolDocs_v261.pdf

#from __future__ import absolute_import, print_function
import sys
import pandas as pd

from weatherlink.importer import Importer
from weatherlink.utils import calculate_all_record_values


def read_and_convert_data(file_name):
    importer = Importer(file_name)

    print('Reading file %s' % importer.file_name)
    print('Year %s' % importer.year)
    print('Month %s' % importer.month)
    print()

    importer.import_data()
    #print("End of import data")

    ##  add calculated values
    for i in range(len(importer.records)):
        record = importer.records[i]
        #print(record)
        record.update(calculate_all_record_values(record))
        importer.records[i] = record
    #print("End of add")

    ##  convert to dataframe
    df = pd.DataFrame.from_records(importer.records)
    print(df.shape)
    
    columns_to_drop = ['solar_radiation', 'solar_radiation_high', 'uv_index', 'uv_index_high']
    df.drop(columns=columns_to_drop, inplace=True)
    print(df.shape)

    ##  calculate values to output
    df['timestamp'] = df['timestamp'].astype(int)
    df['wind_direction_prevailing'] = df['wind_direction_prevailing'].apply(lambda x: str(x).split('.')[1])
    df['wind_direction_speed_high'] = df['wind_direction_speed_high'].apply(lambda x: str(x).split('.')[1])
    df['wind_run_distance_total']   = df['wind_run_distance_total'].apply(lambda x: round(float(x), 3))
    df['temperature_outside']       = df['temperature_outside']      - df['temperature_wet_bulb']
    df['temperature_outside_high']  = df['temperature_outside_high'] - df['temperature_wet_bulb_high']
    df['temperature_outside_low']   = df['temperature_outside_low']  - df['temperature_wet_bulb_low']
    #df['dew_point_outside']
    #df['wind_speed']
    df['wind_run_distance_total'] = df['wind_run_distance_total'].astype(float) * 1.6
    df['wind_speed_high'] = df['wind_speed_high'].astype(float) / 2.25
    #df['wind_chill'] = 
    df['barometric_pressure'] = df['barometric_pressure'].astype(float) * 25.4
    df['temperature_inside']  = df['temperature_inside'].astype(float) - df['temperature_wet_bulb'].astype(float)
    df['dew_point_inside']    = df['dew_point_inside'].astype(float) - 32
    df['rain_collector_type'] = df['rain_collector_type'].apply(lambda x: str(x).split('.')[1])

    ##  rename columns
    columns_output = ["Date", "timestamp", "Temp Out","Hi Temp","Low Temp","Out Hum","Dew Pt.","Wind Speed", 
                    "Wind Dir","Wind Run","Hi Speed","Hi Dir","Wind Chill",
                    #"Heat Index","THW Index",
                    "Bar","Rain","Rain Rate",
                    #"Heat D-D","Cool D-D",
                    "In Temp","In Hum","In Dew", 
                    #"In Heat","In EMC","In Air Density",
                    "Wind Samp",
                    #"Wind Tx", "ISS Recept",
                    "Arc.Int."]
    columns_actual = ['date', 'timestamp', 'temperature_outside', 'temperature_outside_high', 'temperature_outside_low',
                    'humidity_outside', 'dew_point_outside', 'wind_speed', 'wind_direction_prevailing', 'wind_run_distance_total', 
                    'wind_speed_high', 'wind_direction_speed_high', 'wind_chill',
                    #"Heat Index","THW Index",
                    'barometric_pressure', 'rain_amount', 'rain_rate',
                    #"Heat D-D","Cool D-D",
                    'temperature_inside', 'humidity_inside', 'dew_point_inside', 
                    #"In Heat","In EMC","In Air Density",
                    'number_of_wind_samples', 
                    #"Wind Tx", "ISS Recept",
                    'minutes_covered']

    columns_unused =['wind_direction_prevailing_degrees', 'wind_direction_speed_high_degrees',
                    'dew_point_outside_low', 'dew_point_outside_high', 
                    'wind_chill_low', 'wind_chill_high',
                    'rain_collector_type', 'rain_amount_clicks', 'rain_rate_clicks',
                    'temperature_outside_high', 'temperature_outside_low','temperature_wet_bulb',
                    'temperature_wet_bulb_low', 'temperature_wet_bulb_high',
                    'minutes_past_midnight']
    df.rename(columns={A:a for A, a in zip(columns_actual, columns_output)}, errors="raise", inplace=True)

    ##  re-order columns
    columns = columns_output + df.columns.difference(columns_output).tolist()
    df = df[columns]
    return df


############################################################################
############################################################################
if __name__ == "__main__":
    
    datadirname = "D:\\AerosolComplex\\YandexDisk\\ИКМО org.msu\\_Instruments\\_Davis\\2 ВНИИЖТ\\VNIIZT"
    
    ##  find latest "wlk" file
    last_file = ''
    
    ##  read and convert latest "wlk" file
    file_name = f"{datadirname}\\2024-12.wlk"
    df = read_and_convert_data(file_name) 
    file_name_out = file_name.replace('.wlk', '.csv')  
    df.to_csv(file_name_out, index=False, float_format="%.2f")
