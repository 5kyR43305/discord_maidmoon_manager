from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    """
    봇이 살아있는지 확인하는 엔드포인트입니다.
    UptimeRobot과 같은 외부 서비스가 이 주소에 접속하여 봇을 깨어있게 합니다.
    """
    return "Hello! I am alive!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    """
    별도의 스레드에서 웹 서버를 실행하여 봇의 메인 루프를 방해하지 않습니다.
    """
    t = Thread(target=run)
    t.start()
