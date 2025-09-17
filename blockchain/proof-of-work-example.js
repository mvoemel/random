const crypto = require("crypto");

// Transaction class represents individual transactions
class Transaction {
  constructor(from, to, amount, data = null) {
    this.from = from;
    this.to = to;
    this.amount = amount;
    this.data = data; // Additional data for smart contracts
    this.timestamp = Date.now();
    this.signature = null;
  }

  // Calculate hash of the transaction
  calculateHash() {
    return crypto
      .createHash("sha256")
      .update(
        this.from +
          this.to +
          this.amount +
          this.timestamp +
          JSON.stringify(this.data)
      )
      .digest("hex");
  }

  // Sign transaction with private key (simplified)
  signTransaction(privateKey) {
    const hash = this.calculateHash();
    this.signature = crypto
      .createSign("SHA256")
      .update(hash)
      .sign(privateKey, "hex");
  }

  // Verify transaction signature
  isValid() {
    if (this.from === null) return true; // Mining reward transaction

    if (!this.signature || this.signature.length === 0) {
      throw new Error("No signature in this transaction");
    }

    const publicKey = this.from; // Simplified: using address as public key
    const hash = this.calculateHash();

    try {
      return crypto
        .createVerify("SHA256")
        .update(hash)
        .verify(publicKey, this.signature, "hex");
    } catch (error) {
      return false;
    }
  }
}

// Block class represents individual blocks in the blockchain
class Block {
  constructor(timestamp, transactions, previousHash = "") {
    this.previousHash = previousHash;
    this.timestamp = timestamp;
    this.transactions = transactions;
    this.nonce = 0;
    this.hash = this.calculateHash();
  }

  // Calculate block hash using SHA-256
  calculateHash() {
    return crypto
      .createHash("sha256")
      .update(
        this.previousHash +
          this.timestamp +
          JSON.stringify(this.transactions) +
          this.nonce
      )
      .digest("hex");
  }

  // Mine block with Proof of Work consensus
  mineBlock(difficulty) {
    const target = Array(difficulty + 1).join("0");

    while (this.hash.substring(0, difficulty) !== target) {
      this.nonce++;
      this.hash = this.calculateHash();
    }

    console.log(`Block mined: ${this.hash}`);
  }

  // Validate all transactions in the block
  hasValidTransactions() {
    for (const tx of this.transactions) {
      if (!tx.isValid()) {
        return false;
      }
    }
    return true;
  }
}

// Simple Smart Contract class
class SmartContract {
  constructor(address, code, state = {}) {
    this.address = address;
    this.code = code; // Contract code as string
    this.state = state; // Contract state
    this.balance = 0;
  }

  // Execute contract function
  execute(functionName, params, caller, value = 0) {
    try {
      // Create a safe execution context
      const context = {
        state: this.state,
        balance: this.balance,
        caller: caller,
        value: value,
        transfer: (to, amount) => {
          if (this.balance >= amount) {
            this.balance -= amount;
            return { to, amount };
          }
          throw new Error("Insufficient contract balance");
        },
      };

      // Simple function execution (in real implementation, use proper VM)
      const func = new Function("context", "params", this.code);
      const result = func(context, params);

      // Update contract state
      this.state = context.state;
      this.balance = context.balance;

      return result;
    } catch (error) {
      throw new Error(`Contract execution failed: ${error.message}`);
    }
  }
}

// Main Blockchain class
class Blockchain {
  constructor() {
    this.chain = [this.createGenesisBlock()];
    this.difficulty = 2;
    this.pendingTransactions = [];
    this.miningReward = 100;
    this.contracts = new Map(); // Store smart contracts
  }

  // Create the first block in the blockchain
  createGenesisBlock() {
    return new Block(Date.parse("2024-01-01"), [], "0");
  }

  // Get the latest block
  getLatestBlock() {
    return this.chain[this.chain.length - 1];
  }

