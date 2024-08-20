# flow-log-parser
This parser processes flow log data and generates a report with tag counts and port/protocol combination counts.

## How to run the parser:
- `python flow_log_parser.py`
- Can also provide optional command line arguments to customize the file paths. To view more information on this
`python flow_log_parser.py -h`
- The arguments supported are -
    | Argument Name | Description | Default |
    | ------------------------ | -------------------- | ------------------- |
    | protocol_mapping_file  | File containing IANA Protocol numbers and names | manifests/protocol_mapping.csv |
    | lookup_file  | Lookup file containing the mapping between tags and combination of dstport, protocol | manifests/lookup.csv |
    | flow_log_file  | Input file containing the flow log records | manifests/flow_log.txt |
    | output_file  | Path to create output file | manifests/output.txt |
- The arguments can be passed as `python flow_log_parser.py --protocol_mapping_file=<file_path> --lookup_file=<file_path> --flow_log_file=<file_path> --output_file=<file_path>`

## Assumptions:
- The program only supports default log format, not custom and the only version 
that is supported is 2. 
- Lookup table and protocol_mapping tables can be .csv or .txt files.
- The protocol number in each of the flow logs is mapped to the respective protocol name using the protocol_mapping.csv file. This file has been downloaded from [Internet Assigned Protocol Numbers](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml) as guided by [AWS Docs - Flow Log Records](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html)
- A tag can map to more than one port, protocol combination but each port, protocol combination is mapped only to one tag.
- The columns in the lookup table are always in the same order - dstport, protocol, tag.
- The columns in the protocol_mapping table are always in the same order - decimal, keyword.
- The lookup and protocol_mapping table fields are processed by splitting using ',' delimitter. Therefore, it is assumed that ',' is used only as a delimitter but not as a character within any of the fields.
- The flow log file is assumed to be using space as a delimitter between columns.
- Each of the rows in the lookup table have fields which are comma separated.
- The first row of lookup and protocol_mapping tables are assumed to have headers.
- The count of matched for port/protocol combinations outputs the count for all unique port/protocol combinations in the flow logs.

## Tests

The parser has been tested with the following input files:
- protocol_mapping.csv/protocol_mapping.txt: A file containing the IANA Protocol numbers and names.
- lookup.csv/lookup.txt: A file containing the mapping between tags and the combination of dstport and protocol.
- flow_log.txt: A file containing the flow log records.
- output.txt: The output file created after running the parser

## Analysis

The `protocol_mapping()` function loads the protocol mapping from a csv/txt file and stores it in a dictionary.
The `load_lookup_table()` function loads the lookup table from a csv/txt file and stores it in a dictionary.
The `process_flow_log_count()` function processes the flow log file and generates the tag counts and port/protocol combination counts. It uses a defaultdict to store the counts.

The parser has the following performance characteristics:

- The time complexity of the `protocol_mapping()` function is O(n), where n is the number of rows in the protocol mapping file.
- The time complexity of the `load_lookup_table()` function is O(n), where n is the number of rows in the lookup table file.
- The time complexity of the `process_flow_log_count()` function is O(n), where n is the number of rows in the flow log file.

The parser has the following memory usage characteristics:

- The space complexity of the `protocol_mapping()` function is O(n), where n is the number of rows in the protocol mapping file.
- The space complexity of the `load_lookup_table()` function is O(n), where n is the number of rows in the lookup table file.
- The space complexity of the `process_flow_log_count()` function is O(n), where n is the number of rows in the flow log file.

