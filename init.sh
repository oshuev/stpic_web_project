sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/test.conf
sudo rm -f /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart

sudo ln -sf /home/box/web/etc/gunicorn.conf   /etc/gunicorn.d/test
sudo ln -sf /home/box/web/ask/ask.gunicorn.conf   /etc/gunicorn.d/ask-proj
sudo /etc/init.d/gunicorn restart