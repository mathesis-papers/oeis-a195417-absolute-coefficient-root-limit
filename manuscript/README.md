# An elementary answer to Hanna's coefficient root-limit question

Haobo Ma (ChronoAI Pte Ltd, Singapore) and Wenlin Zhang (National University
of Singapore; ChronoAI Pte Ltd, Singapore), November 14, 2026.

For the sum `a_n` of the absolute coefficients of `(1+x-x^3)^n`, the note proves

`R^n <= a_n <= sqrt(3n+1) R^n`, where `R = sqrt((97+26 sqrt(13))/27)`.

In particular `a_n^(1/n)` tends to `R`. This is an elementary consequence of
Baishanski's earlier coefficient-norm limit (1999, §28.1, p. 523) and
Neuwirth's earlier trinomial maximum (2007, Remark 6.4, pp. 13–14).
The note supplies a self-contained derivation and explicit all-index bounds;
it does not present the general norm limit or circle maximum as new.
The coefficient estimate applies to every nonzero complex polynomial.
Its quadratic specialization gives an independent proof of the A084611
root limit, also implied by Diaconis–Saloff-Coste (2012) and announced by
Václav Kotěšovec (2013). For every real `m>=1`, the absolute coefficient sum
`B_n(m)` of `(1+x-m*x^2)^n` lies between `M_m^n` and
`sqrt(2n+1)*M_m^n`, where `M_m=(m+1)*sqrt(1+1/(4m))`.
This gives the root limits `9/sqrt(8)` for A084613 and `sqrt(52/3)`
for A084615. Those entries define their sequences but do not pose root-limit
claims. The note also proves row and edge identities and the ordinary
A084610 diagonal sum. A positive successive-ratio limit, if it exists,
must equal the corresponding root limit; the sources' nonexistence assertions
are outside the proved coverage.
The note also checks the hypotheses of the earlier stability theorem,
which gives a non-explicit constant prefactor for each fixed polynomial here.

## Build

The only LaTeX source is `note.tex`; its bibliography is embedded.
Build with Tectonic 0.17.0:

```sh
tectonic --untrusted note.tex
```

Alternatively run `pdflatex note.tex` twice. No BibTeX invocation or external
bibliography is needed. A standard LaTeX installation with AMS packages,
Latin Modern, booktabs, geometry and hyperref suffices.

## Exact finite checks

`coverage.json` maps source statements to the written proofs, cited earlier
results and finite calculations. `metadata.json` contains the note's
bibliographic metadata.

Python 3.10 or later, standard library only:

```sh
python3 verify.py > verification.json
python3 verify-siblings.py > verification-siblings.json
```

Expected: `status` is `pass`. The program checks the maximum-gap polynomial
identity over `Q(sqrt(13))`, all coefficients for `0 <= n <= 29` against an
independent multinomial formula, the first 30 A195417 terms, and the cubic
and quadratic squared inequalities for `0 <= n <= 1000`. These are finite
checks, separate from the all-index proofs in the note.
The sibling program checks the quadratic maximum-gap identity as a polynomial
identity in `m,u`; squared bounds and row identities for `m=1,2,3`,
`0<=n<=1000`; every coefficient for `0<=n<=29` against a multinomial
formula; five nonnegative row families and the A084610 diagonal sum for
`0<=n<=100`.

An optional comparison with the OEIS table uses:

```sh
curl -fL https://oeis.org/A195417/b195417.txt -o b195417.txt
python3 verify.py --bfile b195417.txt
```

The table's hash is then included in the output. Its coefficients are numeric
comparison data, not premises for the proofs.
To compare the three quadratic sequences as well, download
`b084611.txt`, `b084613.txt` and `b084615.txt` from their respective
`https://oeis.org/A084611/`, `https://oeis.org/A084613/` and
`https://oeis.org/A084615/` entry paths into one directory, then run
`python3 verify-siblings.py --source-dir <directory>`.
The comparisons cover `0<=n<=500`, `0<=n<=1000` and `0<=n<=1000`,
respectively, and bind the numeric tables by SHA-256.

## Mathematical sources

- Dennis M. Girard, *The asymptotic behavior of norms of powers of absolutely
  convergent Fourier series*, Pacific J. Math. 37 (1971), 357–381, §1:
  https://doi.org/10.2140/pjm.1971.37.357.
- Bogdan Baishanski, *Norms of powers and a central limit theorem for
  complex-valued probabilities*, Analysis of Divergence (1999), 523–543,
  §28.1: https://doi.org/10.1007/978-1-4612-2236-1_29.
- Stefan Neuwirth, *The maximum modulus of a trigonometric trinomial*,
  March 8, 2007, Remarks 6.3–6.4, pp. 13–14:
  https://arxiv.org/abs/math/0703236v1. The 2008 journal version has
  DOI https://doi.org/10.1007/s11854-008-0028-2.
- Persi Diaconis and Laurent Saloff-Coste, *Convolution powers of complex
  functions on Z*, May 29, 2012, Theorem 2.1, Example 2.4 and Proposition
  2.5 with its following remarks: https://arxiv.org/abs/1205.6490v1.
- Evan Randles and Laurent Saloff-Coste, *On the convolution powers of
  complex functions on Z*, December 19, 2012, Theorem 1, p. 4:
  https://arxiv.org/abs/1212.4700v1.
- Paul D. Hanna, A195417, first comment and September 17, 2011 history, revision 2:
  https://oeis.org/A195417 and https://oeis.org/history?seq=A195417.
- Paul D. Hanna, A084611, comment and links: https://oeis.org/A084611.
- Václav Kotěšovec, *Asymptotic of sequence A084611*, July 26, 2013, pp. 1–3:
  http://www.kotesovec.cz/math_articles/kotesovec_asymptotic_of_sequence_A084611.pdf.
  It announces the correct limit; the proof here is independent of its
  central-coefficient reduction.
- Frank Calegari, *The abelian house is not closed*, August 3, 2014;
  collected posts, §52.12, pp. 104–105:
  https://math.uchicago.edu/~fcale/papers/blog.pdf.
  Its Laurent polynomial has the same squared circle maximum, not a
  statement about the coefficient-power norm.
- The Lean declaration `D5.S3.Analytic.Polynomial.A195417RootLimit.result`
  states the cubic limit for the same coefficient definition:
  https://github.com/the-omega-institute/trureturing/blob/6bdbb68454659fcccffc7607b5fc292b2ff2fcdf/D5/S3/Analytic/Polynomial/A195417RootLimit.lean.
  Its supporting upper bound uses `3n+1`; the note proves the stronger
  square-root prefactor. The general lemma, quadratic family and row identities have
  written proofs in the note.
- Hanna's cross-referenced quadratic definitions: https://oeis.org/A084613
  and https://oeis.org/A084615; signed row formulas:
  https://oeis.org/A084610, https://oeis.org/A084612, https://oeis.org/A084614.

## License

Copyright 2026 Haobo Ma and Wenlin Zhang. The note and accompanying original
source are licensed under Creative Commons Attribution 4.0 International,
CC BY 4.0: https://creativecommons.org/licenses/by/4.0/.
The cited external sources retain their respective licenses.
