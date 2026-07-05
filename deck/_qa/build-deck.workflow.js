export const meta = {
  name: 'msb-deck-build',
  description: 'Author + collision-QA + assemble the My Second Brain explainer deck (24 slides) to PDF',
  phases: [
    { title: 'Author', detail: 'write the 20 remaining slide HTMLs from briefs' },
    { title: 'QA', detail: 'render + deterministic-audit + vision-crop + geometry-fix per slide' },
    { title: 'Consistency', detail: 'judge all 24 rendered slides together, fix outliers' },
    { title: 'Assemble', detail: 'PNGs -> PDF, verify page count + dims' },
  ],
}

const DECK = '/private/tmp/claude-501/-Users-jiawei-Documents-Jia-Wei-Vault/cb9030fa-eaa2-4285-8f47-cac36e5bfccd/scratchpad/msb-deck'

// ---- shared design contract every authoring agent obeys ----
const CONTRACT = `
You are authoring ONE slide of a 24-slide explainer deck for a Claude Code skill
called "My Second Brain". The deck's visual language is warm cream + charcoal +
rust, minimal-classical "blueprint over poster", bilingual ZH/EN. Canvas is a
FIXED 1920x1080.

FIRST, read these files to absorb the exact grammar (do NOT skip this):
- ${DECK}/shared/tokens.css              (the design tokens; use its CSS variables)
- ${DECK}/slides/01-cover.html           (exemplar: text hero)
- ${DECK}/slides/07-two-wings.html       (exemplar: multi-column card diagram)
- ${DECK}/slides/09-three-layers.html    (exemplar: stacked card tiers)
- ${DECK}/slides/18-distill-pipes.html   (exemplar: inline-SVG connector flow)

Then write your slide to the given path with the Write tool. Match the exemplars'
head block (same Google Fonts <link>, then <link rel="stylesheet" href="../shared/tokens.css">).

SLIDE ANATOMY (follow the exemplars exactly):
- Root: <div class="slide ...">. Optional dark variant: class="slide slide--dark".
- Top: <div class="slide-meta"><span>ZH label</span><span class="counter">NN / 24</span></div>
- A kicker: <div class="kicker"><span class="dash"></span><span>EN LABEL</span></div>
- A title in var(--font-display-cn), font-size var(--fs-title), with the KEY phrase
  wrapped in <em> (em is rendered non-italic in rust: em{font-style:normal;color:var(--rust)}).
- Body (cards / grid / SVG per the brief).
- Optional one-line caption with padding-top + border-top:1px solid var(--rule);
  its EN pull-phrase can use <em> styled italic serif rust.

HARD RULES (non-negotiable):
1. ZERO em-dash characters and ZERO double-hyphens in any VISIBLE text. For a visual
   divider use a CSS line: <span style="display:inline-block;width:30px;height:1px;
   background:var(--rule-strong);vertical-align:middle"></span>, or a middot. Use
   commas / colons / 、，：（） / line breaks. This is a firm rule of this skill.
2. All content stays inside 1920x1080 with >=40px breathing room from every edge.
   Never let content overflow; the page silently clips overflow.
3. Prefer HTML/CSS (grid/flex) for cards, columns, lists, tables. Use inline SVG
   ONLY for genuine connector / flow / loop / rail diagrams.
4. If you use SVG: every rect/text/line/path MUST sit inside the viewBox with >=12px
   margin (set the viewBox height to cover the lowest element + 12). Keep >=24px
   between any text and its box edge, and >=40px between distinct tiles. Copy the
   SVG text-class pattern from exemplar 18 (define .s-* classes, fill via tokens).
5. No overlapping text anywhere. No text touching a border (>=20px inner padding).
6. Exactly ONE rust focal point of gravity per slide (the title em, plus at most one
   accent element). Do not tint everything rust; charcoal ink is the workhorse.
7. Palette + type ONLY through tokens.css variables. Any new font stack must keep
   'Songti SC','PingFang SC' as CJK fallback before the generic keyword.

VOICE: practitioner comrade, native Chinese (no translated-English structure, no AI
tells like 此外 / 综上所述 / 不仅...而且). Business terms may stay English (vault, SOP,
dashboard, Base, MOC). Keep copy tight and slide-sized. Use the brief's copy; you may
lightly tighten wording but do not invent new claims or add content not in the brief.

Return ONLY a one-line status (e.g. "wrote 02-thesis-shift.html, HTML card layout").
`

