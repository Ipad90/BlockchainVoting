from Block.block import Block

import hashlib
import json

if __name__ == '__main__':
    block = Block('1')

    genesis_block = {
        'headers': {
            'prev_hash': '0x' + '0' * 62,
            'timestamp': block.generate_timestamp()
        },
        'tx_details': {
            'tx_type': 'genesis'
        }
    }

    genesis_block_stringed = json.dumps(genesis_block)
    genesis_block['headers']['tx_hash'] = hashlib.sha256(genesis_block_stringed.encode()).hexdigest()
    genesis_block['tx_details']['status'] = 'approved'

    block.create_transaction(genesis_block)
