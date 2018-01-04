// Block Chain should maintain only limited block nodes to satisfy the functions
// You should not have all the blocks added to the block chain in memory 
// as it would cause a memory overflow.

import java.security.HashMap;
import java.util.ArrayList;

public class BlockChain {
    public static final int CUT_OFF_AGE = 10;

    public int maxHeight = 0;
    public int curr_age = 1;

    public TransactionPool currTransPool = new TransactionPool();

    // Class that is mapped to each block at the end of a valid
    // chain within the complete block chain
    public class BuildingBlockFields {
	public BuildingBlockFields (int _chain_len, ArrayList<Integer> _ageList) {
	    int chain_len = _chain_len;
	    ArrayList<Integer> ageList = new ArrayList<>(_ageList);
	}
    }

    // Class that keeps track of the last Block placed and its corresponding
    // Transaction handler
    // This will be mapped to chain length and block age
    public class Chains {
	public Chains (Block _keyblock, TxHandler _blockHandler) {
	    Block keyblock = _keyblock;
	    TxHandler blockHandler = _blockHandler;
	}
    }
    // This maps each chain's last block to its BuildingBlockFields,
    // which are length, age, and its txHandler
    public HashMap <Chains , BuildingBlockFields> LastBlockFields = new HashMap <Chains, BuildingBlockFields> ();

    // Age of current block
    public HashMap <Block, int> BlockAge = new HashMap <Block, int>();

    // Tracks the max height block along with its txHandler
    public Chains max_height_block = new Chains();
    
    /**
     * create an empty block chain with just a genesis block. Assume {@code genesisBlock} is a valid
     * block
     */
    public BlockChain(Block genesisBlock) {
        int len = 1;

	// Calculates the initial UTXO Pool based on the transactions
	// in the block
	UTXOPool genesisUTXOPool = createInitUTXOPool (genesisBlock);

	// Uses the UTXO Pool to create a TxHandler for this chain
	TxHandler initTxHandler = TxHandler (genesisUTXOPool);

	ArrayList<Integer> InitAge = new ArrayList<Integer>();
	InitAge.add(curr_age);
  	BuildingBlockFields GenesisFields = BuildingBlockFields (len, InitAge);
	CalcBlockAge (genesisBlock);

	Chains GenesisBlockKey = Chains (genesisblock, initTxHandler);
	
	LastBlockFields.put (GenesisBlockKey, GenesisFields);
	max_height_block = GenesisBlockKey;
	maxHeight = 1;	
    }

    /** Get the maximum height block */
    public Block getMaxHeightBlock() {
        return max_height_block.keyblock;
    }

    /** Get the UTXOPool for mining a new block on top of max height block */
    public UTXOPool getMaxHeightUTXOPool() {
        return max_height_block.blockHandler.getUTXOPool();
    }

    /** Get the transaction pool to mine a new block */
    public TransactionPool getTransactionPool() {
        return currTransPool;
    }

    /** Delete the transactions from the transaction pool that are in the accepted block */
    public void CleanTransactionPool (Block block) {
	for (Transaction testTx: block.txs) {
	    ByteArrayWrapper hash = new ByteArrayWrapper(testTx.getHash());
	    currTransPool.removeTransaction (hash);
	}
    }

