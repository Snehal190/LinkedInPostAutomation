---
name: meera-linkedin-post-qualifier
description: Decide whether a raw thought, note or voice memo from Meera Pillai (founder of Skinstinct) deserves to become a LinkedIn post. Use this whenever the user shares one or more of Meera's thoughts, notes, ideas or observations and asks whether to post them, which to post, which to prioritise, or to filter/score/evaluate post ideas. Run this BEFORE drafting any LinkedIn post with the meera-pillai-voice skill.
---

# Meera LinkedIn Post Qualifier

## Purpose
Meera's LinkedIn exists to build the Skinstinct brand: a founder with pharmaceutical formulation discipline who holds skincare to documentation standards most brands skip, and who is honest about what she knows, what she got wrong, and what she hasn't solved. Not every thought serves that. This rubric decides which thoughts do.

## Decision rule
- Score each thought on the 8 metrics below. Each metric is PASS (1) or FAIL (0). No half points.
- 5 or more out of 8 = QUALIFIES. The thought becomes a LinkedIn post.
- 4 or fewer = DISCARD for LinkedIn. (Suggest the newsletter if it is consumer education.)
- Before scoring, run the hard stops. Any hard stop = DISCARD regardless of score, unless the issue can be removed without losing the point of the post.
- When several thoughts qualify, rank by score. Tie-break in this order: metric 2 (Only Meera could say it), then metric 5 (Honesty signal), then metric 8 (Professional relevance).

## Hard stops (check first)
1. Needs invented data: the post only works with figures, test results or facts Meera has not provided.
2. It is a pitch: the point is to sell, announce stock or promote a product.
3. Names or attacks a specific supplier, manufacturer, competitor or person. (The same point made about the practice, anonymously, is fine.)
4. Requires a medical or diagnostic claim.

## The 8 metrics

