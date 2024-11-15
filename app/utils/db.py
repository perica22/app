
def make_connection_string(config):
    """
    :param config: Configuration object
    :type config: Config
    :return:
        Connection string suitable for usage in sqlalchemy based on values
        from provided configuration.
    :rtype: str
    """
    params = {'driver': 'postgresql+psycopg2'}
    params.update(config.get('database'))
    if params.get('ssl', False):
        params['ssl'] = '?sslmode=require'
    else:
        params['ssl'] = ''
    conn_str_template = ('{driver}://{username}:{password}@'
                         '{host}:{port}/{database}{ssl}')

    return conn_str_template.format(**params)