# Operating the Second Brain: 每天怎么用你的第二大脑跑活

> 你装好了第二大脑, 但装好跟会用是两件事。这份讲的是我自己每天怎么用它: session 怎么展开、什么时候值得开一份新文档、一场活收尾的时候东西分到哪、指针怎么放、正本怎么不漂。⭐ 每一条都不是「最佳实践」, 是我自己做了几个礼拜之后回头看, 真的一直在重复的动作。
>
> **怎么用这份**: 不是拿去照抄。把这份存进你的 vault 的 `00_Inbox/`, 然后把最后一节那段 prompt 贴给你的 Claude Code, 它会带你把这份消化成**你自己的** playbook, 用你的话、你的例子, 归进你的 `04_Methodology/Playbooks/`。你不做的那几条, 不进。

---

## 0 · 五个该停一下想的关口

整天都在跑, 但真正要停下来想一下的只有五个时刻:

1. **要开一个新 session 之前**: 什么留在主 session, 什么丢出去。
2. **想开一份新文档之前**: 一行指针够不够。
3. **一场活收尾的时候**: 手上的东西分到哪五处。
4. **要放一个指针的时候**: 放哪、指什么、怎么命名。
5. **改了一个正本或搬了一个档之后**: 哪些地方会跟着漂。

下面先讲判断, 再讲动作。判断是重点, 动作是判断长出来的。

---

## 1 · 十条判断

1. **一件事只有一个正本, 其他地方一律指过去。** 不确定正本在哪, 先问你的 AI「现在 SOT 在哪里」, 不要再写一份。你会发现最常漂的是日期跟状态, 因为它们最常被顺手抄一次。
2. **「一个 source of truth」是结构, 也是动作, 而且有先后。** 结构是上面那条。动作是每场 session 收尾的收敛: 讨论期间写的那份 working 文档拆进各处、baton 归档、Inbox 清空、指针扫一遍。少了动作, 结构会在一场 session 里就漂掉。
3. **一行讲得完的东西不开档。** 一个外部资料夹的链接、一张照片库的地址, 在它所属的 project brief 里放一行就好, 不解释为什么。开一份档去装一行字, 就是多一个会漂的地方。
4. **会变的状态只住一处, 别的档不复述。** 一个品牌「目前暂停」这种话, 让它自己的 brand guide 讲; business profile、project brief 都不要再讲一次。写太多 facts 的地方就是会漂的地方。
5. **指针放太多处也会漂。** 我搬过一次家, 四十几条记忆指着已经不存在的路径。所以指针放一处; 搬一个档的时候, 改掉所有指向它的链接是搬的一部分, 改完验零死链。
6. **收尾时「判不进」跟「判进」一样是一个动作。** 无 Lesson、无 decision 要说出口, 不是没说就算了。说出口的不进, 下一场才不会重新问一次。
7. **讨论型的活一定另开 session, 为的是集中。** 定位、brainstorm、理流程, 开一个专门的 session。执行型的活 (改一页、出一张图) 才留在手边做。
8. **让它查你以为你知道的事, 先验管子再下结论。** 「日历上是不是已经排了下几个月的活动?」「那个 skill 是不是已经装好了?」让它去看, 不要它没读过就装懂。读回来是空的, 先确认它读得到别的东西, 才敢说「真的没有」。
9. **先用再搭。** 能力已经到手就别急着先建工具。值得建工具的判准是错误率, 不是能力: 同一件事你手动做了三次都出错, 才值得建。
10. **让它画链条, 不要清单。** 十八张 task 的列表看不出什么; 「定位 → CTA → 剪片 → 投放」这条四环链, 才指得出窄口在最上游那一环。

---

## 2 · 怎么展开 sessions

- **Command Base 是主 session, 只领活、派活、收活, 不在里面做重活。** 重活永远同一句: 「准备一个 handoff, 我去新的 session」。
- **Handoff 写完直接开 task chip** (Claude Desktop 有这个: handoff 写好, 点一下新 session 就带着它起来), 不用先开 session 再手贴。
- **新 session 第一句就是一行 handoff 路径**, 其他什么都不讲。进场包要自己讲完该讲的; 你在新 session 开场补充的每一句, 都是 handoff 漏掉的一句。
- **做完回主 session 的方式是贴 baton 路径**: 新 session 收尾会在 `00_Inbox/` 留一份 session report, 你把它的路径贴回 Command Base, 它读完就归档。⛔ 读过才准归档, 没读过不准动。
- **同一时间只有一个 session 在改 vault 正本; 其他 session 做产出, 做完由主 session 收进来一起 commit。** 并行的 git 机制 (worktree、branch) 不在这份里, 那是另一层的事, 先不碰。
- **主 session 要 ready 别的 session 在动东西。** 看到档案变了, 先当成是另一个 session 改的, 先看 diff 再动, 不要等人报, 因为人不会主动说。人报了的也要核: 「那张 task 我在另一个 session 做完了, 你帮我检查一下」。
- **产出独立、可以并行的活丢给 background agent** (写一篇文案、消化两份文档、出一版方案); 主 session 独占 git 跟 vault 的写入。
- **Session 太长要 compact 前, 先收口, 再要一个「compact 回来」的 prompt**, 重要的 context 才不会在压缩里漏掉。
- **关 session 前要它复述; 做大改前要它先写计划再动。** 「关之前, 复述一次我们今天定的东西」「你先把你的计划写给我看, 我再给 comment」。
- **EOD / compile 只在 Command Base 做**, 而且日期记事情发生那天: 半夜两点做 29 号的 EOD, 就是 29 号的, 不是 30 号的。

