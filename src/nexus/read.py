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
            elif 'body'in message_payload['body'] and ['data'] in message_payload['body']:
                # Fallback if message doesn't have 'parts i.e palian text emails
                return message_payload['body']['data']
        except (AttributeError, TypeError):
            pass
        return ''
    
class GmailAPIReaderWrapper(GamilAPIReadHelper):
    """Wrapper class for reading messages from the Gmail API."""

    def __init__(self):
        """Initialize Gmail API connection and load available labels."""
        self.gmail_api = GmailAPIConnection().gmail_api_connect()
        self.available_labels = self.get_labels()

    def list_messages(self, labels=None, sender=None):
        """
        Retrieve messages filtered by label(s) and optional sender.
        """
        if labels is None:
            labels = [INBOX_LABEL]

        if not isinstance(labels, (list, tuple)):
            raise TypeError("`labels` must be a list or tuple")
        
        missing_lables = set(labels) - set(self.available_labels)
        if missing_lables:
            raise  ValueError(
                f"Invalid labels provided: {', '.join(missing_lables)}. "
                f"Available labels: {', '.join(self.available_labels)}" 
            )
        
        query = f"from:{sender}" if sender else None

        response = self.gmail_api.users().messages().list(
            userId=USER_ID,
            labelIds=labels,
            q=query
        ).execute()

        return response.get('messages', [])
    
    def get_message(self, msg_id):
        """Retrieve a specific message by its ID."""
        return self.gmail_api.users().messages().get(
            userId=USER_ID,
            id=msg_id
        ).execute()
    
    def get_unread_messages(self, sender=None):
        """Retrieve all unread messages, optionally by sender."""
        return self.list_messages(labels=[UNREAD_LABEL], sender=sender)
    
    def check_new_mail(self, sender=None):
        """Check and extract details of all new (unread) emails."""
        processed_messages = []

        unread_messages = self.get_unread_messages(sender=sender)

        for message_meta in unread_messages:
            msg_id = message_meta['id']
            message = self.get_message[msg_id]

            payload = self._get_message_payload(message)
            headers = self._get_message_headers(payload)
            serialized = self._serialize_message_headers(headers)
            serialized['base64_msg_body'] = self._get_message_body(payload)

            processed_messages.append(serialized)
    
        return processed_messages

    def get_labels(self):
        """Retrieve a vailable Gmail labels for the current user."""
        response = self.gmail_api.users().labels().list(userId=USER_ID).execute()
        return [label['name'] for label in response.get('labels', [])]
    
    def get_total_messages(self):
        """Retrieve the total message and thread count for the user."""
        profile = self.gmail_api.users().getProfile(userId=USER_ID).execute()
        stats = {
            'Total Messages': profile.get('messagesTotal', 0),
            'Total Threads': profile.get('threadsTotal', 0),
            'Email Address': profile.get('emailAddress', USER_ID)
        }

        return json.dumps(stats, indent=4)
