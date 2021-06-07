from app import create_app, socketio

app = create_app()

if __name__ == "__main__":
    # app.run()  #! use app.run() when deploying to heroku
    socketio.run(app, debug=True)