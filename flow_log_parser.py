from collections import defaultdict
import argparse

def parse_args():
    # Optional arguments to customize file paths
    args = argparse.ArgumentParser(description="Tool to parse flow log data")
    args.add_argument("--protocol_mapping_file", 
                      default="manifests/protocol_mapping.csv", 
                      type=str, 
                      help="File containing IANA Protocol numbers and names")
    args.add_argument("--lookup_file", 
                      default="manifests/lookup.csv", 
                      type=str, 
                      help="Lookup file containing the mapping between tags and combination of dstport, protocol")
    args.add_argument("--flow_log_file", 
                      default="manifests/flow_log.txt", 
                      type=str, 
                      help="Input file containing the flow log records")
    args.add_argument("--output_file", 
                      default="manifests/output.txt", 
                      type=str, 
                      help="Path to create output file")
    parse_args = args.parse_args()
    return parse_args

def protocol_mapping(protocol_mapping_file):
    # Load the protocol mapping from a CSV file
    protocol_map = {}
    with open(protocol_mapping_file, 'r') as f:
        next(f)
        for line in f:
            decimal, keyword = line.strip().split(',')
            protocol_map[decimal] = keyword.lower()
    return protocol_map

def load_lookup_table(lookup_file):
    # Load the lookup table into a dictionary
    lookup_table = {}
    with open(lookup_file, 'r') as f:
        next(f)
        for line in f:
            dstport, protocol, tag = line.strip().split(',')
            key = (dstport, protocol.lower())
            assert key not in lookup_table
            lookup_table[key] = tag
    return lookup_table

def process_flow_log_count(flow_log_file, protocol_map, lookup_table):
    # Initialize counters for tags and port/protocol combinations
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)

    # Process the flow log file
    with open(flow_log_file, 'r') as f:
        for line in f:
            fields = line.split()
            dstport = fields[6]
            protocol_number = fields[7]
            protocol = protocol_map[protocol_number]
            key = (dstport, protocol)
            if key in lookup_table:
                tag = lookup_table[key]
                tag_counts[tag] += 1
            else:
                tag_counts['Untagged'] += 1
            port_protocol_counts[(dstport, protocol)] += 1
    return tag_counts, port_protocol_counts

if __name__=='__main__':
    args = parse_args()
    protocol_map = protocol_mapping(args.protocol_mapping_file)
    lookup_table = load_lookup_table(args.lookup_file)
    tag_counts, port_protocol_counts = process_flow_log_count(
        args.flow_log_file, protocol_map, lookup_table)

    # Write the output file
    with open(args.output_file, 'w') as f:
        f.write('Tag Counts:\n')
        f.write('Tag,Count\n')
        for tag, count in tag_counts.items():
            f.write(f'{tag},{count}\n')
        f.write('\nPort/Protocol Combination Counts:\n')
        f.write('Port,Protocol,Count\n')
        for (port, protocol), count in port_protocol_counts.items():
            f.write(f'{port},{protocol},{count}\n')
