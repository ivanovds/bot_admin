import psycopg2
from tg_bot import config

error_report_to_chat = '🆘 Error with: %s'


def touch_db(query, params=None, save=False, returning=False):
    """
    Communicates with db

    :param query: str or list, SQL query or list of SQL query's
    :param params: dict/list, parameters for the query
    :param save: bool, True if necessary to save the query changes in database, False otherwise
    :param returning: bool, True if query have to return something, False otherwise
    :return: bool or list, result of the query
    """
    with psycopg2.connect(config.DBP) as conn:
        with conn.cursor() as cur:
            if type(query) == str:
                cur.execute(query, params)
            elif type(query) == list:
                for part in query:
                    cur.execute(part)
            else:
                raise ValueError(f'query type should be str or list, not {type(query)}')
            if save:
                conn.commit()
                if returning:
                    return cur.fetchall()
                else:
                    return True
            else:
                return cur.fetchall()
