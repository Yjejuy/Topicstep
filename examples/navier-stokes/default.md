# default

## Turn 1

**Asker:** I've heard that OpenAI found a solution to the Navier–Stokes equations and that there's some controversy about it. Tell me about that.

**Tutor:**

**Short version:** OpenAI has published a serious *claim* of a Navier–Stokes breakthrough, but it is not yet an accepted mathematical solution.

The Navier–Stokes equations model incompressible fluid motion:

\[
\partial_t u+(u\cdot\nabla)u-\nu\Delta u+\nabla p=f,\qquad \nabla\cdot u=0.
\]

The famous 3D problem asks whether smooth initial conditions can ever lead to a finite-time singularity, where the velocity becomes unbounded, or whether smooth solutions always remain smooth. It is one of the Clay Mathematics Institute’s Millennium Prize Problems.

OpenAI says its internal multi-agent system constructed a smooth, finite-energy solution that starts from rest and develops unbounded velocity in finite time. The construction uses a carefully chosen **smooth external force**, a concentrating vortex, and oscillatory corrections that cancel the singular parts of the equation. OpenAI released a roughly 166-page proof and a Lean formalization, claiming it establishes alternatives C and D in the official Clay formulation. Those alternatives explicitly permit a smooth external force, so this is not automatically outside the written problem. [OpenAI’s announcement](https://openai.com/index/navier-stokes-solution/) · [the proof](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf) · [Clay’s formulation](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf)

But several qualifications matter:

- This is not a general closed-form solution for fluids, nor does it mean ordinary water-flow simulations suddenly fail.
- It is a proof of the **existence of one pathological forced flow**, not a claim that every unforced fluid develops a singularity.
- Lean checks the formalized proof inside Lean’s foundations; independent mathematicians must still establish that the formalization correctly captures the intended theorem and that the underlying construction is sound. The public repository is available [here](https://github.com/openai/NavierStokesAndEuler).
- Clay’s prize rules require publication in a qualifying outlet, at least two years of elapsed time, and general acceptance by the mathematics community. OpenAI says it does not intend to claim the prize now. [Clay’s rules](https://www.claymath.org/millennium-problems/rules/)

**The controversy is mainly about priority, confidentiality, and credit.**

NYU mathematician Tristan Buckmaster and Anthropic researcher Levent Alpöge had been working on related fluid-dynamics problems, using several AI systems. They had reportedly obtained finite-time blow-up results for forced Euler, Boussinesq, and porous-media equations, while exploring a route toward Navier–Stokes. Their work built on earlier ideas by Diego Córdoba and Luis Martínez-Zoroa. [Buckmaster’s statement](https://cims.nyu.edu/~tristanb/statement.pdf)

OpenAI says it began its effort after hearing rumors that researchers associated with Anthropic had solved a major problem. It then used thousands of agents, first on easier related problems and then on Navier–Stokes. Buckmaster alleges that OpenAI learned about their unpublished direction, raced to complete a competing proof, proposed excluding Alpöge from authorship because he worked for Anthropic, and pressured him during discussions. Those are his allegations, not independently established facts; OpenAI researchers dispute his account.

There is also a data-use concern. OpenAI says its researchers and agents did not access the pair’s specific Codex sessions before publication, but acknowledged that it could not rule out de-identified user-derived data having contributed to model training. That distinction is central: **direct use of private prompts is denied; indirect model-training influence is not ruled out**. [WIRED’s reporting](https://www.wired.com/story/openai-navier-stokes-math-discovery-academics/)

So the fairest description today is: **OpenAI has released a potentially prize-relevant, machine-formalized proof of finite-time breakdown for a forced 3D Navier–Stokes system. Its mathematical correctness and its eventual status as a Clay solution remain pending, while the circumstances surrounding how it pursued the result and assigned credit are highly contested.**

## Turn 2

**Asker:** I don’t yet see why a carefully chosen external force does not make the result much easier or change the problem. What exactly do Clay’s alternatives C and D require about the force: must it be fixed in advance, smooth, and independent of the evolving solution? If the force is designed together with the desired singular flow, why is constructing it still nontrivial, and how can a smooth force produce unbounded velocity?

**Tutor:**

Your intuition is right: allowing an arbitrary force makes the target more contrived, and generally easier, than the unforced problem. But Clay’s formulation deliberately permits that route.

**What C and D actually say**

Roughly, alternative C says:

\[
\exists\,u_0,\ f
\]

such that:

- \(u_0\) is smooth and divergence-free on \(\mathbb R^3\);
- \(f(x,t)\) is a smooth prescribed force satisfying strong decay conditions in space and time;
- no globally smooth, bounded-energy solution exists for that \(u_0\) and \(f\).

Alternative D says the analogous thing on the periodic 3-torus, with smooth periodic data and force. The official wording does **not** require the force to be generic, physically realistic, or chosen without knowing the intended construction. It is an existential statement: finding one admissible force is enough. [Clay’s official formulation](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf)

At the end of the proof, however, \(f\) must be a fixed function of \(x\) and \(t\). It cannot be a feedback rule such as “apply whatever force is needed to cancel the current solution’s singularity.” Designing \(u\) and \(f\) together is allowed; leaving \(f\) dependent on the unknown evolving \(u\) is not.

**Why inverse design is not trivial**

For any sufficiently smooth trial fields \(u,p\), one can define

\[
f=\partial_tu+(u\cdot\nabla)u-\nu\Delta u+\nabla p.
\]

So superficially, one could invent a blowing-up \(u\) and call the residual \(f\). The problem is that when \(u\) blows up, the terms in this residual normally blow up too. The force would then be singular, violating Clay’s assumptions.

The real task is therefore to construct a velocity and pressure such that:

1. \(u\) becomes unbounded;
2. \(u\) remains divergence-free and has bounded kinetic energy;
3. viscosity remains positive;
4. every space-time derivative of the residual \(f\) remains smooth through the blow-up time;
5. the force has the required decay or periodicity.

OpenAI’s paper explicitly describes this as the central difficulty: the individual acceleration, nonlinear-advection, viscosity, and pressure terms may diverge, but their sum must cancel to all orders and leave a smooth force. [OpenAI’s proof](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)

**How smooth forcing can coexist with infinite velocity**

Smoothness of the force does not imply a uniform bound on the solution’s pointwise velocity. The nonlinear equation can transfer energy into smaller and smaller regions.

OpenAI’s construction concentrates a vortex near one point. Writing \(\tau=1-t\), its approximate scales are:

\[
\ell_r\sim \tau^{1/2},\qquad
\ell_z\sim \tau^{1/2-h},\qquad
|u|\sim\tau^{-1/2-h},
\]

with small \(h>0\). Thus the velocity diverges, but the affected volume shrinks faster. The kinetic energy scales like

\[
\|u\|_2^2
\sim
\tau^{1/2-3h},
\]

which remains bounded and even tends to zero for the stated range of \(h\).

The construction then adds oscillatory pulses. The background vortex’s shear amplifies these pulses, and their quadratic momentum fluxes provide the stress needed to cancel the singular residual of the background flow. The force only seeds and corrects the construction; it does not itself become infinite.

So the force is functioning like a carefully preprogrammed input that creates a cascade and maintains delicate cancellations. That is still a very difficult PDE construction, but it is not the same challenge as proving blow-up for the physically more natural case \(f=0\).

**Bottom line**

If OpenAI’s proof is correct, it satisfies the literal Clay alternatives C and D. But the headline “Navier–Stokes has been solved” can mislead if read as “unforced 3D fluids are now known to blow up.” It establishes a specially forced counterexample, not the unforced case. Independent verification is still required, and Clay’s prize rules require publication in a qualifying outlet, two years of scrutiny, and broad mathematical acceptance. [Clay’s prize rules](https://www.claymath.org/millennium-problems/rules/)

## Turn 3

**Asker:** I’m confused by the distinction between bounded kinetic energy and a genuine singularity. If the velocity becomes infinite only in a region whose volume shrinks to zero, and the total energy even tends to zero, why can’t we simply define the solution at \(t=1\) and continue it smoothly afterward? What precise regularity condition fails, and can you give a simple toy example showing how an \(L^2\)-bounded function can still be singular?

**Tutor:**

The key distinction is:

\[
\text{bounded kinetic energy} \quad\Longleftrightarrow\quad u\in L^2_x,
\]

whereas a classical Navier–Stokes solution requires, among other things,

\[
u,p\in C^\infty_{x,t}.
\]

The \(L^2\) norm measures an integral. It does not control the largest pointwise velocity or its derivatives.

**What fails at the singular time**

OpenAI’s claimed theorem has

\[
\limsup_{t\uparrow 1}\|u(t)\|_{L^\infty(\mathbb R^3)}=\infty.
\]

That alone prevents a continuous extension through \(t=1\). In the concentrating core, there are points \(x_t\to 0\) for which

\[
|u(x_t,t)|\to\infty.
\]

If a finite continuous value \(u(0,1)\) existed, continuity would require \(u(x_t,t)\to u(0,1)\), a contradiction.

Assigning an arbitrary value at the single point \((0,1)\) cannot fix this: the values in every neighborhood just before \(t=1\) are already becoming arbitrarily large. A smooth continuation would require finite limits not only of \(u\), but of all spatial and time derivatives as well.

The claimed result therefore rules out a **global classical solution**. It does not necessarily rule out some weaker, distributional or \(L^2\)-based continuation; that is a different question. [OpenAI’s theorem](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf) · [Clay’s regularity requirements](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf)

**A smooth toy example**

Let \(0<\tau=1-t\), and let \(\phi\in C_c^\infty(\mathbb R)\) satisfy \(\phi(0)=1\). Define

\[
g(x,t)=\tau^{-1/4}\phi\left(\frac{x}{\tau}\right),
\qquad t<1.
\]

For every \(t<1\), this is smooth. Its peak value is

\[
g(0,t)=\tau^{-1/4}\to\infty.
\]

But its squared \(L^2\) norm is

\[
\begin{aligned}
\|g(\cdot,t)\|_2^2
&=\int \tau^{-1/2}
\left|\phi\left(\frac{x}{\tau}\right)\right|^2\,dx\\
&=\tau^{1/2}\int|\phi(y)|^2\,dy
\longrightarrow 0.
\end{aligned}
\]

So the function’s total \(L^2\) energy tends to zero while its pointwise maximum diverges. The spike is becoming taller faster than it is becoming wide.

At \(t=1\), one could define \(g(x,1)=0\) everywhere, and the \(L^2\) limit would be perfectly reasonable. But there is no continuous extension, because

\[
g(0,t)\to\infty.
\]

Its derivatives also diverge; for example,

\[
\partial_x g(x,t)
=\tau^{-5/4}\phi'\left(\frac{x}{\tau}\right).
\]

This is the basic concentration mechanism behind the Navier–Stokes distinction: finite integral energy does not prevent arbitrarily large local amplitudes or gradients.

## Turn 4

**Asker:** I want to understand what “Lean-verified” really guarantees. If Lean accepts every formal proof step, is a mathematical error impossible, or could the formalized theorem still differ from the intended Navier–Stokes claim through a wrong equation, quantifier, domain, or admissibility condition? What would independent mathematicians need to check before treating the result as reliable?

**Tutor:**

**Lean verifies a formal proposition, not the English claim surrounding it.**

If Lean’s kernel accepts a proof term for \(P\), the strong guarantee is approximately:

\[
\text{Lean's foundations}+\text{imported declarations}\vdash P.
\]

This is conditional on trusting the kernel, the imported libraries, and any axioms used. Lean’s tactics may be buggy, but they ultimately have to produce a proof term accepted by the kernel. [Lean’s reference manual](https://lean-lang.org/doc/reference/latest/)

That still leaves a crucial semantic question:

\[
P_{\text{formal}} \stackrel{?}{=} P_{\text{intended}}.
\]

Lean cannot tell whether the formal proposition is the Navier–Stokes theorem people intended.

For example, Lean could successfully verify a theorem involving:

- the wrong sign on the viscosity term;
- Euler rather than Navier–Stokes;
- forced rather than unforced equations;
- \(\mathbb T^3\) rather than \(\mathbb R^3\);
- “there exists a force” rather than “for every force”;
- weak solutions rather than classical smooth solutions;
- an essential \(L^\infty\) bound rather than the intended pointwise condition;
- a restricted class of test functions or boundary conditions.

Those would be valid Lean theorems but potentially the wrong scientific result.

**What “Lean-verified” rules out**

It gives strong protection against:

- an omitted proof step;
- an invalid algebraic or logical inference;
- a tactic silently leaving a goal unresolved;
- many ordinary implementation bugs in proof automation.

It does **not**, by itself, rule out:

- a mis-translated theorem statement;
- a wrong definition of “smooth,” “solution,” or “blow-up”;
- an accidentally weakened quantifier;
- hidden assumptions;
- admitted axioms or `sorry`-based results in the dependency chain;
- a mismatch between the formal domain and the Clay domain.

Lean’s own validation guidance explicitly says the result is meaningful only if the formal statement matches its intended meaning and the imported libraries and axioms are trusted. It also recommends checking proof artifacts with independent tools where possible. [Validating a Lean proof](https://lean-lang.org/doc/reference/latest/ValidatingProofs/)

**What reviewers would need to check for this result**

1. **The top-level theorem.**  
   They should read the exact Lean proposition, not infer it from the paper title. They need to verify the quantifier order, especially that it proves the appropriate Clay alternative C or D.

2. **The equation and domain.**  
   They should check that the formal equation is genuinely 3D incompressible Navier–Stokes with \(\nu>0\), and distinguish \(\mathbb R^3\) from the periodic torus.

3. **Admissibility of the force.**  
   They should verify that \(f\) is a fixed function of \(x,t\), smooth through the alleged singular time, and satisfies Clay’s decay or periodicity conditions. It must not secretly be a feedback term depending on the evolving solution.

4. **Regularity definitions.**  
   They should inspect what the formalization means by \(C^\infty\), divergence-free, bounded kinetic energy, compact support, and \(L^\infty\) blow-up. A missing derivative, boundary condition, or time endpoint could materially weaken the claim.

5. **The construction-to-theorem bridge.**  
   The human-readable paper must correctly connect the explicit construction to the formal objects. In particular, reviewers need to verify that the formal proof establishes a genuine velocity-pressure-force solution before the blow-up time, not merely an abstract surrogate.

6. **Axiom and dependency audit.**  
   They should inspect the transitive axioms used by the theorem, confirm there are no `sorry` placeholders or unreviewed assumptions, and understand what portions come from Mathlib or other imported code.

7. **Independent rebuilding.**  
   They should rebuild the repository from a clean environment with pinned Lean and library versions. The OpenAI repository also provides Comparator challenges intended for checking with the Lean kernel and an independent checker. [OpenAI’s formalization repository](https://github.com/openai/NavierStokesAndEuler)

8. **Mathematical peer review.**  
   Finally, fluid-dynamics experts must determine whether the formal theorem really satisfies the official Clay statement and whether the definitions and imported analytic results express the intended mathematics. That is why machine verification substantially raises confidence, but does not instantly replace independent mathematical scrutiny.

So the right interpretation is:

> **Lean verification makes “there is a derivation of this exact formal theorem” highly checkable. It does not automatically establish that this exact theorem is the Navier–Stokes Millennium Prize claim that the announcement describes.**

## Turn 5

**Asker:** The axiom issue worries me. Since Lean can accept a theorem declared as an axiom, couldn’t someone simply assume the desired Navier–Stokes result and have Lean “verify” it? In practice, how would reviewers distinguish a genuine derivation from one relying on a newly added axiom or hidden `sorry`, and what does a trustworthy axiom audit look like?

**Tutor:**

Yes. Lean can accept:

```lean
axiom navier_stokes_solved : TargetTheorem
theorem result : TargetTheorem := navier_stokes_solved
```

But that is not a derivation of `TargetTheorem`; it is a theorem conditional on a newly postulated assumption. Lean’s kernel does not check whether axioms are true. [Lean’s axiom documentation](https://lean-lang.org/doc/reference/latest/Axioms/)

**The standard audit**

Reviewers should identify the exact top-level theorem and run:

```lean
#print axioms result
```

Lean reports axioms used directly or transitively by that declaration. A normal finished theorem may depend on the standard logical axioms:

```text
propext
Classical.choice
Quot.sound
```

Those are ordinary foundations of Lean’s mathematics. Red flags include:

```text
sorryAx
```

which means some theorem or dependency contains `sorry` or another incomplete proof, and any unfamiliar custom axiom such as:

```text
NavierStokes.assumed_result
```

A custom axiom does not become trustworthy merely because its name sounds mathematical. Reviewers must inspect its declaration. If it has no proof body, it is an assumption, not a derived theorem. `#print axioms` is specifically designed to expose these transitive dependencies. [Lean’s proof-validation guide](https://lean-lang.org/doc/reference/latest/ValidatingProofs/)

`Lean.trustCompiler` or a generated `native_decide` axiom is a different kind of warning: it indicates reliance on compiled native evaluation rather than only the small kernel. That may be acceptable for some computations, but it must be explicitly justified and audited.

**Why source-code search alone is insufficient**

Searching for `axiom`, `sorry`, and `admit` is useful, but not enough:

- an assumption can be hidden in an imported module;
- `sorry` can occur several dependency levels below the main theorem;
- generated declarations may not literally contain the word `sorry`;
- the theorem may be formally complete but state the wrong proposition.

The transitive `#print axioms` result is therefore more important than a simple text search.

**A stronger reproducibility check**

A serious audit would:

1. Pin the exact repository commit, Lean version, and Mathlib revision.
2. Build everything from source in a clean environment.
3. Run `#print axioms` on every claimed top-level theorem.
4. Reject `sorryAx` and unexplained custom axioms.
5. Run `lean4checker --fresh` to replay the stored declarations through the kernel.
6. Where possible, run an independent checker such as `nanoda` through Comparator. The OpenAI repository provides Comparator challenge instructions. [OpenAI’s formalization repository](https://github.com/openai/NavierStokesAndEuler)

This distinguishes:

> “The theorem has a checked derivation from the stated foundations”

from:

> “The theorem was declared as an assumption somewhere.”

It does not, however, solve the semantic problem.

**The separate statement audit**

Even with an axiom-free proof, reviewers must inspect the fully elaborated theorem and definitions. They need to verify that it actually says:

- 3D incompressible **Navier–Stokes**, not Euler or a surrogate;
- \(\nu>0\);
- the intended domain, \(\mathbb R^3\) or \(\mathbb T^3\);
- the correct quantifier order;
- smooth admissible initial data and force;
- the intended pressure and incompressibility conditions;
- bounded kinetic energy;
- genuine \(L^\infty\) or pointwise breakdown;
- the exact Clay alternative C or D.

For example, Lean will flawlessly prove a theorem of the form

\[
\exists f\;\text{such that breakdown occurs}
\]

even if the intended claim was

\[
\text{for every admissible }f,\text{ breakdown occurs}.
\]

That is a statement error, not a proof-step error.

The clean conceptual division is:

1. **Kernel correctness:** the accepted proof term really proves the formal proposition.
2. **Axiom audit:** the proposition is not being assumed through custom axioms or `sorry`.
3. **Formalization audit:** the formal proposition matches the paper and Clay’s statement.
4. **Mathematical audit:** the definitions, analytic constructions, and theorem bridge express the intended Navier–Stokes mathematics.

Only the first two are substantially automated. The third and fourth still require careful human review.

## Turn 6

**Asker:** I understand the difference between a checked derivation and a checked interpretation. Now I want to understand the controversy on its own terms: what exactly does Buckmaster allege about OpenAI’s use of the unpublished research and the authorship dispute, what does OpenAI or Alpöge say in response, and which parts are supported by public evidence versus still just competing accounts?

**Tutor:**

**The dispute has three separate parts:** priority, possible use of private research data, and authorship/conduct. They should not be collapsed into “OpenAI stole the proof,” which has not been established publicly.

**Buckmaster’s account**

Buckmaster’s public statement says:

- He and Levent Alpöge had worked for roughly a year on a research program involving finite-time blow-up in related fluid equations.
- On August 15 they obtained results for forced Euler, Boussinesq, and porous-media equations. They believed they also had a route toward a Navier–Stokes result, but had not finished or published it.
- On September 3, after hearing that information about their work had reached OpenAI, he contacted an OpenAI mathematician.
- During calls on September 6, OpenAI representatives told him an internal model had produced a roughly 100-page proof of forced Navier–Stokes blow-up. He says he was initially shown a prompt suggesting that the model had simply been given the problem statement, but that later discussion revealed a larger team, easier intermediate problems, an Euler result, substantial human direction, and very large compute usage.
- He says OpenAI eventually acknowledged that the effort had begun after information about their work reached the company.
- He asked whether OpenAI’s model had accessed or been trained on their private Codex sessions. According to him, OpenAI said the model did not look up user data but did not answer the separate training question.
- He says two publication arrangements were proposed: either a coordinated release, or Buckmaster alone rewriting OpenAI’s Navier–Stokes result while acknowledging the internal model. He alleges that Bubeck twice said it would be easier if Alpöge were excluded because he worked for Anthropic.
- When Buckmaster said he would make the interaction public, he attributes to Bubeck remarks about “ruining” his career and Bubeck’s willingness to stop being “nice.” [Buckmaster’s full statement](https://cims.nyu.edu/~tristanb/statement.pdf)

Importantly, Buckmaster explicitly says he had not seen OpenAI’s proof and was not claiming to know whether OpenAI used their data.

**OpenAI and Bubeck’s response**

OpenAI’s official account agrees with some of the timeline:

- It heard a rumor on September 1 that major mathematical problems had been solved.
- It later realized the rumor concerned Alpöge and Buckmaster, and launched a large internal effort.
- It completed its own proof and Lean verification before contacting them.
- It says the pair had solved forced Euler, not Navier–Stokes, and that the two proofs differ materially.
- It says neither researchers nor agents saw their specific work before it was publicly released.
- It also says it cannot rule out the possibility that de-identified data from product usage helped improve the model. That is an important qualification, but it is not an admission that their private proof was accessed or used. [OpenAI’s account](https://openai.com/index/navier-stokes-solution/)

Bubeck’s more detailed response disputes Buckmaster’s interpretation. He says he did not ask for Alpöge to be removed from authorship of Alpöge and Buckmaster’s own work. Instead, he says they discussed Buckmaster potentially becoming lead author of a rewrite of **OpenAI’s** proof, and that his comment about Alpöge’s Anthropic affiliation referred to authorship of OpenAI’s work. He also says he intended to suggest giving them access to OpenAI’s internal model, but the conversation ended before that proposal was made.

Regarding the alleged threat, Bubeck says Buckmaster threatened to go to the press with what Bubeck considered unfounded accusations. He says his “career” remark was intended as concern about Buckmaster damaging his career through those accusations, not as a threat, and says he retracted or apologized for the wording. [Bubeck’s public response](https://twiscan.com/en/x/SebastienBubeck/2097379411691516310)

**Alpöge’s response**

Alpöge’s public comments broadly support Buckmaster’s description of the atmosphere, though they remain another participant’s account rather than independent verification. He says:

- The collaboration was personal, not an Anthropic institutional project.
- He contacted OpenAI because he had information that the company knew about their work and had started a competing effort.
- He understood that a proposal had been made to remove him from a publication in connection with recognition or prize credit.
- He had been willing to cooperate with OpenAI and did not view the work as an Anthropic corporate initiative.
- He regarded the episode as an unnecessary corporate and credit conflict. [Alpöge’s comments as reported by Numerama](https://www.numerama.com/tech/2328733-controverse-autour-de-la-solution-navier-stokes-par-le-chercheur-danthropic-sort-du-silence.html)

**What is publicly supported**

The following points are relatively well supported because they appear in public documents from the participants themselves:

- Both groups published related fluid-dynamics results within days of each other.
- Buckmaster and Alpöge used OpenAI tools as well as Anthropic tools.
- OpenAI’s project was triggered, at least in part, by rumors about an outside breakthrough.
- OpenAI contacted them after its internal result was complete.
- OpenAI’s result concerns Navier–Stokes, while the pair’s published result concerns forced Euler and other related equations.
- Both accounts agree that publication and credit were discussed.

**What remains unresolved**

There is no public independent evidence establishing:

- that OpenAI accessed the pair’s private Codex prompts or drafts;
- that their private data influenced the internal model;
- that OpenAI copied an unpublished proof or technical idea rather than independently following the same earlier Córdoba–Martínez-Zoroa research direction;
- the exact words and meaning of the September 6 calls;
- whether Bubeck’s authorship proposal was an attempt to exclude Alpöge from his own work or a proposal for Buckmaster to rewrite OpenAI’s separate result;
- whether the alleged career remarks were threats, clumsy warnings, or both as interpreted by the participants.

The strongest current conclusion is therefore narrower: **OpenAI openly raced to pursue the problem after learning that outside researchers were making unusual progress, and the two sides give materially different accounts of the subsequent credit negotiations. The public record does not yet prove unauthorized data use or plagiarism, but it does establish a serious provenance and authorship dispute.**

## Turn 7

**Asker:** I’m still unsure how to think about priority when the proofs may differ. If OpenAI learned about an unpublished research direction and then independently completed a different proof using earlier public ideas, what would count as legitimate independent rediscovery rather than copying? What technical or documentary evidence could distinguish those cases, and how does the confidential timing affect the ethical judgment?

**Tutor:**

The key distinction is between **shared provenance** and **confidential appropriation**.

If OpenAI learned only that “another group may be close,” then used the public literature and developed its own proof, that can be legitimate independent rediscovery, even if the timing is uncomfortable. If it learned a distinctive unpublished lemma, construction, parameter choice, or proof strategy from private material and used that information, a different proof would not automatically make the conduct independent.

**What would count as independent rediscovery?**

Evidence would favor independence if:

- OpenAI’s first technical prompts and internal notes predate any contact or information about the researchers’ work;
- the route can be reconstructed from public papers alone;
- its proof uses genuinely different intermediate definitions, lemmas, invariants, and constructions;
- internal logs show no access to the researchers’ Codex sessions or drafts;
- the model’s relevant checkpoint or training data was isolated from those sessions;
- contemporaneous records show that the team’s key ideas arose before learning the confidential details.

A different final proof is relevant, but not decisive. In mathematics, two proofs can differ line by line while depending on the same unusual unpublished idea. Reviewers should compare the **mathematical dependency structure**, especially:

- unusual intermediate equations;
- distinctive ansätze or coordinate choices;
- non-obvious parameter regimes;
- specific cancellation mechanisms;
- the sequence of reductions;
- identical unexpected obstacles and solutions.

Sharing only the broad Córdoba–Martínez-Zoroa research lineage would be weak evidence of copying because that work was public and both groups openly identify it as an ancestor. Sharing a highly specific unpublished extension would be much stronger evidence.

**What evidence would favor copying?**

The strongest evidence would be provenance evidence, not merely textual similarity:

- immutable timestamps on internal drafts, agent prompts, and model outputs;
- access logs showing whether private Codex data was retrieved or exposed;
- training-data lineage and checkpoint dates;
- internal messages identifying the exact information OpenAI received;
- records of when the Navier–Stokes effort and its key prompts were launched;
- contemporaneous communications describing the researchers’ unpublished method;
- recordings, transcripts, or independent witnesses to the September calls.

Because these records are controlled by the parties, a neutral third-party audit under confidentiality would be far more probative than selective screenshots or retrospective explanations. The current public repositories are also limited evidence of discovery timing: public code can establish what was released, but not necessarily when each idea was developed internally. One technical review noted that both projects were published with little development history, leaving many dates dependent on participant testimony. [Stanford Tech Review’s comparison](https://stanfordtechreview.com/articles/openai-buckmaster-navier-stokes-lean-proofs)

**How the current public record fits**

Publicly established or directly documented:

- OpenAI says it began the effort after hearing rumors about major mathematical progress.
- OpenAI says it completed its own result before contacting Buckmaster and Alpöge.
- Buckmaster’s public statement documents his version of the calls, including his claim that OpenAI’s first prompt came after information about their work reached the company.
- OpenAI denies seeing their specific work before publication, while acknowledging that it cannot rule out de-identified user-derived data having influenced model improvement.
- The groups’ published results are not identical: Buckmaster and Alpöge published forced-Euler and related results, while OpenAI claims a forced-Navier–Stokes result and an unforced-Euler result. [OpenAI’s account](https://openai.com/index/navier-stokes-solution/) · [Buckmaster’s statement](https://cims.nyu.edu/~tristanb/statement.pdf)

Still unresolved:

- what information actually reached OpenAI before September 1;
- whether anyone accessed private Codex content;
- whether model training exposed the unpublished work;
- whether OpenAI’s technical route came from public predecessors or private details;
- the exact content and meaning of the authorship discussions;
- whether the “career” remarks were threats, warnings, or a disputed misunderstanding.

**Why confidentiality changes the ethical judgment**

Priority and plagiarism are not the same question.

If a researcher privately tells you, “I have a new proof using this unusual construction,” you may independently solve the problem afterward, but using that confidential construction without permission or credit is generally improper. The U.S. Office of Research Integrity describes unauthorized use of ideas or findings obtained through privileged communication as misappropriation, even when the copied material is an idea rather than text. [ORI policy on plagiarism](https://ori.hhs.gov/ori-policy-plagiarism)

By contrast, learning only that someone is working on a problem, or that a field may be close to a solution, does not reveal the solution itself. Racing them may be ethically ungenerous, especially if the information came through a collaborator or tool relationship, but it is not automatically plagiarism.

My current assessment is therefore:

**The public evidence establishes that OpenAI was prompted to enter the race by rumors about the outside work. It does not yet establish that OpenAI used the researchers’ unpublished technical content. The authorship dispute is supported by two participant accounts but remains a competing-account situation because the decisive communications and telemetry have not been independently disclosed.**

## Turn 8

**Asker:** Given that the provenance dispute is unresolved, how should I judge the mathematical claim itself today? What concrete signs would distinguish a merely difficult proof that needs ordinary peer review, a proof with a localized technical gap, and a fundamentally invalid construction? In other words, what evidence could make us reasonably confident before Clay’s long acceptance process is complete?

**Tutor:**

**My current judgment would be: a serious, formally instantiated claim that remains mathematically unconfirmed.** The public Lean artifact is meaningful evidence, but it is not yet the same as independent validation of the Navier–Stokes result.

**Three possible statuses**

**1. Difficult but credible proof**

This is the best-case interpretation. It would mean:

- the Lean theorem exactly matches Clay’s alternative C or D;
- a clean rebuild succeeds with pinned dependencies;
- no `sorryAx`, custom axioms, or unexplained compiler-trust mechanisms are used;
- independent experts can identify the key construction and verify its estimates;
- the remaining difficulty is mainly length, unfamiliarity, and exposition.

A 166-page proof can be entirely correct while still requiring months of ordinary expert review. Formal verification would make routine algebraic and logical mistakes much less likely, but not eliminate the need to understand the theorem being checked.

**2. Localized technical gap**

This would be a failure at a specific obligation without destroying the whole strategy. Likely examples would include:

- one exponent estimate failing at the singular endpoint;
- insufficient uniform control of derivatives of the residual force;
- a cutoff error that is smooth but not smooth enough;
- an incorrectly stated stress-realization lemma;
- a missing hypothesis in the uniqueness argument;
- the paper claiming a property that the Lean theorem does not actually establish.

A localized gap is credible when reviewers can point to one precise step, explain exactly what fails, and show that a standard repair would fix it without changing the central construction.

If the Lean formalization genuinely covers that step with no admitted assumptions, then a missing explanation in the prose may be only a presentation defect. The important question is whether the formal theorem still proves the required claim.

**3. Fundamentally invalid construction**

Warning signs would include:

- the formal theorem proves a weaker statement than Clay’s C/D;
- the equation is modified, forced in an impermissible way, or posed on the wrong domain;
- the “smooth force” fails to extend through the singular time;
- the constructed field solves only an approximate or distributional equation;
- bounded \(L^2\) energy or \(L^\infty\) blow-up is asserted but not actually established;
- a crucial conclusion is imported as an axiom or hidden `sorry`;
- the construction depends circularly on the singular solution rather than on a prescribed \(f(x,t)\);
- the local blow-up solution is not shown to rule out every admissible global smooth solution.

These are not ordinary missing details. They change the theorem’s meaning or break its central mechanism.

**What would raise confidence now**

I would look for four independent layers of evidence:

1. **Formal audit:** clean rebuild, `#print axioms` on the top-level theorem, `lean4checker --fresh`, and an independent checker such as Comparator or `nanoda`.

2. **Statement audit:** a line-by-line map from the Lean theorem to Clay C/D, including domain, force regularity, initial data, pressure, incompressibility, energy, and the precise blow-up norm.

3. **Analytic audit:** independent experts checking the high-risk parts:
   - the self-similar vortex estimates;
   - the oscillatory pulse construction;
   - cancellation of the residual to all orders;
   - smooth extension of the force through \(t=1\);
   - bounded-energy estimates;
   - the uniqueness argument that excludes a competing global solution.

4. **Reproducibility and criticism:** independent groups reproduce the formal build, publish specific objections, and see whether OpenAI can answer them with corrected statements or proofs. A human-readable simplification of the central estimates would be especially valuable.

The public repository and the claimed formalization are positive evidence. One public inspection reported no extra axioms in the main developments, but also noted that the repositories contain little development history and that the mathematical claim had not yet received independent expert verification. [OpenAI’s formalization repository](https://github.com/openai/NavierStokesAndEuler) · [public technical audit](https://stanfordtechreview.com/articles/openai-buckmaster-navier-stokes-lean-proofs)

So, before Clay’s process finishes, it would be reasonable to become **substantially confident** if the theorem statement is independently confirmed, the formal artifact passes an isolated external replay, and several fluid analysts verify the core estimates. Until then, the appropriate label is not “probably false” or “solved,” but **a high-significance candidate result whose formal plumbing is promising and whose mathematical interpretation and construction still await independent scrutiny**.

## Turn 9

**Asker:** There is one logical step I want to pin down: why does constructing a solution that blows up prove that **no** global smooth solution exists for the same initial data and force? Could there be another smooth solution that follows a different path? Is the argument that smooth solutions are unique before \(t=1\), so any hypothetical global one must coincide with the constructed solution until blow-up, and where exactly does that uniqueness argument enter?

**Tutor:**

Yes, that is exactly the logic. The crucial point is **uniqueness on every interval strictly before \(t=1\)**.

Let \((u,p)\) be the constructed solution on \([0,1)\), and suppose \((v,P)\) were another global smooth solution with the same force \(f\), same initial data, and the admissibility conditions required by Clay.

Fix any \(T<1\), and define

\[
w=v-u,\qquad \pi=P-p.
\]

Subtracting the two Navier–Stokes systems cancels the common force:

\[
\partial_t w+(v\cdot\nabla)w+(w\cdot\nabla)u
-\nu\Delta w+\nabla\pi=0,
\qquad \nabla\cdot w=0,
\]

with

\[
w(\cdot,0)=0.
\]

For smooth periodic solutions, multiply by \(w\) and integrate. The transport and pressure terms vanish because both fields are divergence-free. One obtains

\[
\frac12\frac{d}{dt}\|w(t)\|_2^2
+\nu\|\nabla w(t)\|_2^2
\leq \|\nabla u(t)\|_\infty\|w(t)\|_2^2.
\]

Since \(u\) is smooth on the closed interval \([0,T]\), \(\|\nabla u\|_\infty\) is bounded there. Grönwall’s inequality and \(w(0)=0\) therefore imply

\[
\|w(t)\|_2^2=0
\]

for every \(t\leq T\). Hence \(v=u\) on \([0,T]\).

Because \(T<1\) was arbitrary,

\[
v=u\qquad\text{for every }0\leq t<1.
\]

But the constructed solution has points \(x_t\to0\) for which

\[
|u(x_t,t)|\to\infty\quad\text{as }t\uparrow1.
\]

Therefore \(v\) has the same blow-up. That contradicts the assumption that \(v\) is smooth at \(t=1\): a smooth function is locally bounded, whereas \(v\) would become unbounded in every neighborhood just before \(t=1\).

**On \(\mathbb R^3\), there is an extra technical issue.** One cannot simply integrate over all space and discard the pressure term without checking decay and boundary fluxes. The paper’s Lemma 10.5 handles this by:

- comparing the two solutions on expanding balls;
- reconstructing the pressure gradient using Riesz transforms;
- using the \(L^2\) energy bound to control the difference;
- showing the boundary errors vanish as the ball radius tends to infinity;
- applying Grönwall.

The lemma concludes that any smooth \(L^2\)-bounded competitor with the same force and zero initial data agrees with the constructed solution on every \([0,T]\), \(T<1\). The paper then uses that equality to derive the contradiction. [OpenAI’s Lemma 10.5 and proof of Theorem 1.1](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)

Two qualifications matter:

- This excludes another **admissible smooth solution**, not every conceivable weak or infinite-energy solution.
- A weak solution might not satisfy the regularity needed for the difference estimate, so uniqueness can fail in weaker classes. That does not evade Clay’s C/D alternatives, which concern global smooth physically reasonable solutions.

So the structure is:

\[
\text{same data and force}
\;+\;
\text{smooth uniqueness before }1
\;\Longrightarrow\;
\text{same solution before }1
\;\Longrightarrow\;
\text{same blow-up}
\;\Longrightarrow\;
\text{no global admissible smooth continuation}.
\]

## Turn 10

**Asker:** I now understand why uniqueness turns one blow-up solution into nonexistence of a global smooth one, but I still don’t understand the construction’s central trick. How can rapidly oscillating correction fields have a controlled quadratic average that cancels the singular residual of the background vortex, while the corrections themselves remain compatible with divergence-free flow and bounded energy? What exactly is the “stress defect” in this argument?

**Tutor:**

The central mechanism is a **Reynolds-stress-style cancellation**.

For a divergence-free velocity,

\[
(u\cdot\nabla)u=\nabla\cdot(u\otimes u).
\]

So the nonlinear term is itself the divergence of a quadratic momentum flux.

**1. The background has a stress defect**

OpenAI first constructs a concentrating background flow \((u_B,p_B)\) with the desired velocity blow-up. It is not yet an exact Navier–Stokes solution. Its residual is

\[
R_B
=
\partial_tu_B+\nabla\cdot(u_B\otimes u_B)
-\nu\Delta u_B+\nabla p_B.
\]

Near the shrinking vortex annulus, this residual becomes singular. The construction rewrites its leading part schematically as

\[
R_B=-\nabla\cdot T+r,
\]

where \(T\) is the **stress defect** and \(r\) is a much smaller remainder.

The tensor \(T\) is not an additional physical force. It records the momentum flux missing from the approximate background flow. If one could add a correction \(w\) satisfying

\[
\nabla\cdot\langle w\otimes w\rangle
\approx
\nabla\cdot T,
\]

then the leading singular residual would cancel.

**2. Why zero-mean oscillations have nonzero quadratic effect**

Take a simple divergence-free plane wave

\[
w_k(x)=a\cos(k\cdot x),
\qquad a\cdot k=0.
\]

Then

\[
\langle w_k\rangle=0,
\]

but

\[
\langle w_k\otimes w_k\rangle
=
\frac12 a\otimes a\neq0.
\]

Thus the oscillation disappears in linear averages but survives quadratically. This is the essential nonlinear effect:

\[
w_k\rightharpoonup0,
\qquad
w_k\otimes w_k\rightharpoonup Q\neq0.
\]

With several wave directions and carefully chosen amplitudes, the average covariance can approximate a desired stress. The construction cannot realize an arbitrary tensor for free, so the background is designed so that its required defect lies in an “admissible stress cone” generated by the available pulse families. [OpenAI’s proof](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)

**3. Why the stress has a nonzero divergence**

A constant-amplitude wave has constant average stress, whose divergence is zero. The actual pulses therefore have slowly varying envelopes, locations, orientations, and amplitudes. Their averaged flux varies across the annulus, producing

\[
\nabla\cdot\langle w\otimes w\rangle.
\]

That spatial variation supplies the missing momentum transport. In the paper’s description, one pulse family transports angular momentum and another transports axial momentum in different proportions. Their positive amplitude weights are selected to match the two components of the defect.

**4. How incompressibility is preserved**

Simply multiplying a plane wave by a cutoff would generally create nonzero divergence. The construction instead builds the pulses from vector potentials:

\[
w=\nabla\times A_{\text{wave}},
\]

so

\[
\nabla\cdot w=0
\]

identically. Localized ring geometry, phase choices, and additional corrections are then used to control the errors caused by the envelopes and coordinate changes.

The oscillations are also arranged to have zero angular or local mean, so they do not replace the leading concentrating vortex. Their main effect is through their quadratic momentum flux.

**5. Why the energy can remain bounded**

If a correction has amplitude \(A\) and occupies volume \(V\), its energy is roughly

\[
\int |w|^2\,dx\sim A^2V.
\]

Its local stress is of size \(A^2\), but its total energy includes the shrinking volume \(V\). Therefore a large local momentum flux can coexist with finite total energy.

The same concentration principle applies to the background vortex. In the claimed construction,

\[
|u_B|\sim \tau^{-1/2-h},
\qquad
V\sim\tau^{3/2-h},
\]

so

\[
\int |u_B|^2\,dx
\sim
\tau^{1/2-3h},
\]

which stays bounded for sufficiently small \(h\), even though the pointwise velocity diverges.

High frequency does create large derivatives, so energy control alone is not enough. The pulses are seeded very weakly, amplified by background shear, and eventually damped by viscosity as their wavelength becomes too short. The correction stages are arranged so that the full velocity retains bounded \(L^2\) energy and finite integrated dissipation.

**6. Why this is not automatically a solution**

The first oscillatory average only cancels the leading defect. It also creates new oscillatory errors, cutoff errors, pressure errors, and higher-order residuals. The proof must recursively correct these so that the final residual

\[
f=
\partial_tu+\nabla\cdot(u\otimes u)
-\nu\Delta u+\nabla p
\]

extends smoothly through the singular time.

So the central claim is not merely that “waves average to a stress.” It is that the authors can:

1. realize the required stress with divergence-free pulses;
2. keep their energy controlled;
3. cancel every dangerous residual order;
4. preserve the leading velocity blow-up;
5. leave behind a genuinely smooth prescribed force.

That last chain of estimates is the substantive proof burden. The construction is conceptually related to Reynolds-stress and convex-integration methods, but whether all of its Navier–Stokes estimates close remains a matter for independent mathematical review.

## Turn 11

**Asker:** The averaging argument makes sense only at a coarse scale, but Navier–Stokes is a pointwise differential equation. How does the recursive correction scheme control the leftover high-frequency errors pointwise, especially since viscosity contributes \(\nu\Delta w\sim \nu k^2w\) and therefore becomes very large as the oscillation frequency \(k\) increases? Why doesn’t viscosity destroy the stress-cancellation mechanism?

**Tutor:**

The averaging is only the first step. The construction also solves the leading **pointwise oscillatory equation** for each Fourier mode, then estimates everything left over.

**1. Viscosity is included in the leading wave equation**

For a pulse of the schematic form

\[
w=a(x,t)e^{ik\Phi(x,t)},
\]

the viscous term contains

\[
\nu\Delta w
\approx
-\nu k^2|\nabla\Phi|^2w
\]

plus lower-order envelope and phase-derivative terms.

The construction does not pretend this term is small. In the paper’s normalized variables, the carrier frequency is chosen so that

\[
\varepsilon k^2\sim 1,
\]

meaning viscosity remains in the principal amplitude equation rather than becoming an uncontrolled error. The mode amplitude satisfies an equation schematically like

\[
\frac{d a}{ds}
=
\bigl(\text{shear amplification}
-\text{viscous damping}\bigr)a
+\text{source}.
\]

The paper’s actual equation includes a damping coefficient of the form

\[
d=\varepsilon k^2|\nabla\Phi|^2.
\]

[See the pulse construction in the paper.](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)

**2. The pulse is designed to grow, then die**

Initially, background shear is chosen to dominate viscous damping, so the pulse amplifies enough to produce the desired quadratic momentum flux.

But shear also distorts the phase and increases the effective wave number. Eventually,

\[
\nu k^2|\nabla\Phi|^2
\]

becomes larger than the shear growth rate, and the pulse decays. Thus the pulse is not expected to survive with large amplitude all the way to the singular time. It is a controlled transient whose integrated effect supplies the required stress.

This is why increasing frequency is not automatically fatal: frequency simultaneously strengthens the desired scale separation and the damping, and the amplitude equation explicitly tracks both effects.

**3. How pointwise errors are controlled**

Write the residual of the current approximation as

\[
R(u,p)
=
\partial_tu+\nabla\cdot(u\otimes u)
-\nu\Delta u+\nabla p.
\]

At each correction stage, the residual is decomposed into parts:

- nonzero oscillatory Fourier modes;
- averaged tangential errors;
- mean-flow and pressure errors;
- a finite set of radial moment defects;
- already-flat remainders.

For each oscillatory mode, the construction solves an inhomogeneous amplitude-pressure system whose principal part cancels that mode. The remaining terms include:

- derivatives of the envelope;
- imperfect phase transport;
- curl corrections;
- viscous terms not included in the principal operator;
- interactions with older waves;
- quadratic self-interactions.

These are not discarded by averaging. They are estimated pointwise in the relevant rescaled coordinates and passed to the next correction stage.

The paper describes a four-step cycle:

1. cancel the supported oscillatory harmonics;
2. adjust wave amplitudes to correct the averaged stress;
3. correct the zero-mean part of the residual;
4. repair a finite number of mean and moment defects.

After each full cycle, the claimed residual order improves by a fixed positive amount, written in the paper as

\[
B_{j+1}=B_j+\frac{1}{10},
\qquad
C^*_{j+1}=C^*_j+\frac{1}{10}.
\]

The corrections are then summed so that, for every fixed Cartesian derivative order and every \(N\),

\[
\left|
\partial_x^\alpha\partial_t^bR(u,p)
\right|
\leq C_{\alpha,b,N}q^N
\]

near the singular point. This is “flatness”: the residual and all its fixed-order derivatives vanish faster than every prescribed power of the small scale \(q\). [The paper’s residual-improvement section](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)

**4. Why divergence-free structure survives**

The pulse velocity is generated from a vector potential, schematically

\[
w=\nabla\times A.
\]

Therefore

\[
\nabla\cdot w=0
\]

identically, including after localization. The curl operation creates additional correction terms, but those terms are explicitly estimated and included in the next residual stage.

**5. The essential balance**

The mechanism is therefore not

\[
\text{“high frequency averages away, so viscosity does not matter.”}
\]

It is closer to

\[
\begin{aligned}
&\text{choose the phase and frequency;}\\
&\text{solve the viscous amplitude equation;}\\
&\text{use the growing pulse to generate quadratic stress;}\\
&\text{let viscosity damp it when the wave becomes too fine;}\\
&\text{correct the newly generated errors recursively.}
\end{aligned}
\]

The hard claim is that all of those operations can be made compatible simultaneously: exact incompressibility, the required stress, viscous damping, bounded energy, and pointwise flatness of the final residual. That is the central analytic burden still requiring independent verification.

## Turn 12

**Asker:** I want to understand the final passage from infinitely many approximate corrections to a genuine smooth force. Why does “flatness” of the residual in the rescaled variable \(q\) imply that the residual extends as a \(C^\infty\) function in the original \((x,t)\) coordinates across \(t=1\)? In particular, how do we know that taking \(\partial_t u\) does not leave a delta-like or otherwise nonsmooth term at the blow-up time?

**Tutor:**

There are two different regularity claims here:

1. The velocity \(u\) becomes singular at \(t=1\).
2. The **residual force**
   \[
   f=\partial_tu+(u\cdot\nabla)u-\nu\Delta u+\nabla p
   \]
   extends smoothly through \(t=1\).

The construction claims the second, not the first.

**Why flatness in \(q\) is strong enough**

The relevant estimate is not merely

\[
R=O(q^N)
\]

for the residual itself. The paper claims that for every Cartesian derivative order \(\alpha,j\) and every \(N\),

\[
\left|
\partial_x^\alpha\partial_t^j R(x,t)
\right|
\le C_{\alpha,j,N}q(x,t)^N.
\]

This is important because \(q=q(z,t)\) is a singular rescaled coordinate: its own derivatives can become large near \((z,t)=(0,1)\). The proof claims to account for those chain-rule losses before stating the estimate in original Cartesian \((x,t)\) derivatives.

Since \(q\to0\) only at the singular point, this implies

\[
\partial_x^\alpha\partial_t^jR(x,t)\to0
\]

faster than every power as \((x,t)\to(0,1)\). Thus the residual has a compatible zero jet at the singular point. One can define its value and all derivatives there to be zero.

A standard one-dimensional analogy is

\[
r(t)=
\begin{cases}
e^{-1/(1-t)^2},&t<1,\\
0,&t\ge1.
\end{cases}
\]

Although derivatives of \(e^{-1/(1-t)^2}\) contain negative powers of \(1-t\), the exponential dominates every such power. Every derivative tends to zero, so the zero extension is \(C^\infty\).

**Why the infinitely many corrections can be summed**

The correction terms are multiplied by cutoffs such as

\[
\chi(a_jq),
\qquad a_j\to\infty.
\]

For any fixed \(q>0\), only finitely many terms remain nonzero, so the sum is locally finite away from the singular point. Near \(q=0\), the \(j\)-th correction has increasingly high vanishing order. The scales \(a_j\) are chosen so that, for every fixed derivative order, its contribution is summable.

The result is:

- \(u\) and \(p\) are smooth for \(t<1\);
- their residual has arbitrarily high decay in \(q\);
- every fixed Cartesian derivative of the residual has a limit at \(t=1\).

This is the role of the summation and residual-improvement lemmas. [Summation argument](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf#page=114)

**What happens away from the singular point**

At \(t=1\) and \(x\neq0\), the rescaled core is no longer collapsing onto the point. The paper treats that region separately using the smooth endpoint behavior of the exterior heat-flow solution and the spatial cutoffs.

Thus the argument has two pieces:

- near \((0,1)\): flatness in \(q\);
- away from \((0,1)\): ordinary one-sided smooth bounds.

Together these give limiting functions \(F_j(x)\) satisfying

\[
\lim_{t\uparrow1}\partial_t^j f(x,t)=F_j(x),
\]

with all spatial derivatives converging compatibly. [Lemma 10.2](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf#page=118)

For \(t>1\), the paper does **not** simply set \(f=0\), because \(f\) may have a nonzero limiting value away from the origin. Instead it constructs a Taylor-type extension:

\[
f(x,1+\sigma)
=
\sum_{j\ge0}
\chi_j(\sigma)\frac{\sigma^j}{j!}F_j(x),
\]

with shrinking time cutoffs \(\chi_j\). The one-sided jets match at \(t=1\), so the resulting force is \(C^\infty\). [Lemma 10.3](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf#page=119)

**What about a delta term in \(\partial_tu\)?**

The important correction is: **flatness does not show that \(\partial_tu\) itself is smooth.** In fact, \(\partial_tu\), \((u\cdot\nabla)u\), and \(\Delta u\) may each become very large or fail to have finite limits.

The claim is only that their combination has a smooth residual:

\[
\partial_tu+(u\cdot\nabla)u-\nu\Delta u+\nabla p=f.
\]

The construction never extends \(u\) smoothly through \(t=1\). Therefore it does not claim that the singular velocity defines a global classical solution, or even that an arbitrary extension of \(u\) would have no distributional defect at \(t=1\).

A delta in a time derivative arises when a field is patched across a jump. The force avoids that problem because it is extended separately with all time derivatives matched. But if one tried to patch the singular \(u\) itself across \(t=1\), additional distributional issues could arise. Those are outside the theorem’s claim.

So the precise conclusion is:

> The singular terms in the equation are not individually regularized. Their residual is shown, under the claimed estimates, to have a smooth extension. The equation is exact before \(t=1\); the force is smoothly continued afterward, while the velocity is intentionally not.

## Turn 13

**Asker:** If the constructed velocity exists only for \(t<1\), while the force is extended independently for \(t\ge1\), how exactly does that fit Clay’s global-in-time formulation? Is it enough to exhibit a local smooth solution that blows up, provided uniqueness rules out another global one, and why does the arbitrary post-\(1\) extension of \(f\) preserve all the required decay or periodicity conditions?

**Tutor:**

Yes. A local solution on \(0\le t<1\) is sufficient **if** it proves that no admissible global smooth solution can exist.

Clay’s alternative C has the logical form

\[
\exists u_0\;\exists f\in\mathcal A
\quad\text{such that}\quad
\text{no global admissible smooth }(u,p)\text{ exists}.
\]

It does not require the witness \(u\) used in the proof to continue past its blow-up time. The force \(f\), however, must be defined for all \(t\ge0\).

The argument is:

1. Construct \(u_-,p_-\) solving the equation exactly on \([0,1)\).
2. Show \(u_-\) becomes unbounded as \(t\uparrow1\).
3. Extend the residual force \(f\) smoothly to \(t\ge1\).
4. Assume a global smooth solution \(v,P\) exists for the same \(u_0\) and full force \(f\).
5. For every \(T<1\), compare \(v,P\) with \(u_-,p_-\) on \([0,T]\).
6. Smooth uniqueness gives \(v=u_-\) on \([0,T]\).
7. Since this holds for every \(T<1\), \(v=u_-\) for all \(t<1\), so \(v\) must also blow up as \(t\uparrow1\), contradicting smoothness at \(t=1\).

This is analogous to the ODE

\[
x'=x^2,\qquad x(0)=1,
\]

whose solution \(x(t)=1/(1-t)\) exists only before \(t=1\). ODE uniqueness means any hypothetical global solution would have to equal it before \(1\), which is impossible.

**The post-\(1\) force is not completely arbitrary.**

For \(t<1\), the paper defines

\[
f_-(x,t)=
\partial_tu_-+(u_-\cdot\nabla)u_-
-\nu\Delta u_-+\nabla p_-.
\]

Near the singular point, flatness is claimed in the stronger Cartesian sense:

\[
|\partial_x^\alpha\partial_t^j f_-(x,t)|
\le C_{\alpha,j,N}q(x,t)^N
\]

for every \(N\). Away from the singular point, the exterior flow supplies ordinary one-sided smooth limits. Consequently, for every \(j\), the time derivative \(\partial_t^j f_-\) has a smooth spatial limit \(F_j(x)\) as \(t\uparrow1\).

For \(t>1\), the authors use those \(F_j\) as the Taylor jet of a new function, schematically

\[
f_+(x,1+\sigma)
=
\sum_{j\ge0}
\chi_j(\sigma)\frac{\sigma^j}{j!}F_j(x),
\]

where the cutoffs \(\chi_j\) shrink rapidly with \(j\). Thus \(f_+\) matches every time derivative of \(f_-\) at \(t=1\), making

\[
f(x,t)=
\begin{cases}
f_-(x,t),&t<1,\\
f_+(x,t),&t\ge1
\end{cases}
\]

a \(C^\infty\) function. This matching is what prevents a jump or delta term in the force itself. [OpenAI’s Lemmas 10.2 and 10.3](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf#page=118)

The extension does **not** make \(u_-\) smooth after \(t=1\), nor does it claim that \(\partial_tu_-\) individually has a regular extension. The equation is required for the constructed fields only before \(t=1\). The post-\(1\) force merely completes the globally defined input \(f\) required by Clay.

**Why the admissibility conditions survive**

- In \(\mathbb R^3\), the extended force is claimed to be compactly supported in both space and time, for example inside \(K\times[0,2]\). A smooth compactly supported function automatically satisfies Clay’s rapid-decay estimates.
- On \(\mathbb T^3\), the compactly supported construction is spatially rescaled to fit inside a fundamental cell and then periodized. Because the copies are separated, the periodized force is smooth and periodic.
- Compact time support also makes the required time-decay estimates automatic.

So the post-\(1\) extension cannot rescue a hypothetical global solution: that solution is already forced to coincide with the singular one on every interval \(t<1\). The extension only ensures that the force satisfies Clay’s global-in-time hypotheses.

## Turn 14

**Asker:** Have independent mathematicians actually identified a concrete flaw in the claimed construction, or is the present skepticism mainly that it has not yet been independently checked? How should I distinguish “unverified,” “probably wrong,” and “disproved” here, especially when a 166-page proof is difficult to audit and no decisive public counterexample has appeared?

**Tutor:**

As of September 9, 2026, I have found **no publicly documented, concrete mathematical flaw** in OpenAI’s Navier–Stokes construction. The public status is better described as **unverified**, not “probably wrong” and certainly not “disproved.” A specialist discussion and an independent evidence-tracking record both describe the result as awaiting expert examination rather than reporting a failed step. [MathOverflow discussion](https://mathoverflow.net/questions/515056/proof-outline-and-discussion-openais-claimed-forced-blowup-construction-for-na) · [State of Proof record](https://stateofproof.org/)

**The distinctions**

**Unverified** means:

- no independent mathematician has checked the whole argument;
- no decisive counterargument has been published;
- the claim remains logically open from the public evidence.

That is the current status. The paper and Lean artifact are evidence that OpenAI has made a serious, checkable submission, not evidence that the construction is correct.

**Probably wrong** is a probabilistic judgment. It would become reasonable if independent reviewers found several failures such as:

- the same key estimate failing repeatedly;
- a required exponent inequality being impossible;
- the force not actually smooth at the singular time;
- the stress-cancellation mechanism working only after discarding an uncontrolled term;
- the construction depending on an unstated assumption;
- different reviewers independently finding that the formal theorem is materially weaker than the paper.

A single unexplained difficulty is not enough. Proofs at this scale often contain notation problems, missing explanations, or repairable estimates.

**Disproved** is stronger. It means the mathematical proposition itself is false, not merely that the submitted proof is flawed.

For example:

- Showing that the displayed \(u,p,f\) fail to satisfy the equation would disprove OpenAI’s proposed construction.
- It would **not** prove that some other forced blow-up construction cannot exist.
- Showing that one lemma is false would invalidate the proof unless repaired, but would not by itself disprove the Clay alternative.

This distinction is especially important for an existential theorem. A defective witness is not the same as a proof that no valid witness exists.

**What concrete positive evidence would look like**

The most convincing pre-Clay evidence would be layered:

1. **Formal reproducibility.**  
   An independent group rebuilds the exact repository and verifies the claimed top-level theorem with pinned Lean and Mathlib versions, external checking, and a clean axiom audit. The OpenAI repository makes this possible, but a successful build only establishes the formal proposition encoded there. [Formalization repository](https://github.com/openai/NavierStokesAndEuler)

2. **Statement correspondence.**  
   Experts verify that the Lean theorem exactly matches Clay’s C/D alternatives: the correct Navier–Stokes equation, domain, smooth force, initial data, bounded energy, and breakdown conclusion.

3. **Independent analytic checking.**  
   Fluid analysts verify the genuinely delicate components:
   - the self-similar background;
   - the stress decomposition;
   - the viscous pulse equations;
   - the all-orders residual estimates;
   - smooth extension of the force;
   - the uniqueness argument excluding a global competitor.

4. **Independent reconstruction of the core.**  
   At least one group rederives the central cancellation and scaling estimates in ordinary mathematical language, without relying only on the authors’ generated code.

5. **Stable responses to criticism.**  
   OpenAI publishes versioned corrections, clarifies any changed hypotheses, and independent reviewers confirm that the fixes do not alter the theorem.

**What would be genuinely alarming**

The strongest warning would be a reproducible failure in a central obligation, such as:

\[
\partial_x^\alpha\partial_t^j f
\]

not remaining bounded at \(t=1\), or the leading stress cancellation leaving a term of the same singular order as the original defect. Another serious sign would be that the Lean code proves a surrogate theorem while the paper silently uses a stronger one.

Conversely, the absence of a public flaw means only that nobody has yet exposed one. It is not evidence that the proof is correct. With a 166-page argument, the sensible position is:

> **Treat it as a serious candidate proof with unusually strong formal infrastructure, but with mathematical validity still unsettled. Do not upgrade it to “probably wrong” without a concrete failed obligation, and do not call it “disproved” unless the theorem itself, rather than merely its current proof, has been refuted.**

## Asker final understanding

I understand the claim as a specially forced, finite-energy 3D Navier–Stokes flow whose velocity blows up locally in finite time, not as a proof that ordinary unforced fluids blow up.

The construction relies on concentrating a vortex and using divergence-free oscillatory corrections whose quadratic stress cancels the singular residual; viscosity is included in the pulse dynamics. Smooth uniqueness before the blow-up time then rules out any alternative global smooth solution.

Lean strongly checks the encoded derivation, but humans must still verify the exact theorem statement, assumptions, dependencies, and analytic construction. The current evidence supports “serious candidate proof, not yet independently confirmed,” rather than “probably wrong” or “disproved.”

The controversy concerns priority, possible private-data influence, authorship, and conduct. Public accounts support that OpenAI learned of related unpublished work and pursued the problem, but do not establish copying, unauthorized access, or model-training use. The exact call contents, provenance of technical ideas, and authorship dispute remain unresolved.
