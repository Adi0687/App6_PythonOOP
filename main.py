from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request
import objects

# __name__ contains a string of the current python file,
# nothing but a variable
# We are instantiating the Flask Class
app = Flask(__name__)


class HomePage(MethodView):
    def get(self):
        return render_template('index.html')

class CaloriesFormPage(MethodView):
    def get(self):
        caloriesform = CaloriesForm()
        return render_template('calories_form_page.html', caloriesform=caloriesform)

    def post(self):
        calories_form = CaloriesForm(request.form)

        temp = objects.Temperature(country=calories_form.country.data, city=calories_form.city.data).get()

        cals = objects.Calories(weight=float(calories_form.weight.data), height=float(calories_form.height.data),
                                age=float(calories_form.age.data), temperature=temp)

        calories = cals.calculate()
        return render_template('calories_form_page.html',
                               caloriesform=calories_form,
                               result=True,
                               calories=calories)



class CaloriesForm(Form):
    weight = StringField(label="Weight: ", default=70)
    height = StringField(label="Height: ", default=176)
    age = StringField("Age: ", default=32)

    city = StringField("City: ", default="Jeddah")
    country = StringField("Country: ", default="Saudi Arabia")

    button = SubmitField("Calculate")
# Connects the app to the url
# .as_view is method of MethodView that is inherited by our own Homepage Class
app.add_url_rule('/', view_func=HomePage.as_view('home_page'))
app.add_url_rule('/calories_form', view_func=CaloriesFormPage.as_view('calories_form_page'))
# app.add_url_rule('/results', view_func=ResultsPage.as_view('results_page'))

app.run(debug=True)
