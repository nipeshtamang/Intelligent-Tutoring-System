from owlready2 import *
from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

# Step 1: Create a new ontology
ontology = get_ontology("its-system.owl").load()


# Step 4: Create an instance of User
# user1 = ontology.User("ram.sam")
# user1.fullName.append("Ram Sam")
# user1.email.append("Ram@sam.com")
# user1.password.append("123")
# ontology.save("its-system.owl") 


@app.route('/')
def index():
    # Get cookies
    user_name = request.cookies.get('fullName')
    if user_name:
        return redirect(url_for('dashboard'))
    return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        user = ontology.User(name)
        user.fullName.append(name)
        user.email.append(email)
        user.password.append(password)
        ontology.save('its-system.owl')
        
        # Save user information in cookies
        resp = make_response(redirect(url_for('dashboard')))
        resp.set_cookie('fullName', name)
        resp.set_cookie('email', email)
        
        
        return resp
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Get user information from cookies

    name = request.cookies.get('fullName')
    email = request.cookies.get('email')

    triangle_instance = ontology.triangleFormula
    area = triangle_instance.area if hasattr(triangle_instance, 'area') else "N/A"

    rectangle_instance = ontology.rectangleFormula
    area1 = rectangle_instance.area if hasattr(rectangle_instance, 'area') else "N/A"

    square_instance = ontology.squareFormula
    area2 = square_instance.area if hasattr(square_instance, 'area') else "N/A"

    circle_instance = ontology.circleFormula
    area3 = circle_instance.area if hasattr(circle_instance, 'area') else "N/A"

    
    
    return render_template('index.html', name=name, email=email, triangle_area=area, rectangle_area=area1, square_area=area2, circle_area=area3)

if __name__ == '__main__':
    app.run(debug=True)