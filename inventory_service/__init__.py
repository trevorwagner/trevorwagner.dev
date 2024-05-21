from pathlib import Path

from sqlalchemy import create_engine

from inventory_service.models import *

DIST = Path(__file__).parent.resolve() / "../_dist"
DIST.mkdir(exist_ok=True)

engine = create_engine("sqlite:///{}".format(DIST / "site_inventory.db"))


def init_db():
    Base.metadata.create_all(engine)