// ---- the 20 remaining slides (01/07/09/18 already authored by the lead) ----
const BRIEFS = [
  {
    file: '02-shift.html', num: '02', authored: false,
    metaZH: '02 · AI 执行已经很便宜', kickerEN: 'The Thesis · The Shift',
    titleHTML: '会执行的 AI，<em>到处都是</em>了',
    idiom: 'text statement + a row of faded capability chips',
    spec: `A statement slide. Big title. Under it, a horizontal row of muted/greyed chips
      showing cheap-now capabilities: 写文案 · 做表格 · 查资料 · 写代码 · 翻译 · 总结 (in
      var(--ink-faint), small). Then one lead line in var(--fs-lead): "模型每季度都更强、更便宜。
      执行，已经不是瓶颈了。" Keep it airy; this is the setup for slide 03. No caption needed,
      or a thin faint footer line "So what is still hard? →" pointing forward.`,
  },
  {
    file: '03-scarce.html', num: '03', authored: false,
    metaZH: '03 · 稀缺的是数据有个家', kickerEN: "The Thesis · What's Scarce",
    titleHTML: '稀缺的，是你的数据<em>有一个家</em>',
    idiom: 'centered hinge statement with a two-line contrast',
    spec: `The core belief / the hinge of the whole deck. Large centered title. Below it a
      two-part contrast (two columns or two stacked lines, visually balanced):
      LEFT/TOP (good): "住进一个结构化的 vault → 任何 AI 都能回答关于你自己运营的真问题。"
      RIGHT/BOTTOM (bad): "散在 WhatsApp、一叠收据、某个员工的脑子里 → 再聪明的模型也帮不了你。"
      Use rust for the good side's arrow/verb, faint ink for the bad side. Caption pull-phrase:
      "Models keep changing. Your data having a home does not." styled EN italic serif.`,
  },
  {
    file: '04-pain.html', num: '04', authored: false,
    metaZH: '04 · 你的生意现在住在哪', kickerEN: 'The Problem · Where It Lives Today',
    titleHTML: '现在，你的生意<em>住在哪里</em>？',
    idiom: 'grid of 5 scattered-location cards + a punch line',
    spec: `Grid (e.g. 5 across or 2-3 layout) of the places business knowledge scatters today,
      each a small card with a ZH label + tiny EN gloss: WhatsApp 群聊 (chat threads) ·
      一叠收据 (a pile of receipts) · 到处都是的 Excel (spreadsheets everywhere) ·
      某个员工的脑子 (one employee's head) · 你自己的记忆 (your own memory). Cards look a bit
      "leaky"/faint (dashed borders or muted). Then a strong bottom line in rust-adjacent ink:
      "没有一个地方，是 AI 读得懂的。" Caption optional: the vault fixes exactly this.`,
  },
  {
    file: '05-promise.html', num: '05', authored: false,
    metaZH: '05 · 唯一留下来的资产', kickerEN: 'The Reframe · What Stays Yours',
    titleHTML: '模型换季，<em>你的大脑留下</em>',
    idiom: 'text hero + a small "models pass / vault stays" motif',
    spec: `A reframe/promise slide. Big title. Below, a small horizontal motif: a faded
      sequence of passing model names (GPT · Claude · 下一个更强的...) in faint ink, and BELOW
      or beside it one solid rust-underlined constant: "你的知识库 · stays". Lead line:
      "模型会一个个来、一个个过去。你搭的这个结构化知识库，是唯一不随模型迭代而贬值的资产。它属于你。"
      Caption pull-phrase EN italic: "The one asset that does not depreciate when the model does."`,
  },
  {
    file: '06-arch-divider.html', num: '06', authored: false,
    metaZH: 'Part Two', kickerEN: 'Part Two',
    titleHTML: '架构 · <em>一个家，两只翼</em>',
    idiom: 'DARK divider slide',
    spec: `A section divider. Use class="slide slide--dark" (dark charcoal bg, cream text).
      Large part marker "PART TWO" or "02" in mono rust, a big serif title
      "架构" with EN subtitle "The Architecture" and a one-line: "一个 vault 怎么同时装下你的人生和你的生意。"
      Minimal, lots of negative space, one thin rust rule. This is a breath between acts.
      slide-meta counter still "06 / 24" (can be faint cream).`,
  },
  {
    file: '08-two-axes.html', num: '08', authored: false,
    metaZH: '08 · 两把分类的尺', kickerEN: 'The Architecture · Two Sorting Axes',
    titleHTML: '两只翼，<em>两把不同的尺</em>',
    idiom: 'two-column comparison (Personal axis vs Business axis)',
    spec: `Two columns. LEFT = 个人翼 / Personal, sorted 按「可行动性」(by actionability):
      list PARA with one-line each: Project 有期限、有交付 · Area 长期在管、没有终点 · Resource 参考素材 ·
      Archive 已完成或休眠. RIGHT = 生意翼 / Business, sorted 按「知识类型」(by knowledge type):
      list the three layers: 家当 Assets 由什么构成 · 流程 SOP 怎么做成 · 认知 Methodology 为何这样决定.
      Bottom full-width master rule in a bordered strip: "流程按目的分；家当和记录按归属分。"
      (Processes sorted by intent; assets and records by ownership.) One rust accent per column header.`,
  },
  {
    file: '10-rooms.html', num: '10', authored: false,
    metaZH: '10 · 家当层的两种房间', kickerEN: 'Inside Layer 1 · Assets',
    titleHTML: '家当层：<em>实体房间</em> 与 职能房间',
    idiom: 'two-column room map + a filing-test footer',
    spec: `Two columns of "rooms". LEFT column heading 实体房间 / Entity rooms, sublabel
      "关于某个人、某样东西" and a chip list: 客户 Clients · 供应商 Vendors · 员工 Employees ·
      产品 Products · 文档 Docs · 设备 Equipment. Footer of this column: "一个实体，一条笔记。"
      RIGHT column heading 职能房间 / Function rooms, sublabel "某个职能在用、在管" and chips:
      市场 Marketing · 销售 Sales · 客服 CS · 人事 HR · 财务 Finance · 运营 Operations. Footer:
      "材料、日志、报表的家。" Bottom full-width filing-test strip (rust rule):
      "关于某人某物 → 实体房间。某个职能在用 → 职能房间。"`,
  },
  {
    file: '11-loop.html', num: '11', authored: false,
    metaZH: '11 · 认知层为何留空', kickerEN: 'The Architecture · A Living Loop',
    titleHTML: '第三层<em>故意留空</em>，它从判断里长出来',
    idiom: 'inline-SVG living-loop diagram (two boxes, bidirectional arrows) + feeder',
    spec: `Inline SVG (follow exemplar 18's SVG discipline; viewBox with >=12px margins).
      Two large boxes side by side: LEFT "02 SOP · 流程" and RIGHT "03 Methodology · 认知".
      TOP arrow LEFT->RIGHT labeled "反复踩的同一个坑 → 提炼成 教训" (a recurring pothole distills UP).
      BOTTOM arrow RIGHT->LEFT labeled "打法成熟、每步都写得出 → 降级成 SOP" (a matured playbook demotes DOWN).
      A small feeder arrow into the RIGHT box from a little node "决策记录" labeled "复盘 → 决策规则".
      This shows the three layers as ONE living loop, not three drawers. Keep arrows clearly
      separated (top vs bottom), generous vertical gap so the two arrow labels never collide.
      Caption: "捕捉填不满认知层。它从判断里长出来。" + EN italic "The third layer is a loop, not a drawer."`,
  },
  {
    file: '12-command-base.html', num: '12', authored: false,
    metaZH: '12 · 指挥中心', kickerEN: 'The Command Center · 06',
    titleHTML: '指挥中心：<em>一个决策，只有一个家</em>',
    idiom: 'two-column: rooms list (left) + dashboard views (right)',
    spec: `LEFT column: what 06_Command-Base holds, as a labelled list: Home 前台 ·
      Decisions 决策中央（domain + function 必填，两翼共用）· Tasks 待办 · Sessions 会话记录 ·
      Command-Base.base 仪表盘. RIGHT column: the dashboard = an Obsidian Base rendering
      multiple views, shown as a tidy chip/mini-table: Today · This Week · Red Flags(逾期) ·
      Waiting For · By Domain · Sessions · Decisions. One-line under it: "永不手写 state 进 dashboard,
      它从笔记里自动渲染。" Caption: "决策的归属问题是：这个决定管着谁,而不是给谁看。"`,
  },
  {
    file: '13-constitution.html', num: '13', authored: false,
    metaZH: '13 · 规矩住在 vault 里', kickerEN: 'The Constitution · structure-doctrine.md',
    titleHTML: '规矩住在 <em>vault</em> 里，不在 skill 里',
    idiom: 'lead paragraph + a 2-column iron-laws list',
    spec: `Top: a lead line: "结构法则写在 99_Meta/structure-doctrine.md 这一个文件里,不在技能代码里。
      换模型、换工具、换 AI, 规矩都不漂移。" Then a 2-column list of iron laws, each one short line
      with a rust index (01..06): 01 流水住在系统里,不进 vault · 02 一个东西,一条笔记 ·
      03 文件夹要自己挣来位置(先平铺,聚起三个才建夹)· 04 决策只有一个家 · 05 密码永不进 vault ·
      06 AI 产出和你的捕捉,不静默混在一起. Bottom caption (rust): "按心情归档的 vault,三个月就被弃用。"`,
  },
  {
    file: '14-modes-divider.html', num: '14', authored: false,
    metaZH: 'Part Three', kickerEN: 'Part Three',
    titleHTML: '四种模式 · <em>怎么用它</em>',
    idiom: 'DARK divider slide',
    spec: `Section divider, class="slide slide--dark". Part marker "PART THREE" / "03" in mono rust.
      Big serif title "四种模式" with EN "The Four Modes" and a one-line:
      "搭它、喂它、保它诚实、让它像你。" Minimal, negative space, one thin rust rule. counter "14 / 24".`,
  },
  {
    file: '15-modes-overview.html', num: '15', authored: false,
    metaZH: '15 · 四种模式一览', kickerEN: 'How You Run It · Four Modes',
    titleHTML: '一个 skill，<em>四种模式</em>',
    idiom: '2x2 card grid of the four modes',
    spec: `A 2x2 grid, four equal cards. Each card: mode number (01..04) mono, mode name ZH + EN,
      a time budget chip, a one-line "what it does", and a one-line "payoff" (rust).
      01 Setup 搭建 · ~10 min · 装好 Obsidian,建好整个 vault,生成你的指挥中心 skill · 结束在一张 graph 星图.
      02 Capture 捕捉 · ~10-15 min / 房间 · 一次搬一个房间,一次问一个问题 · 每次给你一个没注意到的观察.
      03 Distill 蒸馏 · ~10 min / 周 · 先体检整理,再用三条管道提炼 · 你只裁 yes / no.
      04 Create-My-Jarvis 造你的 Jarvis · 45-60 min · 两场访谈:profile + 性格 · 让 AI 不再像自动贩卖机.
      Consistent card sizing, one rust accent (the payoff line) per card.`,
  },
  {
    file: '16-setup.html', num: '16', authored: false,
    metaZH: '16 · Setup · 结束在星图', kickerEN: 'Mode 01 · Setup',
    titleHTML: '十分钟，从<em>空机器</em>到一张星图',
    idiom: 'horizontal step sequence (HTML chips/rail) + a payoff callout',
    spec: `A left-to-right step sequence (HTML numbered chips, not SVG unless clean):
      选语言 → 装 Obsidian → 选 vault 位置 → 答 3 个行业开关 + 4 个生意问题 → 一次性 scaffold
      (文件夹 / MOC / Home / 模板 / 仪表盘 / CLAUDE.md) → 生成指挥中心 skill → 打开 graph view.
      Show the 3 industry toggles explicitly somewhere small: 有门店? 有设备? 进口货?
      Then a payoff callout (bordered, rust): "那就是你的第二大脑,搭好了一半。结构齐了,记忆还没搬进来。"
      Caption EN italic: "Ends on the graph view: your half-built brain, as a constellation."`,
  },
  {
    file: '17-capture.html', num: '17', authored: false,
    metaZH: '17 · Capture · 一次一个房间', kickerEN: 'Mode 02 · Capture',
    titleHTML: '一次搬一个房间，<em>结束时多懂一点自己</em>',
    idiom: 'left: capture flow steps; right: the three-layer closing screen mock',
    spec: `Two zones. LEFT: the capture rhythm as steps: 先搬「生意本身」(Business Profile, 8 问, 5 分钟)
      → 房间菜单挑一间 → 一次一个问题,接受粗糙答案 → 归好 3-5 条到对的房间 → 结束给「一个观察 + 两个好问题」.
      Note the observation is owner-level, not a task list. RIGHT: a mono "closing screen" card that
      mocks the three-layer tree after tonight:
        07_<Business>/
        ├─ 01_Assets        今晚 +N 条
        ├─ 02_SOP           今晚 +N 条
        └─ 03_Methodology   留空
      Under the tree, a real example observation in a quote block:
      "你说的三个客户来源里,两个是转介绍,但你没有一套转介绍机制:它发生在你身上,不是你在运营它。"
      (Use ├─ └─ box-drawing, NOT hyphens. No -- anywhere.) Caption:
      "上两层靠捕捉长;第三层要等判断。每一次,都多懂一点自己的生意。"`,
  },
  {
    file: '19-jarvis.html', num: '19', authored: false,
    metaZH: '19 · Create-My-Jarvis', kickerEN: 'Mode 04 · Create-My-Jarvis',
    titleHTML: '两场访谈，让 AI <em>不再像自动贩卖机</em>',
    idiom: 'before/after greeting cards + a genericness-gate checklist',
    spec: `Top row: two interviews explained briefly: Profile 访谈 (10 问,你实际怎么运作,AI 每早读它)
      then Soul 访谈 (8 拍,AI 该怎么陪你). Middle: a before/after of the morning greeting, two cards:
      GENERIC (faint): "Good question! How can I help you today?"  vs  YOURS (rust-accented, named):
      a greeting that uses the AI's chosen name + a voice rule (e.g. "先说风险,再说方案。"). Bottom:
      the genericness gate as a short checklist (硬门): 名字有理由 · 「在乎什么」说到真实生意与利害 ·
      >=3 条能在一句话上被检验的语气规则 · 「我不是什么」用你自己的话. Include the FAIL/PASS calibration
      small: FAIL "清晰、简洁。" / PASS "别用『好问题』开场;我用中文你就用中文;先说风险再说方案。"
      Caption: "一个通用的 soul,只会造出你早就有的那个 AI。"`,
  },
  {
    file: '20-insights.html', num: '20', authored: false,
    metaZH: '20 · 洞察是地图不是判决', kickerEN: 'The Discipline · A Map, Not a Verdict',
    titleHTML: '洞察是<em>地图</em>，不是判决',
    idiom: 'statement + a small observation-vs-diagnosis contrast',
    spec: `Text-forward. Title big. A contrast pair: 观察级 (what it does, rust) vs 诊断级 (what it
      refuses, faint): 观察级 = "一个你没注意到的点 + 两个好问题", framed forward
      ("你的下一个突破口是...")。诊断级 = "你的问题是...", 它不这么说。One line: "它不会承诺数据还撑不起的分析,
      并且会老实告诉你。" Caption EN italic: "Early insight is an observation, and it says so honestly."
      Keep it calm and confident, lots of whitespace.`,
  },
  {
    file: '21-boundaries.html', num: '21', authored: false,
    metaZH: '21 · 诚实的边界', kickerEN: 'The Honest Gate · What It Is Not',
    titleHTML: '它<em>不是</em>什么',
    idiom: '2x2 "not" cards',
    spec: `Four cards, each stating a boundary honestly:
      不是多人 wiki: 单一 owner,你 + 你的 AI。Obsidian 没有权限层,员工要用就导出那一块。
      不是 ERP / CRM: 高频交易流水留在为它们建的系统里。vault 只存 pointer、例外、月度快照。
      不是读心分析师: 早期只给观察,而且它会承认。
      不是课程、不是漏斗: 它是一个长期活着的工具,什么都不卖。
      Each card: a rust "NOT" tag + the boundary. Bottom caption: "把边界说清楚,是这套系统值得信任的原因。"`,
  },
  {
    file: '22-compounds.html', num: '22', authored: false,
    metaZH: '22 · 会复利的那部分', kickerEN: 'The Payoff · What Compounds',
    titleHTML: '搭一次，然后<em>喂它一辈子</em>',
    idiom: 'HTML horizontal loop of 4 stages that cycles back',
    spec: `A cyclical flywheel shown as 4 stages in a loop (HTML chips with arrows between,
      and a "loops back" arrow returning to the start): 捕捉 → 归位 → 连线(MOC) → 每个 session 找 context 更快
      → (回到) 捕捉。Center or side note: "越喂越懂你;越懂你,越值得喂。" Big supporting line:
      "前 5 步是搭建(约 3-4 小时);之后是养,永远不结束。" Caption EN italic serif rust:
      "Build it once; grow it forever." Keep the cycle visually clean, arrows never crossing labels.`,
  },
  {
    file: '23-install.html', num: '23', authored: false,
    metaZH: '23 · 开始 · Install', kickerEN: 'Get Started · Install',
    titleHTML: '一行命令，<em>开始搭</em>',
    idiom: 'install card: mono code block + requirements list',
    spec: `A prominent mono code block card: "npx skills add breakthrough-edu/my-second-brain".
      Under it, a second line: 然后在 Claude Code 里说 → "set up my second brain" (styled as a spoken prompt).
      A requirements list (small, tidy): Claude Code · Obsidian(免费,可代装;开启 Bases 插件) ·
      macOS / Windows / Linux · English 或 中文,setup 时选. Footer line: "MIT. Built and maintained by
      Breakthrough EDU." Give the code block real presence (bordered, bg-soft, rust caret or prompt sign).`,
  },
  {
    file: '24-close.html', num: '24', authored: false,
    metaZH: '24 · One home. Any AI.', kickerEN: 'Close',
    titleHTML: '你的数据，<em>一个家</em>。任何 AI，真答案。',
    idiom: 'closing statement echoing the cover grammar',
    spec: `A closing slide that rhymes with the cover (same hero-title feel, generous margins).
      Big title as given. A calm sub-line: "AI 会一直换。你搭的这个大脑,留下来。" A footer echoing the
      cover footer: By Jia Wei · Breakthrough EDU · a soft prompt echo "say: set up my second brain" ·
      and a small "Open discussion". Feels like a confident full stop, not a sales pitch.`,
  },
]

