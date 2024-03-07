from app.config import Config
from app.app import App

app = App(__name__)

if __name__ == '__main__':
    config_loader = Config()
    config_loader.load_dotenv()
    config = config_loader.get_config()
    app.init(config)
    app.logger.debug("=====================================================================================")
    app.logger.debug(f"Authorized on pixiv account {config['username']}. Please wait for authentication.")
    success, msg = app.run_services()
    if success:
        app.logger.debug("Pixiv Login Complete.")
        app.logger.debug("=====================================================================================")
        app.run(host='0.0.0.0', port=config['port'])
    else:
        app.logger.debug(msg)
        app.logger.debug("Application ends gracefully.")
        app.logger.debug("=====================================================================================")
