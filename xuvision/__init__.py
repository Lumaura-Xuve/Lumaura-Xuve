from flask import Flask

def register_xuvision(app: Flask):
    """
    Register the XUVISION module with the Flask application.
    
    Args:
        app: The Flask application
    """
    from xuvision.models.video import db
    from xuvision.api.routes import xuvision_bp
    
    # Configure upload folder
    app.config.setdefault('UPLOAD_FOLDER', 'uploads/videos')
    
    # Register blueprints
    app.register_blueprint(xuvision_bp)
    
    # Initialize models with the app
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
