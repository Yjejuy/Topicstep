# topicstep

## Turn 1

**Asker:** I've heard that OpenAI found a solution to the Navier–Stokes equations and that there's some controversy about it. Tell me about that.

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：what OpenAI actually claims】

The key distinction is that OpenAI did **not** claim to find a general formula for fluid motion. It claims to have constructed a specific smooth 3D flow that, despite positive viscosity and bounded kinetic energy, develops unbounded velocity in finite time. That would be a counterexample to global smoothness under one of the Clay problem’s permitted forced formulations, not a practical prediction that real water reaches infinite speed. [OpenAI’s announcement](https://openai.com/index/navier-stokes-solution/) · [Clay’s formulation](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf)

OpenAI released a 166-page proof and a Lean formalization, but this remains a **claimed result pending independent mathematical review**. The Clay Institute’s page still lists the problem as unsolved. [OpenAI’s paper](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf) · [Clay status](https://www.claymath.org/millennium/Navier-Stokes-Equation/)

## Turn 2

**Asker:** How can the kinetic energy stay bounded while the velocity becomes unbounded, and why would that count as a failure of the Clay problem’s global smoothness claim?

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：energy concentration versus smoothness】

This is the distinction between an **integral norm** and a **pointwise norm**:

\[
E(t)=\frac12\int_{\mathbb R^3}|u(x,t)|^2\,dx
\]

can remain finite even if

\[
\|u(t)\|_\infty=\sup_x |u(x,t)|
\]

becomes infinite. A simple analogy: a spike of height \(M\) occupying volume \(V\) contributes roughly \(M^2V\) to the energy. If \(V\) shrinks faster than \(1/M^2\), the spike can become infinitely tall while contributing only finite, even vanishing, total energy.

That is essentially the geometry OpenAI describes: a vortex core contracts toward a point while its velocity increases. Its reported scales are roughly

\[
\text{velocity}^2\sim \tau^{-1-2h},\qquad
\text{volume}\sim \tau^{3/2-h},
\]

so its energy scales like

\[
\tau^{1/2-3h},
\]

which tends to zero for the small \(h\) used in the construction, even though the peak velocity diverges. [OpenAI’s paper](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)

Why this defeats global smoothness: the Clay condition is not merely “finite total energy.” It requires \(u(x,t)\) and \(p(x,t)\) to remain smooth for **every finite time**. If \(\|u(t)\|_\infty\to\infty\) as \(t\to T<\infty\), the velocity cannot remain finite and smooth at \(T\), regardless of how small the singular region is.

The Clay formulation explicitly allows a disproof by exhibiting one smooth initial condition and smooth forcing for which no global smooth, bounded-energy solution exists. OpenAI says its construction does exactly that for alternatives C and D. So bounded energy does not rescue global smoothness; it makes the claimed counterexample stronger by showing that the failure occurs through concentration, not through the total energy becoming infinite. [Clay’s official formulation](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf)

## Turn 3

**Asker:** What exactly is being proved here: is OpenAI giving an explicit exact solution of the Navier–Stokes equations, or a numerical construction with error estimates, and what would Lean formally certify?

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：analytical construction versus numerical approximation】

Short answer: it is intended as an **exact analytical construction**, but not as a short closed-form formula.

The paper constructs velocity \(u\), pressure \(p\), and force \(f\) through a carefully designed multiscale process:

1. Define a collapsing vortex as the leading-order flow.
2. Add increasingly oscillatory correction fields.
3. Prove that their combined nonlinear momentum flux cancels the singular residual.
4. Show that the resulting fields satisfy the Navier-Stokes equations exactly for every \(t<1\), while the force remains smooth and the velocity becomes unbounded as \(t\to1\).

So this is not a numerical grid simulation with discretization error bars. The finite-stage approximations and estimates are tools inside an analytic proof that the limiting construction has the required exact properties. [OpenAI’s paper](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)

**Lean certifies the formal theorem, not the physical claim in the abstract.** In the public code, the main theorem is formally stated roughly as:

\[
\forall \nu>0,\ \exists u_0,f:
\text{ admissible data and force}
\land
\neg\exists v,p:\text{ global smooth Navier-Stokes solution}.
\]

The definitions explicitly encode the PDE, incompressibility, initial condition, smoothness, decay or periodicity, and global energy conditions. The candidate construction separately encodes smoothness before the singular time, the exact PDE identity, compact support, and unbounded speed. [Formal comparator definitions](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/NavierStokes/ComparatorDefinitions.lean) · [Formal theorem](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/NavierStokes/ComparatorSolution.lean)

If Lean compiles the code, its kernel has checked the logical derivation with no unfilled `sorry` proofs. The repository metadata reports `sorry_count: 0` and lists only standard foundational axioms such as classical choice. But Lean does **not** independently decide that the formal definitions faithfully capture the intended Clay problem, nor does it verify originality, authorship, or whether the AI used outside researchers’ work. Those remain matters for human mathematical and institutional review. [Project metadata](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/formalization.yaml)

## Turn 4

**Asker:** If the force \(f\) is allowed to be chosen, couldn’t we simply prescribe any collapsing velocity field and define \(f\) to make the equation true? Why is OpenAI’s forced construction nontrivial rather than a formal loophole?

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：why choosing the force is still difficult】

Yes, algebraically one can write

\[
f=\partial_tu+(u\cdot\nabla)u-\nu\Delta u+\nabla p
\]

for any chosen \(u\) and \(p\). But if \(u\) blows up, this residual will usually blow up too. The hard requirement is that \(f\) remain smooth, bounded in the required sense, and extend smoothly through the singular time.

For example, if \(u(x,t)=a(t)\phi(x)\) with \(a(t)\to\infty\), then the residual typically contains terms proportional to \(a'(t)\), \(a(t)^2\), and \(a(t)\). Those diverge unless there is a very precise cancellation. Pressure can remove some gradient components, but it cannot generally cancel the entire singular, divergence-free residual.

OpenAI’s claimed construction tries to engineer exactly that cancellation. It uses a collapsing vortex plus oscillatory pulses whose nonlinear momentum flux cancels the singular part of the background residual. The paper claims that not only the force itself, but all of its derivatives, extend smoothly through the blow-up time. That is the substantive analytic work; simply defining \(f\) after choosing \(u\) does not establish it. [OpenAI’s paper](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)

There is also a second protection against a loophole. Suppose a global smooth solution with the same initial data and the same smooth force existed. Classical uniqueness would force it to agree with OpenAI’s constructed solution for every time before \(T\). It would therefore inherit the constructed solution’s unbounded velocity as \(t\to T\), contradicting global smoothness. The public formalization explicitly encodes this comparison step. [Candidate conditions](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/NavierStokes/R3CompactCandidate.lean) · [Global-solution comparison](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/NavierStokes/R3FiniteEnergyComparison.lean)

So it is not a loophole relative to the Clay statement: alternatives C and D explicitly permit the solver to exhibit a smooth force and data causing breakdown. The force being chosen is allowed; making that chosen force smooth while the solution becomes singular is what must be proved. [Clay’s official formulation](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf)

## Turn 5

**Asker:** If Lean’s kernel checks the formal theorem with no `sorry`s, why isn’t that already enough to call the Clay problem solved, and what specifically must independent mathematicians still verify?

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：what Lean settles and what it does not】

A fully faithful Lean formalization **would be a mathematical proof**. The issue is that Lean’s kernel proves only the formal statement encoded in the source. Independent reviewers must establish that the encoded statement is exactly the Clay problem and that the construction really supplies all of its hypotheses.

They would need to check:

1. **Statement correspondence.** The formal theorem must quantify over the correct viscosity, domain, initial data, and force, and encode the required smoothness, incompressibility, decay or periodicity, and energy conditions. The public comparator explicitly defines these properties, but that translation itself must be audited. [Comparator definitions](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/NavierStokes/ComparatorDefinitions.lean)

2. **The analytic construction.** Reviewers must verify that the infinite correction process actually converges and produces fields that are smooth for \(t<T\), that the force extends smoothly through \(T\), that the PDE holds exactly, and that the velocity really becomes unbounded. This is where estimates that look like “error control” become a proof of an exact limiting object.

3. **The contradiction with global solutions.** It is not enough to show that OpenAI’s particular candidate becomes singular. Reviewers must verify the uniqueness/comparison argument: any hypothetical global smooth solution with the same data and force must coincide with the candidate before \(T\), and therefore cannot remain smooth at \(T\). The public Lean development contains this bridge explicitly. [Comparison theorem](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/NavierStokes/R3FiniteEnergyComparison.lean)

4. **Formalization integrity.** They should rebuild the repository independently, inspect the import chain and axioms, and confirm that no theorem is vacuous, misstated, or relying on an unintended assumption. The repository reports zero `sorry`s and only standard axioms such as classical choice, but it labels its review status “self-assessed.” [Project metadata](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/formalization.yaml)

So Lean is not the weak part. The remaining uncertainty is whether the formal object faithfully represents the intended mathematics and whether the surrounding construction has been independently understood and checked. Separately, Clay’s prize rules require publication in a qualifying outlet, at least two years of rigorous examination, and general acceptance by the mathematics community. [Clay’s prize rules](https://www.claymath.org/millennium-problems/rules/)

## Turn 6

**Asker:** What has the controversy actually been so far: which researchers have challenged or supported the claim, and are their objections mainly about the analytic construction, the Lean statement, or the use of smooth forcing?

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：who is challenging what】

As of September 9, 2026, the controversy is mainly about **provenance, credit, and the meaning of “solved,”** not a publicly demonstrated flaw in the analytic proof.

- **Tristan Buckmaster:** He has challenged OpenAI’s timing and conduct, not the proof’s mathematics. He says OpenAI pursued the relatively unusual smooth-forcing route shortly after learning about his and Levent Alpöge’s work, raises unresolved questions about possible use of Codex-derived data, and alleges pressure over authorship. Crucially, he says he has not seen OpenAI’s proof and is not accusing anyone of wrongdoing. [Buckmaster’s statement](https://cims.nyu.edu/~tristanb/statement.pdf)

- **Levent Alpöge:** He is Buckmaster’s collaborator and the person whose authorship is at issue. I have not found a separate public technical critique from him of OpenAI’s Navier-Stokes proof.

- **Sébastien Bubeck and OpenAI:** They defend the result’s independence. OpenAI says its researchers and agents did not see the pair’s work or specific user data before publication, while acknowledging that it cannot rule out de-identified product-derived data having helped improve its models. Bubeck disputes Buckmaster’s account of the authorship discussions. [OpenAI’s account](https://openai.com/index/navier-stokes-solution/)

- **Terence Tao:** Tao strongly praised Buckmaster and Alpöge’s related smooth-forcing results and said their general method appeared capable, in principle, of reaching Navier-Stokes. That is support for the underlying research program, **not an endorsement or audit of OpenAI’s proof**. [Tao’s assessment](https://terrytao.wordpress.com/2026/09/07/finite-time-blowup-with-smooth-forcing-term-for-the-incompressible-porous-medium-boussinesq-and-incompressible-euler-equations/)

- **Diego Córdoba and Luis Martínez-Zoroa:** They developed the earlier forced-blowup program on which the later work builds. Córdoba reportedly expressed surprise that the full Navier-Stokes claim might already be complete, but he has not publicly identified a technical error in it. [Scientific American’s report](https://www.scientificamerican.com/article/openai-claims-blockbuster-math-breakthrough-amid-swirl-of-controversy/)

The objections therefore divide as follows:

1. **Analytic construction:** No named external mathematician has yet published a specific flaw in OpenAI’s 166-page argument. The proof is too new; independent reading is still beginning.

2. **Lean statement:** The concern is mainly whether the formal theorem faithfully matches the intended Clay formulation, not whether Lean’s kernel has reported a failed check. The public code claims to formalize alternatives C and D, but the project’s own review status is still “self-assessed.” [Formalization metadata](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/formalization.yaml)

3. **Smooth forcing:** This is a caveat, not by itself a disproof. Clay’s official alternatives C and D explicitly allow smooth external forcing. But it matters because many people hear “Navier-Stokes problem” and mean the unforced A/B version. [Clay’s official formulation](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf)

So the current status is two separate questions: **the proof’s mathematical validity remains under review, while the priority and data/credit dispute is already public and sharply contested.**

## Turn 7

**Asker:** Why did Clay include both forced and unforced versions, and is proving blow-up for the forced version genuinely enough to solve the official problem even though it says nothing about whether ordinary unforced fluids blow up?

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：why Clay permits forced alternatives】

**In the narrow official sense, yes; in the ordinary unforced sense, no.**

Fefferman’s formulation deliberately includes four acceptable targets:

- **A/B:** with \(f=0\), every admissible smooth initial condition has a global smooth solution.
- **C/D:** there exist admissible smooth initial data and a smooth, decaying external force for which no global smooth solution exists.

The statement explicitly says this four-way choice is intended to give solvers “reasonable leeway” while retaining the core regularity issue. [Clay’s official formulation](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf)

Why include forcing? The Navier-Stokes equations naturally model externally driven fluids, and a smooth force is much less trivial than an arbitrary singular input. The challenge is to make the force remain smooth while the fluid’s own nonlinear dynamics amplify it into a singularity.

But C/D are **not the logical negation of A/B**. Proving C/D does not show that any unforced flow blows up, and it leaves the famous unforced question A/B unanswered. It shows instead that global smoothness fails somewhere in the broader class of smooth forced problems.

So if OpenAI’s proof really satisfies every hypothesis of C or D, it is a legitimate solution of the Clay problem **as officially written**, even though it does not settle unforced ordinary-fluid behavior. Whether it earns the prize is a separate matter: Clay requires qualifying publication, at least two years of rigorous examination, and general acceptance by the mathematical community. [Clay’s prize rules](https://www.claymath.org/millennium-problems/rules/)

## Turn 8

**Asker:** Can we examine the most vulnerable analytic step, namely how the finite correction stages are shown to converge to an exact solution while the force stays smooth and the velocity blows up, and what a reviewer would try to check there?

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：the convergence-to-smooth-force bridge】

Yes. The most vulnerable point is the **limit near the singular endpoint**, not the algebra at any one finite stage.

The paper’s claimed structure is:

1. At stage \(j\), add velocity and pressure corrections.
2. Recompute the **full nonlinear residual**, including cross-interactions, pressure, curls, and cutoff errors.
3. Prove that the residual gains a fixed amount of decay at each stage, roughly
   \[
   \sigma_{j+1}=\sigma_j+\frac{1}{10}.
   \]
4. Sum the corrections with shrinking cutoffs.

For every fixed \(q>0\), where \(q\) measures distance from the singular point in the similarity variables, only finitely many stages are active. Thus the sum is locally finite and smooth for \(t<1\). But that argument says nothing by itself about \(q\to0\), where infinitely many stages accumulate. [OpenAI’s proof outline](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)

The crucial claimed estimate is stronger than “the residual becomes small”:

\[
\left|\partial_x^\alpha\partial_t^b R(u,p)\right|
\le C_{\alpha,b,N}q^N
\]

for **every** derivative order \((\alpha,b)\) and every \(N\). This “flatness” is what would allow the residual to extend smoothly through \(t=1\), even though \(u\) itself becomes singular. A reviewer would ask whether the constants and domains are uniform enough for this conclusion, especially because differentiating high-frequency corrections costs powers of \(q\).

They would specifically check:

- whether the stage gain really dominates derivative losses for every order;
- whether all nonlinear and cutoff terms are included, rather than only the linearized residual;
- whether the velocity and pressure series converge in the required local spaces;
- whether incompressibility, compact support, and endpoint compatibility survive the limit;
- whether the residual has compatible limits away from the singular point and can be extended to a globally smooth force;
- whether the correction tail is genuinely lower order than the leading vortex, so the blow-up estimate cannot be canceled.

The paper claims precisely this architecture: flat residual estimates near the singular point, separate endpoint estimates away from it, and a final smooth-force extension. If any one of those limit passages fails, the construction may still be an excellent finite-stage approximation, but it would not be an exact smooth-forced blow-up solution. [Paper’s summation and extension sections](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)

## Turn 9

**Asker:** Why does being “flat,” meaning smaller than every power of \(q\), let the residual extend smoothly through \(q=0\), and can we see that with a simple one-variable example?

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：why flatness implies smooth extension】

Consider

\[
r(q)=
\begin{cases}
e^{-1/q^2}, & q>0,\\
0, & q\le 0.
\end{cases}
\]

For every \(N>0\),

\[
e^{-1/q^2}=O(q^N)\qquad(q\to0^+),
\]

because the exponential decays faster than any power. More importantly, every derivative has the form

\[
r^{(k)}(q)=P_k(1/q)e^{-1/q^2},
\]

where \(P_k\) is a polynomial. The exponential still dominates the polynomial, so every derivative also tends to zero faster than every power of \(q\).

Therefore, after defining \(r(0)=0\), the function is \(C^\infty\) at \(q=0\), and every derivative there is zero. It is smooth but not analytic: its Taylor series at zero is identically zero even though \(r(q)>0\) for \(q>0\).

That is the role of flatness in the Navier-Stokes construction. If the residual satisfies, for every derivative order and every \(N\),

\[
|\partial_x^\alpha\partial_t^b R|\le C_{\alpha,b,N}q^N,
\]

then all its derivatives approach compatible limits at the singular endpoint, usually zero at the singular point. The residual can therefore be defined there and extended as a smooth force, even though the velocity itself is blowing up.

The qualification matters: showing only \(R(q)\to0\) is not enough. For example, \(q\sin(1/q)\to0\), but its derivative oscillates and is unbounded. The construction needs flatness estimates for the differentiated residuals as well, which is exactly the delicate claim in the paper. [OpenAI’s paper](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)

## Turn 10

**Asker:** I understand flatness in the similarity variable \(q\), but why does that imply smoothness in the original variables \((x,t)\) at the spacetime singular point \((0,1)\), especially when differentiating \(q=q(x,t)\) mixes space and time?

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：how q-flatness survives the physical chain rule】

The important qualification is that **flatness in \(q\) alone would not be enough**. The proof needs flatness estimates after taking derivatives in the original Cartesian variables:

\[
\left|\partial_x^\alpha\partial_t^b R(x,t)\right|
\le C_{\alpha,b,N}q(x,t)^N
\]

for every \(\alpha,b,N\). This is stronger than merely knowing \(R=O(q^N)\).

Why can the chain rule be absorbed? Suppose, schematically,

\[
R(x,t)=g(q(x,t)),
\]

and derivatives of \(q\) behave like inverse powers of \(q\). Repeated chain-rule differentiation has the form

\[
\partial_{x,t}^\beta R
=
\sum_k g^{(k)}(q)\,P_{\beta,k}
\bigl(\partial^\gamma q\bigr),
\]

where the factors \(P_{\beta,k}\) may grow like \(q^{-M}\). But if \(g\) is flat, then for every \(L\),

\[
g^{(k)}(q)=O(q^L).
\]

Choose \(L\) larger than \(M+N\). Then

\[
q^{-M}O(q^L)=O(q^N),
\]

so the differentiated expression still tends to zero.

A toy example makes this visible. Let

\[
q(x,t)=\sqrt{x^2+(1-t)^2},
\]

and define

\[
R(x,t)=
\begin{cases}
e^{-1/q(x,t)^2}, & (x,t)\ne(0,1),\\
0, & (x,t)=(0,1).
\end{cases}
\]

Although derivatives of \(q\) contain factors such as \(1/q\), derivatives of \(R\) look like polynomial powers of \(1/q\) multiplied by \(e^{-1/q^2}\). The exponential dominates every such power, so every mixed derivative tends to zero at \((0,1)\). The function therefore extends smoothly there with all derivatives equal to zero.

In the actual construction, the similarity variables include \(q\), \(\eta\), and \(X\), and the space-time derivatives mix all of them. The paper therefore needs uniform estimates for derivatives of the full composed residual, not just derivatives with respect to \(q\). At points on \(t=1\) away from \(x=0\), it uses separate endpoint estimates; at \((0,1)\), flatness supplies the compatible zero jet. [OpenAI’s proof outline](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)

## Turn 11

**Asker:** If Buckmaster has not seen OpenAI’s proof and is not alleging a mathematical error or misconduct, what concrete evidence supports his provenance and authorship concerns, and which parts remain only allegations or unresolved questions?

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：what is evidence versus inference】

As of September 9, 2026, Buckmaster’s concern rests on **first-hand testimony plus circumstantial timing evidence**, not proof that OpenAI copied anything.

**Concrete supporting evidence:**

- **His direct account of the calls:** Buckmaster published a dated statement describing his September 3 email, September 6 calls with OpenAI, the claim that an internal model had already produced a forced Navier-Stokes proof, and the publication arrangements he says were proposed. This is evidence of what he personally heard and was offered, though not independent corroboration. [Buckmaster’s statement](https://cims.nyu.edu/~tristanb/statement.pdf)

- **The timing:** OpenAI confirms that it began the effort on September 1 after hearing rumors about two Millennium problems, later realizing those rumors concerned Buckmaster and Alpöge. It also confirms that it contacted them after completing the proof and Lean verification. This supports the broad chronology, but not the claim that private material was used. [OpenAI’s account](https://openai.com/index/navier-stokes-solution/)

- **The unusually specific route:** Buckmaster says the smooth-forcing route corresponding to Clay’s C/D alternatives was not an obvious first attempt and that very few people he knew were pursuing it. OpenAI confirms that it deliberately targeted the forced alternatives and used its Euler result to guide the Navier-Stokes effort. This makes the convergence noteworthy, but the underlying program originated in earlier published work by Córdoba and Martínez-Zoroa, so it is not proof of leakage.

- **The data-access ambiguity:** Buckmaster says his drafts were stored in Codex and that his questions about model training were not answered. OpenAI says no specific user data was accessed, but also says it cannot rule out de-identified product-derived data having helped improve its models. That leaves a technically plausible channel open, but does not show that this channel was used. [OpenAI’s statement](https://openai.com/index/navier-stokes-solution/)

- **The authorship dispute:** Buckmaster reports that Bubeck wanted Alpöge excluded from a paper about OpenAI’s result because Alpöge worked for Anthropic. Bubeck disputes that interpretation and gives a different account, saying he was trying to coordinate recognition and release. There is no public recording or independent transcript resolving the conflict. [NYU’s summary of the dispute](https://rits.shanghai.nyu.edu/ai/openai-navier-stokes-proof-credit-dispute/)

**Still unresolved:**

- Whether Codex sessions or derived training data influenced the internal model.
- Whether OpenAI’s proof contains genuinely independent ideas or reproduces unpublished ideas from Buckmaster and Alpöge.
- Exactly what was said and intended in the authorship discussions.
- Whether the timing reflects improper use of information or simply a rapid response to rumors and public research directions.
- Whether OpenAI’s mathematical proof is correct; no independent mathematician has yet publicly completed a technical audit.

So Buckmaster’s statement is best understood as a **documented concern about provenance and credit**, not a demonstrated plagiarism finding. He explicitly says he has not seen OpenAI’s proof and is not making a categorical accusation; the strongest evidence supports the timeline and the existence of unresolved access and authorship questions, while the crucial inference of actual data use remains unproved.

## Turn 12

**Asker:** What evidence would actually resolve the provenance dispute, as opposed to merely making either side’s story seem more plausible: access logs, model-training records, a detailed comparison of the proofs, or something else?

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：what would count as decisive evidence】

No single item would settle the entire dispute, because there are four different questions:

- **Direct access:** Did any OpenAI employee, agent, retrieval system, or internal tool read the Codex sessions?  
  Relevant evidence: immutable access logs, file/retrieval logs, agent transcripts, and audit trails with timestamps.

- **Training exposure:** Were the sessions or derived data included in pretraining, fine-tuning, or reinforcement-learning data?  
  Relevant evidence: dataset manifests and hashes, sampling and de-identification logs, account settings, training-run dates, model checkpoints, and retrieval-index history. This matters because OpenAI denies specific access but says it cannot rule out de-identified product-derived data having improved its models. [OpenAI’s statement](https://openai.com/index/navier-stokes-solution/)

- **Dependence of the proof:** Did OpenAI’s proof use a distinctive unpublished idea from Buckmaster and Alpöge?  
  Relevant evidence: an independent, line-by-line comparison of both proofs against the earlier Córdoba-Martínez-Zoroa work and the public literature. A highly unusual private lemma, parameter choice, or construction sequence appearing in both proofs would be strong evidence. Similarity at the level of “use smooth forcing and high-frequency corrections” would not be enough, because that strategy was already part of the public research program.

- **Authorship conduct:** What exactly was said and proposed in the September 6 calls?  
  Relevant evidence: complete emails, messages, call recordings or contemporaneous notes, and draft publication proposals. Buckmaster’s statement is direct evidence of his recollection, but Bubeck gives a conflicting account. [Buckmaster’s statement](https://cims.nyu.edu/~tristanb/statement.pdf)

The strongest resolution would combine the evidence. For example, a training manifest showing that the private sessions entered the relevant model, followed by a rare unpublished lemma appearing in the model’s intermediate output, would strongly support the provenance claim. Conversely, records showing that the relevant checkpoints predated the sessions, no retrieval or training path existed, and the proof’s distinctive ideas arose independently would strongly support OpenAI’s account.

Timing, similar methods, public denials, or a clean Lean build are not decisive by themselves. They can make one story more plausible, but only a neutral forensic audit with preserved records, a chain of custody, and an expert proof comparison could address the dispute at the level of evidence rather than competing testimony.

## Turn 13

**Asker:** How should I interpret the absence of a published technical flaw right now: is it meaningful evidence for the proof, or mostly a sign that few experts have had time to audit a 166-page argument, and what would a serious independent audit look like?

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：what the absence of a flaw means】

Right now, it is **mostly a sign that very few experts have had time to audit the argument**, not meaningful confirmation that it is correct. The paper appeared on September 8, and current reporting still describes independent review as only beginning. [Current status report](https://elpais.com/ciencia/2026-09-09/el-anuncio-de-openai-de-que-ha-resuelto-uno-de-los-mayores-enigmas-matematicos-de-la-historia-desata-acusaciones-de-plagio.html)

There is some weak positive evidence: OpenAI published a long proof, public Lean code, and a precise theorem rather than only presenting a numerical experiment. A reproducible Lean build with no unfilled proof holes would also rule out many formal mistakes. But it does not tell us whether the difficult analytic interfaces were modeled correctly or whether the proof’s informal explanation matches the formal object.

A serious audit would proceed in layers:

1. **Reproducibility:** rebuild the exact public commit with the pinned Lean and Mathlib versions; inspect imports, axioms, and all placeholders.

2. **Statement alignment:** compare the formal C/D theorem line by line with Fefferman’s Clay formulation, including domains, quantifiers, smoothness, force decay, energy bounds, and periodicity.

3. **Proof correspondence:** map the 166-page paper’s main lemmas to the Lean declarations and check that no substantial analytic assertion appears only in prose.

4. **Limit analysis:** independently verify the multiscale estimates, convergence of the velocity and pressure sums, derivative losses, common domains, and all nonlinear interaction terms.

5. **Endpoint regularity:** verify that the residual is flat in the original \((x,t)\) derivatives, that the force extends smoothly through \(t=1\), and that no singularity has merely been moved into a cutoff, pressure term, or coordinate change.

6. **Blow-up and exclusion:** check that the correction tail cannot cancel the leading velocity growth, and that the uniqueness/comparison argument really excludes every global smooth competitor.

The key principle is: **Lean replay checks the formal derivation; expert audit checks the formalization’s meaning and the analytic estimates behind it.** Until the second part is done, “no flaw has been reported” should be read as “no flaw has yet been found in the limited time available,” not as independent confirmation. [OpenAI’s paper](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf) · [Lean repository](https://github.com/openai/NavierStokesAndEuler)

## Turn 14

**Asker:** Could you give a concrete example of how a Lean formalization might compile perfectly yet fail to represent the intended Clay problem, such as by weakening a quantifier or accidentally omitting a decay or smoothness condition?

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：how a correct Lean proof can prove the wrong specification】

A proof assistant can verify a theorem perfectly while the theorem is weaker than the English problem it was meant to represent. This is the mathematical analogue of verified software implementing the wrong specification.

**1. Weakening a quantifier**

Suppose the intended global-regularity claim is:

```lean
-- Intended Clay-style statement
theorem global_regular :
  ∀ u₀, AdmissibleInitial u₀ →
    ∃ v p, GlobalSmoothBoundedEnergy ν u₀ f v p
```

A mistaken formalization might prove:

```lean
theorem global_regular :
  ∃ u₀, AdmissibleInitial u₀ ∧
    ∃ v p, GlobalSmoothBoundedEnergy ν u₀ f v p
```

The second theorem may be proved by choosing \(u_0=0\), \(v=0\), and \(p=0\). Lean would correctly verify it, but it says nothing about arbitrary initial data.

**2. Omitting force regularity**

The intended counterexample requires the force to be smooth and rapidly decaying for all future time:

```lean
∀ derivative_order decay_rate,
  ∃ C, ∀ x t ≥ 0, derivative_bound ≤ C / (1 + ‖x‖ + t)^decay_rate
```

A weaker encoding might require only:

```lean
ContDiffOn ℝ 0 f { (x,t) | t < 1 }
```

Then one could choose a collapsing \(u\), define

\[
f=\partial_tu+(u\cdot\nabla)u-\nu\Delta u+\nabla p,
\]

and never prove that \(f\) is smooth through \(t=1\). That would be a valid theorem about a pre-singular, possibly pathological force, but not the Clay problem.

**3. Omitting the energy condition**

For a positive global-existence claim, defining `GlobalSmooth` to mean only \(C^\infty\) and the PDE, while omitting \(L^2\)-integrability and uniformly bounded kinetic energy, could prove the existence of a smooth solution outside the class Clay calls physically reasonable.

The public comparator definitions appear deliberately designed to avoid these errors: they include the PDE, divergence-free condition, initial data, smoothness, decay or periodicity, \(L^2\) integrability, and global energy bounds. [Comparator definitions](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/NavierStokes/ComparatorDefinitions.lean) · [Formal C/D theorem](https://raw.githubusercontent.com/openai/NavierStokesAndEuler/main/NavierStokes/ComparatorSolution.lean)

But a reviewer still has to check that those formal predicates are faithful translations of Fefferman’s official C/D statements. Lean can certify:

\[
\text{formal assumptions} \Rightarrow \text{formal conclusion}.
\]

It cannot, by itself, certify that the formal assumptions are exactly the assumptions intended by Clay. [Clay’s official formulation](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf)

## Turn 15

**Asker:** What should I infer from Tao’s praise of Buckmaster and Alpöge’s related work: does it provide evidence that OpenAI’s proof is mathematically plausible, or only that the broader smooth-forcing strategy is credible?

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：what Tao’s praise actually establishes】

Mostly the latter: Tao’s comments support the **credibility of the broader smooth-forcing strategy**, not the correctness of OpenAI’s specific proof.

Tao had examined Buckmaster and Alpöge’s related results and judged them a major advance. He also said their Córdoba-Martínez-Zoroa-inspired method appeared capable, in principle, of being extended to Navier-Stokes. That makes OpenAI’s claimed route mathematically plausible rather than obviously absurd. [Tao’s assessment](https://terrytao.wordpress.com/2026/09/07/finite-time-blowup-with-smooth-forcing-term-for-the-incompressible-porous-medium-boussinesq-and-incompressible-euler-equations/)

But the inference stops there:

- Buckmaster and Alpöge’s published results concern forced Euler and other related equations.
- OpenAI claims to handle viscous Navier-Stokes and establish Clay alternatives C and D.
- The two groups’ detailed constructions may differ substantially.
- Tao did not independently audit OpenAI’s 166-page proof or its Lean formalization.

So Tao’s praise raises the prior plausibility of OpenAI’s approach, especially because OpenAI says it used a related program. It is **not evidence that the final analytic estimates, smooth-force extension, or Clay statement are correct**. That would require Tao or other independent experts to inspect OpenAI’s actual proof.

## Turn 16

**Asker:** How should we distinguish legitimate use of Córdoba–Martínez-Zoroa’s and Buckmaster–Alpöge’s public ideas from copying an unpublished proof, and what would an independent contribution by OpenAI need to show?

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：public inheritance versus private dependence】

The key distinction is **causal dependence, not superficial similarity**.

Using a published method is legitimate. Córdoba and Martínez-Zoroa’s forced-blowup program was public, and Buckmaster’s statement explicitly credits them. OpenAI could lawfully and academically use that strategy, provided it accurately cited the prior work. A new contribution could consist of extending the method to viscous Navier-Stokes, controlling viscosity, or completing the smooth-force and localization arguments. [Buckmaster’s statement](https://cims.nyu.edu/~tristanb/statement.pdf) · [Tao’s explanation of the public program](https://terrytao.wordpress.com/2026/09/07/finite-time-blowup-with-smooth-forcing-term-for-the-incompressible-porous-medium-boussinesq-and-incompressible-euler-equations/)

Copying an unpublished proof would be different. That could involve using a private lemma, parameter choice, construction sequence, draft, code artifact, or model transcript that was not publicly available. Re-deriving it in different notation or having another model formalize it would not automatically make the dependence independent.

An independent OpenAI contribution would ideally show:

- **Public-source provenance:** prompts, retrieval logs, and research records show that the relevant ideas came from public papers, public discussions, or generic problem exploration, rather than private Codex sessions.
- **Technical separation:** a neutral expert comparison identifies which ingredients were already public and which Navier-Stokes-specific steps are genuinely new.
- **Distinctive derivation:** the proof’s unusual lemmas, parameter choices, and correction architecture can be traced to an independent development path, not merely presented after the fact.
- **Reliable chronology:** preserved model checkpoints, agent transcripts, drafts, and timestamps show when the key ideas appeared.
- **Proper attribution:** the paper credits Córdoba, Martínez-Zoroa, Buckmaster, Alpöge, and others for whatever prior ideas materially enabled the result.

A different final proof is not sufficient, because two proofs can differ in notation while sharing a decisive unpublished idea. Conversely, a similar high-level strategy is not sufficient to establish copying when that strategy was already public. The strongest resolution would combine proof comparison with independent audit of model-data and development records. OpenAI’s public account denies using the pair’s work before release but acknowledges that de-identified product-derived data cannot be completely ruled out, so the issue remains unresolved. [OpenAI’s account](https://openai.com/index/navier-stokes-solution/)

## Turn 17

**Asker:** What exactly is the disagreement between Buckmaster and Bubeck about Alpöge’s authorship, and how is that different from the separate question of who deserves priority for the mathematical idea?

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：public ideas versus private proof dependence】

The distinction is **causal dependence, not whether the final paper looks different**.

Using Córdoba-Martínez-Zoroa’s published forcing program is legitimate. Using Buckmaster and Alpöge’s publicly released results is also legitimate, provided the work is cited. A new contribution could be extending that program from related equations to viscous Navier-Stokes, or solving the smooth-force, localization, and residual-cancellation problems. [Tao’s public explanation](https://terrytao.wordpress.com/2026/09/07/finite-time-blowup-with-smooth-forcing-term-for-the-incompressible-porous-medium-boussinesq-and-incompressible-euler-equations/)

Copying an unpublished proof would mean that a non-public lemma, parameter choice, construction sequence, draft, code artifact, or model transcript materially entered OpenAI’s reasoning. Rewriting such material in different notation or formalizing it in Lean would not make the dependence independent.

There is also a middle case: OpenAI may have learned only that researchers were close to a result. That could be a legitimate research lead. But if the rumor conveyed a distinctive private route, or if private Codex material entered model training, the issue becomes more serious. OpenAI says its effort began after rumors and that it did not access the researchers’ specific work, while acknowledging that it cannot rule out de-identified product-derived data having improved its models. [OpenAI’s account](https://openai.com/index/navier-stokes-solution/) · [Buckmaster’s account](https://cims.nyu.edu/~tristanb/statement.pdf)

An independent OpenAI contribution would need to show:

- a provenance map for every major idea, identifying whether it came from public literature, generic exploration, or a new derivation;
- preserved prompts, retrieval logs, training manifests, checkpoints, and timestamps showing no use of private material;
- an independent expert comparison against both the public Córdoba-Martínez-Zoroa program and Buckmaster-Alpöge’s work;
- genuinely new Navier-Stokes-specific mathematics, not merely a new implementation of a private roadmap;
- accurate credit to prior contributors, even if OpenAI completed the final extension.

A clean Lean build, different notation, or a claim that no one manually opened the Codex sessions would not settle this. The meaningful question is whether any non-public idea was causally used. If it was, OpenAI could still have made a substantial new contribution, but it should describe the result as building on that work rather than as an entirely independent discovery.

## Turn 18

**Asker:** That clarifies priority, but not the call itself: what are Buckmaster’s and Bubeck’s conflicting accounts of the September 6 authorship discussion, and why did Alpöge’s employment at Anthropic matter?

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：the September 6 call and Alpöge’s authorship】

The disagreement is about **which paper Alpöge was supposedly being excluded from**, and whether that exclusion was a normal conflict-of-interest boundary or an attempt to strip a collaborator of credit.

**Buckmaster’s account:**

- OpenAI proposed that Buckmaster and Alpöge release their Euler result, followed by OpenAI’s Navier-Stokes announcement.
- A second proposal, he says, was that Buckmaster alone write a paper presenting OpenAI’s Navier-Stokes result, acknowledging that an internal OpenAI model had found it.
- Buckmaster says Bubeck twice indicated that Alpöge should not be an author because he worked for Anthropic. He understood this as excluding Alpöge from the paper presenting OpenAI’s result, despite Alpöge’s year-long collaboration with him on the relevant research program. [Buckmaster’s statement](https://cims.nyu.edu/~tristanb/statement.pdf)

**Bubeck’s account:**

- He says he never asked Alpöge to be removed from authorship of **Buckmaster and Alpöge’s own work**.
- His version is that they were discussing a separate paper about OpenAI’s independently produced Navier-Stokes proof, for which Buckmaster might be lead author. He says it seemed inappropriate for an Anthropic employee to author work produced by OpenAI.
- He also says his outreach to Alpöge was intended to coordinate the releases and ensure the pair received recognition. [Bubeck’s published response](https://texxr.com/handle/sebastienbubeck) · [Contemporaneous summary](https://venturebeat.com/technology/openai-solves-longstanding-math-problem-with-10-000-agent-swarm-but-cant-rule-out-benefitting-from-a-researchers-private-codex-data)

Thus, Bubeck’s denial is narrower than “Alpöge’s affiliation was never raised.” By his own account, the affiliation was relevant to whether Alpöge could author an OpenAI paper. The unresolved point is whether that proposal would merely have kept Alpöge off an OpenAI-authored proof, or whether it functionally erased his contribution from the broader credit for the result. There is no public recording or agreed transcript of the call.

Alpöge’s employment mattered because Anthropic was OpenAI’s competitor, and Bubeck says Anthropic models had contributed to the pair’s Euler work. Buckmaster viewed that as an institutional affiliation being used against a personal collaboration; Bubeck viewed it as a conflict-of-interest problem for authorship of OpenAI’s separate work.

This is distinct from **priority**. Authorship asks who should be listed on a particular paper. Priority asks who supplied the underlying ideas, when they supplied them, and whether OpenAI’s proof depended on private work. OpenAI could have priority for the first complete Navier-Stokes proof while still owing substantial credit to prior researchers, or it could face a stronger priority challenge if private unpublished ideas materially shaped the result. The call alone cannot answer that.

## Turn 19

**Asker:** Does the public Lean development formally prove the difficult multiscale estimates from the construction, or does it mainly define an abstract candidate satisfying those properties and then prove the comparison theorem from them?

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：what the Lean development actually formalizes】

It is a layered answer, not either/or.

The generic assembly layer is conditional. `MixedCandidateAssembly.StageEstimates` specifies smoothness, derivative, gain, and finite-prefix residual bounds. Its assembly theorem then uses those obligations to construct the diagonal schedule, infinite sums, smooth force, candidate solution, and blow-up consequences. The file explicitly says it does not construct the correction iteration or supply those estimates itself. [MixedCandidateAssembly.lean](https://github.com/openai/NavierStokesAndEuler/blob/main/NavierStokes/MixedCandidateAssembly.lean)

But the public top-level path does not simply assume an abstract `CandidateProperties` witness. `ActualCandidateAssembly.estimates` is built from actual iteration data and `GluedStageEstimates.actualStageEstimates`; exact finite-prefix physical realizations come from `ActualPhysicalPrefixFields.physicalFields_all`. Those are then passed into the generic assembly theorem. [ActualCandidateAssembly.lean](https://github.com/openai/NavierStokesAndEuler/blob/main/NavierStokes/ActualCandidateAssembly.lean), [GluedStageEstimates.lean](https://github.com/openai/NavierStokesAndEuler/blob/main/NavierStokes/GluedStageEstimates.lean)

So the precise characterization is:

- The difficult finite-stage and multiscale bounds are formalized as concrete obligations derived from the actual construction.
- The diagonal convergence, smooth extension, candidate properties, and comparison with the Clay statement are proved by reusable generic theorems conditional on those obligations.
- It is therefore neither merely an abstract candidate axiom nor one monolithic formalization of every analytic detail.

The remaining audit question is whether the concrete `Actual...` definitions and imported lemmas faithfully encode the intended paper construction, with no weakened hypotheses or specification mismatch. The repository’s “full formalization” claim is still a project claim requiring mathematical review. [GermCandidateAssembly.lean](https://github.com/openai/NavierStokesAndEuler/blob/main/NavierStokes/GermCandidateAssembly.lean)

## Turn 20

**Asker:** When the code says the concrete stage estimates are “derived from actual iteration data,” are those estimates themselves proved from explicit definitions and earlier lemmas, or are some of them still supplied as assumptions at the trust boundary?

**Tutor:**

【逐步讨论中｜主题：OpenAI's claimed Navier-Stokes solution and the controversy｜当前：the trust boundary for concrete stage estimates】

Mostly explicit definitions and earlier proved lemmas, with an important architectural qualification.

The generic theorem accepts a packaged `StageEstimates` record as an assumption. But the actual constructor `actualStageEstimates` builds that record from:

- actual state coherence `C`;
- smoothness and bounds for the actual current fields;
- representation data `e`;
- exact finite-prefix physical data `d`.

Its body calls `stageEstimates_of_component_bounds`, `current_fields_smooth`, `current_potential_bound`, and `current_pressure_bound`; the source explicitly says that no physical derivative estimate is supplied as a premise of this constructor. [GluedStageEstimates.lean](https://github.com/openai/NavierStokesAndEuler/blob/main/NavierStokes/GluedStageEstimates.lean)

At the top level, those inputs are themselves produced by earlier formal results. The actual iteration is defined as `CycleState.iterate`; `state_runInvariant` proves its invariant inductively, yielding coherence, particular-data, and step-data theorems. Exact finite-prefix physical data are then proved from stage realizations, smoothness, exterior identities, and cycle representations. [ActualCyclePreservation.lean](https://github.com/openai/NavierStokesAndEuler/blob/main/NavierStokes/ActualCyclePreservation.lean), [ActualPhysicalPrefixFields.lean](https://github.com/openai/NavierStokesAndEuler/blob/main/NavierStokes/ActualPhysicalPrefixFields.lean)

Finally, `ActualCandidateAssembly.estimates` invokes `actualStageEstimates` with those constructed terms, rather than receiving an arbitrary `StageEstimates` witness. [ActualCandidateAssembly.lean](https://github.com/openai/NavierStokesAndEuler/blob/main/NavierStokes/ActualCandidateAssembly.lean)

So the precise answer is:

**At the actual main theorem boundary, the stage-estimate record is claimed to be proved, not left as an uninstantiated assumption.** The generic assembly theorem treats it abstractly only for reuse.

The remaining trust question is semantic: whether the definitions and earlier lemmas faithfully encode the intended analytic construction. The repository reports zero `sorry`s and only standard Lean axioms for the main results, but labels its review status “self-assessed,” so that report is not an independent audit. [formalization.yaml](https://github.com/openai/NavierStokesAndEuler/blob/main/formalization.yaml)

## Asker final understanding

Reliability: OpenAI claims an exact smooth-forced blow-up construction, with Lean checking the encoded derivation; however, experts must still verify that the formal definitions match Clay’s C/D problem and that the analytic estimates truly encode the intended construction.
Controversy: Buckmaster raises timing, provenance, and authorship concerns; OpenAI and Bubeck dispute their interpretation. Tao supports the broader research strategy, not OpenAI’s specific proof. No public evidence yet proves copying or identifies a mathematical flaw.
Remaining uncertainties: Independent technical review has barely begun; the semantic trust boundary of the formalization, possible use of private or derived Codex data, the authorship conversation, and the proof’s ultimate correctness remain unresolved. The result addresses the officially permitted forced formulation, not the unforced A/B question about ordinary fluids.
