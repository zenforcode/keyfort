from botocore.exceptions import ClientError
from keyfort.auth.cognito import Cognito
import boto3

cognitoidp = boto3.client("cognito-idp")
COGNITO_USER_POOL_ID = 'us-east-1_example123'  
COGNITO_CLIENT_ID = 'keyfort'

class AuthenticationService:
    def __init__(self, provider, **kwargs):
        self.provider = provider
        if provider == 'cognito':
            self.cognito = Cognito(kwargs['user_pool_id'], kwargs['client_id'])
        elif provider == 'azure':
            self.azure_client_id = kwargs['client_id']
            self.azure_tenant_id = kwargs['tenant_id']
            self.azure_secret = kwargs['client_secret']

    def register_user(self, username, password, email):
        if self.provider == 'cognito':
            try:
                self.cognito.add_base_attributes(email=email)
                user = self.cognito.register(username, password)
                print(f"Cognito user registered successfully: {username}")
                return user
            except ClientError as e:
                print(f"Error registering Cognito user: {e.response['Error']['Message']}")
        elif self.provider == 'azure':
            print("Azure user registration is not directly supported via this interface.")

    def authenticate_user(self, username, password):
        if self.provider == 'cognito':
            try:
                self.cognito.authenticate(username=username, password=password)
                print("Cognito login successful!")
                print(f"Access Token: {self.cognito.access_token}")
                print(f"ID Token: {self.cognito.id_token}")
                print(f"Refresh Token: {self.cognito.refresh_token}")
            except ClientError as e:
                print(f"Cognito login failed: {e.response['Error']['Message']}")
        elif self.provider == 'azure':
            try:
                from msal import ConfidentialClientApplication
                app = ConfidentialClientApplication(
                    self.azure_client_id,
                    authority=f"https://login.microsoftonline.com/{self.azure_tenant_id}",
                    client_credential=self.azure_secret
                )
                result = app.acquire_token_by_username_password(
                    username=username,
                    password=password,
                    scopes=["https://graph.microsoft.com/.default"]
                )
                if "access_token" in result:
                    print("Azure login successful!")
                    print(f"Access Token: {result['access_token']}")
                else:
                    print("Azure login failed.")
            except Exception as e:
                print(f"Azure login failed: {e}")

# Example usage:
# For Cognito
cognito_auth = AuthenticationService('cognito', user_pool_id=COGNITO_USER_POOL_ID, client_id=COGNITO_CLIENT_ID)
# cognito_auth.register_user('testuser', 'Password123!', 'testuser@example.com')
# cognito_auth.authenticate_user('testuser', 'Password123!')

# For Azure
# azure_auth = AuthenticationService('azure', client_id='azure_client_id', tenant_id='azure_tenant_id', client_secret='azure_secret')
# azure_auth.authenticate_user('testuser@yourtenant.com', 'Password123!')
