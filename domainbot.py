import threading
import queue
import whois
from tqdm import tqdm

# Generate a queue of all possible 3-letter/number domain names
domains_queue = queue.Queue()
for i in range(48, 58):
    for j in range(48, 58):
        for k in range(48, 58):
            domain = chr(i) + chr(j) + chr(k) + ".com"
            domains_queue.put(domain)
for i in range(97, 123):
    for j in range(97, 123):
        for k in range(97, 123):
            domain = chr(i) + chr(j) + chr(k) + ".com"
            domains_queue.put(domain)
for i in range(97, 123):
    for j in range(48, 58):
        for k in range(97, 123):
            domain = chr(i) + chr(j) + chr(k) + ".com"
            domains_queue.put(domain)

# Function to check the availability of a domain name
def check_domain_availability(pbar, available_domains_file):
    while True:
        # Get a domain name from the queue
        domain_name = domains_queue.get()
        try:
            # Check the availability of the domain name using the `whois` library
            w = whois.whois(domain_name)
            pbar.update(1)
            pbar.set_description("Checking %s" % domain_name)
            # Print the status of the domain name
            print("Domain", domain_name, "is already registered.")
        except whois.parser.PywhoisError:
            # Save the available domain name to a file
            available_domains_file.write(domain_name + '\n')
            pbar.update(1)
            pbar.set_description("Checking %s" % domain_name)
            # Print the status of the domain name
            print("Domain", domain_name, "is available for registration!")
        # Mark the task as done in the queue
        domains_queue.task_done()

# Open a file to save available domains
with open("available.txt", "w") as f:
    # Create a progress bar
    with tqdm(total=10**6, desc="Checking domains") as pbar:
        # Start multiple threads to check the availability of the domain names
        for i in range(10):
            t = threading.Thread(target=check_domain_availability, args=(pbar, f))
            t.daemon = True
            t.start()

        # Wait for all tasks to be completed
        domains_queue.join()

# Print a message indicating that the available domains have been saved to a file
print("The available domains have been saved to available.txt")
