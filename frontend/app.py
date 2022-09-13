from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
   return render_template("landingpage.html")

@app.route('/admin')
def admin():
   return render_template("adminpage.html")

@app.route('/information')
def information():
   return render_template("informationpage.html")

@app.route('/landing')
def landing():
   return render_template("landingpage.html")

@app.route('/location')
def location():
   return render_template("locationpage.html")

@app.route('/login')
def login():
   return render_template("loginpage.html")

@app.route('/recommend')
def recommend():
   return render_template("recommendpage.html")

@app.route('/route')
def route():
   return render_template("routepage.html")

@app.route('/selection')
def selection():
   return render_template("selectionpage.html")

@app.route('/suggestion')
def suggestion():
   return render_template("suggestionpage.html")
  
if __name__ == "__main__":
  app.run(debug = True)
