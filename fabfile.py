from fabric.api import *
from settings import *

host = "root@%s" % SERVER_NAME
DIR = "/var/www/onetimedns"

@task(default=True)
@hosts(host)
def deploy():
    local("make index")
    run("mkdir -p %s" % DIR)
    put("persist", "/etc/cron.daily")
    with cd(DIR):
        files = ["static", "pip-requirements.txt", "supervisor.conf", "persist.py", "base36.py", "web.py", "dns.rb"]
        [ put(f, ".") for f in files ]
        run("pip install -q -r pip-requirements.txt")
        run("ln -sf %s/supervisor.conf /etc/supervisor/conf.d/onetimedns.conf && supervisorctl update" % DIR)
        run("supervisorctl restart onetimedns:*")
