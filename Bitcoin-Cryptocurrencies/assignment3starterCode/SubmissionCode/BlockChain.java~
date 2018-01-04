// Block Chain should maintain only limited block nodes to satisfy the functions
// You should not have all the blocks added to the block chain in memory 
// as it would cause a memory overflow.

import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;

public class BlockChain {
    public static final int CUT_OFF_AGE = 10;

    public int maxHeight;
    public int curr_age = 1;

    public TransactionPool currTransPool = new TransactionPool();

    public class TreeChains {
	Block keyblock;
	TxHandler blockHandler;
	int blockAge;
	int chain_len;
	
	public TreeChains (Block _keyblock, TxHandler _blockHandler,
		       int _blockAge) {
	    this.keyblock = _keyblock;
	    this.blockHandler = _blockHandler;
	    this.blockAge = _blockAge;
	}

 	public TreeChains (Block _keyblock, TxHandler _blockHandler,
			   int _blockAge, int _chain_len) {
	    this.keyblock = _keyblock;
	    this.blockHandler = _blockHandler;
	    this.blockAge = _blockAge;
	    this.chain_len = _chain_len;
	}

	public void setChainLen (int _chain_len) {
	    this.chain_len = _chain_len;
	}
	
    }

    // Tree implementation in class MyTreeNode
    public class MyTreeNode  {
	private TreeChains data = null;
	private List<MyTreeNode> children = new ArrayList<>();
	private MyTreeNode parent = null;

	public MyTreeNode(TreeChains data) {
	    this.data = data;
	}

	public void addChild(MyTreeNode child) {
	    child.setParent(this);
	    this.children.add(child);
	}

	public void addChild(TreeChains data) {
	    MyTreeNode newChild = new MyTreeNode (data);
	    newChild.setParent(this);
	    children.add(newChild);
	}

	public void addChildren(List<MyTreeNode> children) {
	    for(MyTreeNode t : children) {
		t.setParent(this);
	    }
	    this.children.addAll(children);
	}

	public List<MyTreeNode> getChildren() {
	    return children;
	}

	public TreeChains getData() {
	    return data;
	}

	public void setData(TreeChains data) {
	    this.data = data;
	}

	private void setParent(MyTreeNode parent) {
	    this.parent = parent;
	}

	public MyTreeNode getParent() {
	    return parent;
	}
    }

    MyTreeNode initNode = new MyTreeNode(null);
    boolean AddBlockSuccess = false;

    // Function that breaks the code
    public void unitBreak (int i) {
	ArrayList <Integer> unitList = new ArrayList<>();

	int x = unitList.get(i);
    }
	
    
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
	TxHandler initTxHandler = new TxHandler (genesisUTXOPool);


	initNode = new MyTreeNode (new TreeChains(genesisBlock, initTxHandler,
						  curr_age, len));
	
