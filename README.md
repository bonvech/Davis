# Davis

Программа для обработки данных, записанных прибором Davis

Файлы:

  davis_main.py
  telebot_config.py
  start.bat
  start_test.bat
  weatherlink:
      davis_convert.py
      importer.py
      models.py
      supervisor.py
      utils.py

Порядок запуска программы
--------------------------
1. В файле davis_main.py написать путь до файлов данных с прибора в строке
   
datadirname = "D:\\AerosolComplex\\YandexDisk\\ИКМО org.msu\\_Instruments\\_Davis\\2 ВНИИЖТ\\VNIIZT"

2. В файле telebot_config.py проверить и при необходимости исправить токен бота и номер канала для вывода сообщений об ошибках.

3. В файле start_test.bat прописать путь до файла davis_main.py
   
Проверить работоспособность программы, запустив start_test.bat

4. В файле start.bat прописать путь до файла davis_main.py
   
Запустить start.bat, убедиться, что работает

5. В планировщике задач создать задачу AA_Davis, которая должна запускать start.bat раз в час
