from app import App

app = App(__name__)


# Only to see if this server is running correctly
@app.route('/')
def lsp():
    return 'Hello World! lsp!'


if __name__ == '__main__':
    app.logger.debug("Authorized on pixiv account %s. Please wait for authentication.", app.username)
    success = app.myPixiv.start_pixiv_session()
    if success:
        app.logger.debug("Pixiv Login Complete.")
        app.logger.debug("=================================================================")
        app.run(host='0.0.0.0', port=5000)
