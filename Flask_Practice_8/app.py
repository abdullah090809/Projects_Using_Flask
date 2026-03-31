from flask import Flask, render_template, request, redirect, url_for, flash
from form import RegistrationForm

app=Flask(__name__)
app.secret_key="12345678"

@app.route("/", methods=["POST","GET"])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        name=form.name.data
        email=form.email.data
        password=form.password.data
        flash(f"Welcome {name}! You Registered Successfully")
        return redirect(url_for("success"))
    return render_template("register.html",form=form)

@app.route("/success")
def success():
    return render_template("success.html")