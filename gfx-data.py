import filecmp, httplib, json, os, re, requests, sys, time, urllib2, socorro
from datetime import date, datetime, timedelta

PLATFORMS = [
    'Windows XP',
    'Windows Vista',
    'Windows 7',
    'Windows 8',
    'Windows 10',
    'OS X',
    'Linux'
]

VENDORS = {
    'amd':'0x1002',
    'intel':'0x8086',
    'nvidia':'0x10de'
}

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

def run_socorro(topic, string, date_start, date_end):
    result = {}
    url = socorro.get_url(topic)
    url = url.replace('__DATE_START__', date_start)
    url = url.replace('__DATE_END__', date_end)
    if url.find('__PLATFORM__') >= 0:
        for platform in PLATFORMS:
            result[platform] = {}
            json = get_json(url.replace('__PLATFORM__', platform))
            result[platform] = socorro.process_json(json)
    if url.find('__VENDOR_ID__') >= 0:
        for vendor in VENDORS.keys():
            result[vendor] = {}
            json = get_json(url.replace('__VENDOR_ID__', VENDORS[vendor]))
            result[vendor] = socorro.process_json(json)
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
    date_start = str(date.today()-timedelta(days=363))
    date_end = str(date.today())
    string = ''
    filename = ''
    
    # Set the start date if one was provided
    if argv.count('-d') > 0:
        p = re.compile('^2[0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]$')
        if p.match(argv[argv.index('-d')+1]):
            date_start = argv[argv.index('-d')+1]
        
    # Run the specified Socorro query, if one was specified
    if argv.count('-s') > 0:
        topic = argv[argv.index('-s')+1]
        path = os.getcwd() + '/data/socorro/{:s}.json'.format(topic)
        if os.path.exists(path):
            f = open(path).read()
            string = f.strip('[]')
        string = run_socorro(topic, string, date_start, date_end)
    
    # Clean up the resulting JSON so that it is valid 
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