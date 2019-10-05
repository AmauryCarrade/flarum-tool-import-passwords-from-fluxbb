import json
import os

import bcrypt
import MySQLdb

from dotenv import load_dotenv

load_dotenv()

FLUXBB_HOST = os.environ.get("FLUXBB_HOST", "localhost")
FLUXBB_USER = os.environ.get("FLUXBB_USER", "root")
FLUXBB_PASS = os.environ.get("FLUXBB_PASS", "")
FLUXBB_BASE = os.environ.get("FLUXBB_BASE", "fluxbb")
FLUXBB_PREFIX = os.environ.get("FLUXBB_PREFIX", "fluxbb_")

FLARUM_HOST = os.environ.get("FLARUM_HOST", "localhost")
FLARUM_USER = os.environ.get("FLARUM_USER", "root")
FLARUM_PASS = os.environ.get("FLARUM_PASS", "")
FLARUM_BASE = os.environ.get("FLARUM_BASE", "flarum")
FLARUM_PREFIX = os.environ.get("FLARUM_PREFIX", "")

flarum_db = MySQLdb.connect(
    host=FLARUM_HOST, user=FLARUM_USER, passwd=FLARUM_PASS, db=FLARUM_BASE
)
fluxbb_db = MySQLdb.connect(
    host=FLUXBB_HOST, user=FLUXBB_USER, passwd=FLUXBB_PASS, db=FLUXBB_BASE
)

fluxbb_cur = fluxbb_db.cursor()
flarum_cur = flarum_db.cursor()

fluxbb_cur.execute(f"SELECT id, password FROM {FLUXBB_PREFIX}users")

print("Processing passwords", end="", flush=True)

counter = 0

for row in fluxbb_cur:
    flarum_cur.execute(
        f"UPDATE {FLARUM_PREFIX}users SET migratetoflarum_old_password = %s WHERE id = %s",
        (
            json.dumps(
                {
                    "type": "sha1-bcrypt",
                    "password": bcrypt.hashpw(
                        str(row[1]).encode("utf-8"), bcrypt.gensalt()
                    ).decode("utf-8"),
                }
            ),
            row[0],
        ),
    )

    counter += 1
    print(".", end="", flush=True)

    if counter % 100 == 0:
        print(counter, end="", flush=True)
        flarum_db.commit()

flarum_db.commit()
print("\nDone.")

fluxbb_cur.close()
flarum_cur.close()

fluxbb_db.close()
flarum_db.close()
