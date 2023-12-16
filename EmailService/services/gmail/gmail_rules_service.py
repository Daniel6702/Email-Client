from ...util import GmailSession 
from ..service_interfaces import RulesService
from ...models import Rule
import logging
from googleapiclient.errors import HttpError
import json

class GmailRulesService(RulesService):
    def __init__(self, session: GmailSession):
        self.service = session.gmail_service

    def get_rules(self) -> list[Rule]:
        results = self.service.users().settings().filters().list(userId='me').execute()
        filters = results.get('filter', [])

        rules = []
        for f in filters:
            rule = Rule(
                name="Gmail Rule",  
                conditions=str(json.dumps(f['criteria'])),
                actions=str(json.dumps(f['action'])),
                id=f['id'],
                sequence=1, 
                is_enabled=True 
            )
            rules.append(rule)
        return rules

    def add_rule(self, rule: Rule) -> Rule:
        filter = {
            'criteria': json.loads(rule.conditions),
            'action': json.loads(rule.actions)
        }

        created_filter = self.service.users().settings().filters().create(
            userId='me', body=filter).execute()

        rule.id = created_filter['id']
        return rule

    def remove_rule(self, rule: Rule):
        self.service.users().settings().filters().delete(
            userId='me', id=rule.id).execute()