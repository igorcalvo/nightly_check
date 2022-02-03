from datetime import date, timedelta

def CheckForTodaysEntry(lastDate: str) -> int:
    delta = date.today() - date.fromisoformat(lastDate)
    return delta.days

def GetLatestDate(data) -> str:
    return data.iloc[-1]['date']

def CreateEntry(data):
    lastDate: str = GetLatestDate(data)
    deltaDays = CheckForTodaysEntry(data.iloc[-1]['date'])
    if deltaDays > 1:
        di = dict.fromkeys(data.columns.values, 'False')
        for day in range(deltaDays):
            newDate = date.fromisoformat(lastDate)
            di['date'] = str(newDate + timedelta(days=(day + 1)))
            data = data.append((di), ignore_index=True)
    return data