// files that the lead already authored + verified clean (QA still re-checks them)
const AUTHORED = ['01-cover.html', '07-two-wings.html', '09-three-layers.html', '18-distill-pipes.html']
const ALL = BRIEFS.concat(
  AUTHORED.map(f => ({ file: f, num: f.slice(0,2), authored: true }))
)

function authorPrompt(b) {
  return `${CONTRACT}

=== YOUR SLIDE ===
File to write:  ${DECK}/slides/${b.file}
slide-meta ZH label (top-left):  ${b.metaZH}
counter (top-right):  ${b.num} / 24
kicker (EN):  ${b.kickerEN}
title (var(--font-display-cn), key phrase in <em>):  ${b.titleHTML}
idiom:  ${b.idiom}

Content spec:
${b.spec}

Write the complete, self-contained HTML file now.`
}

function qaPrompt(b) {
  const base = b.file.replace('.html', '')
  return `You are the collision-QA + fix pass for ONE slide of the "My Second Brain" deck.
Slide file: ${DECK}/slides/${b.file}   (1920x1080 fixed canvas)

Run this loop (up to 3 rounds), all commands from ${DECK}/_qa :

  python3 render.py ../slides/${b.file} ../png/${base}.png
  python3 audit_run.py ../slides/${b.file}          # prints JSON collision report
  python3 crop.py ../png/${base}.png                # writes zoom crops

The JSON report has: overlaps (text-vs-text), oob (text clipped at slide edge),
tileOverlaps (SVG tiles colliding), svgClip (geometry past its viewBox), and clean.

Then READ these images and judge collisions with your own eyes (the detector misses
some things, e.g. text crowding a border, ugly wrapping, a label kissing an arrow):
  ${DECK}/_qa/crops/${base}__overview.png
  ${DECK}/_qa/crops/${base}__r0c0.png ... __r0c2.png ... __r1c0.png ... __r1c2.png

A slide PASSES only when BOTH: (a) audit JSON clean:true, AND (b) your eyes see no
overlap, no clipping, no text touching a border, no awkward overflow, comfortable spacing.

If it fails, EDIT ${DECK}/slides/${b.file} to fix the geometry (adjust gaps, font-size,
grid sizing, SVG coordinates, viewBox height, wrapping), then re-render + re-audit + re-crop
and look again. Keep the design intent; fix only what collides. Common fixes: enlarge a
container / reduce a font-size / add gap / raise viewBox height / shorten a wrapping label.
NEVER introduce an em-dash or a double-hyphen in visible text while fixing.

After at most 3 rounds, return ONLY compact JSON:
{"file":"${b.file}","clean":true|false,"rounds":N,"auditClean":true|false,"notes":"<=12 words"}`
}

