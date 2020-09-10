from flask import request, send_file
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

from api.file_handling import File
from api import app


class FileApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('file', type=FileStorage, location='files')
        self.parser.add_argument('hash')

    def get(self):
        arg = self.parser.parse_args()

        if not self.key_check('hash'):
            err_message = 'Hash didn\'t send.'
            app.logger.info(err_message)
            return {'message': err_message}, 400

        file = File().search(arg['hash'])

        if not file:
            err_message = 'File {} is not exist.'.format(arg['hash'])
            app.logger.info(err_message)
            return {'message': err_message}, 404

        return send_file(file, as_attachment=True)

    def post(self):
        try:
            arg = self.parser.parse_args()

            if not self.key_check('file'):
                err_message = 'File didn\'t send.'
                app.logger.info(err_message)
                return {'message': err_message}, 400

            file = arg['file']
            file_size = request.headers.get('Content-Length')

            if not file_size:
                err_message = 'File is empty.'
                return {'message': err_message}, 400

            file_size = int(file_size)
            file_hash = File().save(file, file_size)

            return {'file_hash': file_hash}, 200

        except FileExistsError:
            return {'message': 'File {} is exist. \n You can remove this file and try send again.'.format(
                    file.filename)}

        except (MemoryError, BaseException) as e:
            app.logger.error(e)
            return {'message': 'Service Unavailable Error'}, 503

    def delete(self):
        try:
            if not self.key_check('hash'):
                err_message = 'Hash not sent.'
                app.logger.info(err_message)
                return {'message': err_message}, 400

            arg = self.parser.parse_args()['hash']
            File().remove(arg)

            return {'message': 'File removed.'}, 200

        except FileNotFoundError:
            err_message = 'File {} is not exist.'.format(arg)
            return {'message': err_message}, 404

        except BaseException:
            return {'message': 'Service Unavailable Error'}, 503

    def key_check(self, key):
        return True if key in self.parser.parse_args().keys() else False