---

## 3 · 什么时候值得开一份新文档

- **一行指针不开档**, 放在它所属的 brief 一行。
- **值得开的三种**: 会一直长的正本兼素材库 (例如一份定位文档, 不只一段话, 还装得下 headline、金句、不同场景的文案); 要 future-proof 的登记簿, 一种东西一本 (例如活动的 WhatsApp 群链接登记簿); draft 要变成 project 的那一刻。
- **一份档只管一件事。** 登记簿只记「现在」, 历史另放。把「当前设定」跟「每一届发生过什么」塞进同一本, 两边都会漂。
- **讨论期间只写一份 working 文档**, 成品不回写 handoff, 也不急着进各处; session 完结才拆分 distill 进 vault。先回 master project brief, 成熟才升 brand asset。
- **关 project 先 graduate 再 archive**: 先看里面什么值得升进 master 夹或 master brief, 剩下的壳才归档。
- **Task 不是默认动作**: 没有 task 的事在 brief 上 remark 一行就好; 要正式讨论那天才针对性开 task; 自己会顺手处理的事不开 task。
- **Reminder、task、每年回来的, 是三种东西。** 一次性、只有一个时间点的, 开日历 event 就好 (Lark Calendar 或你用的日历), 不为它建耐久结构。Task 是挂在 project 底下、有前后依赖、会浮上 brief 跟 deck 的活。⚠️ 会每年回来的 (公司执照、车险这类) 要挂在它的 entity note 上用 `renew_by`, 让 deck 自己倒数; 我第一次就只开了日历没挂 `renew_by`, 那是我不对。

---

## 4 · 收尾分诊: 东西分到五处

- **一场活收尾, 手上的东西分五处, 每一处判进还是不进都要说出口**:
  - **Lesson**: 真的痛过的坑。
  - **cb: decision**: 还立着的裁定。
  - **auto-memory**: 跨 session 会忘的规矩 (「帮我记一个 memory: 以后这类图两边都存」)。
  - **Method 押后**: 可复用的做法, 等活真的关了才写。
  - **brief 一行 remark**: 「帮我 remark 一个点, 我怕我忘记」。
- **两套 memory 两套规矩**: `99_Meta/memory.md` 是两周内会用到的工作记忆 (session log); auto-memory 是跨 session 的指针与规矩。你说「记一个 memory」, 指的是后者。
- **状态跟裁定收法不同**: 状态照实翻牌 (做了就 done); 裁定要写成「刻意保留的不一致 + 别再提」, 否则下一场会重新发现同一个不一致, 再问你一次。
- **Memory 里的指针只准指夹不准指档** (夹的门要先读); **机器特定的事实一律写机器名**, 不写「这台机」, 因为记忆会同步到你另一台机上, 「这台机」到了那边就变假话。

---

## 5 · 指针怎么放, 怎么指外面

- **指针放在 session 会去找的地方, 不能只有 skill 自己知道。** 一支 skill 知道它的产出放哪没用, 下一场 session 不会读那支 skill; 指针要放在那场 session 会打开的 brief 里。
- **指针按用途命名, 不按东西本身。** 「WhatsApp 群头像」不叫「社群头像」; banner 是哪个社群的, wordmark 是哪个品牌的, 写清楚。名字清楚, 指针才清楚。
- **子品牌不抄母品牌**: 各自的 brand guide 放一个指针「先 reference 母品牌的 brand style」, 不各自抄一份颜色跟字体。
- **指外面 (Lark Base / wiki / 本机资料夹 / 线上页): 重物住外面, vault 只留一行指针加地址, 顺手把外面那边的命名规矩定了。** 例如广告图: 本机开一个夹放原档跟 prompt, 一份上你的 Lark Base, 档名定一个格式, vault 里一行指针。
- **给 session 东西的方式是贴绝对路径或链接**, 不描述「那个档」。
- **vault 也是手动步骤的贴板**: 要你手贴进某个后台的 code, 让它先开在 vault 那份 kit 档里、Obsidian 打开, 你贴完它再替换正本。

---

## 6 · folder 怎么 structure (宪法没管到的那层: project 夹里面)

