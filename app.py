from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

# Home Page
@app.route('/')
def index():
    news_list = News.query.all()
    return render_template('index.html', news=news_list)

# Admin Page
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_news = News(title=title, content=content)
        db.session.add(new_news)
        db.session.commit()
        return redirect(url_for('index'))  # Redirect to the homepage after adding news
    return render_template('admin.html')  # Render admin page for GET requests

# Print links in terminal on app start
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure database and tables are created
    print("Audience Page: http://127.0.0.1:5000/")
    print("Admin Page: http://127.0.0.1:5000/admin")
    app.run(debug=True)