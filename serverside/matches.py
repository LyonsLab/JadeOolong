__author__ = 'senorrift'

import json
import pprint

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                                                                                                                     #
# Functions                                                                                                           #
#                                                                                                                     #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#


def get_data(first_sp_id, second_sp_id, json_file):
    """ Get Data
    Given two species IDs and a URL to the SynMap comparison JSON between them,
    Return a list of the (a, b) coordinates, the a coordinates, and the b coordinates.

    :param first_sp_id: Species ID for axis "a".
    :param second_sp_id: Species ID for axis "b".
    :param json_file: URL to SynMap comparison JSON.
    :return: lists of (a, b) coordinates, a coordinates, b coordinates.
    """

    # -----------------------------------------------------------------------------------------------------------------
    # Load JSON into Dictionary
    # -----------------------------------------------------------------------------------------------------------------
    get = json.load(open(json_file, 'r'))

    # -----------------------------------------------------------------------------------------------------------------
    # Determine Species Order
    # -----------------------------------------------------------------------------------------------------------------
    species = []
    pairs = get["layers"]["syntenic_pairs"]["data"]["lines"]
    try:
        test = pairs[first_sp_id]
        species.append(first_sp_id)
        species.append(second_sp_id)
    except KeyError:
        try:
            test = pairs[second_sp_id]
            species.append(second_sp_id)
            species.append(first_sp_id)
        except KeyError:
            print "File/Species Error: Code 1"
            exit()

    # -----------------------------------------------------------------------------------------------------------------
    # Build Data Structures
    #
    #   ######## A Match Locations ########                   ######## B Match Locations ########
    #   # ab_a = {a_ch1: {b_ch1: [a, a, ...],                 # ab_b = {b_ch1: {a_ch1: [b, b, ...],
    #   #                 b_ch2: [a, a, ...],                 #                 a_ch2: [b, b, ...],
    #   #                 ...                                 #                 ...
    #   #                 b_chN: [a, a, ...]},                #                 a_chN: [b, b, ...]},
    #   #         a_ch2: {b_ch1: [a, a, ...],                 #         b_ch2: {a_ch1: [b, b, ...],
    #   #                 b_ch2: [a, a, ...],                 #                 a_ch2: [b, b, ...],
    #   #                 ...                                 #                 ...
    #   #                 b_chN: [a, a, ...]},                #                 a_chN: [b, b, ...]},
    #   #         ...                                         #         ...
    #   #         a_chN: {b_ch1: [a, a, ...],                 #         b_chN: {a_ch1: [b, b, ...],
    #   #                 b_ch2: [a, a, ...],                 #                 a_ch2: [b, b, ...],
    #   #                 ...                                 #                 ...
    #   #                 b_chN: [a, a, ...]}}                #                 a_chN: [b, b, ...]}}
    #
    #   ######## Coordinates A-Indexed ########               ######## Coordinates B-Indexed ########
    #   # ab_cords = {a_ch1: {b_ch1: [[a,b], [a,b], ...],     # ba_cords = {b_ch1: {a_ch1: [[a,b], [a,b], ...],
    #   #                     b_ch2: [[a,b], [a,b], ...],     #               a_ch2: [[a,b], [a,b], ...],
    #   #                     ...                             #               ...
    #   #                     b_chN: [[a,b], [a,b], ...]},    #               a_chN: [[a,b], [a,b], ...]},
    #   #             ...                                     #       ...
    #   #             a_chN: {b_ch1: [[a,b], [a,b], ...],     #       b_chN: {a_ch1: [[a,b], [a,b], ...]
    #   #                     ...                             #               ...
    #   #                     b_chN: [[a,b], [a,b], ...]}}    #               a_ch2: [[a,b], [a,b], ...]}}
    #
    # -----------------------------------------------------------------------------------------------------------------

    ab_a = {}
    ab_b = {}
    ab_cords = {}
    ba_cords = {}

    genomes = get["genomes"]
    a_chromosomes = genomes[first_sp_id]["chromosomes"]
    b_chromosomes = genomes[second_sp_id]["chromosomes"]

    for a_ch in a_chromosomes:
        ab_a[a_ch["name"]] = {}
        ab_cords[a_ch["name"]] = {}
        for b_ch in b_chromosomes:
            ab_a[a_ch["name"]][b_ch["name"]] = []
            ab_cords[a_ch["name"]][b_ch["name"]] = []

    for b_ch in b_chromosomes:
        ab_b[b_ch["name"]] = {}
        ba_cords[b_ch["name"]] = {}
        for a_ch in a_chromosomes:
            ab_b[b_ch["name"]][a_ch["name"]] = []
            ba_cords[b_ch["name"]][a_ch["name"]] = []

    # -----------------------------------------------------------------------------------------------------------------
    # Get Data
    # -----------------------------------------------------------------------------------------------------------------
    data = get["layers"]["syntenic_pairs"]["data"]["lines"][species[0]][species[1]]
    # Iterate through all matches
    for sp1_chr in data:
        for sp2_chr in data[sp1_chr]:
            for match in data[sp1_chr][sp2_chr]:
                # Calculate points for first and second species in JSON
                sp1_start = data[sp1_chr][sp2_chr][match][0]
                sp1_end = data[sp1_chr][sp2_chr][match][1]
                sp1_cord = (sp1_start + sp1_end) / 2

                sp2_start = data[sp1_chr][sp2_chr][match][2]
                sp2_end = data[sp1_chr][sp2_chr][match][3]
                sp2_cord = (sp2_start + sp2_end) / 2

                # Assign correct genome/value by JSON format
                if species[0] == first_sp_id:
                    a_chr = sp1_chr
                    b_chr = sp2_chr
                    a_cord = sp1_cord
                    b_cord = sp2_cord
                elif species[0] == second_sp_id:
                    a_chr = sp2_chr
                    b_chr = sp1_chr
                    a_cord = sp2_cord
                    b_cord = sp1_cord
                else:
                    "File/Species Error: Code 3"
                    exit()

                # Populate data sets
                coordinate = [a_cord, b_cord]
                ab_a[a_chr][b_chr].append(a_cord)
                ab_b[b_chr][a_chr].append(b_cord)
                ab_cords[a_chr][b_chr].append(coordinate)
                ba_cords[b_chr][a_chr].append(coordinate)

    return ab_a, ab_b, ab_cords, ba_cords


