import hashlib
import os

from settings import STORE_PATH, MAX_DIR_SIZE, SYMBOL_COUNT_SEPARATE
from api import app


class File:
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
            file_hash = self.get_filename(file.filename)
            file_hash_path = self.get_full_path(file_hash)
            dir_path = os.path.dirname(file_hash_path)

            store_size = os.path.getsize(self.__store_path)
            current_size = store_size + file_size

            if self.__max_dir_size > current_size:
                if not os.path.exists(dir_path):
                    os.mkdir(dir_path)

                with open(file_hash_path, 'wb') as fw:
                    file.save(fw, buffer_size=16384)
                    file.close()
                return file_hash

            else:
                raise BaseException('No space in store folder')

        except BaseException as e:
            app.logger.warning(e)

    def remove(self, file_hash):
        try:
            file = self.get_full_path(file_hash)
            os.remove(file)

            file_dir = os.path.join(self.__store_path, file_hash[:self.__symbol_count_separate])
            files = os.listdir(file_dir)
            if not files:
                os.rmdir(file_dir)

            return True
        except FileNotFoundError as e:
            app.logger.error(e)
        except BaseException as e:
            app.logger.error(e)
            return False

    def get_hash(self, file_name):
        return hashlib.md5(file_name.encode('utf-8')).hexdigest()

    def get_filename(self, filename):
        filenamelist = filename.split('.')
        name_hash = self.get_hash(filenamelist[0])
        filename = '.'.join([name_hash, filenamelist[1]])
        return filename

    def get_full_path(self, hash_name):
        return os.path.join(self.__store_path, hash_name[:self.__symbol_count_separate], hash_name)
