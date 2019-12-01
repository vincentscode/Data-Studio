from googleapiclient import discovery

from app.routes.auth.GoogleAuth import get_user_info, build_credentials

import calendar
import time
from datetime import datetime


DATA_SOURCE = "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"


def get_data(year, month):
    from_time = int(datetime(year, month, 1).timestamp())
    print(from_time)

    to_time = int(datetime(year, month, calendar.monthrange(year, month)[1]).timestamp())
    print(to_time)

    print(time.time())

    credentials = build_credentials()
    client = discovery.build('fitness', 'v1', credentials=credentials)

    body = {
        "aggregateBy": [
            {
                "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps",
                "dataTypeName": "com.google.step_count.delta"
            }
        ],
        "startTimeMillis": from_time,
        "endTimeMillis": to_time,
    }

    data = client.users().dataset().aggregate(userId='me', body=body).execute()
    print(data)
    return data
    # return client.users().dataSources().datasets().aggregate(userId='me', dataSourceId=DATA_SOURCE, datasetId=f"{from_time}-{to_time}").execute()
