import dns.asyncresolver
import asyncio

async def query_doh(domain, doh_server, log_file):
    try:
        resolver = dns.asyncresolver.Resolver()
        resolver.nameservers = [doh_server]
        result = await resolver.resolve(domain, 'A')

        # Log
        with open(log_file, 'a') as log:
            log.write(f"Results for {domain} from {doh_server}:\n")
            for ip in result:
                log.write(f"  IP Address: {ip.address}\n")

    except dns.resolver.NoNameservers as e:
        with open(log_file, 'a') as log:
            log.write(f"No nameservers available for {domain} from {doh_server}: {e}\n")

    except dns.exception.DNSException as e:
        with open(log_file, 'a') as log:
            log.write(f"Error querying {domain} from {doh_server}: {e}\n")

async def main():
    domains_to_query = ['example.com', 'google.com', 'brainwareuniversity.ac.in']
    doh_server = 'https://localhost/dns-query'
    log_file = 'dns_query_log.txt'
    await asyncio.gather(*(query_doh(domain, doh_server, log_file) for domain in domains_to_query))

if __name__ == "__main__":
    asyncio.run(main())

