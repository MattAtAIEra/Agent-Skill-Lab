---
name: government-research-stance
description: This skill should be used when "writing a government-commissioned research report", "drafting policy recommendations for ministries", "preparing think tank deliverables", "writing technical evaluation reports for public agencies", or when working on tenders such as OECD AI initiative research, 數位發展部 standard projects, 部會委辦案. Ensures the writer stays in a technical advisor / research scholar role and does not overreach into policymaker / legislator authority.
version: 1.0.0
---

# Government Research Stance Discipline

When writing a government-commissioned research report (e.g., OECD AI initiative research, ministry-tendered policy studies, technical evaluation reports for public agencies), the research team must stay strictly within the role of "technical advisor / research scholar" and must not overreach into legislative, regulatory, or policymaking authority. The final decision space belongs to the supervising agency.

## Why This Matters

Research is constrained by AI context window, selective attention, and human/time limits. All matrices, evaluation pipelines, and frameworks produced are **directional reference** for ministries — saving them time searching from a sea of options. They should not be inflated into procurement requirements or legal mandates. Legal/command basis does not rest with the research team.

## The 5-Corner Research Positioning

1. Organize tool attribute mappings (save ministries' search time)
2. Execute black-box testing and validation (provide evidence base)
3. Observe international application scenarios (provide pre-decision research so ministries can adopt with confidence)
4. Propose technical feasibility directions (e.g., conceptual demos of API/MCP/Agent components)
5. Leave to ministries to handle specific policy implementation per their legal authority

## Forbidden Phrases (violate research stance)

- "List X as a **mandatory deliverable** / **mandatory check item** / **mandatory disclosure** / **mandatory field** in procurement specs"
- "**Mandatory** execution / **mandatory** governance review threshold"
- "**Failure to pass shall not** enter the next stage / **shall not** go live / **shall not** complete testing / **shall not** be approved"
- "Recommend that 數位發展部 **explicitly stipulate** … in building the AI Basic Act §16 risk classification framework"
- "Recommend **that X agency oversees and maintains**…" (designating the lead agency is overreach)
- "Recommend **quarterly execution** / **monthly updates** / **annual submission**…" (imposing routine obligations)
- Citing the AI Basic Act §16 as the legal basis for research-derived materials
- Specific Gantt charts with concrete dates / "execution schedules"
- Designs of "automatic matching engines" / "mandatory routing" mechanisms

## Recommended Phrases (align with research stance)

- "The research team observes that…"
- "The research finds that…"
- "**May serve as a reference for the supervising agency in subsequent planning**"
- "**May be provided to the supervising agency for reference when …**"
- "Has reference value / has technical feasibility / has research value"
- "Specific X is to be handled by the supervising agency with relevant authority per their legal mandate"
- "Specific X is to be decided by the supervising agency per their professional judgment"
- "**Is the research team's observational statement, not a normative recommendation**"
- "There is already an existing [Y law/Z case] basis; on this basis, [API/MCP/Agent] technical components may be further constructed"
- "Is one possible research direction worth considering"
- "Final decision space belongs to the supervising agency"

## Chapter Naming Patterns

| Avoid | Use Instead |
|-------|-------------|
| 政策建議 (Policy Recommendations) | 研究觀察與供主管機關參考之方向 (Research Observations and Reference Directions for the Supervising Agency) |
| 8 大共通治理元件 (8 Common Governance Components) | 研究觀察到之 8 項技術機會 (8 Technical Opportunities Observed) |
| 政府 AI 函示庫建置建議 (Recommendation to Build Gov AI Function Library) | API 函示庫／MCP server／AI Agent 之技術可行性觀察 (Technical Feasibility Observations on API Library / MCP Server / AI Agent) |
| 三道治理 Gate (Three Governance Gates) | 三道概念性治理檢查節點 (Three Conceptual Governance Check Nodes) |
| 四項嵌入策略 (Four Embedding Strategies) | 四項概念對應 (Four Conceptual Correspondences) |
| 漸進式導入時程 (Progressive Adoption Timeline) | 概念性先後順序之觀察 (Observations on Conceptual Sequence) |

## Chapter Opening Stance Declaration Template

For important chapters, add a stance declaration at the chapter opening:

> Before the content of this chapter, the research team first clarifies the stance positioning of this framework:
>
> First, this framework **is the research team's conceptual proposal** and has no normative effect.
>
> Second, the main use value of this framework is **to provide visualized correspondence relationships**, so that ministries have a common vocabulary starting point when planning.
>
> Third, the specific designs in this framework are all **conceptual demonstrations by the research team**; they are to be decided by the supervising agency with relevant authority per their resources and policy goals.

## Pharmacovigilance AI Determination — Standard Writing Template

This is the standard template for proposing technical feasibility (demonstrated by Matt):

> The research team observes that there is X common gap; there already exist [Y law / Z business] foundations; on this basis, technical components such as [API library / MCP server / AI Agent] may be further constructed, serving as a service mechanism for [specific application scenario], and completing XAI validation. Such development involves a degree of expertise and difficulty, so such services have professional value, and **may be provided to the supervising agency for reference in subsequent planning**.

Worked example: Pharmacovigilance AI determination service —
- Existing legal basis: Pharmaceutical Affairs Act, Severe Adverse Drug Reaction Reporting Regulations
- Existing business basis: TFDA's National Adverse Drug Reaction Reporting Center (TADRRC)
- Technical feasibility: API library + MCP server + AI Agent + XAI validation (DALEX / Holistic AI cross-model comparison)
- Professional value: such development requires LLM model selection, domain vocabulary construction, explainability validation, and integration with existing professional review processes — these are non-trivial professional demands.

## International Application Scenario Gathering — Research Value Positioning

The research team should position "gathering international scenarios where the same applications exist, validating their methodology, providing pre-decision evidence" as the research's own value output, not as a recommendation for the supervising agency to gather themselves.

For example: international public-sector adoption of DALEX and Holistic AI, third-party audit ecosystem, governance framework citations — these are all within the research team's information-gathering scope.

## Self-Check After Each Section

After writing a section, self-check with these 4 questions:

1. **Did this section decide for the supervising agency** "what should be done", "by whom", "when"? If yes, rewrite.
2. **Did this section anchor research material to a specific clause of the AI Basic Act as legal basis**? If yes, rewrite.
3. **Does this section contain commanding syntax** like "mandatory" / "must" / "shall not" / "if … not, then …"? If yes, rewrite.
4. **Does it clearly mark** "This is the research team's observational statement; specific policy implementation is to be handled by the supervising agency per their legal authority"? If not, add it.

## Scope of Application

This skill applies to:

- Government-commissioned research projects (e.g., OECD AI initiative research, 數位發展部 standard projects, ministry-tendered research)
- Policy research reports
- Technical evaluation reports
- Think tank deliverables
- Any documents produced by the research team in a "technical advisor" capacity

This skill does **not** apply to:

- Product development documents
- Business pitches
- Academic papers (academic papers have their own conventions)
- Internal company strategy discussions

## Final Mantra

> 做好本身的角色，留給上層主管決策的空間。
>
> Do your own role well; leave decision space to the supervising authority.

## Origin

This skill originates from Matt's guidance during the writing of the OECD ZE114018 standard project "OECD AI Priority Initiative Research" report, where the AI assistant initially overreached into policy-mandate language and was corrected by Matt to stay within the technical advisor role.
