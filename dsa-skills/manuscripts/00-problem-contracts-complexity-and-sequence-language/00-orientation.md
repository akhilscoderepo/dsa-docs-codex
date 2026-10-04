<!-- section: orientation -->
## Orientation

This chapter teaches no algorithm. It teaches you how to read a problem before you choose an algorithm. You identify what the limits allow. You record what the input guarantees and whether your method may change it. You define which positions an answer may use. You then estimate the cost and include any Java operation that changes that estimate. Every later chapter relies on these skills.

### Start With These Skills

You should be able to write a loop over an array in Java, read a simple Big-O bound, and run a small program. This chapter uses only arrays and strings. Each exercise isolates one decision. First, you read the input contract. Next, you estimate the cost. Finally, you design an adversarial test that attacks one assumption.

### Learn Eight Core Habits

The chapter builds eight habits. Constraint signals use the input limits to reject approaches that cannot finish in time. Mutation contracts separate the physical array from the logical answer and state which values your method may change. Sequence language distinguishes a subarray, subsequence, and subset through their index rules. Input guarantees separate the caller's promises from your own assumptions.

The remaining habits focus on cost and correctness. Complexity analysis counts how often the dominant statement runs. Amortized analysis spreads an occasional expensive operation across a sequence of operations. Adversarial dry runs use a small input to attack one failure mode. Java API analysis includes the cost and semantics of each library call inside the algorithm.

### Work Through Each Lesson

Read the opening example and the first working solution. Before you continue, predict which input makes that solution too slow or incorrect. Step through the trace and watch how each variable changes. Then solve the four exercises in order. Write your reasoning in the notes box before you open a hint or solution. The build runs every solution's Java assertions, so the executable examples support the numeric claims.

### Check Your Foundation

Before Chapter 01, read a new prompt and write down its guarantees. State whether your method may mutate the input and which part of the output remains valid. Name the required sequence relationship and estimate the time and space budget. Choose one adversarial test. Finally, identify any Java call that changes the claimed cost. The review section tests each skill separately.
