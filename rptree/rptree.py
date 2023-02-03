# rptree.py
"""This module provides RP Tree main module."""
import os
import sys
import pathlib
from collections import deque

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


class DirectoryTree:
    def __init__(self, root_dir, dir_only=False, output_file=sys.stdout):
        self.root_dir = root_dir
        self._output_file = output_file

        self._generator = _TreeGenerator(root_dir, dir_only)


    def generate(self):
        tree = self._generator.build_tree()
        if self._output_file != sys.stdout:
            # Wrap the tree in a markdown code block
            tree.appendleft(f"Tree of ```{os.path.abspath(self.root_dir)}```:\n```") 
            tree.append("```")
            self._output_file = open(
                self._output_file, mode="w", encoding="UTF-8"
            )
        with self._output_file as stream:
            for entry in tree:
                print(entry, file=stream)


class _TreeGenerator:
    def __init__(self, root_dir, dir_only=False):
        self._root_dir = pathlib.Path(root_dir)
        self._dir_only = dir_only

        self._tree = deque() # creates a deque for the tree instead of a list
    
    def build_tree(self) -> list:
        """This public method generates and returns the directory tree diagram.

        Returns:
            list : the created directory tree diagram
        """
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree
    
    def _tree_head(self):
        """ This method adds the name of the root directory to ._tree. 
            Then you add a PIPE to connect the root directory to the rest of the tree.
        """
        self._tree.append(f'{self._root_dir}/')
        self._tree.append(PIPE) 
    
    def _tree_body(self, directory, prefix=""):
        """It takes a directory path as an argument, traverses the file system under that directory, 
           and generates the corresponding directory tree diagram.

        Args:
            directory (string): the os path to the root directory
            prefix (str, optional): holds a prefix string that is used to draw the tree diagram on the terminal window. 
                                    This string helps to show up the position of the directory or file in the file system. 
                                    Defaults to "".
        """
        # creates a generator from the pathlib.Path objects of the root directory
        entries = self._prepare_entries(directory)
        # sorts the directories alphabetically with putting the directories before the files
        # To do this, you create a lambda function that checks if entry is a file and returns True or False accordingly. 
        # In Python, True and False are internally represented as integer numbers, 1 and 0, respectively. 
        # The net effect is that sorted() places the directories first because 
        # entry.is_file() == False == 0 and the files after them because 
        # entry.is_file() == True == 1.
        entries = sorted(entries, key=lambda entry: entry.is_file())
        # counts the number of entries in the current level of the tree
        entries_count = len(entries)
        for index, entry in enumerate(entries): 
            # if the current entry is the last in the directory (index == entries_count - 1), 
            # then you use an elbow (└──) as a connector. 
            # Otherwise, you use a tee (├──).
            connector = ELBOW if index == entries_count - 1 else TEE

            if entry.is_dir():
                self._add_directory(entry, index, entries_count, prefix, connector)
            else:
                self._add_file(entry, prefix, connector)
    
    def _prepare_entries(self,directory):
        """method that if a dir_only flag is raised discards files from the tree

        Args:
            directory (pathlib.Path object): the directory for which to create the tree

        Returns:
            pathlib.Path object: the trimmed or not generator with the entries of the directory tree
        """
        entries = directory.iterdir()
        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()]
            return entries
        entries = sorted(entries, key=lambda entry: entry.is_file())
        return entries

    def _add_directory(self, directory, index, entries_count, prefix, connector):

        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")
        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        self._tree_body(directory=directory,
                        prefix=prefix,
                        )
        # self._tree.append(prefix.rstrip()) # creates vertical space between different directories

    def _add_file(self, file, prefix, connector):
        """This method appends a file entry to the directory tree list.

        Args:
            file (pathlib.Path object): the file as a pathlib.Path object to be addded to the the directory tree
            prefix (str): the default prefix to be added before the connector
            connector (str): the connector for the file
        """
        self._tree.append(f"{prefix}{connector} {file.name}")