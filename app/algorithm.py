import datetime
from dateutil.relativedelta import relativedelta

from app.connect import collection


async def payout_aggregator(first_date, second_date, time):
    pipeline = [
        {'$match': {'dt': {'$gte': first_date, '$lte': second_date}}},
        {'$group': {'_id': {'$dateTrunc': {'date': '$dt', 'unit': time}},
                    'dataset': {'$sum': '$value'}}
         },
        {'$sort': {'_id': 1}}
    ]
    current_date = first_date
    dict1 = {
        'hour': datetime.timedelta(hours=1),
        'day': datetime.timedelta(days=1),
        'month': relativedelta(months=1)
    }
    dict2 = {'dataset': [], 'labels': []}
    aggregation_result = list(collection.aggregate(pipeline))
    while current_date <= second_date:
        index = next((i for i, doc in enumerate(aggregation_result)
                      if doc['_id'] == current_date), None)
        if index is not None:
            dict2['dataset'].append(aggregation_result[index]['dataset'])
        else:
            dict2['dataset'].append(0)
        dict2['labels'].append(current_date.isoformat())
        current_date += dict1.get(time)
    return dict2
