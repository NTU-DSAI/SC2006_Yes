from flask import Flask, render_template, request, redirect, url_for

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

   ICTEquipment = ['Printer', "Laptop", "Mobile phone", "Router", "Tablet"]
   BlubsNLamps = ["Blub", "Long LED tube"]
   Batteries = ['A' * i for i in range(2, 5)]

   return render_template(
      "selectionpage.html", 
      ICTEquipment_name = ICTEquipment, 
      BlubsNLamps_name = BlubsNLamps, 
      Batteries_name = Batteries)

@app.route('/suggestion')
def suggestion():
   return render_template("suggestionpage.html")
  
@app.route('/selection', methods = ['POST'])
def selection_screen_submit():
   if request.method == 'POST':
      print('POST')
   else:
      print('GET')
   return redirect(url_for('location'))

if __name__ == "__main__":
  app.run(debug = True)
