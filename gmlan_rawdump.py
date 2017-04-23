import sys

#id = 0x10004060
#(1492883377.376484) can0 106B8040#0000000000000000

def splitid(line):
    parts=line.strip().split(' ')
    msg = parts[2].split("#")

    id=0 
    try:
        id = int(msg[0], base=16)
    except:
        pass

    return id, msg[1]

def parse_gmlan(id):
    priority = id >> 26
    arb_id = ( id & (0x1FFF << 13) ) >> 13
    address = ( id & 0x1FFF ) 

    return priority, arb_id, address

if __name__ == '__main__':
    for line in sys.stdin:

        id, message = splitid(line)
        priority, arbid, address = parse_gmlan(id)

        print '{:04x} {:04x} {}'.format(arbid, address, message)
