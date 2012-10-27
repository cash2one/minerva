import urllib
import simplejson
from pprint import pprint

print 'enter your query:'
text = raw_input()
gateway = 'http://api.zemanta.com/services/rest/0.0/'
args = {'method': 'zemanta.suggest',
        'api_key': 'em6dgfq7dhyxdfxmyp8jknf3',
        'text': text,
        'return_categories': 'dmoz',
        'format': 'json'}            
args_enc = urllib.urlencode(args)

raw_output = urllib.urlopen(gateway, args_enc).read()

output = simplejson.loads(raw_output)

pprint(output)
