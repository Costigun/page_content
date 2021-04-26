from db import pg_db,Page,PageContent

pg_db.connect()
pg_db.create_tables([Page,PageContent])