def find_matches(species_coordinate, link1, link2, link3):
    """ Find Matches
    Given a list of three species IDs (in order of X, Y, Z axis) and three pairwise comparisons covering all three,
    Returns a list of the coordinates for those matches shared between all three species.

    :param species_coordinate: list containing species ID in order [x axis species, y axis species, z axis species].
    :param link1: Link to a file with pairwise SynMap JSON.
    :param link2: Link to a file with pairwise SynMap JSON.
    :param link3: Link to a file with pairwise SynMap JSON.
    :return: Match coordinate dictionary {X Chr: {Y Chr: {ZChr : [[x_loc, y_loc, z_loc], [x_loc, y_loc, z_loc], ...]}}}
    """

    # Load genome data from each linked file
    link1_data = json.load(open(link1, 'r'))["genomes"]
    link2_data = json.load(open(link2, 'r'))["genomes"]
    link3_data = json.load(open(link3, 'r'))["genomes"]

    # Determine species contained within each file
    link1_spp = link1_data.keys()
    link2_spp = link2_data.keys()
    link3_spp = link3_data.keys()

    # Establish Correct Links/Species
    x_species_id = species_coordinate[0]
    y_species_id = species_coordinate[1]
    z_species_id = species_coordinate[2]
    xy_link = ''
    xz_link = ''
    yz_link = ''

    if x_species_id in link1_spp and y_species_id in link1_spp:
        xy_link = link1
        xy_data = link1_data
    elif x_species_id in link2_spp and y_species_id in link2_spp:
        xy_link = link2
        xy_data = link2_data
    elif x_species_id in link3_spp and y_species_id in link3_spp:
        xy_link = link3
        xy_data = link3_data

    if y_species_id in link1_spp and z_species_id in link1_spp:
        yz_link = link1
        yz_data = link1_data
    elif y_species_id in link2_spp and z_species_id in link2_spp:
        yz_link = link2
        yz_data = link2_data
    elif y_species_id in link3_spp and z_species_id in link3_spp:
        yz_link = link3
        yz_data = link3_data

    if x_species_id in link1_spp and z_species_id in link1_spp:
        xz_link = link1
    elif x_species_id in link2_spp and z_species_id in link2_spp:
        xz_link = link2
    elif x_species_id in link3_spp and z_species_id in link3_spp:
        xz_link = link3

    # Get coordinate information from each file
    xy_x, xy_y, xy_cords, yx_cords = get_data(x_species_id, y_species_id, xy_link)
    xz_x, xz_z, xz_cords, zx_cords = get_data(x_species_id, z_species_id, xz_link)
    yz_y, yz_z, yz_cords, zy_cords = get_data(y_species_id, z_species_id, yz_link)

    # Build Data Structure To Hold 3-Way Matches
    matches = {}
    for x_chr in xy_data[x_species_id]["chromosomes"]:
        matches[x_chr["name"]] = {}
        for y_chr in xy_data[y_species_id]["chromosomes"]:
            matches[x_chr["name"]][y_chr["name"]] = {}
            for z_chr in yz_data[z_species_id]["chromosomes"]:
                matches[x_chr["name"]][y_chr["name"]][z_chr["name"]] = []

    # Find 3-Way Matches
    match_count = 0
    for x_ch in xy_cords:
        for y_ch in xy_cords[x_ch]:
            for xy_match in xy_cords[x_ch][y_ch]:
                for z_ch in xz_cords[x_ch]:
                    for xz_match in xz_cords[x_ch][z_ch]:
                        if xy_match[0] == xz_match[0]:
                            for y_ch in zy_cords[z_ch]:
                                for yz_match in zy_cords[z_ch][y_ch]:
                                    if yz_match[0] == xy_match[1]:
                                        if yz_match[1] == xz_match[1]:
                                            coordinate = [0, 0, 0]
                                            coordinate[0] = xy_match[0]
                                            coordinate[1] = xy_match[1]
                                            coordinate[2] = xz_match[1]
                                            # Ignore duplicate hits
                                            if coordinate not in matches[x_ch][y_ch][z_ch]:
                                                matches[x_ch][y_ch][z_ch].append(coordinate)
                                                match_count += 1
    # Return Matches and Match Count
    return matches, match_count


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                                                                                                                     #
# Main Script                                                                                                         #
#                                                                                                                     #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# Necessary Inputs
output_file = '../data/dog_human_chimp.json'
x = "7057"
y = "25712"
z = "11691"
file1 = "../data/human_dog.json"
file2 = "../data/chimp_dog.json"
file3 = "../data/human_chimp.json"

# Execute Script, Dump JSON with Hits
all_matches, match_number = find_matches([x, y, z], file1, file2, file3)
#pprint.pprint(all_matches)
json.dump(all_matches, open(output_file, "w"))

# Print Match Number
print "You Found %s Matches!" % str(match_number)