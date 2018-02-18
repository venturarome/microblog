from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Comment

# NOTE to run all the tests, just write: 'python tests.py'

class UserModelCase(unittest.TestCase):
    # Will be called before each unit test.
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    # Will be called after each unit test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='ester')
        u.set_password('bebe')
        self.assertFalse(u.check_password('pwned'))
        self.assertTrue(u.check_password('bebe'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        # Create users. At the beginning, zero followed users:
        u1 = User(username='ester', email='ester@mail.com')
        u2 = User(username='ventu', email='ventu@mail.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u2.followed.all(), [])
        # u1 follows u2:
        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'ventu')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'ester')
        # u1 unfollows u2:
        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_comments(self):
        # Create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])
        # Create four comments
        now = datetime.utcnow()
        p1 = Comment(body="comment from john", author=u1, timestamp=now + timedelta(seconds=1))
        p2 = Comment(body="comment from susan", author=u2, timestamp=now + timedelta(seconds=4))
        p3 = Comment(body="comment from mary", author=u3, timestamp=now + timedelta(seconds=3))
        p4 = Comment(body="comment from david", author=u4, timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()
        # Setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()
        # Check the followed posts of each user
        f1 = u1.followed_comments().all()
        f2 = u2.followed_comments().all()
        f3 = u3.followed_comments().all()
        f4 = u4.followed_comments().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == '__main__':
    unittest.main(verbosity=2)

