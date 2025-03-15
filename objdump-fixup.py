#!/usr/bin/python3
#
# MIT License
#
# Copyright (c) 2025 rrmm
#
# See LICENSE file for terms
#

import sys
import os.path
import re

class LabelName:
    def __init__(self, section_offset_target, absolute_target, labelname):
        self.section_offset_target = section_offset_target
        self.absolute_target = absolute_target
        self.labelname = labelname
    # end def

    def set_labelname(self, name):
        self.labelname = name
    # end def
    
    def get_labelname(self):
        return self.labelname
    # end def

    def __repr__(self):
        return self.labelname
    # end def
# end class


class NoCodeLine:
    def __init__(self, line):
        self.line = line
    # end def

    def get_line(self, no_address_column):
        return self.line
    # end if
    
    def __repr__(self):
        return f"NoCodeLine<{self.line}>"
    #end def

    def needs_branch_fixup(self):
        return False
    # end def
# end class

class CodeLine:
    def __init__(self, line, match, branch_target_match=None):
        self.line = line
        self.match = match
        self.addr = int(match.group(1), 16)
        self.code = match.group(2)
        self.disassembly = match.group(3)
        self.branch_target_match = branch_target_match
        if branch_target_match:
            self.branch_absolute_target = int(branch_target_match.group(1),16)            
            self.branch_target_section = branch_target_match.group(2)
            self.branch_target_offset = int(branch_target_match.group(3),16)
        # end if
        self.branch_target_label = None
    # end def

    #  returns a pair (section, offset) to identify a target
    def get_branch_target(self):
        return (self.branch_target_section, self.branch_target_offset)
    # end def

    def get_branch_absolute_target(self):
        return self.branch_absolute_target
    # end def    
    
    # set a label for the target to an object fo the class LabelName
    def set_branch_target_local_label(self, label):
        self.branch_target_label = label
    # end def_

    def get_line(self, no_address_column=False):
        if self.branch_target_label:
            # switch the absolute address with the label
            branch_target_re = r"(%x) (<[A-Za-z0-9_@]+.0x[0-9A-Fa-f]+>)"%self.branch_absolute_target
            substitute = r"%s \2 \1"%str(self.branch_target_label)
            line = re.sub(branch_target_re, substitute, self.line)
            res = line
        else:
            res = self.line
        # end if
        if (no_address_column):
            (_, res) = res.split(":", 1)
        # end if
        return res
    # end def
    
    def __repr__(self):
        if self.branch_target_label:
            return f"CodeLine<{self.addr:x} {self.code} {self.disassembly} {self.branch_target_label}>";
        else:
            return f"CodeLine<{self.addr:x} {self.code} {self.disassembly}>";
        # end if
    # end def

    def needs_branch_fixup(self):
        return self.branch_target_match != None
    # end def
# end class

class StartLine:
    def __init__(self, line, match):
        self.line = line
        self.match = match
        self.addr = int(match.group(1), 16)
        self.name = match.group(2)
    # end def

    def get_line(self, no_address_column):
        return self.line
    # end def
    
    def __repr__(self):
        return f"StartLine<{self.addr:x} {self.name}>";
    # end def

    def needs_branch_fixup(self):
        return False
    # end def
# end class

def read_input_from_stdin():
    # save only the lines whose branches we need to fixup
    fixup_line_list = []
    output_lines = []

    # according to the docs, these are cached so this doesn't buy us that much
    # these regex's are messy but seem to work
    # might have to modify them later if errors are found
    function_start_re = re.compile(r"([0-9A-Fa-f]+) <([A-Za-z0-9_@.\-]+)>:")
    regular_code_re = re.compile(r"([ ]*[0-9A-Fa-f]+):\t([0-9A-Fa-f ]*)\t?(.*)")
    
    # this will look something like <name+0x16> etc
    branch_target_re = re.compile(r".* ([0-9A-Fa-f]+) <([A-Za-z0-9_@]+).?(0x[0-9A-Fa-f]+)>")

    
    for line in sys.stdin.readlines():

        m = regular_code_re.match(line)
        if (m):
            disassembly =  m.group(3)
            target_match = branch_target_re.match(disassembly)
            code_line = CodeLine(line, m, target_match)
            output_lines.append(code_line)

            if code_line.needs_branch_fixup():
                fixup_line_list.append(code_line)
            # end if
            continue
        # end if

        m = function_start_re.match(line)
        if (m):
            section = StartLine(line,m)
            output_lines.append(section)
            continue
        # end if

        output_lines.append(NoCodeLine(line))
        
    # end for

    return (output_lines, fixup_line_list)
# end def read_input_from_stdin


def create_labels(fixup_line_list):
    # labels indexed by absolute target address
    label_absolute_dict = {}
    label_counter = 0
    
    # assign labels to those lines that need fixup
    for line in fixup_line_list:
        
        target = line.get_branch_absolute_target()
        if target in label_absolute_dict:
            label_obj = label_absolute_dict[target]
        else:
            label_name = f".T{label_counter:04d}"
            label_counter+=1
            label_obj = LabelName(line.get_branch_target(), target, label_name)
            label_absolute_dict[target] = label_obj
        # end if
        line.set_branch_target_local_label(label_obj)
    # end for

    # as a convenience we'd like the labels to be named
    # monotonically increasing by absolute address so we'll sort and rename them.
    
    label_absolute_list = list(label_absolute_dict.values())
    
    label_absolute_list.sort(key=lambda x: x.absolute_target)
    label_counter  = 0
    for label_obj in label_absolute_list:
        label_obj.set_labelname(f".L{label_counter:04d}")
        label_counter += 1
    # end for

    return label_absolute_dict
# end def create labels

def istypeofclass(a, klass):
    return type(a).__name__ == klass.__name__
# end def

def output_fixed_listing(output_lines, label_absolute_dict, output_options):

    for line in output_lines:

        # a label can only occur before a codeline
        if istypeofclass(line, CodeLine):
            current_address = line.addr;
            if current_address in label_absolute_dict:
                abs_label = label_absolute_dict[current_address]
                print (f"{abs_label}:")            
            # end if
        # end if

        if not (output_options["suppress_non_code"] and istypeofclass(line, NoCodeLine)):
            print (line.get_line(output_options["no_address_column"]), end="")
        # end if
    # end for
# end def output_fixed_listing


def usage():
    name = os.path.basename(sys.argv[0])
    print("""
Usage: 
\t%s [options]

Options:
\t-na\t\tdo not display the address column in the listing
\t-h, --help\tdisplay this help and exit

Filters the output from objdump to add local labels to the disassembly.  
    
    $ objdump -d [execfile] | %s
"""%(name, name))
# end def



if __name__ == "__main__":

    output_options = {}
    output_options["suppress_non_code"] = False
    
    if "--help" in sys.argv or "-h" in sys.argv:
        usage()
        sys.exit()
    # end if
    
    if "-na" in sys.argv:
        output_options["no_address_column"]=True
    else:
        output_options["no_address_column"]=False
    # end if

    (output_lines, fixup_line_list) = read_input_from_stdin()
    label_absolute_dict = create_labels(fixup_line_list)
    output_fixed_listing(output_lines, label_absolute_dict, output_options)
# end if __main__
