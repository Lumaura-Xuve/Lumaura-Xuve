from flask import Flask

def register_xuvecode(app: Flask):
    """
    Register the XuveCode module with the Flask application.
    
    Args:
        app: The Flask application
    """
    from xuvecode.models.project import db
    from xuvecode.api.routes import xuvecode_bp
    
    # Register blueprints
    app.register_blueprint(xuvecode_bp)
    
    # Initialize models with the app
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
