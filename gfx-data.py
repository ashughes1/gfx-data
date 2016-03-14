import filecmp, httplib, json, os, requests, sys, time, urllib2, socorro
from datetime import date, datetime, timedelta

DELTA = str(date.today()-timedelta(days=363))
PLATFORMS = [
    'Windows XP',
    'Windows Vista',
    'Windows 7',
    'Windows 8',
    'Windows 10',
    'OS X',
    'Linux'
]

def get_dates(data):
    dates = []
    for platform in data.keys():
        for d in data[platform].keys():
            found = 0
            for i in range(len(dates)):
                if d == dates[i]:
                    found = 1
            if found == 0:
                dates.append(d)    
    return sorted(dates)

def get_json(url):
    try:
        json = requests.get(url).json()
    except:
        print('WARNING: No data for {:s}').format(url)
        json = ''
    return json

def run_socorro(topic, string):
    result = {}
    for platform in PLATFORMS:
        result[platform] = {}
        url = socorro.get_url(topic)
        url = url.replace('YYYYMMDD', DELTA)
        url = url.replace('PLATFORM', platform)
        json = get_json(url)
        result[platform] = socorro.process_json(json)
    return socorro.stringify(get_dates(result), result, string)

def write_json(string, path):
    result = ''
    tempfile = path + '.tmp'
    temp = open(tempfile, 'w')
    temp.write(string)
    temp.close()

    if not os.path.exists(path):
        f = open(path, 'w')
        f.write(string)
        f.close()
        result = 'Data written to {:s}!'.format(path)
    else:
        if not filecmp.cmp(tempfile, path):
            f = open(path, 'w')
            f.write(string)
            f.close()
            result = 'Data written to {:s}!'.format(path)
        else:
            result = 'No new data to write!'
            
    os.remove(tempfile)
    return result

def main(argv):
    string = ''
    filename = ''
    if argv.count('-s') > 0:
        topic = argv[argv.index('-s')+1]
        path = os.getcwd() + '/data/socorro/{:s}.json'.format(topic)
        if os.path.exists(path):
            f = open(path).read()
            string = f.strip('[]')
        string = run_socorro(topic, string)
    string = string.replace(',}', '}')
    string = string.replace('}{', '},{')
    string = '[' + string + ']'
    try:
        print write_json(string, path)
    except:
        print 'WARN: Failed to write {:s}!'.format(path)
    
if __name__ == '__main__':
    main(sys.argv[1:])

#if len(sys.argv) <= 1:
#    print "Error> Use the following command syntax:"
#    print "python gfx-data.py outfile.json"
#else:
    #filename = str(sys.argv[1])
    #path = os.getcwd() + '/' + filename
    #string = ""

    #print process_json('')

    # if os.path.exists(path):
    #     f = open(filename).read()
    #     string = process_json(f.strip('[]'))
    # else:
    #     string = process_json('')

    # f = open(filename, 'w')
    # f.write('[' + process_json(string) + ']')
    # f.close()