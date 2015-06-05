import os

import pypicloud
from paste.deploy import loadapp
from pypicloud.cache.sql import SQLCache as SC
from pypicloud.access.sql import SQLAccessBackend as SAB

database = {"username": os.environ['RDS_USERNAME'],
            "password": os.environ['RDS_PASSWORD'],
            "hostname": os.environ['RDS_HOSTNAME'],
            "port": os.environ['RDS_PORT'],
            "db_name": os.environ['RDS_DB_NAME'],
            }

db_url = 'postgres://{username}:{password}@{hostname}:{port}/{db_name}'.format(
    **database)


if not os.path.exists(os.path.join('static', pypicloud.__version__)):
    try:
        os.mkdir('static')
    except OSError:
        pass
    os.symlink(os.path.join(os.path.dirname(pypicloud.__file__), 'static'),
               os.path.join('static', pypicloud.__version__))


class SQLCache(SC):
    @classmethod
    def configure(cls, settings):
        settings['db.url'] = db_url
        return super(SQLCache, cls).configure(settings)


class SQLAccessBackend(SAB):
    @classmethod
    def configure(cls, settings):
        settings['auth.db.url'] = db_url
        return super(SQLAccessBackend, cls).configure(settings)


if not hasattr(pypicloud, 'o_includeme'):
    pypicloud.o_includeme = pypicloud.includeme

    def myincludeme(config):
        config.include('pyramid_hsts')
        settings = config.get_settings()
        settings.setdefault('session.encrypt_key', os.environ['ENCRYPT_KEY'])
        settings.setdefault('session.validate_key', os.environ['VALIDATE_KEY'])
        settings.setdefault('storage.bucket', os.environ['BUCKET_NAME'])
        pypicloud.o_includeme(config)

    pypicloud.includeme = myincludeme


application = loadapp('config:config.ini', relative_to='.')
