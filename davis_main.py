from weatherlink.supervisor import *
from weatherlink.davis_convert import *


############################################################################
############################################################################
if __name__ == "__main__":

    #errors_inside_programm = ""

    davis = Supervisor("Davis")
    davis.datadirname = "D:\\AerosolComplex\\YandexDisk\\ИКМО org.msu\\_Instruments\\_Davis\\2 ВНИИЖТ\\VNIIZT"
    davis.extention = "wlk"
    
    ##  find latest "wlk" file
    last_file = davis.get_latest_file(davis.extention)
    print(last_file)
    
    try:    
        ##  read and convert latest "wlk" file
        file_name = f"{last_file}"
        df = read_and_convert_data(file_name) 
        print(df.head())
        
        ##  write to out csv file
        file_name_out = file_name.replace(davis.extention, 'csv')  
        df.to_csv(file_name_out, index=False, float_format="%.2f")
        df.to_csv(f"data/{file_name_out.split('\\')[-1]}", index=False, float_format="%.2f")        
    except Exception as error:
        davis.write_to_bot(f"{davis.device_name} Convertor: {error}")
        
    # if errors_inside_programm:
        # davis.write_to_bot(f"{davis.device_name} Convertor: {errors_inside_programm}")

