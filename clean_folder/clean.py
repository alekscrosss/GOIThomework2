import os
import shutil
import re

def normalize(name):
    mapping = {
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'Ye',
        'Ж': 'Zh', 'З': 'Z', 'И': 'Y', 'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K', 'Л': 'L',
        'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ю': 'Yu',
        'Я': 'Ya', 'ь': '', '’': ''
    }
    for cyr, lat in mapping.items():
        name = name.replace(cyr, lat)
        name = name.replace(cyr.lower(), lat.lower())

    name = re.sub(r'[^a-zA-Z0-9]', '_', name) # міняємо недопустимі символи
    return name

def unpack(archive_path, path_to_unpack):
    shutil.unpack_archive(archive_path, path_to_unpack)
    os.remove(archive_path)

def get_unique_name(path, name, ext): #Повертаємо ун. ім'я
    counter = 1
    new_name = name
    while os.path.exists(os.path.join(path, new_name + ext)):
        new_name = f"{name}_{counter}"
        counter += 1
    return new_name + ext

def process_folder(folder_path): #Формати та папки
    image_exts = ('JPEG', 'PNG', 'JPG', 'SVG')
    video_exts = ('AVI', 'MP4', 'MOV', 'MKV')
    doc_exts = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
    audio_exts = ('MP3', 'OGG', 'WAV', 'AMR')
    archive_exts = ('ZIP', 'GZ', 'TAR')

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            old_path = os.path.join(root, file)
            file_name, file_ext = os.path.splitext(file)
            file_ext = file_ext[1:].upper()

            new_file_name = normalize(file_name) + '.' + file_ext.lower()
            new_file_name = get_unique_name(root, normalize(file_name), '.' + file_ext.lower())
            new_path = os.path.join(root, new_file_name)

            os.rename(old_path, new_path)

            if file_ext in image_exts:
                if not os.path.exists(os.path.join(folder_path, 'images')):
                    os.mkdir(os.path.join(folder_path, 'images'))
                shutil.move(new_path, os.path.join(folder_path, 'images', new_file_name))

            elif file_ext in video_exts:
                if not os.path.exists(os.path.join(folder_path, 'video')):
                    os.mkdir(os.path.join(folder_path, 'video'))
                shutil.move(new_path, os.path.join(folder_path, 'video', new_file_name))

            elif file_ext in doc_exts:
                if not os.path.exists(os.path.join(folder_path, 'documents')):
                    os.mkdir(os.path.join(folder_path, 'documents'))
                shutil.move(new_path, os.path.join(folder_path, 'documents', new_file_name))

            elif file_ext in audio_exts:
                if not os.path.exists(os.path.join(folder_path, 'audio')):
                    os.mkdir(os.path.join(folder_path, 'audio'))
                shutil.move(new_path, os.path.join(folder_path, 'audio', new_file_name))

            elif file_ext in archive_exts:
                if not os.path.exists(os.path.join(folder_path, 'archives')):
                    os.mkdir(os.path.join(folder_path, 'archives'))
                unpack(new_path, os.path.join(folder_path, 'archives'))

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

def main():
    import sys
    if len(sys.argv) != 2:
        print("Використання: clean-folder <шлях_до_папки>")
    else:
        folder_path = sys.argv[1]
        process_folder(folder_path)

if __name__ == "__main__":
    main()
