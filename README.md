# jekyll_tag_cleanup

Ever worked on a huge Jekyll site with a tag problem that is out of control? Never fear `jekyll_tag_cleanup` is here!

## Requirements

- python3
- A Jekyll site with loads of tags

Clone this repository:

```bash
git clone git@github.com:linaro-marketing/jekyll_tag_cleanup.git
```

`cd` into the directory:

```bash
cd jekyll_tag_cleanup
```

Create a newline separate list of your desired tags e.g `allowed_tags.txt`:

```yaml
UEFI
upstream
upstreaming
validation
VFIO
VirtIO
Virtual Connect 2020
virtual event
Virtualization
VM
```

Run the `jekyll_tag_cleanup` script over your posts directory for a clean start! Provide the full path to your `_posts` directory and to your new allowed tags:

```bash
python3 jekyll_tag_cleanup.py ${pwd}_posts/ ${pwd}allowed_tags.txt
```
