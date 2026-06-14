# By hand (rung 1, no computer)

You cannot hand-verify the 441x441 PSD certificate; that is what the bundle is for. But you can
hand-check the *small* pieces, and a skeptic who checks the parts they can will more readily
grant the part they cannot. Everything here is pen, paper, and a calculator.

Write `w = e^(2*pi*i/3)` (a cube root of 1: `w = -1/2 + i*sqrt(3)/2`, and `1 + w + w^2 = 0`).

## The qubit MUBs (C^2): three bases, written out

Columns are basis vectors. `s = 1/sqrt(2)`.

```
Z (standard) = [ 1  0 ]      X (Hadamard) = [ s   s ]      Y = [ s     s   ]
               [ 0  1 ]                     [ s  -s ]          [ s*i  -s*i ]
```

Mutual unbiasedness check (by hand): take column 0 of Z, which is `(1, 0)`, against column 0 of
X, which is `(s, s)`. The overlap is `|<(1,0),(s,s)>|^2 = |s|^2 = 1/2`. Every cross overlap
between Z, X, Y is `1/2 = 1/d` with `d = 2`. That is what "unbiased" means.

## The qutrit MUBs (C^3): three of the four

`t = 1/sqrt(3)`. Entry in row `j`, column `m` (rows/cols indexed 0,1,2):

```
Z3 (standard) = identity

F3 (Fourier)   : entry = t * w^(j*m)
Q3 (Gauss-sum) : entry = t * w^(j^2 + j*m)
```

Written out:

```
F3 = t * [ 1   1    1  ]      Q3 = t * [ 1    1    1  ]
         [ 1   w    w^2]               [ w    w^2  1  ]
         [ 1   w^2  w  ]               [ w    1    w^2]
```

Check one cross overlap by hand: column 0 of `F3` is `t*(1,1,1)`, column 0 of `Q3` is
`t*(1,w,w)`. The first vector is real, so the inner product is `<u,v> = t^2 (1 + 2w)`. Now
`1 + 2w = 1 + 2(-1/2 + i*sqrt3/2) = i*sqrt3`, so `|1 + 2w|^2 = 3`, and the overlap squared is
`t^4 * 3 = (1/9)*3 = 1/3 = 1/d` with `d = 3`. Unbiased.

## The C^6 triple by tensor product

`C^6 = C^2 (x) C^3`. The canonical triple is

```
basis 0 = Z (x) Z3      basis 1 = X (x) F3      basis 2 = Y (x) Q3
```

A tensor product of two unbiased pairs is unbiased, so these three 6x6 bases are mutually
unbiased (every cross overlap squared `= 1/6`). One column of basis 1, for example, is
`X_col0 (x) F3_col0 = (s,s) (x) t(1,1,1) = s*t * (1,1,1,1,1,1)` (a flat vector). The full 6x6
matrices are just the 6 such tensor columns per basis.

## The product-ceiling law, worked

For an aligned product triple of `C^d = C^a (x) C^b`, a *product* fourth vector can reach at most

```
f_prod = (d - a) / (d - 1).
```

Here `d = 6`, `a = 2`, so `f_prod = (6 - 2)/(6 - 1) = 4/5 = 0.8`. So no product state beats 0.8;
the real wall is higher (0.9535) only because *entangled* fourth vectors do better. That gap,
product 0.8 vs. true wall 0.9535, is itself a hand-checkable sign that the maximiser must be
entangled.

## The wall constant, computed once

```
W = (88 + 3*sqrt(6)) / 100
sqrt(6)   ~ 2.449490
3*sqrt(6) ~ 7.348469
88 + 7.348469 = 95.348469
W ~ 0.95348469
```

And the defect (how far short of perfect unbiasedness `f = 1` you must fall):

```
1 - W ~ 0.04651531.
```

A fourth MUB vector would need `f = 1` exactly. The theorem says the best you can do after this
triple is `W < 1`. You have now checked, by hand, the bases, one unbiasedness overlap in each
factor, the product ceiling, and the wall constant. The 441x441 certificate that turns "the
search stalls at `W`" into "`max f = W`, proved" is rung 6 (the bundle).
