from ...util import GmailSession 
from ..service_interfaces import RulesService
from ...models import Rule
import logging
from googleapiclient.errors import HttpError

class GmailRulesService:
    def __init__(self, session):
        self.service = session.gmail_service

    def get_rules(self) -> list[Rule]:
        try:
            response = self.service.users().settings().filters().list(userId='me').execute()
            gmail_filters = response.get('filter', [])
            rules = []
            for f in gmail_filters:
                rule = Rule(
                    name=f['id'], 
                    conditions=f['criteria'],
                    actions=f['action'],
                    id=f['id']
                )
                rules.append(rule)
            return rules
        except HttpError as error:
            logging.error(f'An error occurred: {error}')
            return []

    def add_rule(self, rule: Rule) -> Rule:
        filter_body = {
            'criteria': rule.conditions,
            'action': rule.actions
        }
        try:
            created_filter = self.service.users().settings().filters().create(userId='me', body=filter_body).execute()
            rule.id = created_filter['id']
            return rule
        except HttpError as error:
            logging.error(f'An error occurred: {error}')
            return None

    def remove_rule(self, rule: Rule):
        try:
            self.service.users().settings().filters().delete(userId='me', id=rule.id).execute()
        except HttpError as error:
            logging.error(f'An error occurred: {error}')
