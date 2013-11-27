#!/usr/bin/env python

# Capstone Python bindings, by Nguyen Anh Quynnh <aquynh@gmail.com>

from capstone import *

X86_CODE16 = "\x8d\x4c\x32\x08\x01\xd8\x81\xc6\x34\x12\x00\x00"
X86_CODE32 = "\x8d\x4c\x32\x08\x01\xd8\x81\xc6\x34\x12\x00\x00"
X86_CODE64 = "\x55\x48\x8b\x05\xb8\x13\x00\x00"
ARM_CODE = "\xED\xFF\xFF\xEB\x04\xe0\x2d\xe5\x00\x00\x00\x00\xe0\x83\x22\xe5\xf1\x02\x03\x0e\x00\x00\xa0\xe3\x02\x30\xc1\xe7\x00\x00\x53\xe3"
ARM_CODE2 = "\x10\xf1\x10\xe7\x11\xf2\x31\xe7\xdc\xa1\x2e\xf3\xe8\x4e\x62\xf3"
THUMB_CODE = "\x70\x47\xeb\x46\x83\xb0\xc9\x68"
THUMB_CODE2 = "\x4f\xf0\x00\x01\xbd\xe8\x00\x88"
MIPS_CODE = "\x0C\x10\x00\x97\x00\x00\x00\x00\x24\x02\x00\x0c\x8f\xa2\x00\x00\x34\x21\x34\x56"
MIPS_CODE2 = "\x56\x34\x21\x34\xc2\x17\x01\x00"
ARM64_CODE = "\x21\x7c\x02\x9b\x21\x7c\x00\x53\x00\x40\x21\x4b\xe1\x0b\x40\xb9"

all_tests = (
        (CS_ARCH_X86, CS_MODE_16, X86_CODE16, "X86 16bit (Intel syntax)"),
        (CS_ARCH_X86, CS_MODE_32 + CS_MODE_SYNTAX_ATT, X86_CODE32, "X86 32bit (ATT syntax)"),
        (CS_ARCH_X86, CS_MODE_32, X86_CODE32, "X86 32 (Intel syntax)"),
        (CS_ARCH_X86, CS_MODE_64, X86_CODE64, "X86 64 (Intel syntax)"),
        (CS_ARCH_ARM, CS_MODE_ARM, ARM_CODE, "ARM"),
        (CS_ARCH_ARM, CS_MODE_ARM, ARM_CODE2, "ARM: Cortex-A15 + NEON"),
        (CS_ARCH_ARM, CS_MODE_THUMB, THUMB_CODE, "THUMB"),
        (CS_ARCH_ARM, CS_MODE_THUMB, THUMB_CODE2, "THUMB-2"),
        (CS_ARCH_ARM64, CS_MODE_ARM, ARM64_CODE, "ARM-64"),
        (CS_ARCH_MIPS, CS_MODE_32 + CS_MODE_BIG_ENDIAN, MIPS_CODE, "MIPS-32 (Big-endian)"),
        (CS_ARCH_MIPS, CS_MODE_64+ CS_MODE_LITTLE_ENDIAN, MIPS_CODE2, "MIPS-64-EL (Little-endian)"),
        )


def to_hex(s):
    # print " ".join("{0:x}".format(ord(c)) for c in s) # <-- Python 3 is OK
    return ' '.join(x.encode('hex') for x in s)    # <-- fails for Python 3


### Test cs_disasm_quick()
def test_cs_disasm_quick():
    for (arch, mode, code, comment) in all_tests:
        print('*' * 40)
        print("Platform: %s" %comment)
        print("Disasm:"),
        print to_hex(code)
        for insn in cs_disasm_quick(arch, mode, code, 0x1000):
            print("0x%x:\t%s\t%s" %(insn.address, insn.mnemonic, insn.op_str))
        print


### Test class cs
def test_class():
    for (arch, mode, code, comment) in all_tests:
        print('*' * 40)
        print("Platform: %s" %comment)
        print("Disasm:"),
        print to_hex(code)
    
        try:
            md = cs(arch, mode)
            for insn in md.disasm(code, 0x1000):
                print("0x%x:\t%s\t%s" %(insn.address, insn.mnemonic, insn.op_str))
            print
        except:
            print("ERROR: Arch or mode unsupported!")


#test_cs_disasm_quick()
#print "*" * 40
test_class()