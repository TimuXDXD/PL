from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from datetime import datetime

def divider(x,n):
    res = []
    for i in range(x):
        temp = []
        for j in range(int(i*(n/x))+1,int((i+1)*(n/x))+1):
            temp.append(j)
        res.append(temp)
    return res

def print_split():
    for _ in range(20):
        print('=',end="")
    print()

def count(start, n):
    sum = 0
    for i in range(start,int(n)+1):
        sum += i
    return sum

def count_multi(temp):
    sum = 0
    for i in range(len(temp)):
        sum += temp[i]
    return sum

def count_by_single_thread(start,n):
    print('Single Thread Start:')
    print_split()
    start_time = datetime.now()
    sum = count(start,n)
    end_time = datetime.now()
    time = (end_time - start_time).total_seconds()
    print('Sum: {}'.format(sum))
    print('Time spent:{:.6f}s'.format(time))
    print_split()
    return time

def count_by_multi_thread(x,n):
    split_x = divider(x,n)
    sum = 0
    futures = []
    thread_res = [0] * x
    thread_start_time = [0] * x
    print('Multi Thread Start:')
    print_split()
    start_time = datetime.now()
    with ThreadPoolExecutor(max_workers=x) as executor:
        for i in range(len(split_x)):
            thread_start_time[i] = datetime.now()
            future = executor.submit(count_multi,split_x[i])
            print('Thread {} is start.'.format(i))
            futures.append(future)
        for future in as_completed(futures):
            thread_end_time = datetime.now()
            print('Thread {} is done.({:.6f}s)'.format(futures.index(future),(thread_end_time - thread_start_time[futures.index(future)]).total_seconds()))
            thread_res[i] = future.result()
            sum += future.result()
    end_time = datetime.now()
    time = (end_time - start_time).total_seconds()
    print('Sum: {}'.format(sum))
    print('Time spent:{:.6f}s'.format(time))
    print_split()
    return time

if __name__ == '__main__':
    x = int(float(input("Input thread number:")))
    n = int(float(input("Input n:")))
    print()
    single_time = count_by_single_thread(1,n)
    print()
    multi_time = count_by_multi_thread(x,n)
    print('Multi is {:.6f} times faster than Single.'.format(single_time/multi_time))
