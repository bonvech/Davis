from weatherlink.davis_convert import *
import os
import sys


############################################################################
############################################################################
if __name__ == "__main__":
    ##  !!! ввести имя папки, где находятся исходные данные от прибора Дэвис
    datadirname = "D:\\AerosolComplex\\YandexDisk\\ИКМО org.msu\\_Instruments\\_Davis\\2 ВНИИЖТ\\VNIIZT"
    ##  расширение исходного файла данных
    extention = "wlk"        
    
    for file in os.listdir(datadirname):
        try:    
            ## 
            if not file.endswith(extention):
                continue
                
            file_name = f"{datadirname}\\{file}"
            print("=============================")
            print(file_name)
            
            ##  read and convert latest "wlk" file
            df = read_and_convert_data(file_name) 
            print(df.head())
            
            ##  write to out csv file
            file_name_out = file_name.replace(extention, 'csv')  
            df.to_csv(file_name_out, index=False, float_format="%.2f")
            
            ##  сохранить в папку data
            dirr = "data"
            if not os.path.isdir(dirr):
                os.mkdir(dirr)
            df.to_csv(f"{dirr}/{file_name_out.split('\\')[-1]}", index=False, float_format="%.2f")
            ##df.to_csv(f"{dirr}/{file_name_out.split(davis.sep)[-1]}", index=False, float_format="%.2f")
           
        except Exception as error:
            print(f"davis translator: file {file_name}: {error}")

#x = input()