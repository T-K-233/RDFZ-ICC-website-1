from flask import session, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from . import app, babel
# from .plugins import HWARecognizer
from config import LANGUAGES
import base64
from matplotlib import pyplot as plt
import os

square_path = "img/square/"

news_feed = [
    ['招生 | 如何才能上人大附中？', '尊重个性，挖掘潜力，一切为了学生的发展，一切为了祖国的腾飞，一切为了人类的进步', '07_03_2018_ruherdfz.png', 'https://kuaibao.qq.com/s/20180531A1EBRK00'],
    ['新闻 | 海外高校录取再创佳绩 三大国际课程让学生全面发展', '经过多年发展，目前已经成为三大顶尖国际课程并行、国际教育人才聚集、多元文化绽放的顶尖国际课程中心。', '07_03_2018_zhongzhao.png', 'https://mp.weixin.qq.com/s?__biz=MzA3MjAxMDAxMw==&mid=2650050593&idx=2&sn=036e05d2b195f3828f73f3e9614b6934'],
    ['毕业 | 人大附中2018届中外合作办学项目毕业典礼翟小宁校长致辞', '又到了一年一度的毕业季，同学们与母校依依惜别。', '07_03_2018_biyedianli.png', 'http://chuzhong.eol.cn/news/201806/t20180625_1612462.shtml'],
    ['回顾 | ICC Star 的精彩瞬间', '今年又有哪些精彩的瞬间 闪耀的时刻呢？我们来带你一一回顾…', '07_03_2018_icc_star.png', 'https://mp.weixin.qq.com/s?__biz=MjM5MTYyMjUyNg==&mid=2650496076&idx=1&sn=7a264d9adaa8b4c1f8c25d7506ec0a9e'],
    ['采访 | 一段有关《鸢缘》的故事', '“这段鸢缘，有段风筝，有关文化，有关传承。”', '07_03_2018_yuanyuan.png', 'https://mp.weixin.qq.com/s?__biz=MjM5MTYyMjUyNg==&mid=2650495932&idx=1&sn=5ba262e6769c972805a6bb0f4ff381a9'],
    ['采访 | 电影《红楼梦·尤二姐之死》主创团队', '“不要像我一样，活得像个笑话。”', '07_03_2018_hongloumeng.png', 'https://mp.weixin.qq.com/s?__biz=MjM5MTYyMjUyNg==&mid=2650495918&idx=1&sn=0ecb69640570fc0ac860a42b96cfbfa7'],
    ['采访 | 电影《余音》主创团队', '“这是老师在我的生活中留下的余音，亦可见全体智者为全体人类留下的绵延千里的余音。”', '07_03_2018_yuyin.png', 'https://mp.weixin.qq.com/s?__biz=MjM5MTYyMjUyNg==&mid=2650495908&idx=1&sn=30f73fed07c772ad41c7770f0bf3831e'],
    ['采访 | 电影《枝下猫》主创团队采访', '“也许我们只是想给大家讲一个照顾流浪猫的人的故事”', '07_03_2018_zhixiamao.png', 'https://mp.weixin.qq.com/s?__biz=MjM5MTYyMjUyNg==&mid=2650495885&idx=1&sn=dae7339e6dd221ace3d16456364ae10d'],
    ['展览 | IBDP 2018视觉艺术展览', 'IBDP Visual Arts Exhibition 2018', '07_03_2018_ib_art.png', 'https://mp.weixin.qq.com/s?__biz=MjM5MTYyMjUyNg==&mid=2650495864&idx=1&sn=17581b6c04e066fd4a89ee06453d7501'],
    ['预告 | 人大附中中外合作办学项目（ICC）开放日直播', 'ICC开放日今年仅设此一场。欢迎初三学生及家长莅临咨询。 ', '07_03_2018_traveled.png', 'https://mp.weixin.qq.com/s?__biz=MzIwOTA3NjMwNw==&mid=2650641261&idx=1&sn=b588ff47771e035824eff8c4e2be5ee6'],
    ['新年 | 狗年旺旺！', '在爆竹声中，我们迎来了新的、会更加精彩的一年～', '07_03_2018_gounianwangwang.png', 'https://mp.weixin.qq.com/s?__biz=MjM5MTYyMjUyNg==&mid=2650495849&idx=1&sn=18e22f69705ad63eb69ca6d6f5d02c6f'],
    ['活动 | Ultimate 活动报名！', '飞盘运动是一种在美国青少年间盛行的运动。', '07_03_2018_feipan.png', 'https://mp.weixin.qq.com/s?__biz=MjM5MTYyMjUyNg==&mid=2650495834&idx=1&sn=0cf4872c6113a2fb580e6413d6640f18'],
    ['回顾 | BF的那些精彩瞬间！', '你还记得那些在舞台上光彩夺目的小哥哥小姐姐们吗？让我们一起回顾一下比赛的一个个精彩瞬间吧～', '07_03_2018_2018bf.png', 'https://mp.weixin.qq.com/s?__biz=MjM5MTYyMjUyNg==&mid=2650495825&idx=1&sn=606554fb637872c039f42c50135f33b3'],
    ['回顾 | 论今年的万圣节经历了什么！', '可爱的万圣节活动布置知道我们经历了什么(ಡωಡ) ', '07_03_2018_happyhlw.png', 'https://mp.weixin.qq.com/s?__biz=MjM5MTYyMjUyNg==&mid=2650495586&idx=1&sn=b7704a5d2f9b6a1fc6b35bc69e85a51e'],
    ['诚信货架 | AirKit here we come', '您好［强行广告］欢迎来到实力至上主义的教室', '07_03_2018_airkit.png', 'https://mp.weixin.qq.com/s?__biz=MjM5MTYyMjUyNg==&mid=2650495784&idx=2&sn=13c2edeaa777d2b3a164454c007e2025'],
    ['竞赛 | IMMC国际中学生数学建模挑战赛【秋季赛】报名', '第四届国际数学建模挑战赛（IMMC 2018）中华区赛季开始报名啦！', '07_03_2018_immc.jpg', 'https://mp.weixin.qq.com/s?__biz=MzA3MzI1NzkxNQ==&mid=2653269430&idx=1&sn=51cb597dd1e9afd716472231deec4a7a'],
    ['活动 | Blazing Fantasy歌赛晋级名单及舞赛初赛预告', '还记得上周精彩的BF歌赛的初赛么？相信现在各位选手们也一定十分期待晋级消息的到来吧', '07_03_2018_bf_pre.png', 'https://mp.weixin.qq.com/s?__biz=MjM5MTYyMjUyNg==&mid=2650495640&idx=1&sn=a579f96b961fcb2cff007a3164be5417'],
    ['竞选 | 2017-18届学生会换届结果', '2017-18届学生会换届结果', '07_03_2018_stuunion.png', 'https://mp.weixin.qq.com/s?__biz=MjM5MTYyMjUyNg==&mid=2650495411&idx=1&sn=f4cdb944ab860c62f20681e031c0463a'],
    ['活动 | ICC师生篮球赛回顾', '炎阳似火，抵不住对篮球的热爱。一年一度的师生篮球赛，是所有喜爱篮球同学最绚丽的舞台。', '07_03_2018_lanqiu.png', 'https://mp.weixin.qq.com/s?__biz=MjM5MTYyMjUyNg==&mid=2650495325&idx=1&sn=875bd3e860a5d368d576536e5156da96'],
    ['ICC*| 精彩瞬间回顾 第一弹', 'ICC Star 精彩瞬间回顾', '07_03_2018_iccstarrrrr.png', 'https://mp.weixin.qq.com/s?__biz=MjM5MTYyMjUyNg==&mid=2650495274&idx=1&sn=0862e85f78c928f8654e7fe4ce791b75'],
    ['ICC*| 精彩瞬间回顾 第二弹', 'ICC Star 精彩瞬间回顾', '07_03_2018_iccstarrrrr.png', 'https://mp.weixin.qq.com/s?__biz=MjM5MTYyMjUyNg==&mid=2650495302&idx=1&sn=23931038bf2961cdf5fa8ff07371d8fb'],
    ['ICC*| 精彩瞬间回顾 第三弹', 'ICC Star 精彩瞬间回顾', '07_03_2018_iccstarrrrr.png', 'https://mp.weixin.qq.com/s?__biz=MjM5MTYyMjUyNg==&mid=2650495325&idx=2&sn=d8fb90eb418e20e89b691981e4759528'],

]
'''

    'academics': {
        'chinese curricula': {'img': 'img/square/6.jpg'},
        'Cambridge A Level Program': {'img': 'img/square/7.jpg'},
        'The Advanced Placement Program': {'img': 'img/square/8.jpg'},
        'International Baccalaureate': {'img': 'img/square/9.jpg'},
    },
    'student': {
        'campus life': {'img': 'img/square/10.jpg'},
        'extra-curricular activity': {'img': 'img/square/11.jpg'},
    },
    'resources': {
        'contacts': {'img': 'img/square/12.jpg'},
        'school calendar': {'img': 'img/square/13.jpg'},
        'campus map': {'img': 'img/square/5.jpg'},
        'location': {'img': 'img/square/8.jpg'},
        'for media': {'img': 'img/square/2.jpg'},
    },
    '''

