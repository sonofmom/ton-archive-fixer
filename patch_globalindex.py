#!/usr/bin/env python3
#
import sys
import os
import getopt
import re


def run(argv):
    missing = [3700000,3709492,3711201,3720000,3724270,3726138,3738097,3739783,3740000,3751961,3753752,3760000,3766206,3767997,3780000,3780743,3782535,3795293,3797106,3800000,3810223,3812076,3820000,3825103,3826937,3840000,3840254,3842151,3855368,3857252,3860000,3870609,3872485,3880000,3885546,3887406,3900000,3900725,3902608,3915901,3917805,3920000,3930954,3932852,3940000,3946324,3948251,3960000,3961557,3963457,3976967,3978867,3980000,3992229,3994134,4000000,4007569,4009479,4020000,4022917,4024817,4037978,4039847,4040000,4053175,4055080,4060000,4068361,4070248,4080000,4083239,4085058,4098270,4100000,4100168,4113345,4115198,4120000,4128450,4130339,4140000,4143555,4145428,4158655,4160000,4160143,4173213,4175032,4180000,4187914,4189739,4200000,4202969,4204872,4218305,4220000,4220218,4233720,4235654,4240000,4248865,4250721,4260000,4263995,4265881,4279231,4280000,4281137,4294359,4296230,4300000,4309364,4311258,4320000,4324439,4326282,4339510,4340000,4341390,4354570,4356431,4360000,4369567,4371437,4380000,4384544,4386413,4399577,4400000,4401436,4414598,4416483,4420000,4429877,4431786,4440000,4445177,4447074,4460000,4460581,4462500,4475714,4477594,4480000,4490770,4492629,4500000,4505684,4507548,4520000,4520797,4522673,4536130,4538024,4540000,4551429,4553335,4560000,4566702,4568588,4580000,4581945,4583812,4597172,4599082,4600000,4612486,4614393,4620000,4627824,4629727,4640000,4643103,4645003,4658423,4660000,4660286,4673602,4675482,4680000,4688683,4690582,4700000,4703962,4705841,4719227,4720000,4721117,4734371,4736229,4740000,4749289,4751122,4760000,4764291,4766173,4779432,4780000,4781297,4794600,4796496,4800000,4809765,4811653,4820000,4824869,4826741,4839961,4840000,4841851,4855027,4856904,4860000,4870096,4871945,4880000,4885260,4887140,4900000,4900525,4902403,4915532,4917429,4920000,4930816,4932728,4940000,4946162,4948060,4960000,4961425,4963333,4976700,4978591,4980000,4991938,4993858]
    dump_file = None

    # Process input parameters
    opts, args = getopt.getopt(argv, "hd:", ["dump="])
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit(0)
        elif opt in ("-d", "--dump"):
            dump_file = arg
            if not os.access(dump_file, os.R_OK):
                print("Dump " + dump_file + " could not be opened")
                sys.exit(1)
    # end for

    if not dump_file:
        print_usage()
        sys.exit(1)

    with open(dump_file, 'r') as f:
        curr_dump = f.read().splitlines()
        f.close()

    curr_packages = decode_node_packages(curr_dump[0])

    try:
        gap_start_index = curr_packages["packages_"].index(3697533)
        gap_end_index = curr_packages["packages_"].index(5000000)
    except:
        print("ERROR: Packages 3697533 and/or 5000000 could not be found in index, is this dump of archival node?")
        sys.exit(1)

    if gap_end_index - gap_start_index != 1:
        print("ERROR: No gap between packages 3697533 and 5000000 detected.")
        sys.exit(1)

    curr_packages["packages_"][gap_end_index:gap_end_index] = missing
    curr_dump[0] = encode_node_packages(curr_packages)

    with open(dump_file, 'w') as f:
        for line in curr_dump:
            f.write("{}\n".format(line))
        f.close()

    print ("SUCCESS")


def reverse_word(word):
    return ''.join(re.findall('..', word)[::-1])


def decode_node_packages(data):
    result = {"key": data[2:10], "prefix": "", "packages_": [], "key_packages_": [], "temp_packages_": []}

    data = re.findall('........', data[17:])
    result["prefix"] = data.pop(0)

    for element in ["packages_", "key_packages_", "temp_packages_"]:
        i = int(reverse_word(data.pop(0)), 16)
        for x in range(0, i):
            result[element].append(int(reverse_word(data.pop(0)), 16))

    return result

def encode_node_packages(data):
    result = "0x" + data["key"] + " ==> 0x" + data["prefix"]
    for element in ["packages_", "key_packages_", "temp_packages_"]:
        result += reverse_word(str(hex(len(data[element])))[2:].upper().zfill(8))
        for package in data[element]:
            result += reverse_word(str(hex(package))[2:].upper().zfill(8))

    return result


def print_usage():
    print('This script will patch your TON archival node globalindex dump and inject missing packs.')
    print('Usage: ')
    print('patch_globalindex.py --dump=<dump file to path>')

if __name__ == '__main__':
    run(sys.argv[1:])
