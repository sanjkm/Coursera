import java.util.ArrayList;
import java.util.Arrays;

public class TxHandler {

    /**
     * Creates a public ledger whose current UTXOPool (collection of unspent transaction outputs) is
     * {@code utxoPool}. This should make a copy of utxoPool by using the UTXOPool(UTXOPool uPool)
     * constructor.
     */

    private UTXOPool currUTXOPool;
    
    public TxHandler(UTXOPool utxoPool) {

	currUTXOPool = new UTXOPool (utxoPool);
    }

    /**
     * @return true if:
     * (1) all outputs claimed by {@code tx} are in the current UTXO pool, 
     * (2) the signatures on each input of {@code tx} are valid, 
     * (3) no UTXO is claimed multiple times by {@code tx},
     * (4) all of {@code tx}s output values are non-negative, and
     * (5) the sum of {@code tx}s input values is greater than or equal to the sum of its output
     *     values; and false otherwise.
     */
    public boolean isValidTx(Transaction tx) {
        // IMPLEMENT THIS
	// Sanjay code
	
	// Checks for double maps of the same UTXO
	ArrayList<UTXO> claimedUTXOlist;
	claimedUTXOlist = new ArrayList<UTXO>();

	double input_sum = 0.0;
 	double output_sum = 0.0;
	
	for (int i=0;i<tx.numInputs();i++) {
	    
	    Transaction.Input inp = tx.getInput(i);
	    UTXO in_utxo = new UTXO(inp.prevTxHash, inp.outputIndex);
	    
	    // Check if in_utxo is in the currUTXOPool
	    // If not in Pool, then not a valid tx
	    if ((currUTXOPool.contains (in_utxo)) == false) {
		return false;
	    }

	    // If in_utxo has already been claimed, then not a valid tx
	    if (claimedUTXOlist.contains (in_utxo) == true) {
		return false;
	    }

	    // Now, we add in_utxo to the claimed list
	    claimedUTXOlist.add (in_utxo);	    
	    
	    // Verify the signature of the claimed output	    
	    // PublicKey in_pub_key = (currUTXOPool.getTxOutput (in_utxo)).address;

	    byte[] msg = tx.getRawDataToSign (i);

	    if (Crypto.verifySignature ((currUTXOPool.getTxOutput (in_utxo)).address,
				 msg, inp.signature) == false) {
		return false;
	    }

	    input_sum +=  (currUTXOPool.getTxOutput (in_utxo)).value;
	}

	// Checks for tx outputs with negative values, and gets the
	// sum of all out tx output values
	for (Transaction.Output op : tx.getOutputs()) {
	    if (op.value < 0) {
		return false;
	    }
	    output_sum += op.value;
	}

	// Input sum less than output sum means invalid tx
	if (input_sum < output_sum) {
	    return false;
	}

	return true;	    
    }

    /**
     * Handles each epoch by receiving an unordered array of proposed transactions, checking each
     * transaction for correctness, returning a mutually valid array of accepted transactions, and
     * updating the current UTXO pool as appropriate.
     */
    public Transaction[] handleTxs(Transaction[] possibleTxs) {
        // IMPLEMENT THIS
	ArrayList <Transaction> acceptedTxs = new ArrayList<Transaction>();
	ArrayList <Integer> accepted_tx_indices = new ArrayList<Integer>();
	int num_accepted;

	ArrayList <Transaction> poss_Txs = new ArrayList<Transaction>();
	
	for (int i=0;i<possibleTxs.length;i++) {
	    poss_Txs.add (possibleTxs[i]);
	}
	
	
	while (true) {
	    num_accepted = 0;
	    
	    for (int i=0; i < poss_Txs.size(); i++) {

		if (isValidTx (poss_Txs.get(i)) == true) {
		    num_accepted += 1;
		    acceptedTxs.add (poss_Txs.get(i));
		    accepted_tx_indices.add(i);

		    // Modify currUTXOlist appropriately
		    // Cycle through the list of inputs in the
		    // transaction
		    for (int j=0; j<(poss_Txs.get(i)).numInputs(); j++) {
			Transaction.Input inp = (poss_Txs.get(i)).getInput(j);
			
			UTXO old_UTXO = new UTXO(inp.prevTxHash, inp.outputIndex);

			// Remove old_UTXO from currUTXOlist
			currUTXOPool.removeUTXO (old_UTXO);
		    }
		    
		    for (int j=0; j<(poss_Txs.get(i)).numOutputs(); j++) {
			// construct new_UTXO with tx input and output
			Transaction.Output op = (poss_Txs.get(i)).getOutput(j);
			UTXO new_UTXO = new UTXO((poss_Txs.get(i)).getRawDataToSign(j),
					     j);
			currUTXOPool.addUTXO (new_UTXO, op);
		    }
		}
	    }
	    
	    // Now, remove the accepted Txs from poss_Txs
	    // and clear the accepted tx indices array
	    
	    for (int nums=0; nums < num_accepted; nums++) {
		int rem_index = accepted_tx_indices.get(num_accepted - nums - 1);
		poss_Txs.remove(rem_index);
	    }
		
	    accepted_tx_indices.clear();	    
	    		    

	    // If no transactions in the list are determined to be acceptable,
	    // then there are no more to be added
	    // Return the list of acceptedTxs
	    if (num_accepted == 0) {
		Transaction[] final_Txs = new Transaction[acceptedTxs.size()];
		int k = 0;
		for (Transaction accTx : acceptedTxs) {
		    final_Txs[k++] = accTx;
		}
		return final_Txs;
		
	    }
	}
    
    }

    public UTXOPool getUTXOPool () {

	return currUTXOPool;
    }
}