  // Mine pending transactions
  minePendingTransactions(miningRewardAddress) {
    const rewardTransaction = new Transaction(
      null,
      miningRewardAddress,
      this.miningReward
    );
    this.pendingTransactions.push(rewardTransaction);

    const block = new Block(
      Date.now(),
      this.pendingTransactions,
      this.getLatestBlock().hash
    );

    block.mineBlock(this.difficulty);

    console.log("Block successfully mined!");
    this.chain.push(block);

    this.pendingTransactions = [];
  }

  // Add transaction to pending transactions
  createTransaction(transaction) {
    // Validate transaction
    if (!transaction.from || !transaction.to) {
      throw new Error("Transaction must include from and to address");
    }

    if (!transaction.isValid()) {
      throw new Error("Cannot add invalid transaction to chain");
    }

    // Check if sender has sufficient balance
    if (transaction.from !== null) {
      const balance = this.getBalance(transaction.from);
      if (balance < transaction.amount) {
        throw new Error("Not enough balance");
      }
    }

    this.pendingTransactions.push(transaction);
  }

  // Deploy a smart contract
  deployContract(contractAddress, contractCode, deployer) {
    const contract = new SmartContract(contractAddress, contractCode);
    this.contracts.set(contractAddress, contract);

    // Create deployment transaction
    const deployTransaction = new Transaction(deployer, contractAddress, 0, {
      type: "contract_deployment",
      code: contractCode,
    });

    this.pendingTransactions.push(deployTransaction);
    console.log(`Smart contract deployed at address: ${contractAddress}`);
  }

  // Execute smart contract function
  executeContract(contractAddress, functionName, params, caller, value = 0) {
    const contract = this.contracts.get(contractAddress);
    if (!contract) {
      throw new Error("Contract not found");
    }

    // Add value to contract balance if sending ether
    if (value > 0) {
      const senderBalance = this.getBalance(caller);
      if (senderBalance < value) {
        throw new Error("Insufficient balance to send value to contract");
      }
      contract.balance += value;
    }

    const result = contract.execute(functionName, params, caller, value);

    // Create contract execution transaction
    const contractTransaction = new Transaction(
      caller,
      contractAddress,
      value,
      {
        type: "contract_execution",
        function: functionName,
        params: params,
        result: result,
      }
    );

    this.pendingTransactions.push(contractTransaction);
    return result;
  }

  // Get balance of an address
  getBalance(address) {
    let balance = 0;

    for (const block of this.chain) {
      for (const trans of block.transactions) {
        if (trans.from === address) {
          balance -= trans.amount;
        }

        if (trans.to === address) {
          balance += trans.amount;
        }
      }
    }

    return balance;
  }

  // Get all transactions for an address
  getAllTransactionsForWallet(address) {
    const txs = [];

    for (const block of this.chain) {
      for (const tx of block.transactions) {
        if (tx.from === address || tx.to === address) {
          txs.push(tx);
        }
      }
    }

    return txs;
  }

  // Validate the entire blockchain
  isChainValid() {
    const realGenesis = JSON.stringify(this.createGenesisBlock());

    if (realGenesis !== JSON.stringify(this.chain[0])) {
      return false;
    }

    for (let i = 1; i < this.chain.length; i++) {
      const currentBlock = this.chain[i];
      const previousBlock = this.chain[i - 1];

      if (!currentBlock.hasValidTransactions()) {
        return false;
      }

      if (currentBlock.hash !== currentBlock.calculateHash()) {
        return false;
      }

      if (currentBlock.previousHash !== previousBlock.hash) {
        return false;
      }
    }

    return true;
  }

  // Get contract state
  getContractState(contractAddress) {
    const contract = this.contracts.get(contractAddress);
    return contract ? contract.state : null;
  }

  // Get contract balance
  getContractBalance(contractAddress) {
    const contract = this.contracts.get(contractAddress);
    return contract ? contract.balance : 0;
  }
}

