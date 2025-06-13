"""Symbolic constants for the Gmail Nexus."""

import os

# Application metadata
APPLICATION_NAME = os.getenv('GN_APPLICATION_NAME', 'Gmail Nexus')
"""Name of the Gmail API application. Defaults to 'Gmail Nexus'."""

USER_ID = os.getenv('GN_USER_ID', 'me')
"""Gmail user ID. Defaults to 'me' (the authenticated user)."""

# Gmail label constants
INBOX_LABEL = 'INBOX'
"""Gmail label for the inbox."""

UNREAD_LABEL = 'UNREAD'
"""Gmail label indicating unread messages."""

READ_LABEL = 'READ'
"""Custom-defined label indicating messages that have been read."""
