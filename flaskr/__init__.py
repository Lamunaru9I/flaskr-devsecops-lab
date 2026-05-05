import os
from flask import Flask, request, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
    
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    @app.route('/')
    def index():
        name = request.args.get('name', 'Guest')
        return render_template('index.html', name=name)
    
    @app.route('/admin')
    def admin():
        auth_token = request.headers.get('Authorization')
        expected_token = os.environ.get('ADMIN_TOKEN')
        
        if not auth_token or auth_token != f'Bearer {expected_token}':
            return 'Unauthorized', 401
        
        return 'Admin panel - Secure!'

    app.config['SECRET_KEY'] = 'test-hardcoded-secret'
    @app.route('/test-eval')
    def test_eval():
        return str(eval(request.args.get('q', '1+1')))
    return app