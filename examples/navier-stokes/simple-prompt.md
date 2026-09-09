# simple-prompt

## Turn 1

**Asker:** I've heard that OpenAI found a solution to the Navier–Stokes equations and that there's some controversy about it. Tell me about that.

**Tutor:**

**First point: OpenAI has made a claim, but the problem is not officially settled.**

OpenAI says an internal AI system produced a proof that certain smooth, three-dimensional Navier–Stokes flows can develop a finite-time singularity, meaning the velocity becomes unbounded. It also released a paper and a Lean formalization of the argument. This would amount to disproving global smoothness for the version of the problem labeled “C” or “D” by the Clay Mathematics Institute. [OpenAI’s announcement](https://openai.com/index/navier-stokes-solution/)

That is different from finding a general formula for water or air flow. The underlying question is whether every physically reasonable smooth initial state remains smooth forever, or whether at least one state eventually “blows up.” OpenAI claims the latter.

The important qualification is that Clay still lists Navier–Stokes as **unsolved**. Its rules require publication in a qualifying outlet, at least two years, and broad acceptance by the mathematical community before recognizing a solution. [Clay’s problem page](https://www.claymath.org/millennium/navier-stokes-equation/) [Prize rules](https://www.claymath.org/millennium-problems/rules/)

So the accurate wording today is: **OpenAI has published a potentially groundbreaking claimed proof, not an officially accepted solution.**

Say “continue” and I’ll explain exactly what statements C and D mean, and why the use of a smooth external force matters.

## Turn 2

**Asker:** continue. What exactly are statements C and D, and why does the choice of a smooth external force matter to whether OpenAI’s result would really disprove the Clay problem?

**Tutor:**

The Navier–Stokes system is usually written

\[
\partial_t u+(u\cdot\nabla)u=-\nabla p+\nu\Delta u+f,\qquad \nabla\cdot u=0.
\]

Here \(u\) is velocity, \(p\) pressure, \(\nu>0\) viscosity, and \(f\) an external force.

**Statement C** says that on all of \(\mathbb R^3\), there exists:

- smooth divergence-free initial data \(u_0\),
- a smooth, suitably decaying force \(f(x,t)\),

such that no globally smooth, bounded-energy solution exists for all \(t\ge 0\).

**Statement D** says the same thing on the periodic three-dimensional domain \(\mathbb R^3/\mathbb Z^3\), essentially a three-dimensional torus. The difference is boundary behavior: C uses the whole space with decay at infinity; D uses periodic fields. [Clay’s official formulation](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf)

Why the force matters:

1. **A singular force would make the result trivial.** One could simply insert an infinite or nonsmooth impulse and cause a breakdown. Clay therefore requires \(f\) itself to remain smooth and satisfy strong regularity and decay conditions.

2. **A smooth force is still allowed to be specially designed.** The force can interact with the nonlinear flow to amplify a vortex. OpenAI claims its constructed force is even compactly supported in space and time, while the velocity becomes unbounded near a finite time. The difficult part is making all the divergent terms cancel so that the *net force remains smooth*. [OpenAI’s paper](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)

3. **This would count under Clay’s literal problem statement.** OpenAI explicitly says its construction establishes C and D. But it would **not** prove blowup for the more familiar unforced equations, where \(f=0\), corresponding to statements A and B. That unforced version remains the one many people informally have in mind when they say “the Navier–Stokes problem.”

So the precise verdict is: **a correct proof of OpenAI’s forced construction would satisfy Clay’s official C/D route, but it would not show that an ordinary unforced fluid spontaneously develops a singularity.**

The next issue is whether allowing a specially engineered smooth force is mathematically legitimate or merely a loophole in the way the problem was formulated.

## Turn 3

**Asker:** How can the velocity become unbounded while the external force stays smooth? I want to understand what is actually cancelling, and why that is a legitimate construction rather than just exploiting a loophole in the problem’s wording.

**Tutor:**

The central distinction is:

\[
f=\partial_tu+(u\cdot\nabla)u-\nu\Delta u+\nabla p.
\]

The velocity \(u\) and its derivatives may become very large, while their **sum**, the residual \(f\), remains smooth.

**What OpenAI says it cancels**

1. It constructs a collapsing vortex whose core shrinks toward one point. The angular and axial velocities grow as the core contracts.

2. The vortex alone would require a force that becomes singular in the surrounding annulus.

3. It adds highly oscillatory velocity pulses. Their individual average velocity is essentially zero, but their quadratic products are not. Through the nonlinear term \((u\cdot\nabla)u\), those pulses transport momentum and create an effective stress.

4. That stress cancels the singular part of the vortex’s momentum residual. Further corrections cancel the remaining singular terms, including their derivatives. The pressure handles part of the centripetal balance, while the outer flow is chosen so that its viscous residual vanishes. [OpenAI’s paper](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)

A simple analogy is:

\[
A(t)=\frac1{1-t},\qquad
B(t)=-\frac1{1-t}+g(t).
\]

Both terms diverge, but \(A+B=g(t)\) is smooth. OpenAI’s construction is vastly more difficult because the cancellation must work in three dimensions, preserve incompressibility, satisfy the PDE, and remain smooth under every relevant space-time derivative.

**Why the velocity can diverge while energy stays finite**

The blowup occurs in a shrinking region. Roughly, if velocity has size \(\tau^{-1/2-h}\) and the core volume has size \(\tau^{3/2-h}\), where \(\tau=1-t\), then

\[
\text{energy}\sim
(\tau^{-1/2-h})^2\,\tau^{3/2-h}
=\tau^{1/2-3h}.
\]

For the small \(h\) used in the construction, this remains bounded, even tends to zero for the concentrating core. Thus \(L^\infty\) can diverge while \(L^2\) energy remains finite.

This is not merely exploiting the wording. Defining \(f\) as the residual of an arbitrary bad velocity field would be trivial, but that residual would normally be singular. The substantive claim is that the residual can be made smooth, compactly supported, and admissible under Clay’s C/D formulation. Under the literal problem statement, that is a legitimate counterexample route. Its limitation is that it does not establish blowup when \(f=0\), the unforced A/B problem.

The next question is whether the claimed cancellations and Lean formalization are actually enough for mathematicians to accept the proof.

## Turn 4

**Asker:** What does the Lean formalization actually certify? Does it verify the entire analytic construction and every cancellation from accepted axioms, or only a simplified statement whose connection to the paper still has to be checked by mathematicians?

**Tutor:**

**Short answer:** the released Lean project appears to formalize the full claimed theorem, not merely a simplified “some expression blows up” statement. But Lean only certifies the theorem as encoded. Mathematicians still must verify that the encoding faithfully represents the paper and Clay’s intended problem.

The formalized candidate includes:

- smooth velocity and pressure before the singular time;
- smooth external force for all future times;
- compact spatial and temporal support;
- zero initial velocity;
- incompressibility;
- the exact Navier–Stokes residual equation;
- unbounded speed as \(t\to1\).

Those requirements are explicit in the Lean structure `R3CompactCandidate.Properties`. [Candidate definition](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/NavierStokes/R3CompactCandidate.lean)

The top-level theorem then proves the actual Clay-style quantifier:

\[
\exists u_0,f\;[
\text{admissible data and force}
\land
\neg\exists v,p\;(\text{global smooth solution})
].
\]

The bridge from the constructed candidate to this nonexistence statement also formalizes the force decay, rescaling to arbitrary \(\nu>0\), and the uniqueness/comparison argument. [Whole-space bridge](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/NavierStokes/ComparatorR3Theorem.lean) [Periodic bridge](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/NavierStokes/ComparatorTheorem.lean)

Lean therefore checks the cancellations as exact symbolic equalities and regularity proofs, not as numerical approximations or sampled tests. According to the repository metadata, the main results have zero `sorry` declarations and depend only on standard Lean foundations such as `Classical.choice`, `propext`, and `Quot.sound`. [Project metadata](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/formalization.yaml)

However, there remains a crucial external layer:

- Did the Lean definitions encode the same domains, norms, derivatives, boundary conditions, and time regularity as the paper?
- Does the selected witness really correspond to every construction claimed in the paper?
- Were any informal assumptions silently weakened during translation?

The separate `ComparatorChallenges/NavierStokes.lean` file contains `sorry` placeholders, but it is only the reference target. The proof root explicitly avoids importing that challenge module and imports the actual formalization instead. [Comparator target](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/ComparatorChallenges/NavierStokes.lean) [Proof adapter](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/NavierStokes/ComparatorSolution.lean)

So the right interpretation is:

**Lean provides strong machine verification of the released formal proof. It does not automatically certify that the formal proof is a faithful translation of the paper. That correspondence still requires expert mathematical audit.**

## Turn 5

**Asker:** If Lean proves the theorem exactly as encoded, what kinds of encoding mistake could still make the result irrelevant to Clay’s problem? For example, could “smooth” or “global solution” be defined more weakly than the usual mathematical meanings, and how would an independent audit detect that?

**Tutor:**

Yes. **Lean proves the formal predicate; it does not decide whether that predicate is the right translation of Clay’s statement.**

In this repository, the target is fairly substantial. A global solution must satisfy the PDE, incompressibility, initial condition, \(C^\infty\) regularity, and, in the whole-space case, finite \(L^2\) energy with a uniform energy bound. The candidate must also provide smooth force, support, divergence-free velocity, the exact residual equation, and unbounded speed. [Formal solution target](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/ComparatorChallenges/NavierStokes.lean) [Candidate properties](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/NavierStokes/R3CompactCandidate.lean)

The main encoding risks are:

1. **Boundary regularity.** The code uses `ContDiffOn` on \(\mathbb R^3\times[0,\infty)\), and encodes the time derivative with `derivWithin` at \(t=0\). That is smoothness *within a set*, with a one-sided time derivative at the boundary. An auditor must establish that this matches Clay’s intended \(C^\infty\) regularity up to the initial time, rather than merely being a weaker one-sided notion. [Mathlib’s `ContDiffOn` definition](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/Calculus/ContDiff/Defs.html) [Repository explanation](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/ComparatorChallenges/NavierStokes.lean)

2. **Quantifier mismatch.** The formal theorem must say “there exist admissible \(u_0,f\) such that no admissible global \(v,p\) exists.” It would be a serious error if it proved only that one particular constructed field blows up, without ruling out another global solution with the same data and force.

3. **Operator mismatch.** The formal `divergence`, gradient, Laplacian, pressure, and time derivative must correspond exactly to the operators in Clay’s formulation. Coordinate changes and cylindrical-to-Cartesian conversions are especially audit-sensitive.

4. **Energy mismatch.** The code’s condition is an integral of \(\|v(x,t)\|^2\) bounded uniformly in time. An audit must check that this is exactly the required finite-energy condition, with no accidental omission of measurability, spatial integrability, or the relevant domain.

5. **Periodic-domain mismatch.** The torus is represented by functions on \(\mathbb R^3\) satisfying unit-periodicity. That is standard, but one must verify that the periodicity conditions for velocity, pressure, force, and derivatives match the \(\mathbb R^3/\mathbb Z^3\) statement.

An independent audit would therefore do four things:

- compare every Lean definition and quantifier line-by-line with the Clay PDF;
- trace the final theorem back to the actual constructed witness, checking that no candidate property is simply assumed;
- rebuild from a clean environment and inspect `#print axioms`, `sorry`, and theorem dependencies;
- try adversarial “countermodels,” such as nonsmooth functions at \(t=0\), pathological boundary behavior, or fields satisfying a formally weakened PDE predicate.

The strongest possible result would be an independently authored equivalence theorem:

\[
\text{Lean’s predicate}
\quad\Longleftrightarrow\quad
\text{Clay’s mathematical predicate}.
\]

Without that equivalence, the formalization is strong evidence that the encoded proof is internally correct, but the final semantic connection still belongs to human mathematical review.

## Turn 6

**Asker:** What have independent researchers actually objected to so far? Have they identified a concrete error in the paper or Lean proof, or are their objections mainly about whether the formalized statement matches the problem mathematicians intended?

**Tutor:**

As of **September 9, 2026**, I found **no credible public report identifying a concrete mathematical error** in either the paper or the Lean proof.

The objections so far fall into three categories:

1. **Priority and research ethics.** Tristan Buckmaster alleges that OpenAI accelerated its work after learning about his and Levent Alpöge’s related research, and that OpenAI pressured him over authorship and credit. Crucially, Buckmaster explicitly says he has **not seen OpenAI’s proof** and does not know whether their data was used. That is a serious provenance dispute, but not a mathematical refutation. [Buckmaster’s statement](https://cims.nyu.edu/~tristanb/statement.pdf)

2. **What problem was solved.** OpenAI’s result concerns the forced C/D alternatives in Clay’s formulation, whereas many mathematicians and headlines naturally mean the unforced A/B problem. That is a legitimate concern about interpretation and significance, but C/D are explicitly part of Clay’s official statement. It is not, by itself, evidence that the formal theorem is false. [Clay’s formulation](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf)

3. **Formalization-to-problem correspondence.** Lean can establish that the encoded theorem follows from its encoded definitions. Independent mathematicians still need to check that those definitions faithfully capture the intended regularity, force, energy, domain, and solution concepts. Public tracking of the claim currently describes this examination as not yet started, and reporting says no external mathematician has independently verified the proof. [State of Proof](https://stateofproof.org/) [EL PAÍS report](https://elpais.com/ciencia/2026-09-09/el-anuncio-de-openai-de-que-ha-resuelto-uno-de-los-mayores-enigmas-matematicos-de-la-historia-desata-acusaciones-de-plagio.html)

Terence Tao’s public reaction was positive toward the related Buckmaster–Alpöge work and its underlying strategy, but he explicitly had not yet digested the precise details of the new constructions, so this is not an independent certification of OpenAI’s Navier–Stokes proof. [Tao’s discussion](https://terrytao.wordpress.com/2026/09/)

Therefore the honest status is: **the public controversy is presently about provenance, credit, interpretation, and the need for independent audit. No concrete error in the OpenAI paper or Lean certificate has yet been publicly established.** This should not be confused with confirmation that no error exists; the claim is only a day old.

## Turn 7

**Asker:** What is the evidence behind Buckmaster’s priority and authorship allegation, and what has OpenAI said in response? I want to distinguish evidence of improper credit or pressure from evidence that OpenAI’s mathematics is wrong.

**Tutor:**

The public evidence supports **a disputed timeline and a disputed conversation**, but not yet a proven case of plagiarism or mathematical misconduct.

**What Buckmaster has directly documented**

Buckmaster published a contemporaneous statement describing:

- his and Alpöge’s progress on forced Euler and related equations;
- his September 3 email warning OpenAI that rumors concerned their work;
- September 6 calls with Sébastien Bubeck;
- being told that OpenAI had a roughly 100-page proof of forced Navier–Stokes under Clay’s C/D alternatives;
- proposals for coordinated publication, or for Buckmaster to rewrite OpenAI’s proof as the main author while excluding Alpöge;
- his account that Bubeck said it would be simpler if Alpöge were not involved because he worked for Anthropic.

This is first-hand evidence of **what Buckmaster says was said to him**. It is not independent proof of the whole conversation: no complete transcript, recording, or internal OpenAI documentation has been made public. Buckmaster also explicitly says he had not seen OpenAI’s proof and does not know whether his data was used. [Buckmaster’s statement](https://cims.nyu.edu/~tristanb/statement.pdf)

**What OpenAI acknowledges**

OpenAI’s own account confirms several important parts of the timeline:

- it heard rumors on September 1;
- it then launched the Millennium Problems effort;
- it completed the Navier–Stokes work and Lean verification before contacting Buckmaster and Alpöge;
- it believed they had solved Navier–Stokes and contacted them about a coordinated release.

OpenAI denies that researchers or agents saw their unpublished work before publication, and says no specific user data was accessed to solve the problem. However, it also says it cannot rule out that de-identified data derived from product use helped improve its models. It claims the proofs differ substantially, and emphasizes that Buckmaster and Alpöge proved forced Euler, while OpenAI claims Navier–Stokes and unforced Euler. [OpenAI’s account](https://openai.com/index/navier-stokes-solution/)

Bubeck’s public clarification narrows his disagreement with Buckmaster: he says he never asked Alpöge to be removed from authorship of **Alpöge’s own work**. He says the Anthropic-affiliation comment concerned a possible OpenAI paper or rewrite of OpenAI’s proof, where he considered it inappropriate for an Anthropic employee to be an author. That partially confirms the context Buckmaster describes, but disputes its characterization as an attempt to strip Alpöge of credit. [Reporting on Bubeck’s response](https://www.wired.com/story/openai-navier-stokes-math-discovery-academics/)

So the evidence separates cleanly:

- **Supported:** OpenAI learned of related work, began its effort afterward, used a related forcing strategy, and discussed coordinated publication.
- **Alleged but unresolved:** access to private Codex material, indirect training use, coercive pressure, or intentional misappropriation of credit.
- **Not established at all:** that OpenAI’s mathematics is wrong.

Even if the priority or authorship allegations were substantiated, the proof could still be mathematically correct. Conversely, a correct Lean proof would not settle whether the research process or credit allocation was improper.

## Turn 8

**Asker:** How closely are the Buckmaster–Alpöge and OpenAI constructions mathematically related? What evidence would distinguish independently discovering the same general strategy from copying private work, especially when the proofs concern different equations?

**Tutor:**

They are **closely related at the level of strategy**, but there is currently no public evidence showing that OpenAI copied Buckmaster–Alpöge’s private technical work.

**Shared mathematical backbone**

Both constructions descend from the Córdoba–Martínez-Zoroa program:

1. Build a controlled, lower-frequency background flow.
2. Add increasingly high-frequency perturbations.
3. Exploit an instability so the perturbations grow near the target time.
4. Arrange their nonlinear momentum fluxes to cancel the singular part of the residual.
5. Keep the external forcing smooth while the velocity becomes singular.

Tao’s description of the Buckmaster–Alpöge method uses essentially this architecture. OpenAI’s paper describes its own vortex, oscillatory pulses, and mean momentum flux in very similar terms. [Tao’s explanation](https://terrytao.wordpress.com/2026/09/) [OpenAI’s paper](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)

**Important differences**

Buckmaster–Alpöge publicly released results for forced incompressible porous media, Boussinesq, and forced 3D Euler. OpenAI claims a positive-viscosity Navier–Stokes construction, plus a separate unforced Euler result. Handling viscosity and obtaining the whole-space or periodic Navier–Stokes conclusion require additional technical work. [Buckmaster’s statement](https://cims.nyu.edu/~tristanb/statement.pdf) [OpenAI’s announcement](https://openai.com/index/navier-stokes-solution/)

Different equations therefore make **literal proof copying less likely**, but they do not rule out borrowing a strategic blueprint. A method developed for Euler or Boussinesq can be adapted to Navier–Stokes precisely because these equations share structural features.

**Evidence that would discriminate the hypotheses**

- **Weak evidence:** OpenAI began its effort after hearing rumors, and the “smooth forcing” route was unusual. This establishes awareness and possible inspiration, but not copying.
- **Strong evidence of copying:** identical unusual ansätze, parameter choices, intermediate lemmas, notation, ordering of corrections, bugs, or distinctive failed approaches that were not public.
- **Strong evidence of independence:** timestamped internal drafts showing the relevant construction before contact with Buckmaster’s work, plus access logs showing no route to the private material.
- **Strongest evidence about data use:** server-access logs, training-data provenance, model checkpoints, and audit records showing whether private Codex material could enter the model-improvement pipeline.

OpenAI says its researchers and agents did not see the private work before publication, but also says it cannot rule out that de-identified data derived from product use helped improve its models. That leaves a provenance question open; it is not evidence that such data actually influenced the proof. [OpenAI’s account](https://openai.com/index/navier-stokes-solution/)

So far, the public record supports this narrower conclusion: **the groups used a common deep mathematical lineage, OpenAI knew related work existed, and the timing is disputed. No public proof-level comparison or forensic evidence has yet established copying of private mathematics.**

## Turn 9

**Asker:** OpenAI also mentions an unforced Euler result. What exactly does that establish, and why can’t a blowup construction for unforced Euler simply be used to prove blowup for unforced Navier–Stokes? I want to understand the role of viscosity here.

**Tutor:**

OpenAI’s unforced Euler result claims:

\[
\partial_tu+(u\cdot\nabla)u+\nabla p=0,\qquad \nabla\cdot u=0
\]

has smooth, compactly supported, divergence-free initial data whose smooth solution exists only up to some finite time \(T_*\). Specifically,

\[
\limsup_{t\uparrow T_*}\|\nabla u(t)\|_\infty=\infty,
\]

and the time integral of the vorticity norm diverges. Thus the **gradient or vorticity** blows up; the theorem does not necessarily say that \(\|u\|_\infty\) itself becomes infinite. [OpenAI’s Euler paper](https://cdn.openai.com/pdf/315b36cd-ec98-4023-8342-93345194ece1/euler.pdf)

Why this does not automatically imply Navier–Stokes blowup:

\[
\partial_tu+(u\cdot\nabla)u
=
-\nabla p+\nu\Delta u.
\]

The extra term \(\nu\Delta u\) is not a small harmless correction near a singularity. If the flow varies over length scale \(\ell\) with velocity scale \(U\), then roughly

\[
(u\cdot\nabla)u\sim \frac{U^2}{\ell},
\qquad
\nu\Delta u\sim \frac{\nu U}{\ell^2}.
\]

As \(\ell\) shrinks, the viscous term acquires two inverse powers of the small scale. Even when \(\nu\) is tiny, it can become comparable to or larger than the inertial term precisely where the Euler construction concentrates its gradients.

Equivalently, the limit

\[
\lim_{\nu\to0^+}u_\nu=u_0
\]

need not be uniform near a blowup time. Every fixed-\(\nu\) Navier–Stokes solution could remain smooth forever while the family becomes increasingly steep as \(\nu\to0\). An Euler singularity does not logically force any member with \(\nu>0\) to blow up.

That is why OpenAI’s Navier–Stokes result requires a separate construction. Its oscillatory corrections are designed from the start to account for viscosity and cancel the viscous contribution as part of the full residual. The paper explicitly says its estimates are proved for the viscous equations, rather than obtained by simply substituting \(\nu>0\) into the Euler proof. [OpenAI’s Navier–Stokes paper](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)

So the logical relationship is:

**unforced Euler blowup is strong evidence that related blowup mechanisms exist, but it is not a proof of unforced Navier–Stokes blowup.**

## Turn 10

**Asker:** For the forced Navier–Stokes claim, why does one singular constructed solution imply that **no** other globally smooth solution with the same initial data and force exists? Is this where uniqueness or a comparison argument enters, and what assumptions make that step valid?

**Tutor:**

Yes. **Uniqueness is the bridge.** A singular solution alone would not rule out a different smooth solution with the same data.

Let \(u\) be OpenAI’s constructed solution on \(0\le t<1\), and suppose \(v\) were a global smooth solution with the same initial data and force. Set \(w=v-u\). Their difference satisfies schematically

\[
\partial_t w+(v\cdot\nabla)w+(w\cdot\nabla)u
=-\nabla q+\nu\Delta w,
\qquad \nabla\cdot w=0.
\]

Multiplying by \(w\) and integrating gives

\[
\frac12\frac{d}{dt}\|w\|_2^2+\nu\|\nabla w\|_2^2
\le \|\nabla u\|_\infty\|w\|_2^2.
\]

Since \(w(0)=0\), Grönwall’s inequality implies \(w=0\) on every interval \([0,T]\) with \(T<1\). Thus any competing smooth solution must coincide with the constructed one for all times before the singular time.

At that point, smoothness of the hypothetical global solution creates a contradiction. The constructed velocity becomes arbitrarily large as \(t\uparrow1\), while a globally smooth competitor is bounded on the compact region containing the constructed flow’s support and on the closed time interval \([0,1]\).

The assumptions differ slightly between the two Clay alternatives:

- **Periodic case D:** periodicity removes boundary terms at spatial infinity. Smoothness, periodic velocity and pressure, incompressibility, equal force, and equal initial data are enough for the energy comparison. The released formalization derives this through periodic integration by parts and Grönwall. [Periodic uniqueness proof](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/NavierStokes/PeriodicUniqueness.lean)

- **Whole-space case C:** finite energy alone does not automatically justify every integration by parts on \(\mathbb R^3\), especially for the pressure. The candidate’s compact support supplies spatial control, while the competitor is assumed smooth with uniformly bounded kinetic energy. The formalization adds a pressure-flux estimate to make the comparison rigorous; it does not assume the competitor itself has compact support or derivative bounds. [Whole-space comparison proof](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/NavierStokes/R3/WholeSpaceUniqueness.lean)

This only excludes solutions in the class stated by Clay: globally smooth solutions, with the relevant energy condition in case C. It does **not** assert uniqueness of arbitrary weak or rough Navier–Stokes solutions. The final formal bridge explicitly uses this pre-singularity agreement to convert the constructed blowup into the nonexistence statement C or D. [C/D bridge](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/NavierStokes/ComparatorR3Theorem.lean)

## Turn 11

**Asker:** Since \(\|\nabla u\|_\infty\) blows up as \(t\to1\), how can Grönwall’s argument remain valid? Why does proving agreement on every interval \(t<1\) suffice to force a contradiction exactly at \(t=1\), without assuming the very regularity we are trying to disprove?

**Tutor:**

The divergence of \(\|\nabla u(t)\|_\infty\) at \(t=1\) does not invalidate Grönwall on any interval ending before \(1\).

For every fixed \(T<1\), the constructed solution is smooth on \([0,T]\). Therefore

\[
B_T=\sup_{0\le t\le T}\|\nabla u(t)\|_\infty
\]

is finite. The difference energy satisfies

\[
E'(t)\le 2B_T E(t),\qquad E(0)=0,
\]

so Grönwall gives \(E(t)=0\) for \(0\le t\le T\). The bound \(B_T\) may become arbitrarily large as \(T\to1\), but that does not matter: the initial difference is exactly zero, and

\[
0\cdot e^{2B_TT}=0
\]

for every finite \(T\).

Because \(T<1\) was arbitrary, the hypothetical global solution \(v\) must satisfy

\[
v(t,x)=u(t,x)\qquad\text{for every }t<1.
\]

No claim is made that \(u\) is smooth at \(t=1\), and no equality at \(t=1\) is needed.

Now assume, for contradiction, that \(v\) is globally smooth. The constructed field is supported in a fixed compact spatial set \(K\). Since \(v\) is continuous on the compact set \([0,1]\times K\),

\[
\sup_{(t,x)\in[0,1]\times K}|v(t,x)|<\infty.
\]

But equality for every \(t<1\), combined with the constructed blowup

\[
\limsup_{t\uparrow1}\|u(t)\|_\infty=\infty,
\]

would force \(v\) to become unbounded on that same compact set. Contradiction.

Thus the logic is:

1. Compare on each safe interval \([0,T]\), where all coefficients are bounded.
2. Obtain equality for every \(T<1\).
3. Use the assumed smoothness of the hypothetical competitor at \(t=1\) to get boundedness.
4. Contradict the known blowup sequence approaching \(t=1\).

The whole-space formalization encodes precisely this structure: agreement before time one followed by compactness and boundedness of a hypothetical smooth competitor. [Whole-space uniqueness](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/NavierStokes/R3/WholeSpaceUniqueness.lean) [Final contradiction](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/NavierStokes/R3CompactCandidate.lean)

## Turn 12

**Asker:** What would have to happen before we should call this a reliable solution rather than a promising claimed proof? Which checks are mathematical, which are formalization checks, and which are only about priority or research conduct?

**Tutor:**

I would use a **layered standard**:

**1. Mathematical validation**

Independent PDE experts would need to verify:

- the constructed fields satisfy the exact 3D Navier–Stokes equations;
- the force is genuinely smooth and admissible under Clay’s C/D conditions;
- every oscillatory correction and residual cancellation works;
- the energy bound and velocity blowup estimates are correct;
- the uniqueness/comparison argument excludes every competing global smooth solution in the required class.

This is the most important check. A Lean certificate does not replace understanding whether the formal objects correspond to the intended analytic objects.

**2. Formalization validation**

An independent person should:

- rebuild the public repository from a clean environment;
- confirm the exact pinned Lean and Mathlib versions;
- inspect the final theorem’s dependency and axiom list;
- confirm there is no hidden `sorry`, `admit`, or unapproved axiom;
- verify that the proof root does not merely import a statement with placeholders.

OpenAI’s repository reports zero unresolved holes in the main results and only standard Lean foundations, but those are properties of the submitted code, not yet an independent mathematical endorsement. [OpenAI’s formalization repository](https://github.com/openai/NavierStokesAndEuler)

**3. Statement correspondence**

A mathematician and a formal-methods expert should compare the Lean predicate with Fefferman’s Clay formulation line by line, especially:

- \(C^\infty\) regularity on the half-space \(t\ge0\);
- the use of one-sided `derivWithin` at \(t=0\);
- the precise force decay and support conditions;
- the definition of bounded kinetic energy;
- periodicity and pressure conditions in case D;
- the quantifier “no global smooth solution exists.”

This is where a formally flawless proof could still answer a subtly different question.

**4. Publication and community acceptance**

For ordinary scientific confidence, independent review and reproduction would be enough to call it a reliable result. For **official Clay recognition**, the rules are stricter: publication in a qualifying outlet, at least two years since publication, and general acceptance by the global mathematics community are all required. [Clay’s rules](https://www.claymath.org/millennium-problems/rules/)

**5. Priority and conduct**

Separate evidence would be needed for:

- who discovered the underlying ideas;
- whether private Codex material was accessed or used;
- whether authorship discussions involved improper pressure;
- whether acknowledgements and credit accurately reflect the work.

Those questions affect attribution and trust, but not whether the theorem is mathematically true.

So the current classification is: **a serious, machine-checkable claimed proof, not yet an independently validated mathematical result, and certainly not yet an officially recognized Clay solution.** Public tracking still describes external examination as not having begun. [State of Proof](https://stateofproof.org/)

## Asker final understanding

I understand that OpenAI claims a forced Navier–Stokes blowup satisfying Clay’s C/D formulation, not blowup for the familiar unforced A/B problem. The construction makes velocity singular in a shrinking region while carefully cancelling the singular residual so the force remains smooth. A uniqueness argument then shows that no competing global smooth solution can avoid the singularity.

The Lean code is strong evidence that the encoded proof is internally checked, but it does not by itself prove that the definitions faithfully match Clay’s intended mathematics. Independent experts still need to audit the PDE estimates, regularity, energy conditions, domains, quantifiers, and Lean-to-paper correspondence. Official Clay recognition also requires publication, two years, and broad acceptance.

The controversy is presently separate from mathematical correctness. Buckmaster alleges disputed priority and improper authorship pressure; Bubeck disputes part of that characterization. OpenAI acknowledges learning of related work and discussing coordinated publication, but denies access to private work. The groups share a broader construction strategy but publicly concern different equations, so copying has not been established. No concrete mathematical error has publicly been demonstrated, but independent verification, the exact semantic correspondence, data provenance, and credit dispute remain unresolved.