# load plugins
# HWA_recognizer = HWARecognizer()


@babel.localeselector
def get_locale():
    return session['lang'] if 'lang' in session else request.accept_languages.best_match(LANGUAGES.keys())


@app.route('/api/change_lang')
def language():
    if request.args.get('lang') in LANGUAGES:
        session['lang'] = request.args.get('lang')
    if request.args.get('redirect'):
        return redirect(request.args.get('redirect'))
    return redirect(url_for('home'))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/<page>.html')
def general_register(page):
    if page == 'news':
        return render_template('first_level/%s.html' % page, INDEX=page, DATA=news_feed)
    if page == 'matriculation':
        import csv
        data_list = []
        for i in range(2010, 2019):
            with open('./matriculation/%s.csv' % i, newline='', encoding='utf-8') as csvfile:
                data_list.append(list(csv.reader(csvfile, delimiter=',')))
        return render_template('first_level/%s.html' % page, INDEX=page, DATA=data_list)
    return render_template('first_level/%s.html' % page, INDEX=page)


@app.route('/<branch>/<page>.html')
def secondary_register(branch, page):
    return render_template('second_level/%s.html' % page, PAGE=page, BRANCH=branch)


@app.route('/author.html')
def author():
    return render_template('author.html')


@app.route('/stem/nai', methods=['GET', 'POST'])
def plugins_ai():
    if request.method == 'POST':
        img = base64.b64decode(request.form.get('img')[22:])
        with open('temp.jpg', 'wb') as f:
            f.write(img)
        img = plt.imread('temp.jpg')
        res_arr = HWA_recognizer.recognize(img)
        return jsonify({'pred': res_arr})
    return render_template('draw.html')


@app.route('/pictures')
def pictures():
    return render_template('pictures.html', PICS=list(os.walk('./app/static/pics'))[0][-1])


@app.route('/pictures', methods=['POST'])
def picture_upload():
    f = request.files['file']
    path = './app/static/pics/'+secure_filename(f.filename)
    f.save(path)
    return redirect(url_for('pictures'))

