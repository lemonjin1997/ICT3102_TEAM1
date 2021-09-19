from mainapp import *
from mainapp.utilities import *
from apscheduler.schedulers.background import BackgroundScheduler

if __name__ == '__main__':
    application.run(debug=True)

    sched_0 = BackgroundScheduler(daemon=True)
    sched_0.add_job(maintainingDic, 'interval', args=[deviceDic], seconds=600)
    sched_0.start()