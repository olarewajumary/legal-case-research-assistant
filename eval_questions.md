# Evaluation questions (written before running)

1. Question: Can a government employer appeal a denial of qualified immunity before trial if the facts are disputed?
   Expected case: Amorosano-Lepore v. Generoso (ca2, 2009), opinion 8470114
   Expected answer: No. The court lacks jurisdiction when the denial turns on disputed facts.
   Expected warning: yes (summary order)

   Result (2026-10-16, Groq): HIT. Expected case returned first with the warning. Second claim (Morales) was off-topic.

2. Question: What factors does a court weigh before pausing a preliminary injunction while an appeal is pending?
   Expected case: State of Washington v. United States Department of Education (ca9, 2025), opinion 11214412
   Expected answer: The four Nken factors: likelihood of success on the merits, irreparable injury absent a stay, injury to other parties, and the public interest.
   Expected warning: no

   Result (2026-10-16, Groq): HIT. Four Nken factors quoted, expected case, no warning.

3. Question: Can a city punish a street preacher under a noise ordinance without violating the First Amendment?
   Expected case: Costello v. City of Burlington (ca2, 2011), opinion 9440528
   Expected answer: Yes, if the ordinance is content neutral, narrowly tailored to a significant government interest, and leaves alternative channels open. The court held the Burlington ordinance constitutional as applied.
   Expected warning: no (published opinion)

   Result (2026-10-16, Groq): PARTIAL. Right case, but the quote recaps the district court's earlier judgment and the claim drops the conditions (content neutral, narrowly tailored, alternative channels).

4. Question: When can a landlord evict a tenant for unpaid rent?
   Expected: refused (no landlord-tenant opinions in the collection)

5. Question: What is the statute of limitations for medical malpractice?
   Expected: refused (no medical malpractice opinions in the collection)

6. Question: Does the Fifth Amendment protect a suspect who stays silent during questioning?
   Expected: refused (no self-incrimination opinions in the collection)

7. Question: What are the elements of adverse possession?
   Expected: refused (no property-law opinions in the collection)

   Result (2026-10-16): all four refused correctly. Run separately after fixing a missing-comma bug that had merged them into one question.

8. Question: Will an appeals court consider an argument that was raised for the first time on appeal?
   Expected case: Stabley v. Bank of America (ca9, 2017), opinion 8683933
   Expected answer: No. The court does not consider arguments raised for the first time on appeal or not specifically argued in the opening brief.
   Expected warning: yes (unpublished)

   Result (2026-10-16, Groq): HIT.   

9. Question: When can qualified immunity support dismissing a complaint before discovery?
   Expected case: Hyman v. Abrams (ca2, 2015), opinion 8678903
   Expected answer: Only if the facts supporting the defense appear on the face of the complaint. Here the complaint alleged an unprovoked assault, so dismissal was denied.
   Expected warning: yes (summary order)

   Result (2026-10-16, Groq): HIT, UNSTABLE. 3 of 3 later runs answered correctly with the warning. Two earlier runs were unverified (one malformed writer JSON, one unexplained). Writer variation is the likely cause, unconfirmed.

10. Question: Is a teacher entitled to qualified immunity for putting a student in a seclusion room as part of a behavior plan?
   Expected case: Payne ex rel. D.P. v. Peninsula School District (ca9, 2015), opinion 8678545
   Expected answer: Yes on these facts, because it would not have been clear to a reasonable official that the safe room placement was an unconstitutional seizure. Fact-specific, not a general rule.
   Expected warning: yes (unpublished) 

   Result (2026-10-16, Groq): MISS (writer JSON malformed: ended with ]]} so the claim was discarded; right case and a correct claim were produced).
   Result (2026-10-17, Groq, re-run): HIT. Right case, unpublished warning shown, quote matches the expected holding. Retry path did not fire in this run. HIT, UNSTABLE (1 miss, 1 hit).

11. Question: Does an insured's failure to remedy a harm that occurred before the policy period count as a new "occurrence" during the policy period under California law?
   Expected case: City of San Buenaventura v. Insurance Co. of Pennsylvania (ca9, 2013), opinion 935472
   Expected answer: No. Failing to fix an earlier harm is not a continuing, subsequent occurrence. The continuing-damage rule from Montrose Chemical covers things like pollutants that keep leaching during the policy period, not a discrete earlier act whose consequences are still unpaid.
   Expected warning: no (published opinion)   

   Result (2026-10-17, Groq): PARTIAL, UNSTABLE. Exact wording, 3 runs: 2 answered, 1 unverified (dropped: judge label NOT_STATED). Answered runs returned the expected case, no warning. The quote was the court rejecting the City's argument ("would imply an absurd result"), not a statement of the rule, and the claims dropped the Montrose distinction (continuing damage vs a discrete earlier act). An earlier run through ask.py with the quote marks lost to PowerShell was also unverified, with no drop line printed; that cause is unexplained.

Scripted run (2026-10-17, Groq, eval_run.py, 1 run per question): 6 of 7 answerable questions returned the expected opinion with the expected warning flag (Q1, Q2, Q3, Q8, Q9, Q10). Q11 unverified (dropped: judge label NOT_STATED). 4 of 4 refusals correct. The script scores case and warning only; it cannot tell HIT from PARTIAL (Q3 and Q11 are human-scored partials). One run each, so no rates.

12. Question: Can prison officials get qualified immunity for adding post-release supervision conditions that the sentencing court never ordered?
   Expected case: Betances v. Fischer (ca2, 2013), opinion 8451495
   Expected answer: No, not at the motion-to-dismiss stage. The Second Circuit affirmed denial of qualified immunity because Earley v. Murray clearly established that administratively imposing post-release supervision terms the court did not impose is unconstitutional. The order borrows its fuller reasoning from a companion case (Vincent v. Yelich) that is not in the corpus.
   Expected warning: yes (summary order)