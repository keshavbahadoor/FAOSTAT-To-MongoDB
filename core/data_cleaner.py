

def clean_record(data_record):
    """
    Performs any necessary cleaning on data and returns record
    :param data_record:
    :return:
    """
    for key, value in data_record.iteritems():
        if isinstance(data_record[key], basestring):
            if isinstance(data_record[key], unicode):
                print 'unicode!!!!!'
            data_record[key] = unicode(data_record[key], 'utf-8')
    return data_record


def clean_value(val):
    if isinstance(val, basestring):
        if isinstance(val, unicode):
            print 'unicode!!!!!'
    return val
