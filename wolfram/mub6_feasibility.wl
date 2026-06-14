(* ::Package:: *)
(* mub6_feasibility.wl  --  exact-symbolic starter for the MUB(6) Wall Atlas.
   SPDX-License-Identifier: Apache-2.0
   Copyright 2026 Noah Erlwein (Invariant Systems).

   This is the Wolfram landing's Mode-B artifact: INDEPENDENT EXACT-SYMBOLIC
   REPRODUCTION, not a machine-checked theorem. It rebuilds the canonical MUB(6)
   product triple from first principles, proves (by FullSimplify over the cyclotomic
   field) that the three bases are mutually unbiased, defines the feasibility
   functional f, and checks the published wall W = (88 + 3 Sqrt[6])/100.

   Run:  wolframscript -file mub6_feasibility.wl     (or paste into a notebook)
   Every VerificationTest below returns Success on a stock Wolfram kernel. *)

omega = (-1 + I Sqrt[3])/2;                       (* primitive cube root of unity, exact *)

Z2 = IdentityMatrix[2];
X2 = (1/Sqrt[2]) {{1, 1}, {1, -1}};               (* qubit Pauli-X eigenbasis (Hadamard) *)
Y2 = (1/Sqrt[2]) {{1, 1}, {I, -I}};               (* qubit Pauli-Y eigenbasis *)

Z3 = IdentityMatrix[3];
F3 = (1/Sqrt[3]) Table[omega^(j m), {j, 0, 2}, {m, 0, 2}];        (* qutrit Fourier basis *)
Q3 = (1/Sqrt[3]) Table[omega^(j^2 + j m), {j, 0, 2}, {m, 0, 2}];  (* qutrit Gauss-sum basis *)

(* The canonical triple {Z2(x)Z3, X2(x)F3, Y2(x)Q3} of C^6 = C^2 (x) C^3.
   Columns of each matrix are the basis vectors. *)
triple = {KroneckerProduct[Z2, Z3], KroneckerProduct[X2, F3], KroneckerProduct[Y2, Q3]};

d = 6;
WExact = (88 + 3 Sqrt[6])/100;                    (* the proven wall, exact *)

(* --- exact-symbolic structure (RootReduce works in the algebraic field exactly) --- *)
modsq[z_] := RootReduce[z Conjugate[z]];          (* exact |z|^2 *)
orthonormalQ[Bi_] := (RootReduce /@ Flatten[ConjugateTranspose[Bi] . Bi - IdentityMatrix[d]]) == ConstantArray[0, d^2];
mubPairQ[Bi_, Bj_] := (modsq /@ Flatten[ConjugateTranspose[Bi] . Bj]) == ConstantArray[1/d, d^2];

(* --- the feasibility functional: f(v) = 1 iff v is unbiased to all three bases,
   and max_{|v|=1} f(v) = WExact (the wall, proven exactly in the Zenodo bundle). --- *)
feasibility[v_] := Module[{u = v/Norm[v]},
   1 - Sum[Total[(Abs[ConjugateTranspose[triple[[i]]] . u]^2 - 1/d)^2], {i, 1, 3}]/(1 - 1/d)];

(* The exact attainment witness v* (numeric here; deriving it in closed exact form is an
   open brick). f(v*) reproduces WExact to machine precision. *)
vstar = {
   0.23363986277347212 + 0.23363986277347204 I,
  -0.33472608108901647 - 0.23656174084697118 I,
   0.40816215995578375 - 0.03750543659243977 I,
  -0.33041666264523295 + 1.4425395699950839*^-16 I,
   0.04162060073316516 + 0.4702016036204432 I,
   0.3863962332689025  + 0.2711452993659118 I};

report = TestReport[{
   VerificationTest[And @@ (orthonormalQ /@ triple), True,
      TestID -> "each basis orthonormal (exact)"],
   VerificationTest[And @@ {mubPairQ[triple[[1]], triple[[2]]],
                            mubPairQ[triple[[1]], triple[[3]]],
                            mubPairQ[triple[[2]], triple[[3]]]}, True,
      TestID -> "triple mutually unbiased (exact, all cross overlaps = 1/6)"],
   VerificationTest[Abs[feasibility[vstar] - N[WExact, 12]] < 10^-12, True,
      TestID -> "witness attains the wall, f(v*) = W (numeric)"],
   VerificationTest[Chop[feasibility[triple[[1]][[All, 1]]]] == 0, True,
      TestID -> "a basis vector is maximally biased, f = 0"]
}];

Print["W = (88 + 3 Sqrt[6])/100 = ", N[WExact, 16]];
Print["f(v*)                    = ", feasibility[vstar]];
Print["AllTestsSucceeded        = ", report["AllTestsSucceeded"]];
report["TestResults"][[All, "TestID"]]

(* Open bricks for the Wolfram community (see WOLFRAM-LANDING.md):
   - derive v* in closed exact-symbolic form and make the witness test exact, not numeric;
   - port a check of the global PSD/Veronese certificate from the bundle;
   - a Manipulate / visualization that makes the wall legible;
   - search nearby product triples for their walls. *)
