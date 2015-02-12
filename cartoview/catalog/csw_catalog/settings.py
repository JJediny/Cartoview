ADMINS = (
     ('OpenData Admins', 'admin@example.org'),
)
SITEHOST = 'localhost'
# the port which the deployment runs on
SITEPORT = 8000
SITE_URL = "http://127.0.0.1:8000/catalog"
# pycsw configuration
CSW = {
    'metadata:main': {
        'identification_title': 'Open Data Catalog CSW',
        'identification_abstract': 'Open Data Catalog is an open data catalog based on Django, Python and PostgreSQL. It was originally developed for OpenDataPhilly.org, a portal that provides access to open data sets, applications, and APIs related to the Philadelphia region. The Open Data Catalog is a generalized version of the original source code with a simple skin. It is intended to display information and links to publicly available data in an easily searchable format. The code also includes options for data owners to submit data for consideration and for registered public users to nominate a type of data they would like to see openly available to the public.',
        'identification_keywords': 'odc,Open Data Catalog,catalog,discovery',
        'identification_keywords_type': 'theme',
        'identification_fees': 'None',
        'identification_accessconstraints': 'None',
        'provider_name': ADMINS[0][0],
        'provider_url': 'https://github.com/azavea/Open-Data-Catalog',
        'contact_name': ADMINS[0][0],
        'contact_position': ADMINS[0][0],
        'contact_address': 'TBA',
        'contact_city': 'City',
        'contact_stateorprovince': 'State',
        'contact_postalcode': '12345',
        'contact_country': 'United States of America',
        'contact_phone': '+01-xxx-xxx-xxxx',
        'contact_fax': '+01-xxx-xxx-xxxx',
        'contact_email': ADMINS[0][1],
        'contact_url': 'https://github.com/azavea/Open-Data-Catalog/',
        'contact_hours': '0800h - 1600h EST',
        'contact_instructions': 'During hours of service.  Off on weekends.',
        'contact_role': 'pointOfContact',
    },
}