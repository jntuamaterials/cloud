from flask import Flask,render_template,request,redirect,flash,session,url_for
import psycopg2
import pandas as pd
import string
import random
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
app=Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'
mydb = psycopg2.connect(
        host="dpg-cgi69aak728gl5vbr07g-a",
        database="cyber_security",
        user='admin',
        password='Ipjv161S2sXKvJmkinvymGTiVz08tsNM',port='5432')
cursor = mydb.cursor()


def random_string(letter_count, digit_count):
    str1 = ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))
    str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))

    sam_list = list(str1)  # it converts the string to list.
    random.shuffle(sam_list)  # It uses a random.shuffle() function to shuffle the string.
    final_string = ''.join(sam_list)
    return final_string

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dp")
def dp():
    return render_template("dp.html")

@app.route('/dpback',methods = ["POST"])
def dpback():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        pwd=request.form['pwd']
        cpwd=request.form['cpwd']
        pno=request.form['pno']
        addr=request.form['addr']

        sql = "select * from dp"
        result = pd.read_sql_query(sql, mydb)
        email1 = result['email'].values
        print(email1)
        if email in email1:
            flash("email already existed","warning")
            return render_template('dp.html', msg="email existed")
        if (pwd == cpwd):
            sql = "INSERT INTO dp (name,email,pwd,addr,pno) VALUES (%s,%s,%s,%s,%s)"
            val = (name, email, pwd, addr, pno)
            cursor.execute(sql, val)
            mydb.commit()
            flash("Successfully Registered", "warning")
            return render_template('dp.html')
        else:
            flash("Password and Confirm Password not same")
        return render_template('dp.html')

    return render_template('dp.html')

@app.route("/dplog")
def dplog():
    a=random_string(7, 3)
    return render_template("dplog.html",a=a)

@app.route('/dplogback',methods=['POST', 'GET'])
def dplogback():
    if request.method == "POST":

        email = request.form['email']
        capt = request.form['capt']
        c1 = request.form['capt1']
        password1 = request.form['pwd']

        sql = "select * from dp where email='%s' and pwd='%s' " % (email, password1)
        print('q')
        x = cursor.execute(sql)
        print(x)
        results = cursor.fetchall()
        print(results)
        global name
        name = results[0][1]
        print(name)
        session['fname'] = results[0][1]
        session['email'] = email
        if(capt==c1):
            if len(results) > 0:
                print('r')
                flash("Welcome to website", "primary")
                return render_template('dphome.html', m="Login Success", msg=results[0][1])

            else:
                flash("Login failed", "warning")
                return render_template('dplog.html', msg="Login Failure!!!")
        else:
            flash("Captcha value mismatches please try again", "danger")
            return render_template('dplog.html', msg="invalid value")

    return render_template('dp.html')

@app.route("/tf")
def tf():
    return render_template("tf.html")

@app.route('/tfback',methods=['POST','GET'])
def tfback():
    print("gekjhiuth")
    if request.method=='POST':
        name=request.form['name']
        remail=request.form['remail']
        fname=request.form['fname']
        faddr=request.form['faddr']
        taddr=request.form['taddr']
        file=request.form['file']

        dd="text_files/"+file
        print(dd)
        f = open(dd, "r")
        data = f.read()

        now = datetime.now()
        # currentDay = datetime.now().strftime('%d/%m/%Y')
        status = 'Request'
        datalen = int(len(data) / 2)
        print(datalen, len(data))
        g = 0
        a = ''
        b = ''
        c = ''
        for i in range(0, 2):
            if i == 0:
                a = data[g: datalen:1]
                # a=a.decode('utf-8')

        print(g)
        print(len(data))
        c = data[datalen: len(data):1]
        # c = c.decode('utf-8')
        print(c)

        currentDay = datetime.now().strftime('%Y-%m-%d')
        t1 = datetime.now().strftime('%H:%M:%S')

        email = session.get('email')
        sql = "INSERT INTO transfer_files (name,email,fname,remail,faddr,taddr,d1,block1,block2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        val = (name, email, fname, remail, faddr, taddr, now, a, c)
        cursor.execute(sql, val)
        mydb.commit()
        # flash("file uploaded successfully", "success")

        sql = "select * from transfer_files where d1='%s' " % (now)
        x = pd.read_sql_query(sql, mydb)
        print("^^^^^^^^^^^^^")
        print(type(x))
        print(x)
        # x = x.drop(['demail'], axis=1)
        x = x.drop(['name'], axis=1)
        # x = x.drop(['fname'], axis=1)
        x = x.drop(['email'], axis=1)
        x = x.drop(['remail'], axis=1)
        x = x.drop(['hash1'], axis=1)
        x = x.drop(['hash2'], axis=1)
        x = x.drop(['faddr'], axis=1)
        x = x.drop(['taddr'], axis=1)
        x = x.drop(['d1'], axis=1)
        x = x.drop(['status'], axis=1)
        return render_template('tfback.html',row_val=x.values.tolist())
    flash("file not puloaded", "danger")
    return render_template('tf.html')
