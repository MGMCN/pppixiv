from app import App
from flask import send_from_directory

app = App(__name__)


# Only to see if this server is running correctly
@app.route('/')
def lsp():
    return 'Hello World! lsp!'


@app.route('/Illusts/<path:path>')
def send_illusts(path):
    return send_from_directory('Illusts', path)


if __name__ == '__main__':
    app.logger.debug("=====================================================================================")
    app.logger.debug("Authorized on pixiv account %s. Please wait for authentication.", app.username)
    success, msg = app.run_services()
    if success:
        app.logger.debug("Pixiv Login Complete.")
        app.logger.debug("=====================================================================================")
        app.run(host='0.0.0.0', port=5000)
    else:
        app.logger.debug(msg)
        app.logger.debug("Application ends gracefully.")
        app.logger.debug("=====================================================================================")
