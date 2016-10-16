from __future__ import print_function, absolute_import
from biogridpy.biogrid_results import ResponseHandler as BGRH

try:
    import urlparse
    from urllib import urlencode
    from urllib2 import urlopen
    from ConfigParser import ConfigParser
    
except:
    from urllib.parse import urlparse
    from urllib.parse import urlencode
    from urllib.request import urlopen
    from configparser import ConfigParser
   
config = ConfigParser()
 
class BioGRID(object):
    """BioGRID API webservice client
    Methods are REST service endpoints, for more detailed description,
    see each method's docstring.
    
    Methods
    -------
    evidence(format_) : format_ is str, either "json" or "tab2"
    identifiers(format_)
    interactions(format_, **kwargs) : valid kwargs in interactions docstring
    interactions_single(format_, interaction_id): "interaction_id" is int
    organisms(format_)
    version()
    """

    def __init__(self, config_filepath='../biogridpyrc'): 
        try:
            config.read(config_filepath) 
        except:
            config.read_file(open(config_filepath))
            
        self.ACCESS_KEY= config.get('BioGRID_ak', 'access_key')
        BASE_URL = 'http://webservice.thebiogrid.org/'
        self.BASE_URL = BASE_URL
        self.EVIDENCE_URL = self.BASE_URL + 'evidence/'
        self.IDENTIFIERS_URL = self.BASE_URL + 'identifiers/'
        self.INTERACTIONS_URL = self.BASE_URL + 'interactions/'
        self.ORGANISMS_URL = self.BASE_URL + 'organisms/'
        self.VERSION_URL = self.BASE_URL + 'version/'

    def evidence(self, format_='tab2'):
        """
        Returns valid evidence names
        
        Usage:
        # Default params return a string identical to the default webservice:
        # http://webservice.thebiogrid.org/evidence/?accesskey=[ACCESSKEY]
        >>> BG = BioGRID()
        >>> evid = BG.evidence(format_='tab2')
        >>> evid.result
            ['AFFINITY CAPTURE-LUMINESCENCE',
             'AFFINITY CAPTURE-MS',
             ...
             'TWO-HYBRID']
         
        Docs:
        The URL http://webservice.thebiogrid.org/evidence/?accesskey=[ACCESSKEY]
        will retrieve the list of evidence names supported by the REST
        evidenceList option. This call only supports the accessKey and format
        parameters (can be tab2 or json
        (e.g. http://webservice.thebiogrid.org/evidence/?accesskey=[ACCESSKEY]&format=json). 
        """
        query_params = (('accessKey', self.ACCESS_KEY),
                        ('format', format_))
                             
        query_string = urlencode(query_params)
        query_string = '{0}?{1}'.format(self.EVIDENCE_URL, query_string)
        
        request = urlopen(query_string)
        results = request.read().decode('utf-8')
        
        return BGRH(results, format_, 'count not supported by this endpoint')
        
    def identifiers(self, format_='tab2'):
        """
        Returns valid identifier types
        
        Usage:
        # Default params return a string identical to the default webservice:
        # http://webservice.thebiogrid.org/identifiers/?accesskey=[ACCESSKEY]
        >>>BG = BioGRID()
        >>>id_types = BG.identifiers(format_='json')
        >>>id_types.result
            {'animalqtldb': '',
             'aphidbase': '',
             ...,
             'zfin': ''}
        
        Docs:
        The URL http://webservice.thebiogrid.org/identifiers/?accesskey=[ACCESSKEY]
        will retrieve the list of identifier type names supported by the
        REST additionalIdentifierTypes option.
        This call only supports the accessKey and format parameters (can be tab2 or json)
        (e.g. http://webservice.thebiogrid.org/identifiers/?accesskey=[ACCESSKEY]&format=json).
        """
        query_params = (('accessKey', self.ACCESS_KEY),
                        ('format', format_))
                             
        query_string = urlencode(query_params)
        query_string = '{0}?{1}'.format(self.IDENTIFIERS_URL, query_string)
        
        request = urlopen(query_string)
        results = request.read().decode('utf-8')
        
        return BGRH(results, format_, 'count not supported by this endpoint')
            
    def interactions(self, format_, **kwargs):
        """
        The positionial argument 'format_' is identical to the 'format'
        biogrid webservice parameter. It avoids interferring with the
        Python <format> built-in.
        
        kwargs are identical to the list of parameters here:
        http://wiki.thebiogrid.org/doku.php/biogridrest#list_of_parameters
        
        Valid keyword arguments include:
        ['start', 'max', 'interSpeciesExcluded',
        'selfInteractionsExcluded', 'evidenceList', 'includeEvidence', 
        'geneList', 'searchIds', 'searchNames', 'searchSynonyms',
        'searchBiogridIds', 'additionalIdentifierTypes', 'excludeGenes', 
        'includeInteractors', 'includeInteractorInteractions', 'pubmedList',
        'excludePubmeds', 'htpThreshold', 'throughputTag', 'taxId'
        'includeHeader', 'translate']
        
        Usage:
        Provide a list of genes:
        >>>BG = BiGRID()
        >>>bg_result = BG.interactions('tab2', geneList=["E2F1", "RB1"])
        
        The kwargs: geneList, evidenceList, additionalIdentifierTypes
        will accept a filepath where the file contains identifiers separated
        by a newline (see examples/ directory)
        
        >>>bg_result = BG.interactions('tab2', geneList='/home/kevin/geneList.txt')
        
        DOCS:
        The URL http://webservice.thebiogrid.org/interactions/?accesskey=[ACCESSKEY]
        will retrieve the first 10,000 interactions in BioGRID, ordered by the
        BioGRID Interaction Id as found in .tab2 files. Results can be modified
        and filtered using the options in our REST list of parameters. 
        """
        # set default parameters
        query_params_default = (('accessKey', self.ACCESS_KEY),
                                ('format', format_))
        start = kwargs.get('start', 0)
        max_ = kwargs.get('max', 10000)
        # pagination handled here (for large queries)
        count = self._getcount(start, max_, **kwargs) #how many records returned by this query?

        results = []
        for page_start in range(start, count, max_):
            valid_kwargs = self._validate_params(kwargs, page_start, max_)
            query_params_kwargs = tuple({(k,v) for k,v in valid_kwargs.items()})
            # combine default parameters with optional params from kwargs
            query_params = query_params_default + query_params_kwargs
                                 
            query_string = urlencode(query_params)
            query_string = '{0}?{1}'.format(self.INTERACTIONS_URL, query_string)
            
            request = urlopen(query_string)
            results.append(request.read().decode('utf-8'))

        return BGRH(results, format_, count)
    
    def interactions_single(self, format_, interaction_id):
        """
        Returns a single interaction.
        
        Usage:
        >>>single_result = BG.interactions_single('json', 103)
        
        Docs:
        Single interactions can be retrieved by appending this URL with a
        Biogrid Interaction ID
        (e.g. http://webservice.thebiogrid.org/interactions/103?accesskey=[ACCESSKEY]).
        """
        # set default parameters
        query_params = (('accessKey', self.ACCESS_KEY), ('format', format_))
                             
        query_string = urlencode(query_params)
        query_string = '{0}{1}?{2}'.format(self.INTERACTIONS_URL,
                                            interaction_id,
                                            query_string)
        request = urlopen(query_string)
        result = request.read().decode('utf-8')

        return BGRH([result], format_, 'count not supported by this endpoint')
    
    def organisms(self, format_='tab2'):
        """
        Returns a json of supported organisms.  
        
        Usage:
        # Default params return a string identical to the default webservice:
        # http://webservice.thebiogrid.org/organisms/?accesskey=[ACCESSKEY]
        >>> id_types = BioGRID().organisms(format_='tab2')
        
        # For a Python list of the identifiers, change tab2_format to 'list':
        >>> id_types = BioGRID().organisms(format_='tab2')
        
        # Finally, to replicate the "format=json" parameter:
        >>> id_types = BioGRID().organisms(format_='json')
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
        query_params = (('accessKey', self.ACCESS_KEY),
                        ('format', format_))
                             
        query_string = urlencode(query_params)
        query_string = '{0}?{1}'.format(self.ORGANISMS_URL, query_string)
        
        request = urlopen(query_string)
        results = request.read().decode('utf-8')
        
        return BGRH(results, format_, 'count not supported by this endpoint')
    
    def version(self):
        '''Returns the biogrid webservice version'''
        query_params = (('accessKey', self.ACCESS_KEY),)
                             
        query_string = urlencode(query_params)
        query_string = '{0}?{1}'.format(self.VERSION_URL, query_string)

        request = urlopen(query_string)
        results = request.read().decode('utf-8')
        return results
    
    def _getcount(self, page_start, max_, **kwargs):
        """
        Gets the number of records returned by the query
        """
        format_ = kwargs.pop('format_', 'count')
        # set default parameters
        query_params_default = (('accessKey', self.ACCESS_KEY),
                                ('format', format_))
        valid_kwargs = self._validate_params(kwargs, page_start, max_)
        query_params_kwargs = tuple({(k,v) for k,v in valid_kwargs.items()})
        # combine default parameters with optional params from kwargs
        query_params = query_params_default + query_params_kwargs
                             
        query_string = urlencode(query_params)
        query_string = '{0}?{1}'.format(self.INTERACTIONS_URL, query_string)

        request = urlopen(query_string)
        return int(request.read().decode('utf-8'))
    
    def _validate_params(self, params, page_start, max_):
        """
        checks paramaeters and transforms the list-like args
        """
        valid_params = (
        'start', 'max', 'interSpeciesExcluded',
        'selfInteractionsExcluded', 'evidenceList', 'includeEvidence', 
        'geneList', 'searchIds', 'searchNames', 'searchSynonyms',
        'searchBiogridIds', 'additionalIdentifierTypes', 'excludeGenes', 
        'includeInteractors', 'includeInteractorInteractions', 'pubmedList',
        'excludePubmeds', 'htpThreshold', 'throughputTag', 'taxId',
        'includeHeader', 'translate'
        )
        # don't modify the params dictionary object, create new one
        returnedParams = params.copy()
        for param in params.keys():
            if param not in valid_params:
                raise ValueError("'%s' parameter not valid: see "
                                 "http://wiki.thebiogrid.org/doku.php/"
                                 "biogridrest#list_of_parameters" % param)
            
            if param == 'evidenceList':
                try: #opening a evidenceList file
                    with open(params[param]) as f:
                        returnedParams[param] = '|'.join(f.read().splitlines())
                except Exception as e:
                    returnedParams[param] = '|'.join(params[param])
            elif param == 'geneList':
                try: #opening a geneList file
                    with open(params[param]) as f:
                        returnedParams[param] = '|'.join(f.read().splitlines())
                except Exception as e:
                    returnedParams[param] = '|'.join(params[param])
            elif param == 'additionalIdentifierTypes':
                try: #opening a additionalIdentifierTypes.List file
                    # this was working
                    with open(params[param]) as f:
                        returnedParams[param] = '|'.join(f.read().splitlines())
                except Exception as e:
                    returnedParams[param] = '|'.join(params[param])
        #pagination
        returnedParams['start']= page_start
        returnedParams['max']= max_
        
        return returnedParams
