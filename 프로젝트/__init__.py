
from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

connect = psycopg2.connect("dbname=church user=postgres password=choi0924") #각자의 데이터 베이스에 맞게 바꾸기
cur = connect.cursor()


@app.route('/')
def opening():
    return render_template("opening.html")


@app.route('/join') #회원 가입하는 템플릿
def join():
    return render_template('join.html')

@app.route('/join_ing', methods=['POST']) #회원 가입하는 과정
def joining():
    ID = request.form['ID']
    password = request.form['pw']
    name = request.form['name']
    church = request.form['church']
    officer = request.form['officer']
    age = request.form['age']
    cur.execute("INSERT INTO person VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', {5});".format(ID, password, name, church, officer, age))
    connect.commit()
    return redirect('/')



@app.route('/login') #로그인 화면 실행
def login():
    return render_template('login.html')



@app.route('/register', methods=['POST']) #로그인 하는 과정
def register():
    ID = request.form['ID']
    password = request.form['pw']
    cur.execute("SELECT * FROM person WHERE ID = '{0}' and password = '{1}' ;".format(ID, password))
    result = cur.fetchall()
    if not result:
        return redirect('/')  #비밀 번호가 틀리면 처음으로 돌아가게 됨
    else:
        return redirect(url_for('yourpage', name=result[0][0])) # 비밀 번호가 맞으면 들어가게 됨



@app.route("/yourpage/<name>") #본인 페이지로 들어가기
def yourpage(name):
    cur.execute("SELECT * FROM person WHERE ID = '{0}' ;".format(name))
    name_ch = cur.fetchall()
    cur.execute("SELECT * FROM belonging_church as B, person as P WHERE B.belonging=P.belonging and P.ID = '{0}' ;".format(name_ch[0][0]))
    church = cur.fetchall() # 교회 소개
    cur.execute("SELECT COUNT(*) FROM person WHERE belonging = '{0}' and age between 20 and 30 ;".format(name_ch[0][3]))
    population = cur.fetchall() # 청년부 명수
    cur.execute("SELECT COUNT(*) FROM person WHERE belonging = '{0}' ;".format(name_ch[0][3]))
    all_print = cur.fetchall()
    return render_template('yourpage.html', you=name_ch, church=church, population=population, all=all_print)





@app.route('/resign', methods=['POST']) #탈퇴하는 과정
def resign():
    ID = request.form['ID']
    cur.execute("delete FROM person WHERE ID = '{0}';".format(ID))
    connect.commit()
    return redirect('/')

@app.route('/checking', methods=['POST'])
def checking():
    ID = request.form['ID']
    return render_template('checking.html', ID = ID)

@app.route('/post', methods=['POST']) #영성생활 보고를 보내는 과정
def post():
    ID = request.form['ID']
    now_date = request.form['date']
    cur.execute("SELECT * FROM takes WHERE ID = '{0}' and date= '{1}';".format(ID, now_date))
    take = cur.fetchall()
    if take:
        return redirect(url_for('update', ID = ID, date=now_date))
    else:
        return redirect(url_for('update_process', ID = ID, date=now_date))

@app.route('/update/<ID>,<date>')
def update(ID, date):
    cur.execute("SELECT * FROM person WHERE ID = '{0}';".format(ID))
    person = cur.fetchall()
    cur.execute("SELECT * FROM takes WHERE ID = '{0}' and date = '{1}';".format(ID, date))
    take = cur.fetchall()
    return render_template('update.html', take=take, person=person)

@app.route('/update_update', methods=['POST'])
def update_update():
    ID = request.form['ID']
    date = request.form['date']
    cur.execute("SELECT * FROM takes WHERE ID = '{0}' and date = '{1}';".format(ID, date))
    fi_ne = cur.fetchall()
    cur.execute("DELETE FROM takes WHERE ID = '{0}' and date = '{1}';".format(ID, date))
    connect.commit()
    date = fi_ne[0][3]
    fine = fi_ne[0][7]
    cur.execute("UPDATE person set all_fine = all_fine - {0} WHERE ID = '{1}';".format(fine, ID))
    connect.commit()
    return redirect(url_for('update_process', ID = ID, date=date))

