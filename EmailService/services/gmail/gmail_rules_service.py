from ...util import GmailSession 
from ..service_interfaces import RulesService
from ...models import Rule
import logging
from googleapiclient.errors import HttpError


class GmailRulesService(RulesService):
    def __init__(self, session: GmailSession):
        self.service = session.gmail_service

    def map_conditions(self, conditions: dict):
        gmail_criteria = {}
        if "sender" in conditions:
            gmail_criteria['from'] = conditions["sender"]
        if "subjectContains" in conditions:
            gmail_criteria['subject'] = conditions["subjectContains"]
        if "bodyContains" in conditions:
            gmail_criteria['query'] = f'"{conditions["bodyContains"]}"'
        return gmail_criteria

    def map_actions(self, actions: dict):
        gmail_actions = {}
        if "delete" in actions and actions["delete"]:
            gmail_actions['removeLabelIds'] = ['INBOX', 'TRASH']
        if "moveToFolder" in actions:
            gmail_actions['addLabelIds'] = [actions["moveToFolder"]]  
        if "setImportance" in actions:
            if actions["setImportance"].lower() == 'high':
                gmail_actions['addLabelIds'] = ['IMPORTANT']
        return gmail_actions

    def get_rules(self) -> list[Rule]:
        try:
            response = self.service.users().settings().filters().list(userId='me').execute()
            gmail_filters = response.get('filter', [])
            rules = []
            for f in gmail_filters:
                print(f)
                rule = Rule(
                    name=f['id'], 
                    conditions=f['criteria'],
                    actions=f['action'],
                    id=f['id']
                )
                rules.append(rule)
            print("Gmail rules: ", rules)
            return rules
        except HttpError as error:
            logging.error(f'An error occurred: {error}')
            return []

    def add_rule(self, rule: Rule) -> Rule:
        filter_body = {
            'criteria': self.map_conditions(rule.conditions),
            'action': self.map_actions(rule.actions)
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