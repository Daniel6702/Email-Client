from ...util import OutlookSession 
from ..service_interfaces import RulesService
from ...models import Rule
import requests
import logging
import json

class OutlookRulesService(RulesService):
    def __init__(self, session: OutlookSession):
        self.result = session.result
        self.base_url = 'https://graph.microsoft.com/v1.0'

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.result['access_token']}",
            'Content-Type': 'application/json'
        }

    def get_rules(self) -> list[Rule]:
        url = f'{self.base_url}/me/mailFolders/inbox/messageRules'
        response = requests.get(url, headers=self.get_headers())
        if response.status_code == 200:
            outlook_rules = response.json().get('value', [])
            rules = [
                Rule(
                    name=rule['displayName'],
                    conditions=str(json.dumps(rule.get('conditions', {}))),
                    actions=str(json.dumps(rule.get('actions', {}))),
                    id=rule['id'],
                    sequence=1, 
                    is_enabled=True
                ) for rule in outlook_rules
            ]
            return rules
        else:
            logging.error(f'An error occurred: {response.text}')
            return []
        
    
    def add_rule(self, rule: Rule) -> Rule:
        url = f'{self.base_url}/me/mailFolders/inbox/messageRules'
        try:
            conditions_obj = json.loads(rule.conditions)
            actions_obj = json.loads(rule.actions)
        except json.JSONDecodeError as e:
            logging.error(f"JSON parsing error: {e}")
            return None

        rule_payload = {
            'displayName': rule.name,
            'sequence': rule.sequence,
            'isEnabled': rule.is_enabled,
            'conditions': conditions_obj,
            'actions': actions_obj
        }

        response = requests.post(url, headers=self.get_headers(), json=rule_payload)
        if response.status_code == 201:
            created_rule = response.json()
            rule.id = created_rule['id']
            return rule
        else:
            logging.error(f'An error occurred: {response.text}')
            return None

    def remove_rule(self, rule: Rule):
        url = f'{self.base_url}/me/mailFolders/inbox/messageRules/{rule.id}'
        response = requests.delete(url, headers=self.get_headers())
        if response.status_code != 204:
            logging.error(f'An error occurred: {response.text}')
