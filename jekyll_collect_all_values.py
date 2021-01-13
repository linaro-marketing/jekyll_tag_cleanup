import frontmatter
import os
import re
import argparse
import yaml

parser = argparse.ArgumentParser(description='Collect all values for a specific front matter key.')
parser.add_argument('posts', metavar='P', help='The full path to your posts root. All subdirectories are included.')
parser.add_argument('tag', metavar='T', help='The yaml key to colect all values for e.g session_track')
parser.add_argument('outfile', metavar='O', help='The name of the file to write tags to.')
args = parser.parse_args()

def collect_all_values(root, tag):
    file_list = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if name.endswith((".markdown", ".md")):
                file_list.append(os.path.join(path, name))
    all_values = []
    for file in file_list:
        print("Processing {}...".format(file))
        try:
            post = frontmatter.load(file)
            if tag in post:
                current_value = post[tag]
                all_values.append(current_value)
        except yaml.scanner.ScannerError as e:
            print("Skipping file since yaml is not formatted correctly...")
        
    return all_values


def write_to_new_line_file(values, tags_file):
    """ Writes the array to a new line separated file"""
    split_on_comma_vals = []
    for val in values:
        if "," in val:
            split_vals = val.split(",")
            for split_val in split_vals:
                split_on_comma_vals.append(split_val)
        else:
            split_on_comma_vals.append(val)
    duplicates_removed = []
    for tag in split_on_comma_vals:
        if tag not in duplicates_removed:
            duplicates_removed.append(tag)
    with open(tags_file, "w+") as new_file:
        for val in duplicates_removed:
            new_file.write(val.strip(" ") + "\n")    
if __name__ == "__main__":
    all_values = collect_all_values(args.posts, args.tag)
    print(all_values)
    write_to_new_line_file(all_values, args.outfile)