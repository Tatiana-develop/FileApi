# FileApi
Данный проект был реализован в рамках тестового задания. Требовалось реализовать Api для загрузки/выгрузки/удаления файлов из локального хранилища.

# Настройка виртуального окружения.
1. Создать виртуальное окружение Python3.7 virtualenv.
```
pip install virtualenv
```
2. Установить зависимости.
```
pip install -r requirements.txt
```
# Настройка Api.
Перед запуском Api следует определить место хранения полученных файлов и ограничения их размера в settings.py.
```python
STORE_PATH = '/path/to/store/'
```
# Запуск Api как демон на Linux.
Для запуска демон-Api можно настроить его работу как сервис на Linux.
1. Создать конфигурационный файл /etc/systemd/system/fileapi.service:
 
- В секции [Unit] нужно описать его и определить после какого сервиса стоит его запускать (например network.target):

```
[Unit]
Description=File Api
After=network.target
```

- В секции [Service] указываем:
  - User - пользователь, под которым нужно стартовать сервис;
  - WorkingDirectory - директория, где хранится проект;
  - ExecStart - команда для запуска Api (с помощью gunicorn);
  - Restart - необходимость перезапуска.

```
[Service]
User=<name_user>
WorkingDirectory=/path/to/directory/FileApi
ExecStart=/path/to/directory/FileApi/venv/bin/gunicorn -b 127.0.0.1:5000 -w 4 wsgi:app
Restart=always
```
- В секции [Install] описываем уровень запуска. В данном случае многопользовательский режим без графики.
```
[Install]
WantedBy=multi-user.target
```
2. Запуск сервиса.
```bash
systemctl start fileapi
```
