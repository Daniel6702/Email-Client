from typing import List
from EmailService.models import Email

class SpamFilter():
    def is_spam(self,email: Email, trusted_senders: List[str], untrusted_senders: List[str]) -> bool:
        suspicious_subjects = ["win", "free", "offer", "urgent", "limited"]
        if email.from_email in untrusted_senders:
            return True
        if any(word in email.subject.lower() for word in suspicious_subjects):
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