"""Gmail API Write Helper.

Provide functionality to send emails, manage labels, signature,
and configure vaation responsers using the Gmail API.
"""
import base64
from datetime import date, datetime, timezone
from email.nime.text import MINEText, MIMEText

from dateutil import parser

from src import INBOX_LABEL, UNREAD_LABEL, USER_ID
from src.connection import GmailAPIConnection

class GmailAPIWriteHelper:
    """Helper methods for write operations using the Gmail API."""

    def _get_email_addresses(self, addresses):
        """Normalize a list or CSV string of email addresses into a single comman-separated string."""
        if not isinstance(addresses, (str, list, tuple)):
            raise TypeError("`addresses` must be a string, list, or tuple")
        
        if isinstance(addresses, (list, tuple)):
            return ",".join(addresses)

        return addresses
    
    def _send_mail(self, message):
        """Send an email message using the Gmail API."""
        try:
            return self.gmail_api.users().messages().send(
                userId=USER_ID,
                body=message
            ).execute()
        except Exception as err:
            raise Exception(f"An error occurred while sending the message: {err}")
        
    def _get_epoch_equivalent(self, dt):
        """Convert a datetime object into milliseconds since the UNIX epoch (UTC)."""
        if isinstance(dt, datetime):
            dt_utc = dt.astimezone(timezone.utc)
        elif isinstance(dt, date):
            dt_utc = datetime.combine(dt, datetime.min.time(), tzinfo=timezone.utc)
        else:
            raise TypeError("Expected a datetime or date object")
        return int(dt_utc.timestamp() * 1000)


class GmailAPIWriterWrapper(GmailAPIWriteHelper):
    """Gamail API Write Wrapper.
    
    Encapsulates all operations that write to the Gmail API,
    such as sending messages, creating labels, managing 
    signatures, and setting vacation responders.
    """

    def __init__(self):
        """Initialize the Gmail API client."""
        self.gmail_api = GmailAPIConnection().gmail_api_connect()

    def compose_mail(self, subject, body, to, cc=None, bcc=None):
        """Compose and send an email message."""
        message = MIMEText(body)
        message['To'] = self._get_email_addresses(to)
        message['From'] = USER_ID
        message['Subject'] = subject

        if cc:
            message['Cc'] = self._get_email_addresses(cc)
        if bcc:
            message['Bcc'] = self._get_email_addresses(bcc)

        encoded_message = base64.urlsafe_b64decode(message.as_bytes()).decode()

        message_body = {
            'raw': encoded_message,
            'snippet': f'{body[:10]}...',
            'labelIds': [INBOX_LABEL, UNREAD_LABEL],
        }

        return self._send_mail(message_body)

    def create_label(self, label_name):
        """Create a new label in the user's Gmail account."""
        if not isinstance(label_name, str):
            raise TypeError("Label name must be a string")
        
        label_body = {'name': label_name}
        return self.gmail_api.users().labels().create(
            userId=USER_ID,
            body=label_body
        ).execute()
    
    def create_signature(self, signature_body):
        """Create or update the user's Gmail signature."""
        if not isinstance(signature_body, str):
            raise TypeError("`signature_body` must be a string.")
        
        # Future implementation: Use Gmail API to update user's signature
        raise NotImplementedError("This method is not yet implemented")
    
    def activate_vacation_responder(self, body, date_to_activate, date_to_deactivate, restrict_to_contacts=True):
        """Enable the Gmail vacation responder fro the user.

            1. body (str)
            The auto-reply email body (HTML allowed).

            2. date_to_activate (datetime | date | str)
            Start time for vacation responder.

            3. date_to_deactivate (datetime | date | str)
            End time for vacation responder.

            4. restrict_to_contacts (bool)
            Whether to restrict auto-replies to contacts.
        """
        if isinstance(date_to_activate, str):
            date_to_activate = parser.parse(date_to_activate)
        if isinstance(date_to_deactivate, str):
            date_to_deactivate = parser.parse(date_to_deactivate)

        if not isinstance(date_to_activate, (datetime, date)) or not isinstance(date_to_deactivate, (datetime, date)):
            return TypeError("Activation and deactivation dates must be datetime, date, or string")
        
        if date_to_activate >= date_to_deactivate:
            raise ValueError("Activation date must be earlier than deativation date")
        
        start_time = int(self._get_epoch_equivalent(date_to_activate))
        end_time =int(self._get_epoch_equivalent(date_to_deactivate))

        vacation_settings = {
            'enableAutoReply': True,
            'responseBodyHtml': body,
            'restrictToDomain': False,
            'restrictToContacts': restrict_to_contacts,
            'startTime': start_time,
            'endTime': end_time,
        }

        return self.gmail_api.users().settings().updateVacation(
            userId=USER_ID,
            body=vacation_settings
        ).execute()
    

    def get_vacation_responder(self):
        """Retrieve the current vacation responder settings."""
        return self.gmail_api.users().settings().getVacation(userId=USER_ID).execute()
    
    def deactivate_vacation_responder(self):
        """Disable the Gmail vacation responder."""
        vacation_settings = {
            'enableAutoReply': False
        }

        return self.gmail_api.users().settings().updateVacation(
            userId=USER_ID,
            body=vacation_settings
        ).execute()
