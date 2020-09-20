class MidasFilters(CDMSFilters):
    """
    NOTE: The filter dictionary will be replaced by a MidasFilters class
          that will inherit from a `CDMSFilters` abstract base class.
          The validation code in MidasOpen.obs will move to methods here.
    """


class CDMSFilters(ABS):
    """Generic ABC for the implementation of CDMS Filters"""

    pass
