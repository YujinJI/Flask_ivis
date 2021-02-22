import urllib
import re
from urllib.request import urlopen, Request
from flask import Flask, render_template, redirect, url_for
from datetime import datetime
import bs4

app = Flask(__name__)


def weather():
    enc_location = urllib.parse.quote('창원시 의창구 사림동 날씨')
    url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=' + enc_location

    html = urlopen(Request(url)).read()
    soup = bs4.BeautifulSoup(html, "html.parser")

    titles_by_select = soup.select('div.today_area > div.main_info > span')

    klass_name = titles_by_select[0].get('class')[1]

    p = re.compile('ws([0-9]*)')
    m = p.search(klass_name)
    svg = m.group(1).zfill(2)

    return 'https://ssl.pstatic.net/sstatic/keypage/outside/scui/weather_new/img/weather_svg/icon_wt_' + svg + '.svg'


last_now = datetime.now()
last_time = last_now.strftime('%Y-%m-%d %H:%M %a')


@app.route('/')
def home():
    now = datetime.now()
    current_time = now.strftime('%Y-%m-%d %H:%M %a')
    return render_template("home.html", current_time=current_time, weather=weather(), last_time=last_time)


@app.route('/last_click', methods=['post'])
def last_click():
    global last_now
    global last_time
    last_now = datetime.now()
    last_time = last_now.strftime('%Y-%m-%d %H:%M %a')
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run()
