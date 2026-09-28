from flask import Flask
from models import db
from prices import price_summary

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///candy.db'
db.init_app(app)

@app.route('/')
def home():
    return "Hello, candy lover!\n🍬🍫🍫\nSomething sweet coming soon!"
if __name__ == '__main__': 
    print("Starting server...")
    app.run(debug=True)
