from app import app_factory


if __name__ == "__main__":
    app = app_factory()
    app.run(app.config['HOST'], debug=app.config['DEBUG'])