@app.route('/tfback1/<s>/<s1>/<s2>')
def tfback1(s=0,s1='',s2=''):
    result1 = hashlib.sha1(s1.encode())
    hash1 = result1.hexdigest()
    result2 = hashlib.sha1(s2.encode())
    hash2 = result2.hexdigest()
    # val=AES_ENCRYPT
    sql="update transfer_files set block1=AES_ENCRYPT('%s','keys'),block2=AES_ENCRYPT('%s','keys'),hash1='%s',hash2='%s' where id='%s'" %(s1,s2,hash1,hash2,s)
    cursor.execute(sql)
    mydb.commit()
    flash("Data stored","success")
    return redirect(url_for('tf'))
@app.route("/vfs")
def vfs():
    email=session.get('email')
    sql = "select * from transfer_files where email='%s' "%(email)
    x = pd.read_sql_query(sql, mydb)
    x = x.drop(['id'], axis=1)
    x = x.drop(['name'], axis=1)
    x = x.drop(['email'], axis=1)
    x = x.drop(['faddr'], axis=1)
    x = x.drop(['block1'], axis=1)
    x = x.drop(['block2'], axis=1)

    return render_template("vfs.html", cal_name=x.columns.values, row_val=x.values.tolist())

@app.route("/cs")
def cs():
    return render_template("cs.html")


@app.route('/csback',methods=['POST', 'GET'])
def csback():
    print("aaaaaaaaaaaaaaa")
    if request.method == 'POST':
        print("aaaaaaaaaaaaaaa")
        username = request.form['uname']
        password1 = request.form['pwd']
        if username == 'cloud' and password1 == 'cloud' :
            flash("Welcome to website cloud", "primary")
            return render_template('cshome.html')
        else:
            print("&&&&&&&&&&&&")
            flash("Invalid Credentials Please Try Again","warning")
            return render_template('cs.html')

    return render_template('cs.html')

@app.route("/vtf")
def vtf():
    sql = "select * from transfer_files where status='waiting' "
    x = pd.read_sql_query(sql, mydb)
    x = x.drop(['block1'], axis=1)
    x = x.drop(['block2'], axis=1)
    x = x.drop(['id'], axis=1)
    x = x.drop(['status'], axis=1)
    x = x.drop(['hash1'], axis=1)
    x = x.drop(['hash2'], axis=1)

    return render_template("vtf.html", cal_name=x.columns.values, row_val=x.values.tolist())

@app.route("/sf")
def sf():
    sql = "select * from transfer_files where status='waiting' "
    x = pd.read_sql_query(sql, mydb)
    x = x.drop(['block2'], axis=1)
    x = x.drop(['block1'], axis=1)
    x = x.drop(['status'], axis=1)
    x = x.drop(['name'], axis=1)
    x = x.drop(['faddr'], axis=1)
    x = x.drop(['email'], axis=1)
    x = x.drop(['d1'], axis=1)
    return render_template("sf.html", cal_name=x.columns.values, row_val=x.values.tolist())

@app.route('/sfsend/<s>')
def sfsend(s=0):
    sql="update transfer_files set status='Transfered' where id='%s'" %(s)
    cursor.execute(sql,mydb)
    mydb.commit()
    flash("File sent to AV","success")
    return redirect(url_for('sf'))

@app.route("/st")
def st():
    sql = "select * from transfer_files where status!='waiting' "
    x = pd.read_sql_query(sql, mydb)
    x = x.drop(['block1'], axis=1)
    x = x.drop(['block2'], axis=1)
    # x = x.drop(['file'], axis=1)
    x = x.drop(['name'], axis=1)
    x = x.drop(['faddr'], axis=1)
    x = x.drop(['email'], axis=1)
    x = x.drop(['d1'], axis=1)
    return render_template("st.html", cal_name=x.columns.values, row_val=x.values.tolist())

