import re

# global variable initialization

max_block = 64
# stores the memory blocks by their starting memory position, the length
# and whether it has been allocated
# initialized as length 64.
block_list = [{"start": 0, "length": max_block, "fill": False}]
user_input = ""


def display():
    '''
        Loop through block_list and check status of fill key.
        Appends - or # by the length of the block
        Joins the list into a single string and prints.
    '''
    outstring = ["|"]
    for block in block_list:
        if block["fill"] is False:
            outstring.append("-"*block["length"])
        elif block["fill"] is True:
            outstring.append("#"*block["length"])
        outstring.append("|")
    print "".join(outstring)


def get_input():
    '''
        Gets user input
    '''
    user_in = raw_input("How many blocks do you want to allocate/free?\n")
    return user_in


def check_input(string):
    '''
        Uses regex to ensure proper formatting of command
        Failure to fit regex string prints out Invalid input
        Else, check if allocation/free command requests more than
        maximum memory capacity.
        Passing requirements returns array splitting by single space
    '''
    result = re.match("(?i)(a \d{1,2})|(f \d{1,2})", string)
    if result is None:
        print "Invalid input\n"
        return False
    else:
        split_string = string.split(" ")
        if int(split_string[1]) > max_block:
            print "Block size is too large"
            return False
        return string.split(" ")


def allocate(allocating_size):
    '''
        Recursively iterate through current blocks,
        splits blocks until appropriate size.
        Changes fill of block to indicate allocation.
    '''
    global block_list
    for block in block_list:
        if block["fill"] is True:
            # Already full, continuing
            continue
        if allocating_size <= block["length"]:
            # Current block fits, continue to see if split block also fits
            if allocating_size <= block["length"]/2:
                # Split block
                # Call allocate again to check if new list has a fitting block
                print "(Splitting {}/{})".format(
                    block["start"], block["length"])
                index_block = block_list.index(block)
                split(index_block)
                allocate(allocating_size)
                break
            else:
                # Appropriate sized block found, change fill and print
                # allocation message
                block["fill"] = True
                print "Blocks {}-{} allocated".format(
                    block["start"], block["start"]+block["length"]-1)
                return 0
        elif allocating_size > block["length"]:
                # Doesn't fit, continuing
                continue


def free(free_location):
    '''
        Iterates through list until appropriate block is found.
        "free" block space and check if next block is empty
        Recusively merge sequential empty blocks
    '''
    global block_list
    for index, block in block_list:
        if free_location == block["start"]:
            # Block found, free space
            block_list[index]["fill"] = False
            if index + 1 < len(block_list):
                # Ensure not out of bounds
                if block_list[index+1]["fill"] is False:
                    # If next block also free, merge blocks
                    print "(merging {}/{} and {}/{})".format(
                        block["start"], block["length"], block_list[index + 1]
                        ["start"], block_list[index+1]["length"])
                    merge(index, free_location)
                    free(free_location)
                    break
                else:
                    # Next block is allocated memory, do nothing
                    break
            else:
                # Out of bounds
                break
    return 0


def split(index):
    '''
        Inserts new block at position of current block with half the length
        Halves length of current block and sets new starting position.
    '''
    global block_list
    to_insert = {"start": block_list[index]["start"], "length":
                 (block_list[index]["length"]/2), "fill": False}
    if index == 0:
        block_list[index]["length"] /= 2
        block_list[index]["start"] = block_list[index]["length"]
    else:
        block_list[index]["length"] /= 2
        block_list[index]["start"] = block_list[index]["start"] +
        block_list[index]["length"]
    block_list.insert(index, to_insert)
    return 0


def merge(index, free_location):
    '''
        Deletes two indices at given position
        Inserts new indice with length of previous two indices combined
    '''
    global block_list
    to_insert = {"start": free_location, "length":
                 block_list[index]["length"] + block_list[index+1]
                 ["length"], "fill": False}
    del block_list[index:index+2]
    block_list.insert(index, to_insert)
    return 0


def execute():
    '''
        Main loop to display memory and query user input
        Calls appropriate functions based on input
    '''
    global user_input
    while(user_input != "q"):
        display()
        user_input = get_input()
        if user_input == "q":
            # Break loop, print terminating, ends program.
            break
        matched_input = check_input(user_input)
        if matched_input is False:
            # Invalid input, run loop again
            continue
        if matched_input[0].lower() == "a":
            allocate(int(matched_input[1]))
        elif matched_input[0].lower() == "f":
            free(int(matched_input[1]))
    print "Terminating"

if __name__ == "__main__":
    execute()
