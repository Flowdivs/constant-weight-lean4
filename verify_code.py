import json
import os
import sys
import subprocess

def codeword_to_bits(cw):
    if isinstance(cw, int):
        return [i for i in range(18) if (cw & (1 << i))]
    elif isinstance(cw, str):
        val = int(cw, 0)
        return [i for i in range(18) if (val & (1 << i))]
    elif isinstance(cw, list):
        return sorted(cw)
    else:
        raise ValueError(f"Unknown codeword format: {cw}")

def verify_code(json_path="t:/Codestral/lemma/orbit_record_found.json"):
    if not os.path.exists(json_path):
        print(f"File {json_path} does not exist yet.")
        return False, None

    with open(json_path, "r") as f:
        data = json.load(f)

    # Could be stored under "codewords", "codewords_hex", "codeword_indices", or direct list
    raw_cws = None
    if isinstance(data, list):
        raw_cws = data
    elif isinstance(data, dict):
        if "codewords" in data:
            raw_cws = data["codewords"]
        elif "codewords_hex" in data:
            raw_cws = data["codewords_hex"]
        elif "codeword_indices" in data:
            # Need lex table if indices, but let's check if bitmasks or lists are available
            raw_cws = data["codeword_indices"]
        elif "code" in data:
            raw_cws = data["code"]
        else:
            for k in ["codewords_bits", "words", "solution"]:
                if k in data:
                    raw_cws = data[k]
                    break

    if raw_cws is None:
        print(f"Could not find codewords in {json_path}: keys={list(data.keys())}")
        return False, None

    codewords = [codeword_to_bits(cw) for cw in raw_cws]
    print(f"Loaded {len(codewords)} codewords.")

    # 1. Check weight and coordinates
    for idx, cw in enumerate(codewords):
        if len(cw) != 5:
            print(f"Codeword {idx} ({cw}) does not have weight 5!")
            return False, None
        for bit in cw:
            if not (0 <= bit < 18):
                print(f"Codeword {idx} ({cw}) has out-of-range coordinate {bit}!")
                return False, None

    # 2. Check pairwise overlaps
    n = len(codewords)
    max_overlap = 0
    min_dist = 18
    violations = 0
    for i in range(n):
        s_i = set(codewords[i])
        for j in range(i + 1, n):
            s_j = set(codewords[j])
            overlap = len(s_i & s_j)
            dist = 10 - 2 * overlap
            if overlap > max_overlap:
                max_overlap = overlap
            if dist < min_dist:
                min_dist = dist
            if overlap > 2 or dist < 6:
                print(f"Violation between {i} and {j}: c1={codewords[i]}, c2={codewords[j]}, overlap={overlap}, dist={dist}")
                violations += 1

    if violations > 0:
        print(f"Found {violations} distance violations!")
        return False, None

    print(f"Mathematical check PASSED! Total codewords: {n}, max overlap: {max_overlap}, min distance: {min_dist}")

    # Generate Lean 4 Certificate
    lean_content = f"""-- Formally Generated Lean 4 Verification Certificate
-- Benchmark: Constant-Weight Binary Code A(18, 6, 5) >= {n}
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

-- The {n} discovered codewords (subsets of size 5 in Fin 18)
def code{n} : List (List Nat) := {codewords}

-- Formal Theorem 1: Code cardinality is exactly {n}
theorem code_cardinality_is_{n} : code{n}.length = {n} := by
  rfl

-- Formal Theorem 2: All codewords have constant weight 5 with support in Fin 18
theorem code_constant_weight_5 : checkWeights code{n} = true := by
  rfl

-- Formal Theorem 3: All {n * (n - 1) // 2} pairs satisfy the Hamming distance constraint d >= 6
theorem code_min_distance_6 : checkAll code{n} = true := by
  rfl

#check code_cardinality_is_{n}
#check code_constant_weight_5
#check code_min_distance_6
#eval code{n}.length
"""

    lean_path = "t:/Codestral/lemma/FormalRecordCertificate.lean"
    with open(lean_path, "w") as f:
        f.write(lean_content)
    print(f"Wrote Lean 4 certificate to {lean_path}")

    # Run Lean compiler
    lean_bin = os.path.expandvars(r"$USERPROFILE\.elan\bin\lean.exe")
    res = subprocess.run([lean_bin, lean_path], capture_output=True, text=True)
    print("Lean output:")
    print(res.stdout)
    if res.stderr:
        print("Lean errors:")
        print(res.stderr)

    if res.returncode == 0:
        print("Lean 4 formal verification SUCCEEDED!")
        return True, (n, lean_path)
    else:
        print(f"Lean 4 compilation failed with return code {res.returncode}")
        return False, None

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "t:/Codestral/lemma/orbit_record_found.json"
    verify_code(path)
