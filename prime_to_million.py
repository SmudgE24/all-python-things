file_path = '/home/pi/Documents/primes_to_1000000.csv'

def find_primes(limit):
    primes = [True] * (limit + 1)
    primes[0] = primes[1] = False
    
    for num in range(2, int(limit ** 0.5) + 1):
        if primes[num]:
            for multiple in range(num * num, limit + 1, num):
                primes[multiple] = False
                
    return [num for num in range(2, limit + 1) if primes[num]]

primes_up_to_million = find_primes(1000000)
#print(primes_up_to_million)
outfile = open(file_path, 'a')
outfile.write(str(primes_up_to_million))

