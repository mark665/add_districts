DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'adddistricts',                      # Or path to database file if using sqlite3.
        'USER': 'glusenkamp',                      # Not used with sqlite3.
        'PASSWORD': 'myPassword' ,          # See imports above
        'HOST': 'ec2-23-21-20-184.compute-1.amazonaws.com', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