@app.route('/update_process/<ID>,<date>') #수정하는 방법
def update_process(ID, date):
    return render_template('update_process.html', ID = ID, date = date)

@app.route('/checking_update', methods=['POST'])
def checking_update():
    ID = request.form['ID']
    date = request.form['date']
    pray_times = int(request.form['pray_times'])
    read_pages = int(request.form['read_pages'])
    QT = request.form['QT']
    if QT == 'O':
        qt = True
    else:
        qt = False
    cur.execute("SELECT officer FROM person WHERE ID='{0}';".format(ID))
    off_icer = cur.fetchall()
    officer = off_icer[0][0]

    cur.execute("SELECT A.ID, A.officer, A.belonging, B.pray_time, B.bible_page, B.QT FROM person A inner join church_officer B ON A.officer = B.officer WHERE A.officer = '{0}';".format(officer))
    standard = cur.fetchall()

    fall = 0
    fall_str = 'ALL_CLEAR'
    penalty_now = []
    if pray_times - int(standard[0][3]) < 0 :
        fall += 1
    if read_pages - int(standard[0][4]) < 0 :
        fall += 1
    if QT == 'X':
        fall += 1
    if fall == 1:
        fall_str = 'one'
    if fall == 2:
        fall_str = 'two'
    if fall == 3:
        fall_str = 'three'
    if fall_str != 'ALL_CLEAR':
        cur.execute("SELECT {0} FROM penalty WHERE belonging = '{1}' and officer = '{2}';".format(fall_str, standard[0][2], officer))
        penalty_now = cur.fetchall()
        cur.execute("UPDATE person set all_fine = all_fine + {0} WHERE ID = '{1}';".format(penalty_now[0][0], ID))
    if not penalty_now:
        cur.execute("INSERT INTO takes VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', {7});".format(ID, standard[0][2], officer, date, pray_times, read_pages, qt, 0))
    else:
        cur.execute("INSERT INTO takes VALUES ('{0}', '{1}', '{2}', '{3}', {4}, {5}, {6}, {7});".format(ID, standard[0][2], officer, date, pray_times, read_pages, qt, penalty_now[0][0]))
    connect.commit()
    cur.execute("SELECT * FROM person WHERE ID = '{0}';".format(ID))
    result = cur.fetchall()[0][0]
    return redirect(url_for('yourpage', name=result))



@app.route('/fine', methods=['POST']) #fine을 결정하는 방법.
def fine():
    ID = request.form["ID"]
    cur.execute("SELECT * FROM person WHERE ID='{0}';".format(ID))
    standard = cur.fetchall()

    cur.execute("SELECT * FROM account WHERE belonging = '{0}';".format(standard[0][3]))
    account = cur.fetchall()

    penalty = standard[0][6]
    cur.execute("SELECT officer, max(all_fine) FROM person group by officer HAVING officer in (SELECT officer FROM person WHERE belonging = '{0}');".format(standard[0][3]))
    officer_fine = cur.fetchall()
    name = []
    for i in officer_fine: # 벌금 최대 치인 사람들을  찾
        cur.execute("SELECT officer, name FROM person WHERE officer = '{0}' and all_fine = {1} and belonging = '{2}';".format(i[0], i[1], standard[0][3]))
        tuple = cur.fetchall()
        for k in tuple: #같은 벌금의 사람이 있을 수도 있으니1
            tuple1 = list(k)
            tuple1.append(i[1])
            name.append(tuple1)

    return render_template('fine.html', penalty=penalty, names=name, ID = ID, account= account) #직분 가져오기

@app.route('/payed', methods=['POST']) #fine을 처리하고 나의 페이지로 가게 된다. 과정
def tax():
    ID = request.form["ID"]
    payed = request.form['payed_tax']
    now = request.form['now_payed']
    renew = int(now) - int(payed)
    if renew < 0:
        return render_template('back!.html')
    else:
        cur.execute("UPDATE person SET all_fine = {0} WHERE ID = '{1}';".format(renew, ID))
        connect.commit()
        cur.execute("SELECT * FROM person WHERE ID = '{0}';".format(ID))
        result = cur.fetchall()[0][0]
        return redirect(url_for('yourpage', name=result))





if __name__ == "__main__":
    app.run()
