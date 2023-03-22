#!/usr/bin/python3

import zipfile # Library to extract zip files
import time # Library to control the time spent in the cracking process
import sys # Library to control the arguments of the script
import multiprocessing # Library to use multi-processing

def extract_zipfile(passwords, filezip, password_found):
    tries = 0
    # Loop through each password in the list
    for password in passwords:
        # Convert the password to bytes using the UTF-8 encoding
        codedpass = password.encode('utf-8')
        tries += 1
        try:
            # Try to extract the zipfile using the password
            filezip.extractall(pwd=codedpass)
        except:
            # If the password was incorrect, do nothing
            pass
        else:
            # If the password was correct, print a message and set the password_found flag to True
            password_found.value = True
            print("[+] Password Found: " + password)
            end_time = time.time()
            time_taken = end_time - start_time.value
            print("[+] Time taken: {:.2f} seconds".format(time_taken))
            print("[+] Tries: {}".format(tries))
            print("[+] Passwords tried per second: {:.2f}".format(tries/time_taken))
            return

if __name__ == '__main__':
    zfile = sys.argv[1]
    dfile = sys.argv[2]
    filezip = zipfile.ZipFile(zfile) # We used the zipfile library to open the zipped file.

    # Open the dictionary file and read the passwords
    with open(dfile, 'r') as passFile:
        passwords = passFile.read().splitlines()

    # Split the password list into smaller chunks
    num_processes = multiprocessing.cpu_count()
    chunk_size = int(len(passwords) / num_processes)
    password_chunks = [passwords[i:i+chunk_size] for i in range(0, len(passwords), chunk_size)]

    count = len(passwords)
    password_found = multiprocessing.Value('b', False)
    start_time = multiprocessing.Value('d', time.time())

    # Create a process for each password chunk and start them concurrently
    processes = []
    for password_chunk in password_chunks:
        p = multiprocessing.Process(target=extract_zipfile, args=(password_chunk, filezip, password_found))
        p.start()
        processes.append(p)

    # Wait for all processes to finish
    for p in processes:
        p.join()

    # Print the appropriate message based on whether the password was found or not
    if password_found.value:
        end_time = time.time()
        time_taken = end_time - start_time.value
        print("[+] Total Time {:.2f} seconds".format(time_taken))
    else:
        end_time = time.time()
        time_taken = end_time - start_time.value
        print("[-] Password not found. Attempted: {}. Time taken: {:.2f} seconds. Passwords tried per second: {:.2f}".format(count, time_taken, count/time_taken))
