from flask import Flask,request,render_template # import the Flask class for creating a web application/server.

print("Inside app.py")  

app = Flask(__name__)   # Creating the flask application object (server) by assigning the name app.

@app.route('/')         # when someone visit http://127.0.0.1:5000/
def index():
  tasks = [
    "Learn Flask",
    "Learn SQL",
    "Learn FastAPI"
  ]          
  return render_template("index.html", name = "Akhil", age = 22, profession="AI Generalist", tasks=tasks)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/user/<name>')
def callUser(name):
  return "Hello " + name

@app.route('/op/<ops>/<int:n>')
def getResult(ops, n):
  return performOps(ops, n)

def performOps(ops, n):
  ops = ops.lower()
  if ops == "square":
    return str(n**2)
  elif ops == "cube":
    return str(n**3)
  elif ops == "half":
    return str(n/2)

@app.route('/greet')
def greet():
  name = request.args["name"]
  return "Hello " + name

if __name__ == "__main__":  # If this file is executed directly, start the Flask development server, 
  print("Starting server")
  app.run(debug=True)        # debug=True enables automatic reload and detailed error messages.
