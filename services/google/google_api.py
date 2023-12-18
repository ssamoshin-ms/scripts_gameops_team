import io
from typing import List, Optional

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

from secrets import GoogleAccountInfo

class GoogleApi(GoogleAccountInfo):
    def __init__(self, api_name: str, api_version: str, scope: list):
        super().__init__()

        path = '/Users/samoshinsergey/project/scripts_gameops_team/secrets/key.json'
        # self.credentials = Credentials.from_service_account_info(self.get_account_info(), scopes=scope)
        self.credentials = Credentials.from_service_account_file(path, scopes=scope)
        self.service: Resource = build(api_name, api_version, credentials=self.credentials)

    def _get_files_metadata(self, file_id: str) -> Optional[dict]:
        """Get a file metadata or content by file ID

        :param file_id: file ID
        :return: metadata
        https://developers.google.com/drive/api/reference/rest/v3/files/get
        """

        try:
            response = self.service.files().get(supportsAllDrives=True, fileId=file_id).execute(num_retries=2)
            return response
        except HttpError as error:
            # LOGGER.debug(f"Status code: {error.status_code}, Error reason: {error.reason}. "
            #              f"Error details: {*error.error_details,}")
            return None

    def _create_folder_in_parent_folder(self, folder_name: str, parent_id: str) -> Optional[str]:
        """Create a parent folder which would contain child folder.

        :param: folder_name: child folder to be created.
        :param: parent_id: parent folder name to be created.

        https://developers.google.com/drive/api/guides/folder
        """

        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }

        try:
            response = self.service.files().create(supportsAllDrives=True, body=file_metadata, fields='id').execute(
                num_retries=2)
            # LOGGER.debug(f"Created 'NEW' folder: {folder_name} with folder id: {parent_id}")
            return response.get('id')
        except HttpError as error:
            # LOGGER.debug(f"Status code: {error.status_code}, Error reason: {error.reason}. "
            #              f"Error details: {*error.error_details,}")
            return None

    def _get_list_of_files(self, fields: str, filtering: str) -> List:
        """Method to search for files and folders on Google Drive.

        :param fields: return specific fields for a file.
        :param fields: The token for continuing a previous list request on the next page. This should be set to the
        value of 'nextPageToken' from the previous response.
        :params filtering: A query for filtering the file results.

        https://developers.google.com/drive/api/guides/search-files
        """

        files, page_token = [], None
        try:
            while True:
                response = self.service.files().list(supportsAllDrives=True, includeItemsFromAllDrives=True,
                                                     fields=fields,
                                                     q=filtering,
                                                     pageToken=page_token
                                                     ).execute(num_retries=2)
                files.extend(response.get('files', []))
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break
        except HttpError as error:
            # LOGGER.debug(f"Status code: {error.status_code}, Error reason: {error.reason}. "
            #              f"Error details: {*error.error_details,}")
            files = []
        return files

    def _download_file(self, file_id: str, file_name: str, file_path: str) -> bool:
        """Download a file
        :param file_id: ID of the file to download
        :param file_name: NAME of the file to download
        :param file_path: PATH of the file to download
        :return: TRUE/FALSE if file was downloaded

        https://developers.google.com/drive/api/guides/manage-downloads
        """

        new_file_path = ''.join([file_path, '/', file_name])
        done = False

        try:
            request = self.service.files().get_media(fileId=file_id)
            # Instead of io.BytesIO() the io.FileIO() was used
            # https://stackoverflow.com/questions/42800250/difference-between-open-and-io-bytesio-in-binary-streams
            file = io.FileIO(new_file_path, 'wb')
            downloader = MediaIoBaseDownload(file, request)

            while not done:
                status, done = downloader.next_chunk(num_retries=2)
                # LOGGER.info(f'Download file: {file_name} - {int(status.progress() * 100)}')
        except HttpError as error:
            # LOGGER.debug(f"Status code: {error.status_code}, Error reason: {error.reason}. "
            #              f"Error details: {*error.error_details,}")
            return None
        return done

    def _upload_new_file(self, folder_id: str, file_name: str, file_path, description: str = None) -> Optional[str]:
        """Upload new file to provided path and description
        :param folder_id: file metadata (body) for the request.
        :param file_path: PATH to file.
        :param file_name: provided file name to upload.
        :param description: provided description of the uploaded file.
        :return: ID of uploaded file
        https://developers.google.com/drive/api/guides/manage-uploads
        """

        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        if description is not None:
            file_metadata.update({'description': description})

        try:
            media_file = MediaFileUpload(file_path, resumable=True)
            response = self.service.files().create(supportsAllDrives=True, body=file_metadata, media_body=media_file,
                                                   fields='id').execute(num_retries=2)
        except HttpError as error:
            # LOGGER.debug(f"Status code: {error.status_code}, Error reason: {error.reason}. "
            #              f"Error details: {*error.error_details,}")
            response = None
        return response.get('id')

    def _delete_file(self, file_id: str):
        """Permanently delete file by file id.
        :param file_id: ID of the file to be deleted.
        https://developers.google.com/drive/api/reference/rest/v3/files/delete
        """

        try:
            self.service.files().delete(supportsAllDrives=True, fileId=file_id).execute(num_retries=2)
        except HttpError as error:
            # LOGGER.debug(f"Status code: {error.status_code}, Error reason: {error.reason}. "
            #              f"Error details: {*error.error_details,}")
            return None

