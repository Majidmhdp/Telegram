import psycopg2
import datetime

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="mydb",
    user="admin",
    password="admin123"
)

cursor = conn.cursor()
print("✅ Connected to TimescaleDB successfully!")


def create_time_scale_table():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS channel_messages (
        id SERIAL PRIMARY KEY,
        channel_id BIGINT NOT NULL,
        message_id BIGINT NOT NULL,
        message_text TEXT,
        message_date TIMESTAMPTZ NOT NULL
    );
    '''
    cursor.execute(create_table_query)
    # cursor.execute("SELECT create_hypertable('sensor_data', 'time', if_not_exists => TRUE);")
    conn.commit()
    print("✅ Table 'channel_messages' is ready.")



def insert_message(channel_id, message_id, message_text, message_date):
    # now = datetime.datetime.utcnow()
    insert_query = '''
    INSERT INTO channel_messages (channel_id, message_id, message_text, message_date)
    VALUES (%s, %s, %s, %s);
    '''

    cursor.execute(insert_query, (channel_id, message_id, message_text, message_date))
    conn.commit()
    print(f"✅ Inserted message {message_id} from channel {channel_id}.")


def retrieve_messages(channel_id, limit=10):
    select_query = '''
    SELECT message_id, message_text, message_date
    FROM channel_messages
    WHERE channel_id = %s
    ORDER BY message_date DESC
    LIMIT %s;
    '''

    cursor.execute(select_query, (channel_id, limit))
    rows = cursor.fetchall()
    return rows

def retrieve_messages_by_timebucket(channel_id, start_time, end_time):
    select_query = '''
    SELECT time_bucket('1 hour', message_date) AS bucket,
           COUNT(*) AS message_count
    FROM channel_messages
    WHERE channel_id = %s AND message_date BETWEEN %s AND %s
    GROUP BY bucket
    ORDER BY bucket;
    '''

    cursor.execute(select_query, (channel_id, start_time, end_time))
    rows = cursor.fetchall()
    return rows

def retrieve_first_last_message(channel_id):
    cursor.execute("""
    SELECT channel_id,
           first(message_id, message_date) AS first_temp,
           last(message_id, message_date) AS last_temp
    FROM channel_messages
    GROUP BY channel_id;
    """)

    for channel_id, first_temp, last_temp in cursor.fetchall():
        print(f"Sensor {channel_id}: first={first_temp}, last={last_temp}")


def retrieve_percentile_messages(channel_id, percentile):
    select_query = '''
    SELECT approx_percentile(0.5, temperature) AS median_temp
    FROM channel_messages;
    '''

    cursor.execute(select_query, (percentile, channel_id))
    result = cursor.fetchone()
    return result[0] if result else None


def close_connection():
    cursor.close()
    conn.close()
    print("🔌 Connection to TimescaleDB closed.")
