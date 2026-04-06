---
name: better-translate
description: >
  Best practices for AI-driven English-to-Chinese translation.
  This skill should be used when the user asks to "translate to Chinese",
  "update the Chinese translation", "improve Chinese translation",
  "fix translation quality", "review Chinese translation", or when
  translating any English text into Chinese. Also applies when polishing
  an existing Chinese translation of English content.
---

# English-to-Chinese Translation

Produce natural, accurate Chinese translations that read as if written by a native speaker — free of 翻译腔 (translationese) and AI slop patterns.

## Overview

AI models produce predictable defects in Chinese translation: English word order calqued into Chinese, filler phrases added for politeness, over-emphasis not present in the source, and tone shifts. This skill provides a structured iterative workflow to eliminate these issues through comprehension, translation, and repeated polish passes.

## When to Use

- Translating documents, articles, or prose from English to Chinese
- Improving or polishing an existing Chinese translation
- Reviewing machine-translated Chinese content for quality

## When NOT to Use

- Translating into languages other than Chinese
- Translating non-English source text
- Writing original Chinese content (not a translation)
- Quick gloss translations where quality is unimportant

## Translation Workflow

### Phase 1: Comprehension

Read the full English source document before translating anything.

Identify ambiguous passages, domain-specific terminology, and phrases that could be interpreted multiple ways. Present ambiguities in a table:

| English Passage | Possible Meanings | Chosen Interpretation |
|---|---|---|
| ... | ... | ... |

For unresolved terminology:
1. Explore the project context (README, codebase, related docs) for usage conventions.
2. If ambiguity persists, stop and ask the user.

Do not proceed to translation until all ambiguities are resolved.

### Phase 2: Initial Translation

Translate the full document in one pass. During the initial draft:

- Preserve all formatting (headings, lists, code blocks, links, images)
- Keep proper nouns untranslated (product names, project names, person names)
- Translate technical terms by established convention (e.g., "machine learning" → "机器学习")
- Match the source tone and formality level
- Do not polish during this phase — produce a complete draft first

### Phase 3: Iterative Polish

Run a minimum of **3 rounds**. Each round performs three distinct checks in order. If any round produces changes, run one additional round after the minimum 3.

#### Accuracy Check

Compare translated text against the English source line by line. Fix:

- 含义改变 — meaning differs from source
- 添油加醋 — content added that source does not contain
- 遗漏 — content present in source but missing from translation
- 格式改变 — formatting broken (headings, links, code blocks)
- 标点符号 — English punctuation left in Chinese text, or wrong Chinese punctuation
- 语法错误 — grammatical errors in Chinese

#### Fluency Check

Read the Chinese text without referring to the English source. Fix:

- 英语语序 — English word order literally transplanted into Chinese
- 费解的表述 — phrasing that requires re-reading to understand
- 缺少衔接 — missing transitions between sentences or paragraphs
- 不自然的搭配 — word combinations no native Chinese speaker would use
- 能否改用更自然的表述 — rephrase for naturalness without changing meaning

#### AI Slop Check

Detect and remove AI-specific defect patterns:

- 过度强调 — excessive emphasis ("极其", "至关重要" where source says "important")
- 废话填充 — filler phrases not in source ("值得注意的是", "不言而喻", "毋庸置疑")
- 不自然的客套 — unnatural hedging or politeness not matching source tone
- 原文没有的展开 — elaboration added beyond what source states
- 翻译腔 — literal calques, unnatural collocations, mechanical "的" chains

For a detailed catalog of these patterns with examples, consult **`references/translation-examples.md`**.

### Final Validation

After iterative polish converges (a round produces zero changes):

1. Read the complete Chinese document from start to finish, as a Chinese reader, without referring to the English source.
2. Ask: does this read like a native Chinese speaker wrote it? Any AI slop indicators or 翻译腔 remaining?
3. If any issue is found, return to Phase 3 for another round.
4. Claim translation complete only when the full read-through raises no issues.

Do not rush this step.

## Quick Reference

| Phase | Action | Goal |
|-------|--------|------|
| 1. Comprehension | Read source, list ambiguities, resolve terminology | Full understanding |
| 2. Initial Translation | Translate in one pass, preserve formatting | Complete draft |
| 3. Iterative Polish | Accuracy → Fluency → AI Slop, minimum 3 rounds | High quality |
| 4. Final Validation | Full read-through as Chinese reader | Confirm quality |

## Additional Resources

- **`references/translation-examples.md`** — Good vs bad translation examples, 翻译腔 pattern catalog, and detailed quality checklist
