from helpers import print
from app import app, db
from app.models import AccountModel, GoogleAccountModel, UserModel
import config
import os


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'UserModel': UserModel, 'AccountModel': AccountModel, 'GoogleAccountModel': GoogleAccountModel}


if __name__ == '__main__':
    if not os.path.exists(os.path.join(config.basedir, 'app.db')):
        print("Creating the database...")
        db.create_all()

    app.run(host='0.0.0.0', port=80, debug=True, threaded=False)
