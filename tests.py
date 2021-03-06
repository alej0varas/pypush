import unittest
import unittest.mock

import pypn


the_id = 'an:id'
second_id = 'other:id'
ids = the_id, second_id
payload = {
    'title': "Hello",
    'body': "Hello World!",  # APNs alert or alert.body, GCM body
    'apns_sound': "default",
    'apns_badge': 1,
    'apns_acme': {'aa_key': 'aa_value'},
    'gcm_data': {'gd_key': 'gn_value'},
    'gcm_notification': {'gn_key': 'gn_value'}
}


@unittest.mock.patch('pypn.apns2.APNSClient.push')
class APNsTests(unittest.TestCase):
    def test_send_single(self, mock_request):
        sin = pypn.Notification(pypn.APNS)

        sin.send(the_id, payload)

        self.assertTrue(mock_request.called)
        self.assertIn('device_token', mock_request.call_args[1])
        self.assertEqual(mock_request.call_args[1]['device_token'], the_id)
        self.assertIn('n', mock_request.call_args[1])
        self.assertIsInstance(mock_request.call_args[1]['n'], pypn.apns2.Notification)

    def test_send_multiple(self, mock_request):
        sin = pypn.Notification(pypn.APNS)

        sin.send(ids, payload)

        self.assertEqual(mock_request.call_count, 2)
        self.assertIn('device_token', mock_request.call_args_list[0][1])
        self.assertEqual(mock_request.call_args_list[0][1]['device_token'], the_id)
        self.assertIn('n', mock_request.call_args_list[0][1])
        self.assertIsInstance(mock_request.call_args_list[0][1]['n'], pypn.apns2.Notification)
        self.assertIn('device_token', mock_request.call_args_list[1][1])
        self.assertEqual(mock_request.call_args_list[1][1]['device_token'], second_id)
        self.assertIn('n', mock_request.call_args_list[1][1])
        self.assertIsInstance(mock_request.call_args_list[1][1]['n'], pypn.apns2.Notification)


class GCMTests(unittest.TestCase):
    @unittest.mock.patch('pypn.gcm.GCM.send_to_message')
    def test_send_single_notification_payload(self, mock_request):
        sin = pypn.Notification(pypn.GCM)

        sin.send(the_id, payload)

        self.assertTrue(mock_request.called)
        self.assertIn('to', mock_request.call_args[1])
        self.assertEqual(mock_request.call_args[1]['to'], the_id)
        self.assertIn('data', mock_request.call_args[1])
        self.assertIn('notification', mock_request.call_args[1])

    @unittest.mock.patch('pypn.gcm.GCM.json_request')
    def test_send_multiple_notification_payload(self, mock_request):
        sin = pypn.Notification(pypn.GCM)

        sin.send(ids, payload)

        self.assertTrue(mock_request.called)
        self.assertIn('registration_ids', mock_request.call_args[1])
        self.assertEqual(mock_request.call_args[1]['registration_ids'], ids)
        self.assertIn('data', mock_request.call_args[1])
        self.assertIn('notification', mock_request.call_args[1])

    @unittest.mock.patch('pypn.gcm.GCM.send_topic_message')
    def test_send_topic_notification_payload(self, mock_request):
        topic = 'topic'
        sin = pypn.Notification(pypn.GCM)

        sin.send(topic, payload)

        self.assertTrue(mock_request.called)
        self.assertIn('topic', mock_request.call_args[1])
        self.assertEqual(mock_request.call_args[1]['topic'], topic)
        self.assertIn('data', mock_request.call_args[1])
        self.assertIn('notification', mock_request.call_args[1])


@unittest.mock.patch('yaosac.client.create_notification')
class OneSignalTests(unittest.TestCase):
    def test_send(self, mock_request):

        sin = pypn.Notification(pypn.OS)

        sin.send(the_id, payload)

        self.assertTrue(mock_request.called)
        self.assertIn('include_player_ids', mock_request.call_args[1])
        self.assertEqual(mock_request.call_args[1]['include_player_ids'],
                         the_id)
        self.assertIn('heading', mock_request.call_args[1])
        self.assertEqual(mock_request.call_args[1]['heading'],
                         payload['title'])
        self.assertIn('contents', mock_request.call_args[1])
        self.assertEqual(mock_request.call_args[1]['contents'],
                         payload['body'])
        self.assertNotIn('data', mock_request.call_args[1])

        # Support data
        os_payload = payload.copy()
        data = {'a': 'dict'}
        os_payload['data'] = data

        sin.send(the_id, os_payload)

        self.assertIn('data', mock_request.call_args[1])
        self.assertEqual(data, mock_request.call_args[1]['data'])


class DummyProviderTests(unittest.TestCase):
    def test_send(self):
        sin = pypn.Notification(pypn.DUMMY)

        result = sin.send(ids, payload)

        self.assertEqual(result, (ids, payload))


class BadProviderTests(unittest.TestCase):
    def test_bad_provider(self):
        self.assertRaises(AttributeError, pypn.Notification, 'bad-provider')


if __name__ == '__main__':
    unittest.main()