### 1. Reinforces a brand pillar
PASS if the thought strengthens at least one thing Skinstinct stands for:
- documentation and verification over trust (CoA, pH, stability, spec sheets)
- formulation quality over ingredient lists and label claims
- honest, calibrated evidence (saying what is and isn't known)
- fragrance-free / sensitisation-aware formulation
- formulating for Indian conditions
Test: after reading, would someone understand Skinstinct's standards better?

### 2. Only Meera could say it
PASS if it comes from her pharma formulation background or from something that happened inside Skinstinct (a batch, a supplier exchange, a customer case, her own data).
FAIL if any skincare influencer, dermatologist or textbook could have written the same post.

### 3. Exposes a gap or corrects a misconception
PASS if it shows a difference between what is claimed or assumed and what is actually true: label vs formulation, "same formula" vs actual formula, spec sheet vs production log, what customers blame vs what is really happening.

### 4. Concrete proof in hand
PASS if Meera has provided at least one specific anchor: a number, a measurement, a dated event, a document, a real case (e.g. "pH dropped 0.4 units", "log showed 70-85°C").
FAIL if the thought is a general explanation or opinion with nothing specific behind it.

### 5. Honesty signal
PASS if she admits a mistake, a limit, uncertainty, or shows a decision that cost Skinstinct something (holding a batch, rejecting an ingredient, a commercial tension she won't resolve dishonestly).
This is what makes her critiques of the industry credible, so it matters for brand trust.

### 6. Clear reader action
PASS if the reader walks away knowing what to ask, check or change (e.g. "check the CoA against a baseline every batch", "ask for the production log, not the spec sheet").
FAIL if the reader can only agree.

### 7. Fresh angle
PASS if it says something Meera has not already published, or takes a clearly new angle on a familiar topic.
Check against her published topics: niacinamide percentage and pH; the 2021 pharma stability meeting; humidity and returns / reformulation; "clinically tested"; pH and layering with Vitamin C; Vitamin C derivatives and stability; fragrance and sensitisation; SPF application amounts; ceramides and the barrier (brick-and-lipid matrix, ceramide NP/AP); "natural" and cold-pressed temperature logs; clean beauty and parabens; peptides; 18-month retrospective.
FAIL if it repeats one of these without a new lens.

### 8. Professional relevance
PASS if founders, formulators, product developers or industry people would learn something useful, not only consumers. LinkedIn is where she speaks to the industry; pure consumer how-to belongs in the newsletter.

## Output format
For each thought, return:

Thought: [one-line summary]
Hard stops: [none / which one, and whether it can be removed]
1 Brand pillar: PASS/FAIL - [reason in one line]
2 Only Meera: PASS/FAIL - [reason]
3 Gap exposed: PASS/FAIL - [reason]
4 Proof in hand: PASS/FAIL - [reason]
5 Honesty signal: PASS/FAIL - [reason]
6 Reader action: PASS/FAIL - [reason]
7 Fresh angle: PASS/FAIL - [reason]
8 Professional relevance: PASS/FAIL - [reason]
Score: X/8
Verdict: QUALIFIES / DISCARD
Angle to write: [one sentence: the core point of the post, if it qualifies]
To strengthen: [which failed metric could be fixed, and how; or where to redirect it, e.g. newsletter]

After all thoughts, give a ranked list of the ones that qualify. Do not draft posts unless asked; when asked, draft with the meera-pillai-voice skill.

## Calibration examples (scored September 2026)

A. Batch 14: supplier quietly changed the preservative blend; pH dropped ~0.4, texture off; revised spec sheet got buried; batch held.
Hard stops: none (do not name the supplier). 1 PASS documentation pillar. 2 PASS happened inside Skinstinct. 3 PASS "same formula" reorder isn't the same formula. 4 PASS 0.4 pH units, batch 14, spec sent three months earlier. 5 PASS their own team missed the spec sheet; holding the batch costs money. 6 PASS compare every CoA to a baseline. 7 PASS new; supplier-change risk not covered before. 8 PASS every founder using a contract manufacturer needs this.
Score 8/8. QUALIFIES.

B. Customer thinks serum stopped working; she started applying a heavy, likely silicone-based moisturiser before the serum.
Hard stops: none. 1 PASS vehicle and layering decide delivery. 2 FAIL any esthetician could explain layering order. 3 PASS customers blame the product that didn't change. 4 PASS a real, specific customer case. 5 FAIL nothing admitted or risked. 6 PASS occlusives go last. 7 PASS pH layering was covered, occlusive order wasn't. 8 FAIL mainly consumer education.
Score 5/8. QUALIFIES (borderline). To strengthen: add the professional lens, e.g. brands' customer support should ask "what else changed in your routine?" before treating it as a product complaint. Also works well as a newsletter.

C. Emollient spec sheet said cold-pressed; production log showed 70-85°C; ingredient rejected.
Hard stops: none (do not name the supplier; do not allege intent, she doesn't know if it was an error). 1 PASS documentation pillar. 2 PASS her own sourcing review. 3 PASS spec sheet vs production log. 4 PASS below 49°C vs 70-85°C. 5 PASS "we would have used it if I hadn't asked"; she admits she doesn't know if it was an error. 6 PASS ask for the production log, not the spec sheet. 7 FAIL newsletter 008 already told a cold-pressed temperature-log story. 8 PASS useful to anyone sourcing ingredients.
Score 7/8. QUALIFIES. Note: frame it for founders and sourcing teams so it doesn't read as a retelling of the newsletter.

D. Skin barrier: different causes of damage (over-exfoliation, lipid depletion, genetic ceramide issues) need different solutions.
Hard stops: none. 1 PASS formulation precision. 2 FAIL textbook knowledge. 3 PASS "barrier repair" treated as one fix. 4 FAIL no specific case or data. 5 FAIL. 6 FAIL no action stated. 7 FAIL newsletter 007 covered the barrier. 8 FAIL consumer education.
Score 2/8. DISCARD for LinkedIn. Redirect: possible newsletter follow-up to 007.

E. Clean beauty: imprecise term, but the audience that values it is exactly the engaged audience she wants; ingredient blacklists don't measure formulation quality.
Hard stops: none. 1 PASS formulation quality over ingredient lists. 2 PASS the founder's commercial-vs-intellectual tension is hers. 3 PASS a product can pass every clean checklist with sub-therapeutic actives. 4 FAIL no specific example or data. 5 PASS admits the commercial appeal of the audience. 6 FAIL no reader action yet. 7 FAIL she has covered clean beauty (newsletter 009) and says so herself. 8 PASS founders face the same positioning dilemma.
Score 5/8. QUALIFIES (borderline). The new angle is the founder's dilemma: wanting the clean-beauty audience without using a term she thinks is imprecise. To strengthen: add a concrete anchor and a reader action (e.g. what to ask beyond the checklist: concentration, pH, stability data).

Ranked: A (8), C (7), E (5, wins tie-break on metric 2), B (5), D discarded.
