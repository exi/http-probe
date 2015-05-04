import urllib.request
import time
import traceback
import sys

FILE_PATH = 'http://absolute.fail/50mb.bin'
MEASURE_FILE = 'measures.txt'
MEASURES_PER_HOUR = 4
MAX_DOWNLOAD_TIME = 60

SLEEP_TIME = (60 * 60) / MEASURES_PER_HOUR
print('downloading {} every {} seconds'.format(FILE_PATH, SLEEP_TIME))
sys.stdout.flush()


def run_download():
    start_time = time.time()
    last_time = start_time
    with urllib.request.urlopen(FILE_PATH) as req:
        measures = []

        while True:
            data = req.read(10240)
            measures.append((time.time() - last_time, len(data)))
            last_time = time.time()
            if req.isclosed() or (time.time() - start_time) > MAX_DOWNLOAD_TIME:
                break

    total_time = 0
    total_bytes = 0
    for t, b in measures:
        total_time += t
        total_bytes += b

    bytes_per_second = total_bytes/total_time
    return time.time() - start_time, bytes_per_second


def run():
    with open(MEASURE_FILE, 'a') as f:
        while True:
            next_measure = time.time() + SLEEP_TIME
            try:
                total_time, bytes_per_second = run_download()

                print('download took {}s, {}b/s'.format(total_time, bytes_per_second))
                sys.stdout.flush()
                print('{};{}'.format(round(time.time()), round(bytes_per_second)), file=f)
                f.flush()
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
                print("{};{}".format(round(time.time()), 0), file=f)
                f.flush()

            rest_sleep = max(0, next_measure - time.time())
            print('sleeping {}s'.format(round(rest_sleep)))
            sys.stdout.flush()
            time.sleep(rest_sleep)

if __name__ == '__main__':
    run()



