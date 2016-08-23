import os

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


DATABASE_ENGINE_SCHEMES = {
    "postgres": "django.db.backends.postgresql_psycopg2",
    "postgresql": "django.db.backends.postgresql_psycopg2",
    "pgsql": "django.db.backends.postgresql_psycopg2",
    "postgis": "django.contrib.gis.db.backends.postgis",
    "mysql": "django.db.backends.mysql",
    "mysql2": "django.db.backends.mysql",
    "mysqlgis": "django.contrib.gis.db.backends.mysql",
    "mysql-connector": "mysql.connector.django",
    "spatialite": "django.contrib.gis.db.backends.spatialite",
    "sqlite": "django.db.backends.sqlite3",
    "oracle": "django.db.backends.oracle",
    "oraclegis": "django.contrib.gis.db.backends.oracle",
}

for scheme in DATABASE_ENGINE_SCHEMES.keys():
    urlparse.uses_netloc.append(scheme)


def db(key="DATABASE_URL", default="", **kwargs):
    config = {}
    url = os.environ.get(key, default)
    if url:
        config = db_url_parse(url, **kwargs)
    return config


def db_url_parse(url, engine=None, conn_max_age=0):
    """
    Parses a database URL.
    """
    if url == "sqlite://:memory:":
        # urlparse will choke on :memory:
        return {
            "ENGINE": DATABASE_ENGINE_SCHEMES["sqlite"],
            "NAME": ":memory:",
        }

    config = {}
    url = urlparse.urlparse(url)

    # split query strings from path
    path = url.path[1:]
    if "?" in path and not url.query:
        path, query = path.split("?", 2)
    else:
        path, query = path, url.query
    query = urlparse.parse_qs(query)

    # sqlite with no path should assume :memory: (sqlalchemy behavior)
    if url.scheme == "sqlite" and path == "":
        path = ":memory:"

    # handle postgresql percent-encoded paths
    hostname = url.hostname or ""
    if "%2f" in hostname.lower():
        hostname = hostname.replace("%2f", "/").replace("%2F", "/")

    config.update({
        "NAME": urlparse.unquote(path or ""),
        "USER": urlparse.unquote(url.username or ""),
        "PASSWORD": urlparse.unquote(url.password or ""),
        "HOST": hostname,
        "PORT": url.port or "",
        "CONN_MAX_AGE": conn_max_age,
    })

    engine = DATABASE_ENGINE_SCHEMES[url.scheme] if engine is None else engine

    # pass the query string into OPTIONS
    options = {}
    for key, values in query.items():
        if url.scheme == "mysql" and key == "ssl-ca":
            options["ssl"] = {"ca": values[-1]}
            continue
        options[key] = values[-1]

    # postgresql schema URLs
    if "currentSchema" in options and engine == "django.db.backends.postgresql_psycopg2":
        options["options"] = "-c search_path={0}".format(options["currentSchema"])

    if options:
        config["OPTIONS"] = options
    if engine:
        config["ENGINE"] = engine

    return config
