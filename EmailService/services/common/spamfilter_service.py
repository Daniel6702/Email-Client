from typing import List
from EmailService.models import Email
import pandas as pd
import re

class SpamFilter():
    def __init__(self):
        # Naive Bayes spam filter guide by: https://www.kdnuggets.com/2020/07/spam-filter-python-naive-bayes-scratch.html
        # Read the data
        sms_spam = pd.read_csv('AI_SpamFilter\\SMSSpamCollection', sep='\t',
        header=None, names=['Label', 'SMS'])

        # Randomize the dataset
        data_randomized = sms_spam.sample(frac=1, random_state=1)

        # Calculate index for split
        training_test_index = round(len(data_randomized) * 0.8)

        # Split into training and test sets
        training_set = data_randomized[:training_test_index].reset_index(drop=True)
        test_set = data_randomized[training_test_index:].reset_index(drop=True)

        #------------------------
        # Data Cleaning
        training_set['SMS'] = training_set['SMS'].str.replace( '\W', ' ') # Removes punctuation
        training_set['SMS'] = training_set['SMS'].str.lower() # Lowercases all words

        #------------------------
        # Create the vocabulary
        training_set['SMS'] = training_set['SMS'].str.split()

        vocabulary = []
        for sms in training_set['SMS']:
            for word in sms:
                vocabulary.append(word)

        vocabulary = list(set(vocabulary))

        #------------------------
        # The Final Training Set
        word_counts_per_sms = {unique_word: [0] * len(training_set['SMS']) for unique_word in vocabulary}

        for index, sms in enumerate(training_set['SMS']):
            for word in sms:
                word_counts_per_sms[word][index] += 1

        word_counts = pd.DataFrame(word_counts_per_sms)

        training_set_clean = pd.concat([training_set, word_counts], axis=1)

        #------------------------
        # Calculating Constants First

        # Isolating spam and ham messages first
        spam_messages = training_set_clean[training_set_clean['Label'] == 'spam']
        ham_messages = training_set_clean[training_set_clean['Label'] == 'ham']

        # P(Spam) and P(Ham)
        self.p_spam = len(spam_messages) / len(training_set_clean)
        self.p_ham = len(ham_messages) / len(training_set_clean)

        # N_Spam
        n_words_per_spam_message = spam_messages['SMS'].apply(len)
        n_spam = n_words_per_spam_message.sum()

        # N_Ham
        n_words_per_ham_message = ham_messages['SMS'].apply(len)
        n_ham = n_words_per_ham_message.sum()

        # N_Vocabulary
        n_vocabulary = len(vocabulary)

        # Laplace smoothing
        alpha = 1

        #------------------------
        # Calculating Parameters

        # Initiate parameters
        self.parameters_spam = {unique_word:0 for unique_word in vocabulary}
        self.parameters_ham = {unique_word:0 for unique_word in vocabulary}

        # Calculate parameters
        for word in vocabulary:
            n_word_given_spam = spam_messages[word].sum() # spam_messages already defined
            p_word_given_spam = (n_word_given_spam + alpha) / (n_spam + alpha*n_vocabulary)
            self.parameters_spam[word] = p_word_given_spam

            n_word_given_ham = ham_messages[word].sum() # ham_messages already defined
            p_word_given_ham = (n_word_given_ham + alpha) / (n_ham + alpha*n_vocabulary)
            self.parameters_ham[word] = p_word_given_ham

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