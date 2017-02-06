
"""Represent the Interface for
        Adapters that convert the Request DTO
        to machine learning features."""
class FeatureAdapterInterface(object):
    
    """ Return list of Integer"""
    def convert(self, requestDTO):
        raise NotImplementedError('Interface classess must implement this method')

        