import datetime
import time

import pandas as pd
import requests


def get_overtime(from_date, to_date, harvest_user_id, user_name, pw):
    json_data = request_time_report(from_date, to_date, harvest_user_id, user_name, pw)
    my_overtime = calculate_overtime(json_data)
    print "From {from_date} to {to_date} you have {overtime} hours overtime!".format(from_date=from_date,
                                                                                     to_date=to_date,
                                                                                     overtime=my_overtime)


def request_time_report(from_date, to_date, harvest_user_id, user_name, pw):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}

    payload = {'from': from_date, 'to': to_date}

    r = requests.get('https://comsysto.harvestapp.com/people/{0}/entries'.format(harvest_user_id),
                     params=payload,
                     headers=headers,
                     auth=(user_name, pw))
    return r.json()


def calculate_overtime(harvest_report_json):
    overtime = 0

    harvest_list = [item['day_entry'] for item in harvest_report_json]
    df = pd.DataFrame(harvest_list)
    grouped_df = df.groupby('spent_at')['hours'].sum()

    # print grouped_df.head(10)

    # from IPython import embed
    # embed()

    for spent_at, worked_hours in grouped_df.iteritems():
        if is_weekend(spent_at):
            # on weekends all work is overtime
            overtime += worked_hours
            # print overtime, spent_at, is_weekend(spent_at)
        else:
            overtime += worked_hours - 8
            # print overtime, spent_at, is_weekend(spent_at)

    return overtime


def is_weekend(date_str):
    datetime_object = time.strptime(date_str, '%Y-%m-%d')
    weekday = datetime.datetime(*datetime_object[:6]).weekday()
    return weekday == 5 or weekday == 6