	maxHeight = 1;	
    }


    public MyTreeNode getMaxHeightIndexT(MyTreeNode parentNode, MyTreeNode currMaxNode) {


	for (int i = 0; i < parentNode.children.size(); i++) {
	    if (parentNode.children.get(i).children.size() > 0) {
		currMaxNode = getMaxHeightIndexT (parentNode.children.get(i), currMaxNode);
	    }

	    // If an end node, do comparisons
	    else {
		if (parentNode.children.get(i).data.chain_len > currMaxNode.data.chain_len) {
		    currMaxNode = parentNode.children.get(i);
		}

		// Compare chain age if chain lengths are the same
		if (parentNode.children.get(i).data.chain_len == currMaxNode.data.chain_len) {
		    MyTreeNode testNode = parentNode.children.get(i);
		    MyTreeNode MaxTestNode = currMaxNode;
		    while (testNode.data.blockAge == MaxTestNode.data.blockAge) {
			if (testNode.parent == null) {
			    break;
			}

			testNode = testNode.parent;
			MaxTestNode = MaxTestNode.parent;
		    }
		
		    if (testNode.data.blockAge < MaxTestNode.data.blockAge) {
			currMaxNode = parentNode.children.get(i);
		    }

		}
	    }
	}

	maxHeight = currMaxNode.data.chain_len;
	return currMaxNode;
    }

    public int getMaxHeight() {
	MyTreeNode MaxHeightNode = getMaxHeightIndexT (initNode, initNode);
	return MaxHeightNode.data.chain_len;
    }
	
    /** Get the maximum height block */
    public Block getMaxHeightBlock() {
	MyTreeNode MaxHeightNode = getMaxHeightIndexT (initNode, initNode);
	return MaxHeightNode.data.keyblock;
    }

    /** Get the UTXOPool for mining a new block on top of max height block */
    public UTXOPool getMaxHeightUTXOPool() {
	MyTreeNode MaxHeightNode = getMaxHeightIndexT (initNode, initNode);
	return MaxHeightNode.data.blockHandler.getUTXOPool();
    }

    /** Get the transaction pool to mine a new block */
    public TransactionPool getTransactionPool() {
        return currTransPool;
    }

    /** Delete the transactions from the transaction pool that are in the accepted block */
    public void CleanTransactionPool (Block block) {
	for (Transaction testTx: block.getTransactions()) {
	    currTransPool.removeTransaction (testTx.getHash());
	}
    }


    // Checks if the block b can be built upon the chain ending in childNode
    public boolean checkValidChain (Block block, MyTreeNode childNode) {

	// Check if hashes match up
	if (compareBlockHash (block, childNode.data.keyblock) == false) {
	    return false;
	}

	// Check if all transactions are valid
	Transaction[] txs = block.getTransactions().toArray (new Transaction[0]);
	Transaction[] validTxs = childNode.data.blockHandler.handleTxs(txs);

	if (txs.length != validTxs.length) {
	    return false;
	}
	
	// All transactions are valid, so check appropriate
	// block length
	int newHeight = childNode.data.chain_len + 1;

	if (newHeight > (maxHeight - CUT_OFF_AGE)) {
	    return true;		
	}

	return false;
    }

    // This function is called if the block can be added on top of
    // the chain ending in parentNode
    // It makes a new node containing the block and enters its fields appropriately
    public MyTreeNode buildBlockonNode (Block block, MyTreeNode currNode) {
	
	// Update the UTXOPool by incorporating the transactions
	// from the block

	Transaction[] blockTxArray = new Transaction[block.getTransactions().size()];
	for (int i = 0; i<blockTxArray.length; i++) {
	    blockTxArray[i] = block.getTransactions().get(i);
	}

	TxHandler NewChainBlockHandler = new TxHandler (currNode.data.blockHandler.getUTXOPool());
	NewChainBlockHandler.handleTxs (blockTxArray);
	
	MyTreeNode newNode = new MyTreeNode(new TreeChains (block, NewChainBlockHandler, curr_age,
							currNode.data.chain_len + 1));
	
	// Update the transaction pool by deleting all the transactions
	// in this accepted block from the transaction pool
	CleanTransactionPool (block);

	return newNode;
    }
    
    public List<MyTreeNode> traverse(MyTreeNode parentNode, Block block) {
	// traverse all children nodes of the parent
	for(int i=0; i<parentNode.children.size(); i++) {
	    // Check if valid to add block onto child node
	    if (checkValidChain (block, parentNode.children.get(i)) == true) {
     
		// Create a child note containing this block,
		// make it a child of the inputted node
		parentNode.children.get(i).
		    children.add (buildBlockonNode (block,
						    parentNode.children.get(i)));
		AddBlockSuccess = true;

		//		unitBreak(i);
	    }
	    		
	    // traverse children
	    int NumChildren = parentNode.children.get(i).children.size();
	    parentNode.children.get(i).addChildren (traverse(parentNode.children.get(i), block));
	    // Removes the old version of children that may not have added
	    // the new block
	    for (int j=NumChildren-1;j>=0;j--) {
		parentNode.children.get(i).children.remove(j);
	    }
	}
	return parentNode.children;
    }

    
    // Function will cycle through all active nodes. It will run
    // another function to check if block b can be built on top
    // of the node. If so, it will build the block on top of the node
    public boolean addBlock (Block block) {

	AddBlockSuccess = false;
	
	// Increment the current blockchain age to mark this block's age
	curr_age++;
	
	// if genesis block (prev hash is null) return false
	if (block.getPrevBlockHash() == null) {
	    return false;
	}
	
	getMaxHeightIndexT(initNode, initNode); // refreshes MaxHeight variable	

	// check the parent node to see if can add block

	if (checkValidChain (block, initNode)) {
	    // Create a child note containing this block,
	    // make it a child of the inputted node
	    AddBlockSuccess = true;
	    initNode.children.add (buildBlockonNode (block, initNode));
	}
	    		
	// traverse children
	int NumChildren = initNode.children.size();
	
	initNode.addChildren (traverse(initNode, block));

	for (int j=NumChildren-1;j>=0;j--) {
	    initNode.children.remove(j);
	}

	getMaxHeightIndexT(initNode, initNode); // refreshes MaxHeight variable

	if ((getMaxHeight() > 20) && (AddBlockSuccess == false)) {
	    unitBreak(maxHeight);
	}
	
	return AddBlockSuccess;
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
	UTXO coinbase_UTXO = new UTXO(coinbase_tx.getHash(), 0);
	InitUTXOPool.addUTXO (coinbase_UTXO, (coinbase_tx.getOutputs()).get(0));

	// Now, we will add the other non coinbase transactions to the pool

	for (Transaction init_tx:initBlock.getTransactions()) {
	    int index = 0;
	    for (Transaction.Output initOp:init_tx.getOutputs()) {
		UTXO test_UTXO = new UTXO (init_tx.getHash(), index);
		InitUTXOPool.addUTXO (test_UTXO, initOp);
		index++;
	    }
	}

	// Finally, this will check if any inputs among the block's transactions
	// were also earlier outputs. If this is the case, the UTXO will be
	// deleted from the pool, as it has already been spent

	for (Transaction init_tx:initBlock.getTransactions()) {
	    int index = 0;
	    for (Transaction.Input initInp:init_tx.getInputs()) {
		UTXO test_UTXO = new UTXO (initInp.prevTxHash, initInp.outputIndex);
		index++;
		if (InitUTXOPool.contains(test_UTXO)) {
		    InitUTXOPool.removeUTXO (test_UTXO);
		}
	    }
	}

	return InitUTXOPool;
    }

    public boolean compareBlockHash (Block current, Block parent) {

	for (int i=0;i<current.getPrevBlockHash().length;i++) {
	    if ((current.getPrevBlockHash())[i] != (parent.getHash())[i]) {
		return false;
	    }
	}

	return true;
    }
}

