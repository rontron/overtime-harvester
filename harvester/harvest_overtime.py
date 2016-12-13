import datetime
import time

import pandas as pd
import requests


def get_overtime(from_date, to_date, user_name, pw):
    user_id = get_user_id(user_name, pw)
    json_data = request_time_report(from_date, to_date, user_id, user_name, pw)
    my_overtime = calculate_overtime(json_data)
    print "From {from_date} to {to_date} you have {overtime} hours overtime!".format(from_date=from_date,
                                                                                     to_date=to_date,
                                                                                     overtime=my_overtime)


def get_user_id(user_name, pw):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}
    r = requests.get('https://comsysto.harvestapp.com/account/who_am_i',
                     headers=headers,
                     auth=(user_name, pw))
    return r.json()['user']['id']


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

    day_entry_list = [item['day_entry'] for item in harvest_report_json]
    df = pd.DataFrame(day_entry_list)
    spent_hours_per_day = df.groupby('spent_at')['hours'].sum()

    overtime = 0
    for spent_at, spent_hours in spent_hours_per_day.iteritems():
        if is_weekend(spent_at):
            # on weekends all work is overtime
            overtime += spent_hours
        else:
            overtime += spent_hours - 8

    return overtime


def is_weekend(date_str):
    datetime_object = time.strptime(date_str, '%Y-%m-%d')
    weekday = datetime.datetime(*datetime_object[:6]).weekday()
    return weekday == 5 or weekday == 6
