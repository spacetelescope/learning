from unittest import TestCase

from stsci.learning.corpus import get_messages, get_users, get_channels


class CorpusTestCase(TestCase):
    def setUp(self):
        self.messages = list(get_messages(20))
        self.users = list(get_users(12))
        self.users_by_id = {user['id']: user for user in self.users}
        self.channels = list(get_channels(1, True))

    def test_len(self):
        self.assertEqual(len(self.messages), 20)
        self.assertEqual(len(self.users), 12)
        self.assertEqual(len(self.channels), 1)

    def test_channels(self):
        channel = self.channels[0]
        self.assertEqual(channel['id'], 'C8WSCQ000')
        self.assertEqual(channel['name'], 'example')
        self.assertEqual(channel['created_at'], 1516736123)
        self.assertSetEqual(set(channel['users']), set(self.users_by_id))

    def test_users(self):
        for user in self.users:
            self.assertEqual(user['real_name'], 'Pat Developer')
            self.assertEqual(user['first_name'], 'Pat')
            self.assertEqual(user['last_name'], 'Developer')
            self.assertIn('dev', user['display_name'])
            self.assertIn('dev', user['email'])
            self.assertIn('@example.edu', user['email'])
            if user['id'].startswith('U'):
                self.assertEqual(len(user['id']), 11)
            if user['id'].startswith('U'):
                self.assertEqual(len(user['id']), 11)

    def test_messages(self):
        for message in self.messages:
            self.assertSetEqual(set(message), {'channel', 'id', 'user', 'text', 'ts', 'reactions'})
            self.assertIn(message['user']['id'], self.users_by_id)
            self.assertEqual(message['channel'], 'example')
            self.assertIn(len(message['reactions']), (0, 1))
            self.assertIn(message['ts'].year, (2019, 2021))
