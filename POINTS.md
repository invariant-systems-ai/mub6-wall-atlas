# Atlas points, badges, and the wall-map ledger

> **Read [`ACKNOWLEDGMENTS.md`](ACKNOWLEDGMENTS.md) first.** The four-decade board this work stands
> on comes before any point or badge. Atlas points score contributions to *this atlas's bricks*;
> they are **not** a leaderboard of MUB(6) research, and reading them as one would be a social
> "label-up" of the kind the project's own rigor forbids. You enter the ledger by contributing a
> brick; you do not reach the board by accumulating points (see the three-classes rule there).

> **Atlas points are reputation markers, not currency. They are revocable if the underlying
> claim fails.**
> The score is not who wins. It is how much of the defect surface becomes checkable.

Mapping MUB(6) defects earns **atlas points** and creates checkable **bricks** in the wall map.
The ledger is the typed memory of the project: every entry is a **node** that points to a
claim, a scope, an artifact, a verifier, a status, and its known weaknesses. The value is not
the points; it is that the state of the problem becomes auditable instead of anecdotal.

**This is not a cryptocurrency, a token, or a financial instrument.** Atlas points are
non-financial, non-transferable, artifact-linked, evidence-weighted, and revocable if a claim
is later broken. There is no chain, no wallet, no trading. Think research reputation bound to
runnable artifacts.

## Vocabulary

| word | meaning |
|---|---|
| **brick** | one scoped contribution to the MUB(6) wall map |
| **node** | an entry in the ledger (a result, with its full typed record) |
| **claim** | a mathematical statement a node asserts |
| **certificate** | a machine-checkable proof artifact someone else can run |
| **artifact** | a concrete output: a module, a certificate file, a Lean proof, a note |
| **badge** | recognition for the *kind* of contribution |
| **atlas points** | a nonfinancial score based on verification level |

## Node kinds (the map objects)

| kind | is | example |
|---|---|---|
| **wall** | a proven obstruction or bound | `max f = W = (88 + 3√6)/100` for the canonical triple |
| **witness** | a construction that attains, violates, or stress-tests a bound | the explicit algebraic witness attaining `W` |
| **certificate** | a machine-checkable proof artifact | the exact PSD certificate + independent stdlib verifier |
| **defect** | a mapped failure mode (where *not* to waste effort) | no degree-4/6 SOS certificate exists; T1 global bound open |

A defect node is a first-class result: it says where the next method has to be stronger.

## Badges (recognition for a kind of contribution)

`witness` · `certificate` · `formalization` · `reproduction` · `exposition` · `defect`

A badge records *what you did*; atlas points record *how strong it was*.

## Atlas points (Fibonacci scale)

```text
 1 point  = useful route, citation, or exposition fix
 2 points = replicated numerical evidence
 3 points = new witness or failed-extension (defect) map
 5 points = independent verifier run
 8 points = exact certificate or proof artifact
13 points = independent implementation (another system reproduces a checker)
21 points = formalized theorem / major new wall
```

The Fibonacci scale is deliberately game-like without pretending to be money. **Independent**
work is where the points are: a result self-checked by its author is intrinsically valuable,
but the 5- and 13-point awards exist because an outside rerun or reimplementation is what turns
"trust me" into "checked."

## Evidence ladder (a node's strength only rises by work)

```text
conjecture  ->  numerical evidence  ->  exact witness  ->  certificate  ->  independent rerun  ->  formal (kernel) proof
```

**Never label up.** A `float` result that looks like a closed form stays `float` until someone
makes it `exact`. Most past MUB(6) confusion came from treating evidence as proof.

## Five dimensions (the deeper readout, not a people-leaderboard)

| dimension | question |
|---|---|
| **Truth** | how verified is the claim? (`exact`/`kernel` > `60-digit` > `float` > `conjecture`) |
| **Scope** | how much of MUB(6) does it cover? |
| **Repro** | can outsiders rerun it? (verifier present, and how many *independent* reruns) |
| **Novelty** | does it add a new invariant, wall, witness, or method? |
| **Route** | does it help another person contribute? |

We deliberately do not rank *people*. The headline metric is how much of the wall is mapped and
how strongly. Atlas points score contributions *to this atlas's bricks*; they are not a
leaderboard of MUB(6) research. The foundational work in [`ACKNOWLEDGMENTS.md`](ACKNOWLEDGMENTS.md)
is the ground the scoring stands on, not an entry in it.

## The game loop

1. **Pick a board:** canonical triple, T1, d=10, the Weyl board, parametric product triples.
2. **Lay a brick:** a witness, a bound, a certificate, a formalization, a search, a refutation.
3. **Assign an evidence level** honestly, per the ladder above.
4. **Add or update a node** and earn its atlas points.
5. **Update the atlas:** what is now solved, what is blocked, what to try next.

That is a game, and more usefully a research-coordination protocol.

## How a node stays honest

- A node counts as `verified` only once at least one **independent** party reruns its verifier
  (for `exact`/`kernel`) or reproduces it (for `float`/`60-digit`). That rerun earns 5 points.
- A node is **revoked** (status `refuted`) the moment its check fails for anyone, and its
  points are revoked with it. A found break is a successful outcome: it improves the map.
- Every node links to its artifact and verifier, so the claim is never "trust the author."
- **The reproduction counters cannot be inflated.** `independent_reruns` and
  `independent_implementations` are not free integers; each is **derived** from a list of
  checkable evidence entries (`reruns[]` / `implementations[]`), where every entry names who,
  when, and the artifact a stranger can inspect. The scorer (and therefore CI) rejects any count
  that does not equal the number of entries backing it. You raise the number by filing the
  receipt, never the reverse: the "never label up" rule, enforced by a machine instead of a
  maintainer.

## The machine-readable ledger

The ledger lives as data, not prose, so it is itself checkable:

- [`ledger/nodes.json`](ledger/nodes.json): the nodes, seeded with the current results.
- [`ledger/nodes.schema.json`](ledger/nodes.schema.json): the shape every node must satisfy.
- [`ledger/score_atlas.py`](ledger/score_atlas.py): stdlib-only. Validates the ledger and prints
  the atlas points plus the five dimensions. Run `python3 ledger/score_atlas.py`.
- [`SCOREBOARD.md`](SCOREBOARD.md): the current standings, **generated** from the ledger by
  `python3 ledger/score_atlas.py --write-scoreboard`. Never hand-edited; CI fails if it drifts
  from the ledger, so the public numbers are always coherent with the data with no one
  reconciling them by hand.

Each node carries: `id`, `kind`, `title`, `claim`, `scope`, `artifact[]`, `verifier`,
`evidence_level`, `status`, `independent_reruns`, `independent_implementations`,
`dependencies[]`, `known_weaknesses`, `contributor`, and the optional evidence lists
`reruns[]` / `implementations[]` that back the two counters. That is the typed memory: claim,
scope, artifact, verifier, status, dependencies, known weaknesses, all in one place.
