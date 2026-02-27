from flask import Flask, render_template, session, redirect, url_for
from flask_mysqldb import MySQL
from flask_session import Session
from config import Config
from datetime import timedelta

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure permanent session lifetime
    app.permanent_session_lifetime = timedelta(days=30)
    
    mysql.init_app(app)
    Session(app)
    
    # Root route
    @app.route('/')
    def index():
        if session.get('user_id'):
            return redirect(url_for('dashboard.kid'))
        return render_template('auth/welcome.html')
    
    # Test navigation route
    @app.route('/test')
    def test_nav():
        return render_template('test_navigation.html')
    
    from routes.auth import auth_bp
    from routes.detection import detection_bp
    from routes.learning import learning_bp
    from routes.performance import performance_bp
    from routes.dashboard import dashboard_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(detection_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(performance_bp)
    app.register_blueprint(dashboard_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
