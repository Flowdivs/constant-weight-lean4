-- Formally Generated Lean 4 Verification Certificate
-- Benchmark: Constant-Weight Binary Code A(18, 6, 5) >= 69
-- Certified via Lean 4 kernel reflexivity (rfl)

def overlap (c1 c2 : List Nat) : Nat :=
  (c1.filter (fun x => c2.contains x)).length

def isPairValid (c1 c2 : List Nat) : Bool :=
  overlap c1 c2 <= 2

def checkAll (l : List (List Nat)) : Bool :=
  match l with
  | [] => true
  | x :: xs => xs.all (isPairValid x) && checkAll xs

def checkWeights (l : List (List Nat)) : Bool :=
  l.all (fun c => c.length == 5 && c.all (fun x => x < 18))

-- The 69 discovered codewords (subsets of size 5 in Fin 18)
def code69 : List (List Nat) := [[13, 14, 15, 16, 17], [10, 11, 12, 16, 17], [7, 8, 9, 16, 17], [4, 5, 6, 16, 17], [1, 2, 3, 16, 17], [6, 9, 12, 15, 17], [3, 8, 11, 15, 17], [2, 5, 7, 15, 17], [1, 4, 10, 15, 17], [2, 4, 8, 12, 17], [3, 5, 12, 14, 17], [1, 7, 12, 13, 17], [1, 6, 8, 14, 17], [5, 8, 10, 13, 17], [0, 2, 6, 13, 17], [3, 6, 7, 10, 17], [1, 5, 9, 11, 17], [3, 4, 9, 13, 17], [0, 4, 7, 11, 17], [2, 9, 10, 14, 17], [5, 8, 12, 15, 16], [1, 6, 7, 15, 16], [2, 4, 11, 15, 16], [3, 9, 10, 15, 16], [3, 6, 12, 13, 16], [1, 4, 9, 12, 16], [2, 7, 12, 14, 16], [1, 8, 11, 13, 16], [3, 4, 8, 14, 16], [0, 2, 8, 10, 16], [2, 5, 9, 13, 16], [1, 5, 10, 14, 16], [3, 5, 7, 11, 16], [4, 7, 10, 13, 16], [0, 9, 11, 14, 16], [2, 10, 12, 13, 15], [3, 4, 7, 12, 15], [1, 11, 12, 14, 15], [0, 4, 8, 13, 15], [7, 8, 10, 14, 15], [1, 2, 8, 9, 15], [5, 6, 10, 11, 15], [2, 3, 6, 14, 15], [1, 3, 5, 13, 15], [4, 5, 9, 14, 15], [7, 9, 11, 13, 15], [6, 7, 8, 11, 12], [8, 9, 12, 13, 14], [1, 3, 8, 10, 12], [1, 2, 5, 6, 12], [0, 4, 6, 10, 12], [0, 5, 11, 12, 13], [5, 7, 9, 10, 12], [0, 2, 3, 9, 12], [3, 5, 6, 8, 9], [1, 4, 5, 7, 8], [2, 5, 8, 11, 14], [2, 3, 7, 8, 13], [4, 8, 9, 10, 11], [0, 5, 6, 7, 14], [4, 6, 11, 13, 14], [1, 6, 9, 10, 13], [2, 4, 6, 7, 9], [0, 1, 3, 6, 11], [2, 3, 4, 5, 10], [0, 3, 10, 13, 14], [0, 1, 2, 4, 14], [1, 3, 7, 9, 14], [1, 2, 7, 10, 11]]

-- Formal Theorem 1: Code cardinality is exactly 69
theorem code_cardinality_is_69 : code69.length = 69 := by
  rfl

-- Formal Theorem 2: All codewords have constant weight 5 with support in Fin 18
theorem code_constant_weight_5 : checkWeights code69 = true := by
  rfl

-- Formal Theorem 3: All 2346 pairs satisfy the Hamming distance constraint d >= 6
theorem code_min_distance_6 : checkAll code69 = true := by
  rfl

#check code_cardinality_is_69
#check code_constant_weight_5
#check code_min_distance_6
#eval code69.length
