# RPTree - Directory Tree Generator

A simple directory tree generator based on the tutorial by [realpython.com](https://realpython.com/directory-tree-generator-python/)

# Usage
first clone the repository and then type in a terminal:
```
python /path-to-repo-dir/tree.py ROOT_DIR
```
where ROOT_DIR is the relative path to the directory for which you want to create a directory tree.

also to print a help in the command line you can type:
```
python /path-to-repo-dir/tree.py -h
```

# TODO

- Add support for sorting files and directories:
    - e.g. Add -s and --sort-tree Boolean flags to allow the user to tweak the order of files and directories in the final tree diagram.

- Add icons and colors to the tree diagram:
    - Adding icons (add custom folder icons for dirs and type-based icons for the files),
    - adding font colors,