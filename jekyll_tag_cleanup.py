import frontmatter
import os
import re
import argparse

parser = argparse.ArgumentParser(description='Cleanup Jekyll post tags that have gone crazy!')
parser.add_argument('posts', metavar='P', help='The full path to your posts root. All subdirectories are included.')
parser.add_argument('tags', metavar='T', help='Path to newline-separated allowed tags.')
args = parser.parse_args()

def get_allowed_tags(tags_path):
    dirty_tags = []
    clean_allowed_tags = []
    with open(tags_path) as my_new_tags_file:
        for line in my_new_tags_file:
            dirty_tags.append(line.rstrip("\n"))
    # Cleanup the new tags and remove duplicates / capitalize appropriately
    for tag in dirty_tags:
        exceptions = ["and", "or", "the", "a", "of", "in"]
        lowercase_words = re.split(" ", tag)
        lowercase_words = [word if word.isupper() or any(x.isupper() for x in word) else word.lower() for word in lowercase_words]
        final_words = [lowercase_words[0].capitalize() if lowercase_words[0].islower() else lowercase_words[0]]
        final_words += [word if word in exceptions else word.capitalize() for word in lowercase_words[1:]]
        final_tag = " ".join(final_words)
        # remove duplicates!!!
        found_duplicate = False
        for tag in clean_allowed_tags:
            if final_tag.lower() == tag.lower():
                found_duplicate = True
        if not found_duplicate:
            clean_allowed_tags.append(final_tag)
    return clean_allowed_tags

def replace_tags_in_posts(root, allowed_tags):
    file_list = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if name.endswith((".markdown", ".md")):
                file_list.append(os.path.join(path, name))
    # Open each markdown file found and get the current list of tags
    for file in file_list:
        print("Processing {}...".format(file))
        post = frontmatter.load(file)
        if "tags" in post:
            current_post_tags = post["tags"]
            new_post_tags = []
            for post_tag in current_post_tags:
                # Loop over current tags
                for allowed_tag in allowed_tags:
                    if post_tag.lower() == allowed_tag.lower():
                        new_post_tags.append(allowed_tag)
            print("Current Tags:", current_post_tags)
            print("Replacing with:", new_post_tags)
            post["tags"] = new_post_tags
        # write new tags to file
        with open(file, "w+") as new_post_file:
            new_post_file.writelines(frontmatter.dumps(post, sort_keys=False))
                    

    

if __name__ == "__main__":
    allowed_tags = get_allowed_tags(args.tags)
    replaced = replace_tags_in_posts(args.posts, allowed_tags)