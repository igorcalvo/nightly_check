from datetime import date

def CheckForTodaysEntry(lastDate: str) -> bool:
    delta = date.today() - date.fromisoformat(lastDate)
    return delta.days >= 1

def CreateEntry(data):
    if CheckForTodaysEntry(data.iloc[-1]['date']):
        di = dict.fromkeys(data.columns.values, False)
        di['date'] = str(date.today())
        data = data.append((di), ignore_index=True)
    return data