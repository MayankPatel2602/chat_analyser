import re
import pandas as pd

def preprocessor(data):
    pattern = '\d{1,2}/\d{2,4}/\d{2,4},\s\d{1,2}:\d{1,2}\s\w{1,2}\s-\s'
    pattern2 = '\d{1,2}/\d{2,4}/\d{2,4},\s\d{1,2}:\d{1,2}\s'
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern2, data)
    df = pd.DataFrame({'user_message': message, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M\u202f')
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W)]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns='user_message', inplace=True)
    df['Year'] = df['message_date'].dt.year
    df['Month'] = df['message_date'].dt.month_name()
    df['Day'] = df['message_date'].dt.day
    df['Hour'] = df['message_date'].dt.hour
    df['Minute'] = df['message_date'].dt.minute
    df['month_num'] = df['message_date'].dt.month
    df['day_name'] = df['message_date'].dt.day_name()
    df.drop(columns='message_date', inplace=True)

    return df
