from flask import Flask, render_template, request
import MySQLdb as db

app = Flask(__name__)

dbconfig = {"host" : "nikaa131.mysql.pythonanywhere-services.com",
            "user" : "nikaa131",
            "password" : "Password",
            "database" : "nikaa131$newdb"}



@app.route('/myip', methods = ['POST'])
def greeting():
    global user_name, ip_addr
    user_name = request.form['user_name']
    ip_addr = request.headers['X-Real-IP']
    results = f"Hello {user_name}! Your IP is {ip_addr}."
    persons_request(user_name, ip_addr)
    return render_template('myip.html', results = results)


@app.route('/')
def entry_page():
  return render_template('index.html')



def persons_request(user_name, ip_addr):
    connection =db.connect(**dbconfig)
    cursor = connection.cursor()
    _SQL = """INSERT INTO persons
                (fName, ip)
                VALUES
                (%s, %s)"""
    cursor.execute(_SQL,(user_name,ip_addr))
    connection.commit()
    cursor.close()
    connection.close()


@app.route('/viewlog')
def view_log():
    titles = ["id", "Date", "Name", "ip"]
    connection =db.connect(**dbconfig)
    cursor = connection.cursor()

    _SQL = "SELECT * FROM persons"
    cursor.execute(_SQL)
    contents = cursor.fetchall()

    cursor.close()
    connection.close()


    return render_template('viewlog.html', the_data=contents, the_row_titles = titles)

if __name__ == '__main__':
  app.run(debug = True)
