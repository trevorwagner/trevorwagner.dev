from pathlib import Path

from sqlalchemy import create_engine

from site_data_service.models import *

DIST = Path(__file__).parent.resolve() / '../_dist'

engine = create_engine('sqlite:///{}/site_data.db'.format(str(DIST)))
conn = engine.connect()


def init_db():
  Base.metadata.create_all(engine)
