"""Google API Connection Manager for services like Gmail."""
import os 
import sys
import httplib2
import argparse

from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import  Storage

from src.nexus import APPLICATION_NAME


class GoogleAPIConnection:
    """
    Establishes and manages a secure connection to Google APIs.

    Supports authentication and service initialization for APIs 
    like Gmail.
    """

    def __init__(self, service: str, version: str):
       """
       Initialize the GoogleAPIConnection.
       """
       self.service = service
       self.version = version
       self.scopes = os.environ['GN_SCOPES']
       self.ca_certs = os.getenv('GN_CA_CERTS_PEM_FILE')
       self.disable_ssl = self._str_to_bool(os.getenv('GN_DISABLE_SSL_CERTS', 'False'))

    def _str_to_bool(self, value: str) -> bool:
        """
        Convert a string to a boolean.
        """
        return value.lower() in {'true', 'yes', '1'}
    
    def _get_connection_falgs(self):
        """
        Parse command-line flags for OAuth2.
        """
        try:
            return argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            return None

    def _get_client_secret_filename(self, file_path: str) -> str:
        """
        Extract the filename from a given file path.
        """
        return os.path.basename(file_path)
    
    def _get_credentials(self):
        """
        Retrieve or generate OAuth2 credentials.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        os.makedirs(credential_dir, exist_ok=True)

        credential_path = os.path.join(credential_dir,  'client_secret.json')
        store = Storage(credential_path)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(credential_path, self.scopes)
            flow.user_agent = APPLICATION_NAME
            flags = self._get_connection_flags()

            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:
                credentials = tools.run(flow, store)
    
        return credentials
    
    def get_service(self):
        """
        Build and return a Google API service object.
        """
        credentials = self._get_credentials()
        http = credentials.authorize(
            httplib2.Http(
                ca_certs=self.ca_certs,
                disable_ssl_certificate_validation=self.disable_ssl
            )
        )
        return discovery.build(self.service, self.version, http=http)
    
class GmailAPIConnection:
    """Establishes a connection to the Gmail API."""

    def gmail_api_connect(self):
        """Authenticate and return a Gmail API service instance."""
        google_api = GoogleAPIConnection(service='gmail', version='v1')
        return google_api.get_service()
