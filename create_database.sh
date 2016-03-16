mysql -uroot -e "create database if not exists db_ask"
python ask/manage.py syncdb
