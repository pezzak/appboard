import pytz

def get_or_create(db, model, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

def datetimefilter(value, format="%Y-%m-%d %H:%M:%S"):
    tz = pytz.timezone('Europe/Moscow')
    utc = pytz.timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(format)

def nonefilter(value):
    if value:
        return value
    else:
        return "-"
