import pandas as pd  #depends
import os, json

class ResponseHandler(object):
    """
    pandas DataFrame object
    provides methods for exporting to file
    """
    def __init__(self, response, output_format):
        self.result = response
        self.output_format = output_format
    #def __repr__(self):
        #return 'ResultHandler(result=%s)' % (self.result)
    
    #def __str__(self):
        #return 'ResultHandler(result=%s)' % (self.result)
    
    def export(self, outdir=os.getcwd(), filename='biogridpy_response'):
        """
        To export the web service response as a file.
        
        Usage:
        >>>BG = BioGrid()
        >>>bg_results = BG.interactions(geneList='genelist.txt', Format='json')
        >>>bg_results.export(outdir='/home/user', fileame='biogridpy_response')
        """
        if self.output_format == 'json' or self.output_format == 'jsonExtended':
            suffix = self.output_format
            filepath = os.path.join(outdir, filename + "." + suffix)
            with open(filepath, 'w') as outfile:
                json.dump(self.result, outfile)
        
        elif self.output_format == 'tab2' or self.output_format == 'extendedTab2':
            suffix = self.output_format
            filepath = os.path.join(outdir, filename + "." + suffix)
            

            
    def toDataFrame(self):
        """
        To convert the response object to a pandas DataFrame.
        
        Usage:
        >>>BG = BioGrid()
        >>>bg_results = BG.interactions(geneList='genelist.txt', Format='json')
        >>>bg_results.toDataFrame(outdir='/home/user', fileame='biogridpy_response')
        """

