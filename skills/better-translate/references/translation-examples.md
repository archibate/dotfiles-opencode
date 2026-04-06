# Translation Examples and Pattern Catalog

Good vs bad translation examples, common 翻译腔 patterns, and a detailed quality checklist for English-to-Chinese translation.

## Good vs Bad Examples

### Example 1: Technical Documentation

**English:**
> The compiler optimizes the loop by unrolling it, which reduces the number of branch instructions executed.

**Bad (翻译腔):**
> 编译器通过展开循环来优化循环，这减少了被执行的分支指令的数量。

Problems: "被执行的" is passive voice calqued from English. "分支指令的数量" is a rigid 的-chain. "优化循环" repeats "循环" awkwardly.

**Good:**
> 编译器通过循环展开进行优化，减少了分支指令的执行次数。

### Example 2: Prose

**English:**
> It's worth noting that the project has grown significantly over the past year.

**Bad (AI slop):**
> 值得注意的是，该项目在过去一年中取得了显著的增长。

Problems: "值得注意的是" is a filler phrase — the source uses a casual hedge, not a formal announcement. "取得了显著的增长" is over-formal.

**Good:**
> 这个项目过去一年规模增长了不少。

### Example 3: Passive Voice

**English:**
> The data is processed in real-time by the pipeline.

**Bad:**
> 数据被管道实时处理。

Problem: Chinese rarely uses 被 for neutral, non-adversative actions. The passive is calqued from English.

**Good:**
> 管道会实时处理数据。

### Example 4: Long 的-chain

**English:**
> The configuration file for the database connection pool.

**Bad:**
> 数据库连接池的配置文件。

Acceptable, but can be smoother:

**Good:**
> 数据库连接池配置文件。

### Example 5: Over-translation

**English:**
> Run the command below.

**Bad:**
> 请运行以下命令来执行操作。

Problems: Added "请" (politeness not in source), added "来执行操作" (elaboration not in source).

**Good:**
> 运行以下命令。

## Common 翻译腔 Pattern Catalog

| Pattern | Description | Example (Bad → Good) |
|---------|-------------|----------------------|
| Passive 被 | Using 被 for non-adversative actions | 数据被处理 → 处理数据 |
| 的-chain | Excessive 的 connecting modifiers | 用户的配置文件的路径 → 用户配置文件路径 |
| Literal "是...的" | Unnecessary emphasis structure | 这是重要的 → 这很重要 |
| Which-clause calque | Translating "which..." as a separate "，这..." clause | 优化了性能，这使得... → 从而提升性能 |
| "进行" inflation | Using 进行 before a verb to sound formal | 进行修改 → 修改 |
| "的" after every adjective | Adding 的 where compound nouns are natural | 高级的特性 → 高级特性 |
| "当...时" calque | Translating "when" literally | 当用户点击时 → 用户点击后 |
| "一个" inflation | Adding 一个 where Chinese omits it | 创建一个文件 → 创建文件 |
| "被称之为" | Over-formal passive naming | 被称之为方法 → 叫做方法 / 是方法 |
| "其" overuse | Using 其 where 的 or 它 is natural | 其主要功能 → 它的主要功能 |

## Detailed Quality Checklist

### Accuracy

- [ ] Every sentence in the translation corresponds to a sentence in the source
- [ ] No content from the source is missing
- [ ] No content is added that the source does not contain
- [ ] Technical terms are translated consistently throughout
- [ ] Numbers, names, and code remain unchanged
- [ ] Links and references point to the correct targets

### Fluency

- [ ] Each sentence reads smoothly on its own
- [ ] Sentence-to-sentence transitions feel natural
- [ ] No English word order patterns (subject-verb-object rigidness, trailing modifiers)
- [ ] Paragraphs flow logically
- [ ] No redundant pronouns (Chinese often omits subjects)
- [ ] Measure words and classifiers are correct

### Tone

- [ ] Formality level matches the source
- [ ] No added politeness markers (请, 您) where source is casual
- [ ] No added emphasis (极其, 非常, 至关重要) beyond what source contains
- [ ] No hedging phrases (值得注意的是, 不言而喻, 毋庸置疑) not in source
- [ ] Imperative mood preserved where source uses imperatives

### Formatting

- [ ] Markdown headings, lists, and code blocks preserved
- [ ] Bold, italic, and inline code formatting preserved
- [ ] Tables render correctly
- [ ] English punctuation not left in Chinese text (use ，。：；！？ instead of ,.:;!?)
- [ ] Chinese punctuation uses full-width characters
