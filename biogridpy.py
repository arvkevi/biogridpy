from __future__ import print_function
from biogrid_results import ResponseHandler as BGRH


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


class BioGrid(object):
    """BioGrid API"""

    def __init__(self): 
        self.access_key= config.get('BioGrid', 'access_key')
        
        BASE_URL = 'http://webservice.thebiogrid.org/'
        self.BASE_URL = BASE_URL
        #Endpoints
        self.EVIDENCE_URL = BASE_URL + 'evidence/'
        self.IDENTIFIERS_URL = BASE_URL + 'identifiers/'
        self.INTERACTIONS_URL = BASE_URL + 'interactions/'
        self.ORGANISMS_URL = BASE_URL + 'organisms/'
        self.VERSION_URL = BASE_URL + 'version/'

    def evidence(self, Format='tab2'):
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
        The URL http://webservice.thebiogrid.org/evidence/?accesskey=[ACCESSKEY]
        will retrieve the list of evidence names supported by the REST
        evidenceList option. This call only supports the accessKey and format
        parameters (can be tab2 or json
        (e.g. http://webservice.thebiogrid.org/evidence/?accesskey=[ACCESSKEY]&format=json). 
        """
        query_params = (('accessKey', self.access_key),
                        ('format', Format)
                        )
        
        query_params = [(param[0], param[1].encode('utf-8')
                         if type(param[1]) is types.UnicodeType
                         else param[1]) for param in query_params]
                             
        query_string = urlencode(query_params)
        query_string = '{0}?{1}'.format(self.EVIDENCE_URL, query_string)
        
        request = urlopen(query_string)
        results = request.read()
        
        if Format == 'json':
            ids_json = self.byteify(json.loads(results))
            return ids_json
        elif Format == 'tab2':
            return results

        else:
            print ("Specify either <'json'> or <'tab2'> as arguments for the Format parameter")
            return
        
    def identifiers(self, Format='tab2', **kwargs):
        """
        Returns valid identifier types
        
        Usage:
        # Default params return a string identical to the default webservice:
        # http://webservice.thebiogrid.org/identifiers/?accesskey=[ACCESSKEY]
        >>> id_types = BioGrid().identifiers(Format='tab2')
        
        # For a Python list of the identifiers, change tab2_format to 'list':
        >>> id_types = BioGrid().identifiers(Format='tab2')
        
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
            return results
        else:
            print ("Specify either <'json'> or <'tab2'> as arguments for the Format parameter")
            return
    
    def validate_interaction_param(self, **kwargs):
            valid_params = (
            ('accessKey', self.access_key),
            ('Format', kwargs.pop('Format', 'tab2')),
            ('tab2_format', kwargs.pop('tab2_format', 'list')),
            ('start', kwargs.pop('start', 0)),
            ('max', kwargs.pop('max', 10000)),
            ('interSpeciesExcluded', kwargs.pop('interSpeciesExcluded', 'false')),
            ('selfInteractionsExcluded', kwargs.pop('selfInteractionsExcluded', 'false')),
            ('evidenceList', kwargs.pop('evidenceList', '')), #str-like pipe-separated list of evidence codes
            ('includeEvidence', kwargs.pop('includeEvidence', 'false')),
            ('geneList', kwargs.pop('geneList', '')), #str-like pipe-separated list of gene names or ids
            ('searchIds', kwargs.pop('searchIds', 'false')), #If 'true', try to match
            ('searchNames', kwargs.pop('searchNames', 'false')), #If 'true' try to match names
            ('searchSynonyms', kwargs.pop('searchSynonyms', 'false')),
            ('searchBiogridIds', kwargs.pop('searchBiogridIds', 'false')),
            ('additionalIdentifierTypes', kwargs.pop('additionalIdentifierTypes', '')), #str-like pipe-separated
            ('excludeGenes', kwargs.pop('excludeGenes', 'false')),
            ('includeInteractors', kwargs.pop('includeInteractors', 'true')),
            ('includeInteractorInteractions', kwargs.pop('includeInteractorInteractions', 'false')),
            ('pubmedList', kwargs.pop('pubmedList', '""')), #pipe-separated list of pmids
            ('excludePubmeds', kwargs.pop('excludePubmeds', 'false')),
            ('htpThreshold', kwargs.pop('htpThreshold', 2147483647)),
            ('throughputTag', kwargs.pop('throughputTag', 'any')), # "any", "low", "high"
            ('taxId', kwargs.pop('taxId', 'All')),
            ('includeHeader', kwargs.pop('includeHeader', 'false')),
            ('translate', kwargs.pop('translate', 'false')),
                       )
            
    def interactions(self, **kwargs):
        """
        Format can be 'tab2', '
        """
        Format = kwargs.pop('Format', 'tab2')
        
        query_params_default = (('accessKey', self.access_key),
                                ('Format', Format),
                                )
        
        query_params_kwargs = tuple({(k,v) for k,v in kwargs.items()})
        
        query_params = query_params_default + query_params_kwargs
        
        query_params = [(param[0], param[1].encode('utf-8')
                         if type(param[1]) is types.UnicodeType
                         else param[1]) for param in query_params]
                             
        query_string = urlencode(query_params)
        query_string = '{0}?{1}'.format(self.INTERACTIONS_URL, query_string)
        print (query_string)
        request = urlopen(query_string)
        results = request.read()
        
        return BGRH(results, Format)
        

        
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
        