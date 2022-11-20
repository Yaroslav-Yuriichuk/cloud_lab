import sqlalchemy

headers = {
    'Access-Control-Allow-Origin': '*'
}

cache_headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600'
}


def add_data(request):
    if request.method == 'OPTIONS':
        return '', 204, cache_headers

    insert_query = sqlalchemy.text('insert into lab2.sensors ({}) values ({})'.format(
        ', '.join(map(str, request.get_json())),
        ', '.join(map(str, request.get_json().values()))
    ))

    db = sqlalchemy.create_engine('mysql+pymysql://root:pass1234@10.100.96.3:3306/lab2?unix_socket=/cloudsql/fluted-gantry-367015:europe-west1:lab2',
                                  pool_size=5,
                                  max_overflow=2,
                                  pool_timeout=30,
                                  pool_recycle=1800)
    try:
        with db.connect() as conn:
            conn.execute(insert_query)
            return 'Success', 201, headers
    except Exception as e:
        return f'Error: {e}', 500, headers
