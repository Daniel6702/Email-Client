from ...util import OutlookSession 
from ..service_interfaces import RulesService
from ...models import Rule
import requests
import logging

class OutlookRulesService(RulesService):
    def __init__(self, session: OutlookSession):
        self.result = session.result
        self.base_url = 'https://graph.microsoft.com/v1.0'

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.result['access_token']}",
            'Content-Type': 'application/json'
        }

    def map_conditions(self, conditions: dict):
        outlook_conditions = {}
        if "sender" in conditions:
            outlook_conditions['senderContains'] = [conditions["sender"]]
        if "subjectContains" in conditions:
            outlook_conditions['subjectContains'] = [conditions["subjectContains"]]
        if "bodyContains" in conditions:
            outlook_conditions['bodyContains'] = [conditions["bodyContains"]]
        return outlook_conditions

    def map_actions(self, actions: dict):
        outlook_actions = {}
        if "delete" in actions and actions["delete"]:
            outlook_actions['delete'] = True
        if "moveToFolder" in actions:
            outlook_actions['moveToFolder'] = actions["moveToFolder"]
        if "setImportance" in actions:
            outlook_actions['markImportance'] = actions["setImportance"].capitalize()
        return outlook_actions

    def get_rules(self) -> list[Rule]:
        url = f'{self.base_url}/me/mailFolders/inbox/messageRules'
        response = requests.get(url, headers=self.get_headers())
        if response.status_code == 200:
            outlook_rules = response.json().get('value', [])
            rules = [Rule(name=rule['displayName'],
                          conditions=self.map_conditions(rule.get('conditions', {})),
                          actions=self.map_actions(rule.get('actions', {})),
                          id=rule['id']) for rule in outlook_rules]
            return rules
        else:
            logging.error(f'An error occurred: {response.text}')
            return []

    def add_rule(self, rule: Rule) -> Rule:
        url = f'{self.base_url}/me/mailFolders/inbox/messageRules'
        rule_payload = {
            'displayName': rule.name,
            'conditions': self.map_conditions(rule.conditions),
            'actions': self.map_actions(rule.actions)
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