    /**
     * Add {@code block} to the block chain if it is valid. For validity, all transactions should be
     * valid and block should be at {@code height > (maxHeight - CUT_OFF_AGE)}.
     * 
     * <p>
     * For example, you can try creating a new block over the genesis block (block height 2) if the
     * block chain height is {@code <=
     * CUT_OFF_AGE + 1}. As soon as {@code height > CUT_OFF_AGE + 1}, you cannot create a new block
     * at height 2.
     * 
     * @return true if block is successfully added
     */
    public boolean addBlock(Block block) {
	boolean add_success = false;
	// Cycle through all possible Forks of the Blockchain

	for (Chains TestChain: LastBlockFields.keySet()) {
	    // Test if transactions are valid
	    boolean valid_check = true;
	    for (Transaction test_tx:block.txs) {
		if (!TestChain.BlockHandler.isValidTx(test_tx)){
		    valid_check = false;
		    break;
		}
	    }
	    // All transactions are valid, so check appropriate
	    // block length
	    if (valid_check == true) {
		int newHeight = (LastBlockFields.get(TestChain)).chain_len + 1;
		if (newHeight > (maxHeight - CUT_OFF_AGE)) {
		    
		    // Update the UTXOPool by incorporating the transactions
		    // from the block

		    TestChain.BlockHandler.handleTxs (block.txs);
		    
			
		    // Add the block to this chain, and add to the
		    // hashmap

		    Chains addedBlock = Chains (block, TxHandler(TestChain.BlockHandler.getUTXOPool()));
		    // Determine age of the block and add that age to the ageList array

		    CalcBlockAge (block);
		    newAgeList = new ArrayList<>(LastBlockFields.get(TestChain).ageList);
		    newAgeList.add(BlockAge.get(block));
		    BuildingBlockFields addedFields = new BuildingBlockFields (newHeight, newAgeList);
		    // Put chain and its Fields (length and age list) into hashmap

		    LastBlockFields.put (addedBlock, addedFields);

		    add_success = true;

		    // Update the transaction pool by deleting all the transactions
		    // in this accepted block from the transaction pool

		    CleanTransactionPool (block);
		    
		    // Check if this chain is the new max chain length
		    if (newHeight > maxHeight) {
			max_height_block = Chains (addedBlock.keyblock,
						   addedBlock.BlockHandler);
			maxHeight = newHeight;
		    }

		    if (newHeight == maxHeight) {
			maxHeightAgeList =  LastBlockFields.get(max_height_block).AgeList;
			testIndex = newHeight - 1;
			while (testIndex >= 0) {
			    while (maxHeightAgeList(testIndex) == newAgeList(testIndex)) {
				testIndex = testIndex - 1;
			    }
			}
			
			if (newAgeList(testIndex) < maxHeightAgeList(testIndex)) {
			    max_height_block = Chains (addedBlock.keyblock, addedBlock.BlockHandler);
			    maxHeight = newHeight;
			}
		    }
		}
	    }
	}

	return add_success;	
    }

    /** Add a transaction to the transaction pool */
    public void addTransaction(Transaction tx) {
        currTransPool.addTransaction (tx);
    }

    // This creates the UTXOPool for the initial genesis block
    // of the blockchain
    public UTXOPool createInitUTXOPool (Block initBlock) {
	UTXOPool InitUTXOPool = new UTXOPool();
	
	// First, let's deal with the coinbase
	Transaction coinbase_tx = initBlock.getCoinbase();
	UTXO coinbase_UTXO = UTXO(coinbase_tx.hash, 0);
	InitUTXOPool.addUTXO (coinbase_UTXO, (coinbase_tx.outputs).get(0));

	// Now, we will add the other non coinbase transactions to the pool

	for (Transaction init_tx:initBlock.txs) {
	    int index = 0;
	    for (Transaction.Output initOp:init_tx.outputs) {
		UTXO test_UTXO = UTXO (init_tx.hash, index);
		InitUTXOPool.addUTXO (test_UTXO, initOp);
		index++;
	    }
	}

	// Finally, this will check if any inputs among the block's transactions
	// were also earlier outputs. If this is the case, the UTXO will be
	// deleted from the pool, as it has already been spent

	for (Transaction init_tx:initBlock.txs) {
	    int index = 0;
	    for (Transaction.Input initInp:init_tx.inputs) {
		UTXO test_UTXO = UTXO (initInp.prevTxHash, initInp.outputIndex);
		index++;
		if (InitUTXOPool.contains(test_UTXO)) {
		    InitUTXOPool.removeUTXO (test_UTXO);
		}
	    }
	}

	return InitUTXOPool;
    }

    // Determines the age of a block and enters the block into the hashmap
    // if not already there

    public int CalcBlockAge (Block EndBlock) {
	if (!BlockAge.contains(EndBlock)) {
	    BlockAge.put (EndBlock, curr_age);
	    curr_age++;
	}

	return BlockAge.get(EndBlock);
    }
	
}
