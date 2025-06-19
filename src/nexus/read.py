"""
Gmail API Read Helper

This module provides helper classes to read and process messages using the Gmail API.
"""
import json
from dateutil import parser

from src import INBOX_LABEL, UNREAD_LABEL, USER_ID
from src.connection import GmailAPIConnection

class GamilAPIReadHelper:
    """Helper class for extracting and formatting Gmail message contents."""

    def _serialize_message_headers(self, message_headers):
        """
        Extract and serialize key headers from a Gmail message.
        """
        payload = {}
        for header in message_headers:
            name = header.get('name')
            value = header.get('value')

            if name == 'Subject':
                payload['subject'] = value
            elif name == 'Date':
                payload['date'] = parser.parse(value).isoformat()
            elif name == 'From':
                payload['from'] = value

            if all(k in payload for k in ['from', 'subject', 'date']):
                break
        return payload
    
    def _get_message_headers(self, message):
        """
        Retrieve message headers from a Gmail message object.
        """
        return message.get('headers', [])
    
    def _get_message_payload(self, message):
        """Retrieve the payload section from a Gmail message."""
        return message.get('payload', {})
    
    def _get_message_body(self, message_payload):
        """Retrieve the base64-encoded body content from a message payload."""
        try:
            parts = message_payload.get('parts', [])
            if parts and 'body' in parts[0] and 'data' in parts[0]['body']:
                return parts[0]['body']['data']
            elif 'body'in message_payload['body']['data']
        except (AttributeError, TypeError):
            pass
        return ''