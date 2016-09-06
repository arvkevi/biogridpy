# biogridpy

from __future__ import print_function

try:
    import urlparse, types
    from urllib import urlencode
    from urllib2 import urlopen
    from ConfigParser import ConfigParser
    config = ConfigParser()
    config.read('biogridpy.ini')
except:
    from urllib.parse import urlparse
    from urllib.parse import urlencode
    from urllib.request import urlopen
    from configparser import ConfigParser
    config = ConfigParser()
    config.read_file(open('biogridpy.ini'))
import json

class BioGrid(object):
    """BioGrid API"""

    def __init__(self): 
        self.access_key= config.get('BioGrid', 'access_key')
        
        BASE_URL = 'http://webservice.thebiogrid.org/'
        self.BASE_URL = BASE_URL
        #Endpoints
        self.IDENTIFIERS_URL = BASE_URL + 'identifiers/'
        self.INTERACTIONS_URL = BASE_URL + 'interactions/'
        self.ORGANISMS_URL = BASE_URL + 'organisms/'
        self.VERSION_URL = BASE_URL + 'version/'

    def identifiers(self, Format='tab2', tab2_format='str'):
        """
        Returns valid identifier types
        
        Usage:
        # Default params return a string identical to the default webservice:
        # http://webservice.thebiogrid.org/identifiers/?accesskey=[ACCESSKEY]
        >>> id_types = BioGrid().identifiers(Format='tab2', tab2_format='str')
        
        # For a Python list of the identifiers, change tab2_format to 'list':
        >>> id_types = BioGrid().identifiers(Format='tab2', tab2_format='list')
        
        # Finally, to replicate the "format=json" parameter:
        >>> id_types = BioGrid().identifiers(Format='json')
        
        Docs:
        The URL http://webservice.thebiogrid.org/identifiers/?accesskey=[ACCESSKEY]
        will retrieve the list of identifier type names supported by the
        REST additionalIdentifierTypes option.
        This call only supports the accessKey and format parameters (can be tab2 or json)
        (e.g. http://webservice.thebiogrid.org/identifiers/?accesskey=[ACCESSKEY]&format=json).
        """
        query_params = (('accessKey', self.access_key),
                        ('format', Format)
                        )
        
        query_params = [(param[0], param[1].encode('utf-8')
                         if type(param[1]) is types.UnicodeType
                         else param[1]) for param in query_params]
                             
        query_string = urlencode(query_params)
        query_string = '{0}?{1}'.format(self.IDENTIFIERS_URL, query_string)
        
        request = urlopen(query_string)
        results = request.read()
        
        if Format == 'json':
            ids_json = self.byteify(json.loads(results))
            return ids_json
        elif Format == 'tab2':
            if tab2_format == 'str': #return raw string w/ newline chars
                return results
            elif tab2_format == 'list':
                return results.split('\n')
        else:
            print ("Specify either <'json'> or <'tab2'> as arguments for the Format parameter")
            return
        
    def organisms(self, Format='tab2', tab2_format='str'):
        """
        Returns a json of supported organisms.  
        
        Usage:
        # Default params return a string identical to the default webservice:
        # http://webservice.thebiogrid.org/organisms/?accesskey=[ACCESSKEY]
        >>> id_types = BioGrid().organisms(Format='tab2', tab2_format='str')
        
        # For a Python list of the identifiers, change tab2_format to 'list':
        >>> id_types = BioGrid().organisms(Format='tab2', tab2_format='list')
        
        # Finally, to replicate the "format=json" parameter:
        >>> id_types = BioGrid().organisms(Format='json')
            {'10029': 'Cricetulus griseus',
             '10090': 'Mus musculus',
             '10116': 'Rattus norvegicus',
             ...
        
        Docs:
        The URL http://webservice.thebiogrid.org/organisms/?accesskey=[ACCESSKEY]
        will retrieve the list of organism IDs and names supported by the
        REST taxId option.  This call only supports the accessKey and format
        parameters (can be tab2 or json)
        (e.g. http://webservice.thebiogrid.org/organisms/?accesskey=[ACCESSKEY]&format=json).
        """
        query_params = (('accessKey', self.access_key),
                        ('format', Format)
                        )
        
        query_params = [(param[0], param[1].encode('utf-8')
                         if type(param[1]) is types.UnicodeType
                         else param[1]) for param in query_params]
                             
        query_string = urlencode(query_params)
        query_string = '{0}?{1}'.format(self.IDENTIFIERS_URL, query_string)
        
        request = urlopen(query_string)
        results = request.read()
        
        if Format == 'json':
            ids_json = self.byteify(json.loads(results))
            return ids_json
        elif Format == 'tab2':
            if tab2_format == 'str': #return raw string w/ newline chars
                return results
            elif tab2_format == 'list':
                return results.split('\n')
        else:
            print ("Specify either <'json'> or <'tab2'> as arguments for the Format parameter")
            return
        
    def interactions(self, query, **kwargs):
        
        query_params = (
                        ('q', query),
                        ('max', kwargs.pop('max_results', 600)),
                        ('facet', kwargs.pop('facet', 'association')),
                        ('pvalfilter', kwargs.pop('pvalfilter', '5e-8')),
                        ('orfilter', kwargs.pop('orfilter', '')),
                        ('betafilter', kwargs.pop('betafilter', '')),
                        ('datefilter', kwargs.pop('datefilter', '')),
                        ('sort', kwargs.pop('sort', '')),
                        ('asc', kwargs.pop('asc', ''))
                       )
        
        query_params = [(param[0], param[1].encode('utf-8')
                         if type(param[1]) is types.UnicodeType
                         else param[1]) for param in query_params]
                             
        query_string = urlencode(query_params)
        query_string = '{0}?{1}'.format(self.search_url, query_string)
        
        request = urlopen(query_string)
        results = request.read()
        
        return self.byteify(json.loads(results))
    
    def version(self):
        '''Returns the biogrid webservice version'''
        query_params = (('accessKey', self.access_key),)
        
        query_params = [(param[0], param[1].encode('utf-8')
                         if type(param[1]) is types.UnicodeType
                         else param[1]) for param in query_params]
                             
        query_string = urlencode(query_params)
        query_string = '{0}?{1}'.format(self.VERSION_URL, query_string)

        request = urlopen(query_string)
        results = request.read()
        return results
    
    def byteify(self, inpt):
        """
        Helper function, recursively keeps elements as strings.
        """
        if isinstance(inpt, dict):
            return {self.byteify( key): self.byteify(value)
                    for key, value in inpt.iteritems()}
        elif isinstance(inpt, list):
            return [self.byteify(element) for element in inpt]
        elif isinstance(inpt, unicode):
            return inpt.encode('utf-8')
        else:
            return inpt
        