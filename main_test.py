import unittest
from datetime import datetime
import email_util
import client_controller
from time import sleep

class SendRecieveEmailTest(unittest.TestCase):
    client = None  

    def setUp(self):
        self.client = SendRecieveEmailTest.client

    def test_email_received(self):
        email_sent = email_util.get_test_email(self.client.client_type)
        client.send_email(email_sent)
        print("Email sent!")
        
        sleep(5)
        
        email_received = self.client.get_emails(number_of_mails=1)[0]
        print("Email received!")

        # Check if email received is the same as email sent
        self.assertEqual(email_received.from_email, email_sent.from_email)
        self.assertEqual(email_received.to_email, email_sent.to_email[0])
        self.assertEqual(email_received.subject, email_sent.subject)
        self.assertTrue(email_util.visually_similar(email_received.body, email_util.text_to_html(email_sent.body)))

        datetime1 = datetime.strptime(email_received.datetime_info['date'] + ' ' + email_received.datetime_info['time'], '%Y-%m-%d %H:%M:%S.%f')
        datetime2 = datetime.strptime(email_sent.datetime_info['date'] + ' ' + email_sent.datetime_info['time'], '%Y-%m-%d %H:%M:%S.%f')
        self.assertTrue(abs((datetime1 - datetime2).total_seconds()) < 120)

        self.assertEqual(str(email_received.attachments[0].get('file_name')), 'Notes.txt')

def suite_setup(client):
    SendRecieveEmailTest.client = client
    suite = unittest.TestLoader().loadTestsFromTestCase(SendRecieveEmailTest)
    return suite

if __name__ == '__main__':
    client = client_controller.ClientController("outlook")  #google or outlook
    client.login()
    
    #while client.logged_in == False:
    #    sleep(1)

    test_suite = suite_setup(client)
    runner = unittest.TextTestRunner()
    runner.run(test_suite)