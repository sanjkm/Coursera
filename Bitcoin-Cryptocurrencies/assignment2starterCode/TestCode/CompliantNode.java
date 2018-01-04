import java.util.ArrayList;
import java.util.Set;

/* CompliantNode refers to a node that follows the rules (not malicious)*/
public class CompliantNode implements Node {

    public CompliantNode(double p_graph, double p_malicious, double p_txDistribution, int numRounds) {
        // IMPLEMENT THIS
	double _p_graph = p_graph;
	double _p_malicious = p_malicious;
	double _p_txDistribution = _p_txDistribution;
	double _numRounds = numRounds;

	int currRound = 1;
    }

    // Creates an integer arraylist with the indices of each node
    // following this node
    
    public void setFollowees(boolean[] followees) {
        // IMPLEMENT THIS
	ArrayList <Integer> followees_list = new ArrayList <Integer>();

	for (int i = 0; i < followees.size(); i++) {
	    if (followees[i] == true)
		followees_list.add (i);
	}
		
    }

    // Creates Set containing the initally allocated valid transactions
    // to the node
    public void setPendingTransaction(Set<Transaction> pendingTransactions) {
        // IMPLEMENT THIS
	
	Set <Transaction> initValidTransactions = new Set<Transaction> ();

	for (Transaction pendingTx : pendingTransactions) 
	    initValidTransactions.add (pendingTx);
    }

    // If this is the first round, send to Followers only the transactions that
    // have initially been provided as valid, from the setPendingTransactions
    // function

    // Otherwise, run the program to determine what other transactions to send
    // over along with the initValidTransactions
    
    public Set<Transaction> sendToFollowers() {
	if (currRound == 1) {
	    currRound += 1;
	    return initValidTransactions;
	}

	else {
	    currRound += 1;

	    Set <Transaction> AllValidTxs = new Set<Transaction>();
	    AllValidTxs.addAll (initValidTransactions);
	    AllValidTxs.addAll (OthAcceptedTransactions);
	    return AllValidTxs;
	}
	
    }

    // Creates map, where key is the node index, and value is a set of
    // transactions that the key proposed as valid
    public void receiveFromFollowees(Set<Candidate> candidates) {
	
	HashMap<Integer, Set<Transaction>> receivedTransactions = new HashMap<Integer, Set<Transaction>>();

	for (Candidate test_candidate : candidates) {
	    if (!receivedTransactions.containsKey (test_candidate.sender)) {
		Set<Transaction> transactions = new HashSet<>();
		receivedTransactions.put (test_candidate.sender, transactions);

	    }

	    Transaction cand_tx = new Transaction(test_candidate.tx);
	    receivedTransactions.get(test_candidate.sender).add(cand_tx);
	}

	OthAcceptedTxs = CalcOtherValidTransactions (receivedTransactions);
	
    }


    // Returns an ArrayList of AcceptedTransactions based on the proposed
    // transactions sent over by the nodes that this node follows
    
    private Set<Transactions> CalcOtherValidTransactions (HashMap <Integer, Set<Transaction>> receivedTransactions) {

	HashMap<Transaction, Integer> TxAcceptanceCount = new HashMap<Transaction, Integer>();

	ArrayList<Transaction> AcceptedTxs = new ArrayList <Transaction> ();

	int thresh_num = 3; // if a transaction is sent over this many times,
	// it is assumed to be valid

	for (Integer node_test: receivedTransactions.keySet()) {
    
	    for (Transaction received_tx : receivedTransactions.get(node_test)) {
		if (!TxAcceptanceCount.containsKey (received_tx)) {
		    int test_int = 1;
		    TxAcceptanceCount.put (received_tx, test_int);
		}
		else {

		    TxAcceptanceCount.put(received_tx,
					  TxAcceptanceCount.get(received_tx) + 1);
		}

		if (TxAcceptanceCount.get(received_tx) == thresh_num) 
		    AcceptedTxs.add (received_tx);
	    }
		
		 
	}

	return AcceptedTxs;

    }
    
}
