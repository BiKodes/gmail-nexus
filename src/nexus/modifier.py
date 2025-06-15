"""
Gmail API Modifier Helper.

This module provides functionality to mark Gmail messages as READ or UNREAD
using the Gmail API.
"""
from src.nexus import READ_LABEL, UNREAD_LABEL, USER_ID
from src.connection import GmailAPIConnection

class GmailAPIModifyWrapper:
    """A wrapper class for modifying Gmail messages via the Gmail API."""
    
    def __init__(self):
        """Initialize the Gmail API client connection."""
        self.gmail_api = GmailAPIConnection.gmail_api_connect()

    def mark_as_read(self, msg_id):
        """Mark a single email message as READ."""
        body = {
            'removeLableIds': [UNREAD_LABEL]
        }
        return self.gmail_api.users().messages().modify(
            userId=USER_ID,
            id=msg_id,
            body=body
        ).exceute()
    
    def bulk_mark_as_read(self, message_ids=None):
        """Bulk mark multiple email messages as READ."""
        if message_ids is None:
            message_ids = []

        body = {
            'messagesIds': message_ids,
            'addLabelIds': [READ_LABEL],
            'removeLabelIds': [UNREAD_LABEL]
        }

        return self.gmail_api.users().messages().batchModify(
            userId=USER_ID,
            body=body
        ).execute()
