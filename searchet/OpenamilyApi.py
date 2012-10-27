#!/usr/bin/env python
from urllib import urlencode
import optparse
import urllib2
import sys
import simplejson

class Amplify:
    
    def __init__(self, api_key):
        self.url = "http://portaltnx20.openamplify.com/AmplifyWeb_v21/AmplifyThis"
        self.api_key = api_key


    def amplify(self, text, analysis='all', output_format=''):
        """
        Send a request to the openamplify server
        Arguments:
          analysis - 'all','topics','actions','demographics','styles'
          output_format - 'xml','json','dart'
        """
        
        post_parameters = {
            'inputtext': text,
            'apiKey': self.api_key,
            'outputformat':output_format,
            'analysis':analysis,
        }
        
        try:
            response = urllib2.urlopen(self.url, urlencode(post_parameters))
        except urllib2.HTTPError, e:
            # Check for for Forbidden HTTP status, which means invalid API key.
            if e.code == 403:
                return 'Invalid API key.'
            
        amp_output = response.read()
        return amp_output

# When run as a standalone script:
if __name__ == '__main__':

    api_key = 'twjeg7dhsq4dv9mzhvzkpaqr6cegb4hu'
    input_text = 'china'
    # Initialize Amplify proxy class
    amplify = Amplify(api_key)

        # Getting the result as a python dictionary is simple using the
        # JSON output format and the simplejson library. 
    amp_json = amplify.amplify(input_text, 'all', 'json') # Send the request
    amp_dict = simplejson.loads(amp_json) # Parse the resulting JSON
    demographics = amp_dict['ns1:AmplifyResponse']['AmplifyReturn']['Demographics']
    #print 'Gender:', demographics['Gender']['Name']
    #print 'Age:', demographics['Age']['Name']
    #print 'Education:', demographics['Education']['Name']
    print amp_json

        

    # Send the request and print the resulting XML
    #amp = amplify.amplify(input_text, analysis='all', output_format='xml')
    #print amp
    
    
    