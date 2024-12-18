from owlready2 import *
from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

# Step 1: Create a new ontology
ontology = get_ontology("its-system.owl").load()


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

    name = request.cookies.get('fullName')
    email = request.cookies.get('email')

    triangle_instance = ontology.Triangle("triangleFormula")
    rectangle_instance = ontology.Rectangle("rectangleFormula")
    square_instance = ontology.Square("squareFormula")
    circle_instance = ontology.Circle("circleFormula")
    
    return render_template('index.html', name=name, email=email, triangle_area=triangle_instance.area[0], rectangle_area=rectangle_instance.area[0], square_area=square_instance.area[0], circle_area=circle_instance.area[0])


questions = []
correct_answers = {}
for quiz in ontology.Quiz.instances():
    question_text = quiz.question[0] if quiz.question else "No question text available"
    answer_text = quiz.answer[0] if quiz.answer else "No answer available"
    questions.append(question_text)
    correct_answers[question_text] = answer_text 

@app.route('/quiz')
def quiz():
    return render_template('quiz.html', questions=questions)

@app.route('/result', methods=['POST'])
def result():
    score = 0
    total_questions = len(questions)

    # Check each question's answer
    for question in questions:
        user_answer = request.form.get(question)  # Get the user's answer
        correct_answer = correct_answers.get(question)  # Get the correct answer

        if user_answer == correct_answer:
            score += 1  # Increment score for correct answer

    return render_template('result.html', score=score, total=total_questions)




if __name__ == '__main__':
    app.run(debug=True)