// Example usage and demonstration
console.log("=== Blockchain with Smart Contracts Demo ===\n");

// Create blockchain instance
const myBlockchain = new Blockchain();

// Create wallet addresses (simplified)
const wallet1 = "wallet1-public-key";
const wallet2 = "wallet2-public-key";
const miner = "miner-address";

console.log("1. Mining initial blocks...");
myBlockchain.minePendingTransactions(miner);

// Create some transactions
console.log("\n2. Creating transactions...");
const tx1 = new Transaction(miner, wallet1, 50);
const tx2 = new Transaction(wallet1, wallet2, 20);

myBlockchain.createTransaction(tx1);
myBlockchain.createTransaction(tx2);

console.log("\n3. Mining transactions...");
myBlockchain.minePendingTransactions(miner);

// Deploy a smart contract (simple token contract)
console.log("\n4. Deploying smart contract...");
const tokenContractCode = `
    if (!context.state.totalSupply) {
        context.state.totalSupply = 1000;
        context.state.balances = {};
        context.state.balances[context.caller] = 1000;
    }
    
    if (params.function === 'transfer') {
        const from = context.caller;
        const to = params.to;
        const amount = params.amount;
        
        if (context.state.balances[from] >= amount) {
            context.state.balances[from] -= amount;
            context.state.balances[to] = (context.state.balances[to] || 0) + amount;
            return { success: true, message: 'Transfer successful' };
        }
        return { success: false, message: 'Insufficient balance' };
    }
    
    if (params.function === 'balanceOf') {
        return context.state.balances[params.address] || 0;
    }
    
    return { success: false, message: 'Unknown function' };
`;

myBlockchain.deployContract(
  "token-contract-address",
  tokenContractCode,
  wallet1
);

// Execute smart contract functions
console.log("\n5. Executing smart contract functions...");

// Check initial balance
const initialBalance = myBlockchain.executeContract(
  "token-contract-address",
  "balanceOf",
  { function: "balanceOf", address: wallet1 },
  wallet1
);
console.log(`Initial token balance for wallet1: ${initialBalance}`);

// Transfer tokens
const transferResult = myBlockchain.executeContract(
  "token-contract-address",
  "transfer",
  { function: "transfer", to: wallet2, amount: 100 },
  wallet1
);
console.log(`Token transfer result:`, transferResult);

// Check balances after transfer
const balance1After = myBlockchain.executeContract(
  "token-contract-address",
  "balanceOf",
  { function: "balanceOf", address: wallet1 },
  wallet1
);
const balance2After = myBlockchain.executeContract(
  "token-contract-address",
  "balanceOf",
  { function: "balanceOf", address: wallet2 },
  wallet1
);

console.log(`Token balance for wallet1 after transfer: ${balance1After}`);
console.log(`Token balance for wallet2 after transfer: ${balance2After}`);

// Mine the contract transactions
console.log("\n6. Mining contract transactions...");
myBlockchain.minePendingTransactions(miner);

// Display blockchain information
console.log("\n7. Blockchain Information:");
console.log("Balances:");
console.log(`Miner: ${myBlockchain.getBalance(miner)}`);
console.log(`Wallet1: ${myBlockchain.getBalance(wallet1)}`);
console.log(`Wallet2: ${myBlockchain.getBalance(wallet2)}`);

console.log("\nContract State:");
console.log(
  "Token Contract State:",
  myBlockchain.getContractState("token-contract-address")
);
console.log(
  "Token Contract Balance:",
  myBlockchain.getContractBalance("token-contract-address")
);

console.log("\nBlockchain Valid:", myBlockchain.isChainValid());
console.log("Total Blocks:", myBlockchain.chain.length);

// Display the entire blockchain
console.log("\n8. Complete Blockchain:");
console.log(JSON.stringify(myBlockchain.chain, null, 2));
