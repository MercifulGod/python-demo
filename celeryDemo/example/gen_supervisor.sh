pa=`pwd`
cd ../
# 进入项目根目录
ROOT_PATH=`pwd`

cat >> /etc/supervisor/conf.d/celery.conf <<EOF
[program:celery]
directory=$ROOT_PATH
command=/usr/local/bin/celery worker -A example.tasks --loglevel=INFO
user=nobody
autostart=true
autorestart=true
stopasgroup=true
priority=20
redirect_stderr=true
stdout_logfile=/var/log/demo/%(program_name)s.std
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=1
EOF









