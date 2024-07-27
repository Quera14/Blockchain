# Module1 Blockchain
import datetime
import hashlib
import json
import time
import matplotlib.pyplot as plt
from essential_generators import DocumentGenerator
import csv




# Build blockchain!
class Blockchain:
    def __init__(self):
        gen = DocumentGenerator()
        self.chain = []
        self.create_block (proof = 1, prev_hash = '0', data=gen.paragraph())
    def create_block(self, proof, prev_hash, data):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'prev_hash': prev_hash,
                 'data': data}
        self.chain.append(block)
        return block
    
    def get_prev_block(self):
        return self.chain[-1]
    
    def proof_of_work (self, prev_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256 (str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
        
    def hash (self, block):
        encoded_block = json.dumps(block, sort_keys= True).encode()
        return hashlib.sha256(encoded_block). hexdigest()
        # nonce = 0
        # while True:
        #     block['proof'] = nonce
        #     encoded_block = json.dumps(block, sort_keys= True).encode()
        #     hash_result = hashlib.sha256(encoded_block). hexdigest()
        #     if hash_result[:4] == '0000':
        #         return hash_result
        #     print('Jumlah nonce: ', nonce, "Hash Result Fail : ", hash_result)
        #     nonce += 1
    
    def is_chain_valid(self, chain):
        prev_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['prev_hash'] != self.hash(prev_block):
                return False
            prev_proof = prev_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256 (str(proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            prev_block = block
            block_index += 1
        return True


#Mining Blockchain

#Create blockchain
Blockchain = Blockchain()

#MINING BLOCK
def mine_block(data):
    prev_block = Blockchain.get_prev_block()
    prev_proof = prev_block ['proof']
    proof = Blockchain.proof_of_work(prev_proof)
    prev_hash = Blockchain.hash(prev_block)
    block = Blockchain.create_block(proof, prev_hash, data)
    response = {'message': 'Congrats, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'prev_hash': block['prev_hash']}
    return response
            
#Blockchain FULL UI
def get_chain():
    response = {'chain': Blockchain.chain,
                'length': len(Blockchain.chain)}
    return response

totaltime = []

for block in range (500):
    # data = input('Masukkan Data: ')
    start_time = time.time()
    print (mine_block('Some data here'))
    end_time = time.time()
    totaltime.append(end_time - start_time)
    # Data waktu per satu block
    data = totaltime

# # Tentukan nama file CSV
#     file_name = './data/waktu_per_block_SHA256.csv'

# # Tulis data ke dalam file CSV
# with open(file_name, mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Block', 'Waktu (s)'])
#     for idx, time in enumerate(data):
#         writer.writerow([idx+1, time])
#         print(f"Data waktu per satu block telah ditulis ke dalam file CSV: {file_name}")
print (totaltime)



fig, Blockchain = plt.subplots()
Blockchain.plot(totaltime,label='SHA256')
Blockchain.set_xlabel('Block')
Blockchain.set_ylabel('Time [s]')
Blockchain.set_title('Compare Algorithm SHA256')
Blockchain.legend()
plt.show()    

#check if valid
def is_valid():
    is_valid = Blockchain.is_chain_valid(Blockchain.chain)
    if is_valid:
        response = {'message': 'All Good. The Blockchain is valid.'}
    else: 
        response = {'message': 'Ali, we have a problem. The Blockchain is not valid'}
    return response


