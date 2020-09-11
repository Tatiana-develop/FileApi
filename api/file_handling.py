import hashlib
import os

from datetime import datetime

from settings import STORE_PATH, MAX_DIR_SIZE, SYMBOL_COUNT_SEPARATE, BUF_SIZE
from api import app


class File:
    __buf_size = BUF_SIZE
    __symbol_count_separate = SYMBOL_COUNT_SEPARATE
    __store_path = STORE_PATH
    __max_dir_size = MAX_DIR_SIZE

    def __init__(self):
        if not os.path.exists(self.__store_path):
            os.mkdir(self.__store_path)

    def search(self, file_hash):
        file_hash_path = self.get_full_path(file_hash)
        if os.path.exists(file_hash_path):
            return file_hash_path
        else:
            return None

    def save(self, file, file_size=0):
        try:
            name_temp_file = self.get_hash(file.filename + str(datetime.now()))
            md5 = hashlib.md5()

            fw = open(name_temp_file, 'wb')
            while True:
                data = file.read(self.__buf_size)

                if not data:
                    break

                fw.write(data)
                md5.update(data)

            file.close()
            fw.close()

            file_hash = md5.hexdigest()
            file_hash_path = self.get_full_path(file_hash)
            dir_path = os.path.dirname(file_hash_path)

            if os.path.exists(file_hash_path):
                raise FileExistsError()

            store_size = os.path.getsize(self.__store_path)
            current_size = store_size + file_size

            if self.__max_dir_size < current_size:
                raise MemoryError('No space in store folder')

            if not os.path.exists(dir_path):
                os.mkdir(dir_path)

            os.rename(name_temp_file, file_hash_path)

            return file_hash

        except BaseException as e:
            os.remove(name_temp_file)
            raise e

    def remove(self, file_hash):
        try:
            file = self.get_full_path(file_hash)
            os.remove(file)

            file_dir = os.path.join(self.__store_path, file_hash[:self.__symbol_count_separate])
            files = os.listdir(file_dir)
            if not files:
                os.rmdir(file_dir)

        except FileNotFoundError as e:
            raise FileNotFoundError()

        except BaseException as e:
            app.logger.error(e)
            raise BaseException()

    def get_hash(self, file_name):
        return hashlib.md5(file_name.encode('utf-8')).hexdigest()

    def get_full_path(self, hash_name):
        return os.path.join(self.__store_path, hash_name[:self.__symbol_count_separate], hash_name)
