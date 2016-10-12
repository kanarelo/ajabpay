from flask import Flask

from .config import (
    get_default_config, setup_database, setup_auth, cross_origin,
    setup_cors, setup_session, setup_logging, setup_current_user)

app = Flask(__name__)
app.config.from_object(get_default_config())

setup_session(app)

(sentry, client) = setup_logging(app)
(db, bcrypt) = setup_database(app)
login_manager = setup_auth(app)
cors = setup_cors(app)

app.before_request(setup_current_user(client))