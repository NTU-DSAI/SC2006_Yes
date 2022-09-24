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

# -------------  LOCATION PAGE  -------------

@app.route('/location/using_address', methods = ['POST'])
def update_using_address():

   # lat, long = pull from backend
   address='NTU'
   lat, long = 1.34463493822005, 103.680705586564
   return render_template("locationselectedpage.html", lat = lat, long = long, zoom = 15, address=address)

@app.route('/location/using_gps')
def update_using_gps():

   # lat, long = pull from gps
   lat, long = 1.2966, 103.7764
   return render_template("locationselectedpage.html", lat = lat, long = long, zoom = 15, address='')

@app.route('/location')
def location():
   return render_template("locationpage.html", lat = 1.3521, long = 103.8198, zoom = 12)



@app.route('/login')
def login():
   return render_template("loginpage.html")

@app.route('/recommend')
def recommend():
   return render_template("recommendpage.html")

@app.route('/route')
def route():
   return render_template("routepage.html")

# -------------  SELECTION PAGE  -------------

@app.route('/selection')
def selection():

   # update to pull from backend
   ICTEquipment = ['Printer', "Laptop", "Mobile phone", "Router", "Tablet"]
   BlubsNLamps = ["Blub", "Long LED tube"]
   Batteries = ['A' * i for i in range(2, 5)]

   return render_template(
      "selectionpage.html", 
      ICTEquipment_name = ICTEquipment, 
      BlubsNLamps_name = BlubsNLamps, 
      Batteries_name = Batteries)

@app.route('/selection', methods = ['POST'])
def selection_screen_submit():
   if request.method == 'POST':
      print('POST')
      
   return redirect(url_for('location'))

@app.route('/suggestion')
def suggestion():
   return render_template("suggestionpage.html")

@app.route('/suggestion/completed')
def suggestion_completed():
   return render_template('suggestion_completed.html')
   
if __name__ == "__main__":
  app.run(debug = True)
