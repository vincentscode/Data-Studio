from googleapiclient import discovery

from app.routes.auth.GoogleAuth import get_user_info, build_credentials

import time


DATA_SOURCE = "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"


def get_data(from_time=None, to_time=None):
    if to_time is None:
        to_time = time.time_ns()
    if from_time is None:
        from_time = 0

    credentials = build_credentials()
    client = discovery.build('fitness', 'v1', credentials=credentials)
    return client.users().dataSources().datasets().aggregate(userId='me', dataSourceId=DATA_SOURCE, datasetId=f"{from_time}-{to_time}").execute()