// ---------- run ----------
phase('Author')
log(`Authoring ${BRIEFS.length} slides + QA on all ${ALL.length}. 4 exemplars pre-authored.`)

const results = await pipeline(
  ALL,
  // stage 1: author (skip the 4 exemplars)
  (b) => b.authored
    ? Promise.resolve({ file: b.file, authored: 'pre' })
    : agent(authorPrompt(b), { label: `author:${b.num}`, phase: 'Author' }).then(() => ({ file: b.file })),
  // stage 2: render + collision-QA + fix (all 24)
  (_prev, b) => agent(qaPrompt(b), {
    label: `qa:${b.num}`, phase: 'QA',
    schema: {
      type: 'object', additionalProperties: true,
      properties: {
        file: { type: 'string' }, clean: { type: 'boolean' },
        rounds: { type: 'number' }, auditClean: { type: 'boolean' }, notes: { type: 'string' },
      }, required: ['file', 'clean'],
    },
  }),
)

const clean = results.filter(Boolean).filter(r => r.clean)
const dirty = results.filter(Boolean).filter(r => !r.clean)
log(`QA done: ${clean.length}/${ALL.length} clean; ${dirty.length} still flagged.`)

// ---------- Consistency (barrier: judge all 24 together) ----------
phase('Consistency')
const consist = await agent(
  `You are the final consistency judge for the 24-slide "My Second Brain" deck.
Read the 24 rendered overview crops (one per slide) at:
  ${DECK}/_qa/crops/NN-*__overview.png    (list them: run  ls ${DECK}/_qa/crops/*__overview.png)
Render any that are missing first with:  cd ${DECK}/_qa && python3 render.py ../slides/<file> ../png/<png> && python3 crop.py ../png/<png>

Check ACROSS the set: (1) every counter reads "NN / 24" with the right number and they run 01..24;
(2) consistent outer margins + title placement + kicker style; (3) the "one rust focal point" rule
(no slide over-uses rust); (4) dividers (06, 14) share a dark treatment; (5) no slide is visibly
crowded or off-grammar vs the others; (6) no em-dash / double-hyphen visible anywhere.
For any slide needing a tweak, EDIT ${DECK}/slides/<file>, then re-render + re-crop it. Keep changes
minimal and on-grammar. Return compact JSON:
{"reviewed":24,"edited":["NN-file", ...],"notes":"<=20 words"}`,
  { label: 'consistency', phase: 'Consistency',
    schema: { type: 'object', additionalProperties: true,
      properties: { reviewed: { type: 'number' }, edited: { type: 'array', items: { type: 'string' } }, notes: { type: 'string' } },
      required: ['reviewed'] } }
)
log(`Consistency pass: edited ${(consist && consist.edited && consist.edited.length) || 0} slides.`)

