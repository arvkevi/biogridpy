from __future__ import print_function, absolute_import
import os, json, inspect
from itertools import chain
try:
    from cStringIO import StringIO
except:
    from io import StringIO

class ResponseHandler(object):
    """
    In-memory BioGRID REST Service response object
    
    Attributes
    ----------
    count : int
        The number of results returned by query
    
    endpoint : str
        The name of the enpoint in this result object
    
    headers : list
        list of the column headers/dictionary keys
        
    output_format : str
        Output format from the BG instance
    
    raw_result : list of unformatted response objects
    
    result : str or list
        formatted appropriately according to output_format
        
    Methods
    -------
    export(outdir, filename) : outdir - str, filename - str
        saves the results as a file
        
    toDataFrame() :
        formats the results for consumption by a pandas DataFrame
    """    
    def __init__(self, response, output_format, count):
        # attributes
        self.raw_result = response
        self.output_format = output_format
        self.count = count
        self.endpoint = inspect.stack()[1][3]

        #########################
        # HANDLE COLUMN HEADERS #
        #########################
        __tab2headers = ['BioGRID Interaction ID', 'Entrez Gene Interactor A',
            'Entrez Gene Interactor B', 'BioGRID ID Interactor A',
            'BioGRID ID Interactor B', 'Systematic Name Interactor A',
            'Systematic Name Interactor B', 'Official Symbol Interactor A',
            'Official Symbol Interactor B', 'Synonyms Interactor A',
            'Synonyms Interactor B', 'Experimental System',
            'Experimental System Type', 'Author', 'Pubmed ID',
            'Organism Interactor A', 'Organism Interactor B', 'Throughput',
            'Score', 'Modification', 'Phenotypes', 'Qualifications', 'Tags',
            'Source Database']
        __extheaders = ['Source Database Identifiers',
                    'Number of Interactions per Publication',
                    'Additional Identifiers']
        __tab1headers = ['INTERACTOR_A', 'INTERACTOR_B',
              'OFFICIAL_SYMBOL_FOR_A', 'OFFICIAL_SYMBOL_FOR_B',
              'ALIASES_FOR_A', 'ALIASES_FOR_B',
              'EXPERIMENTAL_SYSTEM', 'SOURCE', 'PUBMED_ID']
        
        self.headers = __tab2headers #initialize default hedears for tab2/json
        if (self.output_format == 'extendedTab2' or
            self.output_format == 'jsonExtended'):
            self.headers = __tab2headers + __extheaders
        elif self.output_format == 'tab1':
            self.headers = __tab1headers
        
        ##############################
        # NON-interactions ENDPOINTS #
        ##############################
        if self.endpoint not in ('interactions', 'interactions_single'):
            #don't need column headers for these endpoints
            delattr(self, 'headers') # <--best practice?
            if self.output_format == 'json':
                try: #2
                    self.result = self._byteify2(json.loads(self.raw_result))
                except AttributeError: #3
                    self.result = self._byteify3(json.loads(self.raw_result))
            elif self.output_format == 'tab2':
                # organisms endpoint has two columns
                if self.endpoint == 'organisms':
                    result_ = []
                    for record in self.raw_result.splitlines():
                        result_.append(tuple(record.split('\t')))
                    self.result = result_
                else:
                    self.result = self.raw_result.splitlines()
            else:
                print('The positional argument <format> can only be "json" '
                      'or "tab2" for the /{0}/ endpoint '
                      'you are requesting'.format(self.endpoint))
        
        ##########################
        # FORMAT RESPONSE OBJECT #
        ##########################
        elif (self.output_format == 'json' or
              self.output_format == 'jsonExtended'):
            # list of dicts
            jsons = [json.loads(page) for page in self.raw_result]
            merged_json = jsons.pop(0) # first dict
            for json_obj in jsons:
                try: #2
                    merged_json = dict(chain(merged_json.iteritems(),
                                                  json_obj.iteritems()))
                except: #3
                    merged_json = dict(chain(merged_json.items(),
                                                  json_obj.items()))
            self.result = merged_json
        
        elif (self.output_format == 'tab2' or
              self.output_format == 'extendedTab2' or
              self.output_format == 'tab1'):
            self.result = ''.join(self.raw_result)
            
    
    def export(self, outdir=os.getcwd(), filename='biogridpy_response'):
        """
        To export the web service response as either a json or tab2 file file.
        
        Usage:
        >>>BG = BioGrid()
        >>>bg_results = BG.interactions('json', geneList='geneList.list')
        >>>bg_results.export(outdir='/home/user', filename='biogridpy_response')
        """

        suffix = self.output_format
        
        #json out includes headers in response
        if (self.output_format == 'json' or
            self.output_format == 'jsonExtended'):
            filepath = os.path.join(outdir, filename + "." + suffix)
            try:
                with open(filepath, 'w') as outfile:
                    json.dump(self._byteify2(self.result), outfile)
            except AttributeError:
                with open(filepath, 'w') as outfile:
                    json.dump(self._byteify3(self.result), outfile)
        #tab out need to add headers
        elif (self.output_format == 'tab2' or
              self.output_format == 'extendedTab2' or
              self.output_format == 'tab1'):
            filepath = os.path.join(outdir, filename + "." + suffix + ".txt")
            with open(filepath, 'w') as outfile:
                outfile.write('#' + '\t'.join(self.headers))
                outfile.write(self.result)
    
    def toDataFrame(self):
        """
        Converts the result object into pandas-friendly format.
        
        Usage:
        >>>BG = BioGrid()
        >>>bg_results = BG.interactions(geneList='genelist.txt', Format='json')
        >>> import pandas as pd
        >>>df = pd.read_json(bg_results.toDataFrame(), orient='index')
        
        >>>bg_results = BG.interactions(geneList='genelist.txt', Format='tab2')
        >>>import pandas as pd
        >>>df = pd.read_csv(bg_results.toDataFrame(), sep='\t')
        """
        if self.output_format in ('json', 'jsonExtended'):
            return json.dumps(self.result)
        
        elif self.output_format in ('tab2', 'extendedTab2'):
            return StringIO('\t'.join(self.headers) + self.result)
        
    def _byteify2(self, inpt):
        """
        Helper function, recursively keeps elements as strings.
        """
        if isinstance(inpt, dict):
            return {self._byteify2( key): self._byteify2(value)
                    for key, value in inpt.iteritems()}
        elif isinstance(inpt, list):
            return [self._byteify2(element) for element in inpt]
        elif isinstance(inpt, unicode):
            return inpt.encode('utf-8')
        else:
            return inpt
    
    def _byteify3(self, inpt):
        """
        Helper function, recursively keeps elements as strings.
        """
        if isinstance(inpt, dict):
            return {self._byteify3( key): self._byteify3(value)
                    for key, value in inpt.items()}
        elif isinstance(inpt, list):
            return [self._byteify3(element) for element in inpt]
        elif isinstance(inpt, str):
            return inpt
        else:
            return inpt