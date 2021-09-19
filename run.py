from mainapp import *
from apscheduler.schedulers.background import BackgroundScheduler

if __name__ == '__main__':
    app.run(debug=True)

    sched_0 = BackgroundScheduler(daemon=True)
    sched_0.add_job(maintainingDic,'interval',seconds=600)
    sched_0.start()