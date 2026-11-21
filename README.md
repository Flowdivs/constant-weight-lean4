# Formal Verification of the Constant-Weight Binary Code $A(18, 6, 5) \ge 69$ in Lean 4 and Computational Rigidity Analysis

This repository provides a machine-checked formal verification in **Lean 4** of the lower bound for the binary constant-weight code parameter $A(18, 6, 5) \ge 69$, alongside an algebraic orbit decomposition and a CDCL SAT-based local rigidity analysis.

---

## 1. Mathematical Background

In combinatorial coding theory, $A(n, d, w)$ denotes the maximum possible cardinality of a binary code of block length $n$, constant Hamming weight $w$, and minimum pairwise Hamming distance at least $d$. Equivalently, this corresponds to the maximum size of a family of $w$-element subsets of an $n$-element set such that every distinct pair intersects in at most $w - d/2$ elements.

For the parameter set $(n=18, d=6, w=5)$:
* The theoretical linear programming / Johnson upper bound is $A(18, 6, 5) \le 72$.
* The best-known lower bound is **$A(18, 6, 5) \ge 69$**, established in 2003 by Hui Kheng Aw, Yeow Meng Chee, and Alan C. H. Ling ([*Ars Combinatoria*, Vol. 67, pp. 313–318](https://www.win.tue.nl/~aeb/codes/Andw.html)).
* The exact value of $A(18, 6, 5)$ remains open in the range $\{69, 70, 71, 72\}$.

This project provides:
1. **Formal Proof:** A standalone, kernel-verified proof in **Lean 4** establishing that the 69-codeword construction satisfies all distance and weight constraints using compiler reflexivity (`rfl`).
2. **Algebraic Orbit Decomposition:** An exact classification of all $\binom{18}{5} = 8,568$ codewords under the cyclic groups $C_{18}$ and $C_{17}$.
3. **Rigidity Analysis:** A Boolean Satisfiability (SAT) verification using CaDiCaL 1.9.5 exhaustively proving that the 69-codeword configuration admits zero 3-for-4 codeword exchanges.

---

## 2. Formal Verification in Lean 4

The file `FormalRecordCertificate.lean` contains the self-contained formal proof. Each codeword is represented as a 5-element coordinate list over $\{0, \dots, 17\}$. 

The Lean 4 kernel evaluates three theorems directly via reflexivity:

```lean
-- Theorem 1: The code cardinality is exactly 69
theorem code_cardinality_is_69 : code69.length = 69 := by rfl

-- Theorem 2: Every codeword has constant weight 5 with support in Fin 18
theorem code_constant_weight_5 : checkWeights code69 = true := by rfl

-- Theorem 3: All 2,346 pairs satisfy pairwise Hamming distance >= 6 (overlap <= 2)
theorem code_min_distance_6 : checkAll code69 = true := by rfl
```

### Reproducing the Formal Proof
Requires Lean 4 (version 4.x or later):

```bash
lean FormalRecordCertificate.lean
```

Execution terminates with return code `0`, confirming all $\binom{69}{2} = 2,346$ pairwise distance checks pass the Lean kernel without external axioms or unproven dependencies.

---

## 3. Computational Rigidity & SAT Findings

To investigate whether the 69-codeword code could be extended or locally modified to reach size 70, we evaluated its combinatorial neighborhood using the CaDiCaL 1.9.5 CDCL SAT solver:

1. **Direct Addition (0-Conflict):** Out of all 8,499 words outside the code, **0 words** are compatible with the entire 69-code.
2. **1-for-2 Exchanges:** Exactly 5 outside words conflict with only one codeword in the 69-code. Zero pairs among them share the same target and are mutually compatible.
3. **2-for-3 Exchanges:** Exactly 46 outside words conflict with only two codewords. Zero triples form a valid mutually compatible replacement for any pair.
4. **3-for-4 Exchanges (Exhaustive SAT Sweep):** We tested all $\binom{69}{3} = 52,394$ subsets of 3 dropped codewords. 
   * 12,946 candidate pools contained $\ge 4$ surviving compatible words.
   * CaDiCaL evaluated each candidate pool with Cardinality Totalizer constraints.
   * **Result:** All 12,946 candidate pools returned **UNSAT**.

This establishes that the 69-codeword construction is an **isolated local maximum**; reaching size 70 (if it exists) requires a global structural divergence of at least 4 codewords.

---

## 4. Group Action & Orbit Classification

The script `algebraic_orbits.py` groups the $\binom{18}{5} = 8,568$ words into orbits under prescribed permutation groups:

| Group Action | Total Orbits | Internally Valid Orbits | Max Orbit Clique | Codewords |
| :--- | :---: | :---: | :---: | :---: |
| **$C_{18}$ on $\mathbb{Z}_{18}$** | 476 | 273 | 3 orbits | 54 |
| **$C_{17}$ on $\mathbb{Z}_{17} \cup \{\infty\}$** | 504 | 236 | 4 orbits | 68 |
| **$D_{18}$ (Dihedral)** | 252 | 9 | 2 orbits | 36 |
| **$D_{17}$ (Dihedral)** | 280 | 12 | 4 orbits | 68 |
| **$C_3$ on $\mathbb{Z}_{18}$** | 2,856 | 2,646 | — | — |

*Note: For $C_{18}$, clique size $\ge 4$ ($\ge 72$ words) was proven UNSAT by CaDiCaL. For $C_{17}$, clique size $\ge 5$ ($\ge 85$ words) was proven UNSAT.*

---

## 5. Repository Structure

```
├── FormalRecordCertificate.lean  # Self-contained Lean 4 kernel verification
├── orbit_record_found.json       # 69 codewords (integers, bitsets, hex coordinates)
├── algebraic_orbits.py           # Group theory orbit decomposition engine
├── orbit_sat_solver.py           # PySAT (CaDiCaL 1.9.5) orbit compatibility solver
├── verify_code.py                # Standalone Python verification script
└── README.md                     # Documentation and mathematical background
```

---

## 6. Provenance & Methodology

This research was conducted using human-directed algorithmic search assisted by a coordinated multi-agent software framework:
* **Mathematical Direction & Scoping:** Problem selection, formal parameter bounding, and strategy formulation.
* **Algebraic Orbit Construction:** Automated permutation group classification and orbit compatibility modeling.
* **Exact Constraint Solving:** Automated formulation and execution of CDCL SAT instances using PySAT and CaDiCaL 1.9.5.
* **Formal Verification:** Translation into dependent type theory and kernel verification via the Lean 4 proof assistant.

---

## References

1. H. K. Aw, Y. M. Chee, and A. C. H. Ling, *"Six New Constant Weight Binary Codes,"* *Ars Combinatoria*, Vol. 67, pp. 313–318, 2003.
2. A. E. Brouwer, J. B. Shearer, N. J. A. Sloane, and W. D. Smith, *"A new table of constant weight codes,"* *IEEE Transactions on Information Theory*, Vol. 36, No. 6, pp. 1334–1380, 1990.
3. A. E. Brouwer, *"Tables of Bounds for Binary Constant Weight Codes,"* Eindhoven University of Technology, [Online Database](https://www.win.tue.nl/~aeb/codes/Andw.html).
4. The Lean 4 Theorem Prover, [https://lean-lang.org/](https://lean-lang.org/).
