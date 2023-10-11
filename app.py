from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# everytime u run flask, you need to instatiate Flask
RESPONSES_KEY = "responses"
app = Flask(__name__)
app.config['SECRET_KEY'] = "mooncakes"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


#survey=survey: This part is passing a variable called survey to the template. It's assigning the value of the Python variable survey (which was imported earlier in the code) to the template variable also named survey. This allows you to access the survey variable within the HTML template.
@app.route('/')
def home_survey_start():
    """Shows start page"""
    return render_template("home_survey_start.html", survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session responses"""
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def handle_question():
    """Append answers to response list and redirect to next question"""

    # get response choice
    choice = request.form['answer']

    # add response choice to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # All questions have been answered. Thank them.
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")



@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question."""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != qid):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)


    @app.route("/complete")
    def complete():
        """Survey Complete. Show completetion page"""

        return render_template("completion.html")
