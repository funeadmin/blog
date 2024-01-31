"""
Populate twitter database with fake data using the SQLAlchemy ORM.
"""

import random
import string
import hashlib
import secrets
from faker import Faker
from shout.src.models import User, Shout, likes_table, db
from shout.src import create_app

USER_COUNT = 50
SHOUT_COUNT = 100
LIKE_COUNT = 400

assert LIKE_COUNT <= (USER_COUNT * SHOUT_COUNT)


def random_passhash():
    """Get hashed and salted password of length N | 8 <= N <= 15"""
    raw = ''.join(
        random.choices(
            string.ascii_letters + string.digits + '!@#$%&',  # valid pw characters
            k=random.randint(8, 15)  # length of pw
        )
    )

    salt = secrets.token_hex(16)

    return hashlib.sha512((raw + salt).encode('utf-8')).hexdigest()


def truncate_tables():
    """Delete all rows from database tables"""
    db.session.execute(likes_table.delete())
    Shout.query.delete()
    User.query.delete()
    db.session.commit()


def main():
    """Main driver function"""
    app = create_app()
    app.app_context().push()
    truncate_tables()
    fake = Faker()

    last_user = None  # save last user
    for _ in range(USER_COUNT):
        last_user = User(
            username=fake.unique.first_name().lower() + str(random.randint(1, 150)),
            password=random_passhash()
        )
        db.session.add(last_user)

    # insert users
    db.session.commit()

    last_shout = None  # save last shout
    for _ in range(SHOUT_COUNT):
        last_shout = Shout(
            content=fake.sentence(),
            user_id=random.randint(last_user.id - USER_COUNT + 1, last_user.id)
        )
        db.session.add(last_shout)

    # insert tweets - shouts
    db.session.commit()

    user_shout_pairs = set()
    while len(user_shout_pairs) < LIKE_COUNT:

        candidate = (
            random.randint(last_user.id - USER_COUNT + 1, last_user.id),
            random.randint(last_shout.id - SHOUT_COUNT + 1, last_shout.id)
        )

        if candidate in user_shout_pairs:
            continue  # pairs must be unique

        user_shout_pairs.add(candidate)

    new_likes = [{"user_id": pair[0], "shout_id": pair[1]}
                 for pair in list(user_shout_pairs)]
    insert_likes_query = likes_table.insert().values(new_likes)
    db.session.execute(insert_likes_query)

    # insert likes
    db.session.commit()


# run script
main()
