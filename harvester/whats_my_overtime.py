import getopt
import sys

from harvest_overtime import get_overtime


def main(argv):
    user_id = ''
    user_name = ''
    password = ''
    from_date = '20160101'
    to_date = '20161231'
    try:
        opts, args = getopt.getopt(argv, "hf:t:i:u:p:", ["fromDate=", "toDate=", "userId=", "username", "password"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--userId"):
            user_id = arg
        elif opt in ("-u", "--username"):
            user_name = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-f", "--fromDate"):
            from_date = arg
        elif opt in ("-t", "--toDate"):
            to_date = arg
    get_overtime(from_date, to_date, user_id, user_name, password)


def usage():
    print 'whats_my_overtime.py -i <userId> -u <username> -p <password> [-f <fromDate>] [-t <toDate>]'


if __name__ == "__main__":
    main(sys.argv[1:])
