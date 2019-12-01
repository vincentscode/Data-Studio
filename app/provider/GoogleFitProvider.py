from googleapiclient import discovery
from app.routes.auth.GoogleAuth import get_user_info, build_credentials


class GoogleFitProvider:
    def __init__(self):
        credentials = build_credentials()
        self.client = discovery.build('fitness', 'v1', credentials=credentials).files()

    def get_data(self):
        return self.client