import concurrent.futures


def do(a):
    return (f'hrello {a}')


with concurrent.futures.ThreadPoolExecutor() as executor:
    f1 = executor.submit(do, 'abhi')
    print(f1.result())
