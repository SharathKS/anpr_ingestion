"""Configuration for the anpr_ingestion service
"""

class ConfigBase:
    """Base config

    Define default values for all parameters.
    """

    # ---- expiry for vehicle data (days)
    #      If the expiry time is exceeded, the vehicle
    #      data is updated
    VEHICLE_DATA_EXPIRY = 7

class ConfigDevelopment(ConfigBase):
    """Config for development environments
    """
    pass

class ConfigStaging(ConfigBase):
    """Config for staging environments
    """
    pass

class ConfigTest(ConfigBase):
    """Config for test environments
    """
    pass

class ConfigProduction(ConfigBase):
    """Config for production environments
    """
    pass

# ---- specify required config file
#      TBA: do this dynamically as its not good practice to define
#      the config to use here
CFG = ConfigDevelopment
