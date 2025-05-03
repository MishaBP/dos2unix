#!/usr/bin/env python3
"""
Умный конвертер DOS-to-Unix с автоопределением кодировки
Usage: dos2unix.py <input> <output>
"""
import sys
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)  # Анализируем первые 10КБ для определения кодировки
        result = chardet.detect(raw_data)
        return result['encoding']

def convert_file(input_path, output_path):
    try:
        # Определяем кодировку
        encoding = detect_encoding(input_path)
        if not encoding:
            encoding = 'utf-8'  # По умолчанию, если не удалось определить
        
        print(f"Определена кодировка: {encoding}")

        # Конвертируем построчно с учетом кодировки
        with open(input_path, 'r', encoding=encoding, newline='') as infile, \
             open(output_path, 'w', encoding='utf-8', newline='\n') as outfile:
            
            crlf_count = 0
            line_count = 0
            
            for line in infile:
                line_count += 1
                if line.endswith('\r\n'):
                    crlf_count += 1
                outfile.write(line.rstrip('\r\n') + '\n')
            
            print(f"Обработано строк: {line_count}")
            print(f"Заменено CRLF: {crlf_count}")
            print(f"Файл сохранен в UTF-8 с Unix-переносами строк")

    except Exception as e:
        sys.exit(f"Ошибка: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    
    convert_file(sys.argv[1], sys.argv[2])
