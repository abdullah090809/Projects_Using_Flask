from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']="abdullah1234"
    app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:abdullah1234@localhost/todolist'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from app.models import User, Task
        db.create_all()

    from app.routes.auth import auth_bp
    from app.routes.tasks import task_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    return app