// ---------- Assemble (deterministic; agent runs the scripts) ----------
phase('Assemble')
const asm = await agent(
  `Assemble the final PDF for the "My Second Brain" deck. Run, from ${DECK}/_qa :
  1) Ensure all 24 PNGs are current. For every ${DECK}/slides/NN-*.html, if the matching
     ${DECK}/png/NN-*.png is missing or older than the html, re-render it:
       python3 render.py ../slides/<file> ../png/<png>
  2) python3 assemble.py ${DECK}/png ${DECK}/My-Second-Brain-Deck.pdf
  3) Verify: run
       python3 -c "import fitz; d=fitz.open('${DECK}/My-Second-Brain-Deck.pdf'); print('pages', d.page_count); print('p0', d[0].rect)"
     Confirm page_count == 24. Also list ${DECK}/png/[0-9][0-9]-*.png and confirm there are exactly 24.
  4) Render 3 spot pages back to PNG to confirm the PDF is not blank:
       python3 -c "import fitz; d=fitz.open('${DECK}/My-Second-Brain-Deck.pdf'); [d[i].get_pixmap(dpi=72).save('${DECK}/_qa/_pdfcheck_%02d.png'%i) for i in (0,11,23)]"
  Return compact JSON: {"pdf":"${DECK}/My-Second-Brain-Deck.pdf","pages":N,"pngCount":N,"ok":true|false,"notes":"<=15 words"}`,
  { label: 'assemble', phase: 'Assemble',
    schema: { type: 'object', additionalProperties: true,
      properties: { pdf: { type: 'string' }, pages: { type: 'number' }, pngCount: { type: 'number' }, ok: { type: 'boolean' }, notes: { type: 'string' } },
      required: ['ok'] } }
)

return {
  authored: BRIEFS.length,
  qaClean: clean.length,
  qaDirty: dirty.map(d => d.file),
  consistencyEdited: (consist && consist.edited) || [],
  assemble: asm,
}