@app.route("/av")
def av():
    return render_template("av.html")


@app.route('/avback',methods=['POST', 'GET'])
def avback():
    if request.method == 'POST':
        username = request.form['uname']
        password1 = request.form['pwd']
        if username == 'av' and password1 == 'av' :
            flash("Welcome to website AV", "primary")
            return render_template('avhome.html')
        else:
            flash("Invalid Credentials Please Try Again","warning")
            return render_template('av.html')

    return render_template('av.html')

@app.route("/ft")
def ft():
    sql = "select * from transfer_files where status='Transfered' "
    x = pd.read_sql_query(sql, mydb)
    x = x.drop(['block1'], axis=1)
    x = x.drop(['block2'], axis=1)
    x = x.drop(['name'], axis=1)
    x = x.drop(['faddr'], axis=1)
    x = x.drop(['status'], axis=1)
    x = x.drop(['email'], axis=1)
    x = x.drop(['d1'], axis=1)
    return render_template("ft.html", cal_name=x.columns.values, row_val=x.values.tolist())


@app.route('/transfer/<s>/<s1>/<s2>/<s3>/<s4>')
def transfer(s=0,s1='',s2='',s3='',s4=''):
    msg = 'Thanks for choosing Online file transfer'
    otp = "Your file is successfully transfered and it can be delivered from:"
    m1 = 'This are the keys for decrypting the file'
    t='Regards,'
    t1='AV.'
    mail_content = msg + '\n' + otp+m1+'Key-1 values is '+s3+'and key-2 value is '+s4+'.'+'\n'+'\n'+t+'\n'+t1
    sender_address = 'chakralalokesh01@gmail.com'
    sender_pass = 'smuwferiuustrvge'
    receiver_address = s2
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Cyber Security for Cloud-based Transportation Systems'

    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    sql="update transfer_files set status='Completed' where id='%s'" %(s)
    cursor.execute(sql,mydb)
    mydb.commit()
    flash("File transefered","success")
    return redirect(url_for('ft'))


@app.route("/dr")
def dr():
    return render_template("dr.html")

@app.route('/drback',methods = ["POST"])
def drback():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        pwd=request.form['pwd']
        cpwd=request.form['cpwd']
        pno=request.form['pno']
        addr=request.form['addr']

        sql = "select * from dp"
        result = pd.read_sql_query(sql, mydb)
        email1 = result['email'].values
        print(email1)
        if email in email1:
            flash("email already existed","warning")
            return render_template('dp.html', msg="email existed")
        if (pwd == cpwd):
            sql = "INSERT INTO dp (name,email,pwd,addr,pno) VALUES (%s,%s,%s,%s,%s)"
            val = (name, email, pwd, addr, pno)
            cursor.execute(sql, val)
            mydb.commit()
            flash("Successfully Registered", "warning")
            return render_template('dr.html')
        else:
            flash("Password and Confirm Password not same")
        return render_template('dr.html')

    return render_template('dr.html')


@app.route("/drlog")
def drlog():
    a=random_string(7, 3)
    return render_template("drlog.html",a=a)

@app.route('/drlogback',methods=['POST', 'GET'])
def drlogback():
    if request.method == "POST":

        email = request.form['email']
        capt = request.form['capt']
        c1 = request.form['capt1']
        password1 = request.form['pwd']

        sql = "select * from dp where email='%s' and pwd='%s' " % (email, password1)
        print('q')
        x = cursor.execute(sql)
        print(x)
        results = cursor.fetchall()
        print(results)
        global name
        name = results[0][1]
        print(name)
        session['fname'] = results[0][1]
        session['email'] = email
        if(capt==c1):
            if len(results) > 0:
                print('r')
                flash("Welcome to website", "primary")
                return render_template('drhome.html', m="Login Success", msg=results[0][1])

            else:
                flash("Login failed", "warning")
                return render_template('drlog.html', msg="Login Failure!!!")
        else:
            flash("Captcha value mismatches please try again", "danger")
            return render_template('drlog.html', msg="invalid value")

    return render_template('dr.html')

@app.route("/rtf")
def rtf():
    return render_template("rtf.html")

