from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flash messages

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Contact Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        print(f"New Contact Message:\nName: {name}\nEmail: {email}\nMessage: {message}")
        flash('Thank you for your message! I will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Projects Page
@app.route('/projects')
def projects():
    return render_template('projects.html')

# UP Yatra Project Page
@app.route("/up-yatra")
def up_yatra():
    return render_template(
        "project.html",
        github_link="https://github.com/Akhil2279/HISTORICAL_TOUR_AND_TRAVEL"
    )

if __name__ == '__main__':
    app.run(debug=True)
