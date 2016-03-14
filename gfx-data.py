import httplib, json, os, requests, sys, time, urllib2, socorro
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

def run_socorro(topic):
    result = {}
    for platform in PLATFORMS:
        result[platform] = {}
        url = socorro.get_url(topic)
        url = url.replace('YYYYMMDD', DELTA)
        url = url.replace('PLATFORM', platform)
        json = get_json(url)
        result[platform] = socorro.process_json(json)
    return socorro.stringify(get_dates(result), result)

def write_json(string, filename):
    path = os.getcwd() + '/data/' + filename
    f = open(path, 'w')
    f.write(string)
    f.close()

def main(argv):
    string = ''
    filename = ''
    if argv.count('-s') > 0:
        filename = 'socorro/{:s}.json'.format(argv[argv.index('-s')+1])
        string = run_socorro(argv[argv.index('-s')+1])
    string = string.replace(',}', '}')
    string = string.replace('}{', '},{')
    string = '[' + string + ']'
    try:
        write_json(string, filename)
        print 'Data written to {:s}!'.format(filename)
    except:
        print 'WARN: Failed to write {:s}!'.format(filename)
    
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