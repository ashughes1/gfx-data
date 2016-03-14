MANIFEST = {
    'crashes-per-adi':'https://crash-stats.mozilla.com/api/SuperSearch/?&signature=~gfx&signature=~layers&signature=~canvas&date=%3E%3DYYYYMMDD&platform_pretty_version=~PLATFORM&_histogram.date=_cardinality.install_time&_histogram_interval=1d'
}

def get_url(topic):
    result = 'Not Found in Manifest!'
    if MANIFEST.has_key(topic):
        result = MANIFEST[topic]
    return result

def process_json(json):
    result ={}
    for data in json['facets']['histogram_date']:       
        crashes = data['count']
        installs = data['facets']['cardinality_install_time']['value']
        rate = float(crashes)/float(installs)
        result[data['term'][0:10]] = rate
    return result

def stringify(dates, data, string):
    for i in range(len(dates)):
        if string.find(dates[i]) <= 0:
            string += '{'
            string += '"date":"{:s}",'.format(dates[i])
            for platform in data.keys():
                if data[platform].has_key(dates[i]):
                    string += '"{:s}":{:.2f},'.format(platform,data[platform][dates[i]])
                else:
                    string += '"{:s}":0,'.format(platform)
            string += '}'
    return string
