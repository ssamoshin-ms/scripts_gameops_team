from google.cloud import secretmanager


class GoogleSecretManager:
    def __init__(self, project_id='fa-dev-231913'):
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret_info(self, secret_id):
        """
        Get information about the given secret. This only returns metadata about
        the secret container, not any secret material.

        Args:
            secret_id: the secret id, e.g. 'fa-dev-qaa-appcenter_api_token_android_dev'

        Returns:
            metadata about the secret container
        """
        secret_id = self.client.secret_path(self.project_id, secret_id)
        response = self.client.get_secret(request={"name": secret_id})
        return response

    def get_secret_info_by_name(self, secret_name):
        """
        Get information about the given secret by full name. This only returns metadata about
        the secret container, not any secret material.

        Args:
            secret_name: the full name in the format 'projects/{project_id}/secrets/{secret_id}'

        Returns:
            metadata about the secret container
        """
        response = self.client.get_secret(request={"name": secret_name})
        return response

    def access_secret(self, secret_id: str, version_id: str = 'latest'):
        """
        Access the given secret version if one exists

        Args:
            secret_id: the secret id, e.g. 'fa-dev-qaa-appcenter_api_token_android_dev'
            version_id: The version can be a version number as a string (e.g. "5") or an alias (e.g. "latest")

        Returns:
            the secret value for the specific version
        """
        name = self.client.secret_version_path(self.project_id, secret_id, version_id)
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode('UTF-8')

    def access_secret_by_name(self, secret_name: str, version_id: str = 'latest'):
        """
        Access the given secret version if one exists by full name

        Args:
            secret_name: the full name in the format 'projects/{project_id}/secrets/{secret_id}'
            version_id: The version can be a version number as a string (e.g. "5") or an alias (e.g. "latest")

        Returns:
            the secret value for the specific version
        """
        name = f"{secret_name}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode('UTF-8')

    def get_secrets(self):
        """
        List all secrets in the given project.

        Returns:
            the list of secrets
        """
        parent = f"projects/{self.project_id}"
        response = self.client.list_secrets(request={"parent": parent})
        return list(response)

    def get_secrets_by_filter(self, filter_str: str):
        """
        List all secrets in the given project by filter

        Args:
            filter_str: the filter string, e.g. "labels.is_production=true"

        Returns:
            the list of secrets
        """
        parent = f"projects/{self.project_id}"
        response = self.client.list_secrets(request={"parent": parent, "filter": filter_str})
        return list(response)