@app.route('/rtfback',methods=['POST','GET'])
def rtfback():
    print("gekjhiuth")
    if request.method == 'POST':
        name = request.form['name']
        remail = request.form['remail']
        fname = request.form['fname']
        faddr = request.form['faddr']
        taddr = request.form['taddr']
        file = request.form['file']

        dd = "text_files/" + file
        print(dd)
        f = open(dd, "r")
        data = f.read()

        now = datetime.now()
        # currentDay = datetime.now().strftime('%d/%m/%Y')
        status = 'Request'
        datalen = int(len(data) / 2)
        print(datalen, len(data))
        g = 0
        a = ''
        b = ''
        c = ''
        for i in range(0, 2):
            if i == 0:
                a = data[g: datalen:1]
                # a=a.decode('utf-8')

        print(g)
        print(len(data))
        c = data[datalen: len(data):1]
        # c = c.decode('utf-8')
        print(c)

        currentDay = datetime.now().strftime('%Y-%m-%d')
        t1 = datetime.now().strftime('%H:%M:%S')

        email = session.get('email')
        sql = "INSERT INTO transfer_files (name,email,fname,remail,faddr,taddr,d1,block1,block2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        val = (name, email, fname, remail, faddr, taddr, now, a, c)
        cursor.execute(sql, val)
        mydb.commit()
        # flash("file uploaded successfully", "success")

        sql = "select * from transfer_files where d1='%s' " % (now)
        x = pd.read_sql_query(sql, mydb)
        print("^^^^^^^^^^^^^")
        print(type(x))
        print(x)
        # x = x.drop(['demail'], axis=1)
        x = x.drop(['name'], axis=1)
        x = x.drop(['email'], axis=1)
        x = x.drop(['remail'], axis=1)
        x = x.drop(['hash1'], axis=1)
        x = x.drop(['hash2'], axis=1)
        x = x.drop(['faddr'], axis=1)
        x = x.drop(['taddr'], axis=1)
        x = x.drop(['d1'], axis=1)
        x = x.drop(['status'], axis=1)
        return render_template('tfback.html', row_val=x.values.tolist())
    flash("file not puloaded", "danger")
    return render_template('rtf.html')


@app.route("/rvfs")
def rvfs():
    email=session.get('email')
    sql = "select * from transfer_files where email='%s' "%(email)
    x = pd.read_sql_query(sql, mydb)
    x = x.drop(['name'], axis=1)
    x = x.drop(['email'], axis=1)
    x = x.drop(['faddr'], axis=1)
    x = x.drop(['prkey'], axis=1)
    x = x.drop(['file'], axis=1)

    return render_template("rvfs.html", cal_name=x.columns.values, row_val=x.values.tolist())

@app.route("/rf")
def rf():
    email=session.get('email')
    print(email)
    sql = "select * from transfer_files where remail='%s' and status='Completed' "%(email)
    x = pd.read_sql_query(sql, mydb)
    x = x.drop(['remail'], axis=1)
    x = x.drop(['taddr'], axis=1)
    x = x.drop(['block1'], axis=1)
    x = x.drop(['block2'], axis=1)
    x = x.drop(['hash1'], axis=1)
    x = x.drop(['hash2'], axis=1)
    x = x.drop(['status'], axis=1)

    return render_template("rf.html", cal_name=x.columns.values, row_val=x.values.tolist())

@app.route("/down/<s>")
def down(s=0):
    global g
    g=s
    return render_template("down.html",g=g)

@app.route("/downfile",methods=['POST','GET'])
def downfile():
    print("dfhlksokhso")
    if request.method == 'POST':
        print("gekjhiuth")
        gkey = request.form['p1']
        gkey1 = request.form['p2']
        fid = request.form['id']

        sql = "select count(*),CONCAT(aes_decrypt(block1,'keys'),aes_decrypt(block2,'keys'),'') from transfer_files where id='"+fid+"' and hash1='"+gkey+"' and hash2='"+gkey1+"'"
        x = pd.read_sql_query(sql, mydb)
        count=x.values[0][0]
        print(count)
        asss=x.values[0][1]
        asss=asss.decode('utf-8')
        if count==0:
            flash("Invalid key please try again","danger")
            return render_template('down.html')
        if count==1:
            return render_template("downfile.html", msg=asss)

    return render_template("down.html")



if __name__=='__main__':
    app.run(debug=True)