- **一个 project 夹不只有 Tasks**: handoff、逐字稿、草稿、导出的档全住里面。要讲的是那个夹, 不是那张任务清单。
- **母子结构**: master project 夹按素材种类开子夹 (Sales、Landing-Page 这类); 每一届 (Cohort 01、Vol 03) 是自己的 project, 只装那一届的活; 一届关掉, 值得留的升进 master 夹。
- **重物住 vault 外面按品牌 / 活动分夹** (图、片、PDF、生图母版), vault 只装字跟指针。
- **提醒类的机制加在 Command Base 的 morning routine, 不加进 CLAUDE.md**: CLAUDE.md 是每场都读的法, morning routine 才是每天开门那一下。

---

## 7 · 日常几招

- **要决策的东西一多就开一个 temp HTML**: 让它出一页, 每笔一格排序一格备注, 填完贴回对话。我排二十几张 task 的顺序是这样做的, 审这份 playbook 的四十几条也是。
- **要持续追踪、有固定日子的 project 翻成 milestone**, 它就进 deck 的 countdown 跟 swimlane。
- **思绪乱的时候先讲出来让它整理, 不急着建东西; 流程乱就走 SORT。**
- **让它查你以为你知道的事**: 「日历上是不是已经排了?」「那支 skill 是不是已经装好了? double confirm 一下」。

---

## 附 · 把这份消化成你自己的 playbook: 贴给你的 Claude Code 的 prompt

先把这份 .md 存进你的 vault 的 `00_Inbox/`, 在你的 vault 开一个 Claude Code session (working directory 选 vault 根目录), 然后整段贴进去:

```text
我 00_Inbox/ 里有一份「Operating the Second Brain 学生版」, 是我老师每天怎么用第二大脑跑活的做法。
我要把它消化成我自己的 playbook, 不是照抄。请照下面的顺序做, 一步做完才做下一步。

1. 先读: 那份文档整份; 我 vault 的 99_Meta/structure-doctrine.md 的 §7 (playbook 是什么、怎么挣来的) 跟 §9 (playbook 夹跟它的门); 99_Meta/Templates/ 里的 Playbook.md 和 Playbook-Guide.md; 再看一眼 04_Methodology/Playbooks/ 底下现在有什么夹。
   如果我装了 breakthrough-method-builder 这支 skill, 用它的 Branch B (主人亲口要一份 playbook, 夹是空的, 从我怎么做的口述写起); 没装也没关系, 照模板手写是合法的。

2. 逐条跟我过, 一次一条, 不要一次丢一整节。文档有七块 (五个关口、十条判断、展开 session、开档、收尾分诊、指针、folder), 每一条问我同一组问题:
   「你现在是这样做的吗? 要采用、改成你的版本、还是不要?」
   我答「改」的, 追问我改成什么, 用我的话记, 不要替我润饰。
   我答「不要」的, 记下不进, 不要再提。
   我讲到「我其实是这样做的」而文档里没有的, 那条更值钱, 单独记下来。
   ⛔ 只有我亲口说进的才进。文档里的例子 (他的活动、他的品牌、他的坑) 一律换成我自己的, 我没有对应例子的那条就不带例子。

3. 全部过完, 用 Playbook.md 模板写一份 playbook, 三段照模板: When to run it · What to weigh · The moves。
   夹名 04_Methodology/Playbooks/operating-the-second-brain/ (照工作命名, 不带来源), 档名 operating-the-second-brain-playbook.md。
   frontmatter: type: playbook, lane 你照 §1 的四条 lane 判 (这种活通常是 run), status: forming, confirmed_by_owner: false, references 留空 list (我还没有它靠着的 lesson 或 decision), tags 留空。
   写完先给我看整份, 我说「可以」你才把 confirmed_by_owner 翻 true。我没说, 就一直是 false。

4. 同一口气写夹的门: _Operating-The-Second-Brain-Guide.md, 形状只准从 Playbook-Guide.md 模板抄, 四拍用你自己的话写, 上半是这份 playbook 的摘要, 下半那张表空着是对的。

5. 收尾三件, 同一场做完: 02_Command-Base/Home.md 那行 04_Methodology/Playbooks/ 加上这个夹名; 你自己的记忆 (auto-memory) 加一行指针, 指夹不指档; 99_Meta/filing-log.md 加一行。
   然后把 00_Inbox/ 那份学生版搬去 98_Archive/, 档名不变: 它是种子, 种完就归档, 我的正本是我自己那份。

写的时候: 我的话就是我的话, 不要改成文档腔; 一条听起来像说明书, 就是写错了。
```

跑完你会有: 一支自己的 `operating-the-second-brain/` 夹 (playbook + 门)、Home 一行、一条记忆指针、一行 filing-log, 而且里面每一条都是你亲口说进去的。三个月后回来看门的下半, 那张表会告诉你这套做法在你身上到底有没有用。

---

*从内部 playbook 干净重写, 2026-09-04。内部那份改了, 这份跟着重推。*
