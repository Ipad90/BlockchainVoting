from Block.block import Block

if __name__ == '__main__':
    block = Block('1')
    
    # tx = block.get_block("042cc167896b6b9caf7528d52370b15e173ab74914e8b0a5e0ee0bf775199a56")
    # print(tx)
    print(block.tally_votes_of_election('68319757087a0a9450a4cecbadb7398f8060c3dab018803d43ff2426f053d48c'))
