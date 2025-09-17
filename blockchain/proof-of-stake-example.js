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
  constructor(timestamp, transactions, previousHash = "", validator = null) {
    this.previousHash = previousHash;
    this.timestamp = timestamp;
    this.transactions = transactions;
    this.validator = validator; // Address of the validator who created this block
    this.hash = this.calculateHash();
    this.signature = null; // Validator's signature on the block
  }

  // Calculate block hash using SHA-256
  calculateHash() {
    return crypto
      .createHash("sha256")
      .update(
        this.previousHash +
          this.timestamp +
          JSON.stringify(this.transactions) +
          this.validator
      )
      .digest("hex");
  }

  // Sign block with validator's private key
  signBlock(privateKey) {
    const hash = this.calculateHash();
    this.signature = crypto
      .createSign("SHA256")
      .update(hash)
      .sign(privateKey, "hex");
  }

  // Validate block signature
  isValidBlock() {
    if (!this.signature) {
      return false;
    }

    const hash = this.calculateHash();
    try {
      return crypto
        .createVerify("SHA256")
        .update(hash)
        .verify(this.validator, this.signature, "hex");
    } catch (error) {
      return false;
    }
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

// Validator class for Proof of Stake
class Validator {
  constructor(address, stake) {
    this.address = address;
    this.stake = stake;
    this.isActive = true;
    this.blocksProduced = 0;
    this.lastBlockTime = 0;
  }

  // Increase validator's stake
  addStake(amount) {
    this.stake += amount;
  }

  // Decrease validator's stake (for slashing or withdrawal)
  removeStake(amount) {
    this.stake = Math.max(0, this.stake - amount);
    if (this.stake === 0) {
      this.isActive = false;
    }
  }
}
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

// Main Blockchain class with Proof of Stake
class Blockchain {
  constructor() {
    this.chain = [this.createGenesisBlock()];
    this.pendingTransactions = [];
    this.blockReward = 100;
    this.contracts = new Map(); // Store smart contracts
    this.validators = new Map(); // Store validators
    this.minimumStake = 1000; // Minimum stake to become validator
    this.blockTime = 10000; // Target block time in milliseconds (10 seconds)
    this.slashingPenalty = 0.1; // 10% penalty for malicious behavior
  }

  // Create the first block in the blockchain
  createGenesisBlock() {
    return new Block(Date.parse("2024-01-01"), [], "0", "genesis");
  }

  // Get the latest block
  getLatestBlock() {
    return this.chain[this.chain.length - 1];
  }

  // Add a validator to the network
  addValidator(address, stake) {
    if (stake < this.minimumStake) {
      throw new Error(`Minimum stake required: ${this.minimumStake}`);
    }

    const validator = new Validator(address, stake);
    this.validators.set(address, validator);
    console.log(`Validator ${address} added with stake: ${stake}`);
  }

  // Select validator using weighted random selection based on stake
  selectValidator() {
    const activeValidators = Array.from(this.validators.values()).filter(
      (v) => v.isActive
    );

    if (activeValidators.length === 0) {
      throw new Error("No active validators available");
    }

    // Calculate total stake
    const totalStake = activeValidators.reduce(
      (sum, validator) => sum + validator.stake,
      0
    );

    // Generate random number between 0 and totalStake
    const randomNum = Math.random() * totalStake;

    // Select validator based on weighted probability
    let currentWeight = 0;
    for (const validator of activeValidators) {
      currentWeight += validator.stake;
      if (randomNum <= currentWeight) {
        // Additional check: ensure validator hasn't produced a block too recently
        const currentTime = Date.now();
        if (
          currentTime - validator.lastBlockTime >=
          this.blockTime / activeValidators.length
        ) {
          return validator;
        }
      }
    }

    // Fallback: return first active validator
    return activeValidators[0];
  }

  // Create and validate a new block using Proof of Stake
  createBlock(validatorAddress, privateKey) {
    const validator = this.validators.get(validatorAddress);
    if (!validator || !validator.isActive) {
      throw new Error("Invalid or inactive validator");
    }

    // Add block reward to pending transactions
    const rewardTransaction = new Transaction(
      null,
      validatorAddress,
      this.blockReward
    );
    this.pendingTransactions.push(rewardTransaction);

    const block = new Block(
      Date.now(),
      this.pendingTransactions,
      this.getLatestBlock().hash,
      validatorAddress
    );

    // Validator signs the block
    block.signBlock(privateKey);

    // Verify block is valid
    if (!block.isValidBlock()) {
      throw new Error("Invalid block signature");
    }

    // Update validator stats
    validator.blocksProduced++;
    validator.lastBlockTime = Date.now();

    console.log(`Block created by validator ${validatorAddress}`);
    this.chain.push(block);

    this.pendingTransactions = [];
    return block;
  }

  // Automatic block production (simulates network consensus)
  produceNextBlock() {
    try {
      const selectedValidator = this.selectValidator();

      // Simulate private key for demonstration (in reality, each validator has their own key)
      const simulatedPrivateKey = crypto
        .generateKeyPairSync("rsa", {
          modulusLength: 2048,
        })
        .privateKey.export({ type: "pkcs8", format: "pem" });

      return this.createBlock(selectedValidator.address, simulatedPrivateKey);
    } catch (error) {
      console.error("Failed to produce block:", error.message);
      return null;
    }
  }

  // Slash a validator for malicious behavior
  slashValidator(validatorAddress, reason) {
    const validator = this.validators.get(validatorAddress);
    if (!validator) {
      throw new Error("Validator not found");
    }

    const penalty = validator.stake * this.slashingPenalty;
    validator.removeStake(penalty);

    console.log(
      `Validator ${validatorAddress} slashed for ${reason}. Penalty: ${penalty}`
    );

    if (validator.stake < this.minimumStake) {
      validator.isActive = false;
      console.log(
        `Validator ${validatorAddress} deactivated due to insufficient stake`
      );
    }
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

  // Stake tokens to become or strengthen validator position
  stake(address, amount) {
    const balance = this.getBalance(address);
    if (balance < amount) {
      throw new Error("Insufficient balance to stake");
    }

    // Create staking transaction
    const stakingTransaction = new Transaction(
      address,
      "staking-pool",
      amount,
      { type: "stake" }
    );
    this.createTransaction(stakingTransaction);

    // Add or update validator
    if (this.validators.has(address)) {
      this.validators.get(address).addStake(amount);
    } else if (amount >= this.minimumStake) {
      this.addValidator(address, amount);
    }

    console.log(`${address} staked ${amount} tokens`);
  }

  // Get validator information
  getValidator(address) {
    return this.validators.get(address);
  }

  // Get all active validators
  getActiveValidators() {
    return Array.from(this.validators.values()).filter((v) => v.isActive);
  }

  // Calculate validator's expected return rate
  calculateValidatorReward(validatorAddress) {
    const validator = this.validators.get(validatorAddress);
    if (!validator) return 0;

    const totalActiveStake = this.getActiveValidators().reduce(
      (sum, v) => sum + v.stake,
      0
    );

    if (totalActiveStake === 0) return 0;

    // Expected reward per block based on stake proportion
    const stakeRatio = validator.stake / totalActiveStake;
    return this.blockReward * stakeRatio;
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

      // Validate block signature for PoS
      if (!currentBlock.isValidBlock()) {
        return false;
      }

      if (currentBlock.hash !== currentBlock.calculateHash()) {
        return false;
      }

      if (currentBlock.previousHash !== previousBlock.hash) {
        return false;
      }

      // Ensure validator was eligible to create this block
      const validator = this.validators.get(currentBlock.validator);
      if (!validator || !validator.isActive) {
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
console.log("=== Proof of Stake Blockchain with Smart Contracts Demo ===\n");

// Create blockchain instance
const myBlockchain = new Blockchain();

// Create wallet addresses (simplified)
const wallet1 = "wallet1-public-key";
const wallet2 = "wallet2-public-key";
const validator1 = "validator1-address";
const validator2 = "validator2-address";

// Initialize some balance for setup (simulate genesis distribution)
console.log("1. Setting up initial balances and validators...");

// Add some initial transactions to give wallets balance
const genesisTransactions = [
  new Transaction(null, wallet1, 5000), // Genesis distribution
  new Transaction(null, wallet2, 3000),
  new Transaction(null, validator1, 2000),
  new Transaction(null, validator2, 1500),
];

// Add transactions and produce first block
genesisTransactions.forEach((tx) => myBlockchain.createTransaction(tx));

// Create initial validators by staking
myBlockchain.stake(validator1, 1200);
myBlockchain.stake(validator2, 1000);

// Produce the first block
console.log("\n2. Producing first block...");
const firstBlock = myBlockchain.produceNextBlock();

// Create some transactions
console.log("\n3. Creating transactions...");
const tx1 = new Transaction(wallet1, wallet2, 500);
const tx2 = new Transaction(wallet2, validator1, 200);

myBlockchain.createTransaction(tx1);
myBlockchain.createTransaction(tx2);

console.log("\n4. Producing second block...");
const secondBlock = myBlockchain.produceNextBlock();

// Deploy a smart contract (simple token contract)
console.log("\n5. Deploying smart contract...");
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
console.log("\n6. Executing smart contract functions...");

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

// Produce block with contract transactions
console.log("\n7. Producing block with contract transactions...");
const contractBlock = myBlockchain.produceNextBlock();

// Display validator information
console.log("\n8. Validator Information:");
const activeValidators = myBlockchain.getActiveValidators();
activeValidators.forEach((validator) => {
  const expectedReward = myBlockchain.calculateValidatorReward(
    validator.address
  );
  console.log(`Validator ${validator.address}:`);
  console.log(`  - Stake: ${validator.stake}`);
  console.log(`  - Blocks Produced: ${validator.blocksProduced}`);
  console.log(`  - Expected Reward per Block: ${expectedReward.toFixed(2)}`);
  console.log(`  - Active: ${validator.isActive}`);
});

// Display blockchain information
console.log("\n9. Blockchain Information:");
console.log("Balances:");
console.log(`Wallet1: ${myBlockchain.getBalance(wallet1)}`);
console.log(`Wallet2: ${myBlockchain.getBalance(wallet2)}`);
console.log(`Validator1: ${myBlockchain.getBalance(validator1)}`);
console.log(`Validator2: ${myBlockchain.getBalance(validator2)}`);

console.log("\nContract State:");
console.log(
  "Token Contract State:",
  myBlockchain.getContractState("token-contract-address")
);

console.log("\nBlockchain Stats:");
console.log("Blockchain Valid:", myBlockchain.isChainValid());
console.log("Total Blocks:", myBlockchain.chain.length);
console.log("Total Active Validators:", activeValidators.length);

// Demonstrate validator slashing
console.log("\n10. Demonstrating validator slashing...");
const validator1Info = myBlockchain.getValidator(validator1);
console.log(`Validator1 stake before slashing: ${validator1Info.stake}`);

myBlockchain.slashValidator(validator1, "Invalid block production");

console.log(
  `Validator1 stake after slashing: ${
    myBlockchain.getValidator(validator1).stake
  }`
);
console.log(
  `Validator1 still active: ${myBlockchain.getValidator(validator1).isActive}`
);

// Display block details showing validators
console.log("\n11. Block Details (showing validators):");
myBlockchain.chain.forEach((block, index) => {
  console.log(`Block ${index}:`);
  console.log(`  - Validator: ${block.validator}`);
  console.log(`  - Transactions: ${block.transactions.length}`);
  console.log(`  - Timestamp: ${new Date(block.timestamp).toISOString()}`);
  console.log(`  - Hash: ${block.hash.substring(0, 32)}...`);
});
