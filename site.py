from flask import *
import psycopg2
from random import shuffle

app = Flask(__name__)

@app.route('/results', methods=['GET','POST'])
def results():
	user_entry = request.form["blogname"]
	#apparently input will be sanitized by psycopg2? http://modpython.org/pipermail/mod_python/2004-December/016984.html
	conn_string = "host='localhost' dbname='cs585' user='cs585' "
	db_conn = psycopg2.connect(conn_string)
	cursor = db_conn.cursor()
	cursor.execute("SELECT blog_name FROM colors WHERE blog_name = '{0}';".format(user_entry))
	#check to see if blog isn't in the color DB, if so return page with error message
	result = cursor.fetchone()
	if result is None:
		return render_template("results.html", blog = user_entry, found = False)

	cursor.execute("SELECT * FROM colors WHERE blog_name = '{0}';".format(user_entry))
	user_blog = cursor.fetchone()
	cursor.execute("SELECT * FROM colors WHERE color1 LIKE '{0}' OR color2 LIKE '{1}' OR color3 LIKE '{2}';".format(user_blog[1],user_blog[2],user_blog[3]))
	results = cursor.fetchall()
	#instead of doing actual smart ranking, just shuffle the results
	shuffle(results)
	return render_template("results.html", blog = user_entry, found = True, target = user_blog, results = results)

@app.route('/')
def home():
	return render_template("home.html")

if __name__ == '__main__':
	app.run(debug=True, port=8080, host='0.0.0.0')