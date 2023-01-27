class ObservationType():
    def __init__(self,
                 name: str = None,
                 description: str = None,
                 link: str =None
                 ) -> None:
        self.name = name
        self.description = description
        self.link = link

class FeatureType():
    def __init__(self,
                 name: str = None,
                 description: str = None,
                 link: str =None
                 ) -> None:
        self.name = name
        self.description = description
        self.link = link

class ObservedProperty():
    def __init__(self,
                 name: str = None,
                 short_name: str = None,
                 standard_name: str = None,
                 units: str = None,
                 description: str = None,
                 link: str =None
                 ) -> None:
        self.name = name
        self.description = description
        self.short_name = short_name
        self.standard_name = standard_name
        self.units = units 
        self.link = link

class ObservingProcedure():
    def __init__(self,
                 name: str = None,
                 description: str = None,
                 link: str =None
                 ) -> None:
        self.name = name
        self.description = description
        self.link = link


class RecordStatus():
    def __init__(self,
                 name: str = None,
                 description: str = None
                 ) -> None:
        self.name = name
        self.description = description

class Station():
    pass

class Sensor():
    pass

class Observation():
    pass

class Collection():
    pass

class Feature():
    pass

class User():
    pass

class  StationRole():
    pass