import os
import psycopg2
import time

output_directory = '/Users/gpatel/Library/CloudStorage/Dropbox/Coursera/DL_in_Health/data/MimicIII/Patients/notes/'


def connect():
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host="localhost",
                                database="postgres",
                                user="postgres",
                                password="7452670")
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def disconnect(conn):
    if conn is not None:
        conn.close()
        print('Database connection closed.')



def do_db_query(conn, query):
    """ Connect to the PostgreSQL database server """
    try:
        # create a cursor
        cur = conn.cursor()

        # execute a statement
        #print('PostgreSQL database version:')
        cur.execute(query)#'SELECT version()')

        # display the PostgreSQL database server version
        ret = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()

        return ret
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_list_patient_id(conn):
    query = "select distinct(subject_id) from mimiciii.noteevents where subject_id > 51999 order by subject_id;"
    patients = do_db_query(conn, query)
    clean_patients = []
    for l in patients:
        clean_patients.append(l[0])
    return clean_patients


def write_notes(conn, folder, patient_id):
    output_file_name = os.path.join(str(folder), str(str(patient_id) + ".txt"))
    outfile = open(os.path.join(output_directory, output_file_name), 'w')
    query = "select string_agg(text, ' ') from mimiciii.noteevents group by subject_id having subject_id = " + str(patient_id) + ";"
    notes = do_db_query(conn, query)
    #print(notes[0])
    outfile.write('%s\n' % notes[0])
    outfile.close()


if __name__ == "__main__":

    conn = connect()

    patients = get_list_patient_id(conn)
    print(patients)

    for i in range(0, 99000, 1000):
        path = os.path.join(output_directory, str(i))
        if not os.path.exists(path):
            os.makedirs(path)

    i = 0
    #write_notes(11233)
    for patient in patients:
        folder = patient / 1000
        print(patient)
        write_notes(conn, folder*1000, patient)
        i = i + 1
        if i % 1000 == 0:
            print('sleeping')
            time.sleep(5)
    disconnect(conn)

