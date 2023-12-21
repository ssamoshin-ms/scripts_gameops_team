from dataclasses import dataclass
from services.google.secret_manager.google_secret_manager import GoogleSecretManager


@dataclass
class GoogleAccountInfo:

  type: str = "service_account",
  project_id: str = "melsoft-infra",
  private_key_id: str = None,
  private_key: str = None,
  client_email: str = "gcpsa-clientautoqa-gdrive@melsoft-infra.iam.gserviceaccount.com"
  client_id: str = "107377526488336154387"
  auth_uri: str = "https://accounts.google.com/o/oauth2/auth"
  token_uri: str = "https://oauth2.googleapis.com/token"
  auth_provider_x509_cert_url: str = "https://www.googleapis.com/oauth2/v1/certs"
  client_x509_cert_url: str = "https://www.googleapis.com/robot/v1/metadata/x509/gcpsa-clientautoqa-gdrive%" \
                              "40melsoft-infra.iam.gserviceaccount.com"
  universe_domain: str = "googleapis.com"

  def get_account_info(self):
    manager = GoogleSecretManager()
    self.private_key_id = manager.access_secret('fa-dev-qaa-gd_private_key_id')
    private_key_string = manager.access_secret('fa-dev-qaa-gd_private_key')
    self.private_key = private_key_string.replace('\\n', '\n')
    return self.__dict__

