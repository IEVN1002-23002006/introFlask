from blueprints.alumnos.routes import alumnos_bp
from blueprints.maestros.routes import maestros_bp

def register_blueprint(app):
    app.register_blueprint(alumnos_bp)
    app.register_blueprint(maestros_bp)