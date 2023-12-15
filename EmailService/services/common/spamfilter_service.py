from typing import List
from EmailService.models import Email
import json
import re

class SpamFilter():
    def __init__(self):
        # Import relevant variables from file
        with open('AI_SpamFilter\\info.json', 'r') as file:
            info = json.load(file)

        self.p_spam = info[0]
        self.p_ham = info[1]
        self.parameters_spam = info[2]
        self.parameters_ham = info[3]

    #------------------------
    # Classifying function
    def classify(self, message):
        message = re.sub('\W', ' ', message)
        message = message.lower().split()

        p_spam_given_message = self.p_spam
        p_ham_given_message = self.p_ham

        for word in message:
            if word in self.parameters_spam:
                p_spam_given_message *= self.parameters_spam[word]

            if word in self.parameters_ham: 
                p_ham_given_message *= self.parameters_ham[word]

        if p_ham_given_message >= p_spam_given_message:
            return 'ham'
        elif p_ham_given_message < p_spam_given_message:
            return 'spam'


    def is_spam(self,email: Email, trusted_senders: List[str], untrusted_senders: List[str]) -> bool:
        if email.from_email in untrusted_senders:
            return True

        if self.classify(email.subject) == 'spam':
            if email.from_email not in trusted_senders:
                return True
        return False

    def filter_emails(self,emails: List[Email], trusted_senders: List[str], untrusted_senders: List[str]) -> (List[Email], List[Email]):
        accepted_emails = []
        spam_emails = []

        for email in emails:
            if self.is_spam(email, trusted_senders, untrusted_senders):
                spam_emails.append(email)
            else:
                accepted_emails.append(email)

        return accepted_emails, spam_emails