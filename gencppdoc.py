''' Generate blank docstrings for all functions and classes in CPP source file '''

import os
import sys
import argparse
import subprocess

import clang.cindex as cl
from collections import namedtuple
from collections import OrderedDict

llvm_lib_path = subprocess.check_output(['llvm-config', '--libdir']) ## hacky bit to ensure we are loading the correct libclang.so
cl.Config.set_library_path(llvm_lib_path.decode('utf-8')[0:-1])

type_mapping = {
  cl.CursorKind.CONSTRUCTOR: "function",
  cl.CursorKind.DESTRUCTOR: "function",
  cl.CursorKind.CXX_METHOD: "function",
  cl.CursorKind.FUNCTION_DECL: "function",
  cl.CursorKind.FUNCTION_TEMPLATE: "function",
  cl.CursorKind.CLASS_TEMPLATE: "class",
  cl.CursorKind.CLASS_DECL: "class",
  cl.CursorKind.STRUCT_DECL: "class",
}


''' Dump node information '''
def node_dump(n):
  print(n.type, n.name, n.line, n.func_args, n.ret_type)

''' Build a docstring from a Node '''
class DocStringBuilder():
  ''' Initialize doc_string_builder; creates empty string'''
  def __init__(self):
    self.outstring = ''

  ''' Build a docstring from a Node '''
  def build(self, n):
    self.add_doc_begin()
    if n.type == 'class':
      self.add_class_tag(n)
      self.add_brief(True)
    else:
      if n.type == 'function':
        self.add_brief(False)
        self.add_params(n)
        self.add_return(n)
    self.add_doc_end()
    return self
  
  ''' Get the docstring from this instance '''
  def get(self):
    return self.outstring

  ''' Add the \class tag to the docstring '''
  def add_class_tag(self, n):
    self.outstring += '\\class ' + n.name + '\n'

  ''' Add the \brief tag to the docstring '''
  def add_brief(self, is_class):
    if is_class: self.outstring += ' *  '
    self.outstring += '\\brief \n'

  ''' Add all \param tags to the docstring '''
  def add_params(self, n):
    for param in n.func_args:
      self.outstring += ' *  \\param ' + param + '\n'

  ''' Add the \return tag to the docstring '''
  def add_return(self, n):
    if n.ret_type != 'void':
      self.outstring += ' *  \\return\n'

  ''' Add docstring initilizer to the docstring '''  
  def add_doc_begin(self):
    self.outstring = '/** '

  ''' Add docstring terminator to the docstring '''
  def add_doc_end(self):
    self.outstring += ' */\n'

  ''' Clear the internal string; ready to build new docstring '''
  def clear(self):
    self.outstring = ''

''' Doc writer to parse a file and generate doc nodes for writing '''
class CppDocWriter():
  ''' Initialize a CppDocWriter '''
  def __init__(self, filename):
    self.filename = filename
    self.src_file = open(filename, 'r')
    self.file_data = self.src_file.readlines()
    self.file_nodes = self.parse()  

  ''' Parse a source file using libclang to get information about the nodes in this file '''
  def parse(self):
    index = cl.Index.create()
    tu = index.parse(self.filename, '64')
    children = tu.cursor.walk_preorder()
    
    nodes = list()

    for src_node in children:
      if src_node.kind in type_mapping.keys() and src_node.location.file.name == self.filename:
        if type_mapping[src_node.kind] == 'function':
          arg_list = [arg.displayname for arg in src_node.get_arguments()]
          nodes.append(Node('function', src_node.spelling, src_node.location.line if src_node.kind != cl.CursorKind.FUNCTION_TEMPLATE else src_node.location.line - 1, arg_list, src_node.result_type.spelling))
        elif type_mapping[src_node.kind] == 'class':
          nodes.append(Node('class', src_node.spelling, src_node.location.line if src_node.kind != cl.CursorKind.CLASS_TEMPLATE else src_node.location.line - 1, [], src_node.result_type.spelling))

    return nodes

  ''' Write the doc strings where their CursorKind was found in source file adding a padding space above'''
  def write(self):
    dsb = DocStringBuilder()
    docstrings = OrderedDict()

    for n in self.file_nodes:
      docstrings[n.line] = dsb.build(n).get()
      dsb.clear()

    for line, doc in reversed(docstrings.items()):
      indent = len(self.file_data[line-1]) - len(self.file_data[line-1].lstrip())
      line_counter = line-1
      for doc_line in doc.splitlines(True):
        self.file_data.insert(line_counter, ' '*indent  + doc_line)
        line_counter += 1
      self.file_data.insert(line-1, '\n')

    os.rename(self.filename, self.filename + '.bak')

    with open(self.filename, 'w') as outfile:
      for line in self.file_data:
        outfile.write(line)
    

def main():
  parser = argparse.ArgumentParser(description='Generate blank docstrings for all functions and classes in CPP source file')
  parser.add_argument('-f', '--file', help="Source file to parse", required=True)

  args = parser.parse_args()

  cdw = CppDocWriter(args.file)
  cdw.parse()
  cdw.write()


if __name__ == '__main__':
  main()

