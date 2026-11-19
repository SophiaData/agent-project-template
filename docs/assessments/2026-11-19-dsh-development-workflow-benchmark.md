# DSH Development Workflow Benchmark：文档同步与 Agent 代码协作

- 日期：2026-11-19
- 基准仓库：[deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)
- 对标仓库：[SophiaData/agent-project-template](https://github.com/SophiaData/agent-project-template)
- 对标版本：模板 v2.6.0（master）
- 关联：[Issue #14](https://github.com/SophiaData/agent-project-template/issues/14)、[总体治理审计 PR #13](https://github.com/SophiaData/agent-project-template/pull/13)
- 范围：需求分解、跨 Agent 协作、文档与代码同步、Commit/PR、Pre-push、Review 和 Merge
- 审计性质：对源码、规则、文档和 CI 接线的静态核对；未执行真实 DSH Team、多 IDE 子代理或跨仓库集成验收

## 1. 结论与纠偏

目前模板缺的主要不是“提醒 Agent 写文档的语句”，而是可以证明文档和代码同步、任务分工没有重叠、PR 范围可审查、合并门禁没有漂移的**可执行交付契约**。

- DSH 对特定 package 的行为变更明确要求：README 和 JSDoc 与行为**同一 Commit**更新；它还有文档模板、单一事实来源、语义审查 Skill 和可执行文档检查。模板目前要求“同一 change”，但无面向消费项目的文档影响检测器。
- DSH Team 有带 expectedRevision 的任务认领及依赖关系、有 writeScopes 重叠提示；**没有**原生 worktree/文件写锁/跨进程协作，重叠路径警告不是强制隔离。模板不能仅凭 AGENTS 声称实现这些能力。
- DSH 支持 GitHub 原生 Stacked PR 生命周期和按层审核；这不是“所有大需求必须多个 Commit”。**一个原子 Commit、一个小 PR**可以是合理结果；混合无关变更的大 PR 才是核心问题。
- DSH 的 doc-sync 是一组结构/链接/配对/引用/产物新鲜度等检查，不可能自动证明每段说明都语义正确。真实行为、默认值、错误和限制仍要与源码及测试互相核验。

本次仅提出设计方案，没有将任何检查“已实现”或“真实宿主行为已验证”作为事实。

## 2. DSH 实证机制

| 环节 | DSH 的可核验机制 | 可靠性意义 | 必须保留的边界 |
|---|---|---|---|
| 文档分层 | docs/AGENTS.md 定义 one home per fact、文档层级与预算 | 避免多处复制造成漂移 | 不等同于自动识别语义过期 |
| 行为同步 | packages/AGENTS.md 要求 package README + JSDoc 与行为同一 Commit | 同一历史变更有完整契约 | 不是所有纯内部改动都要改 README |
| 文档作者工作流 | dsh-doc-writing、dsh-prose-standard、引用代码/测试事实；翻译配对同一轮更新 | 有可复核的执行步骤 | 不能把“看起来写了”当成命令执行证据 |
| 文档门禁 | test:docs、doc-sync、verify-md-links、verify-export-jsdoc、README 元数据/摘要/限制检查 | 结构问题在 CI 发现，而非等人为遗漏 | JSDoc 自动检查只对应其 TypeScript 生态；其它栈要自选 |
| 计划 / Todo | Plan 计划审阅、Todo 单 Session 任务清单 | 需求分解和过程可追踪 | Plan Guidance 不是强制 Sandbox；Todo 不是跨 Agent 共享板 |
| Team 协作 | Team task expectedRevision CAS、依赖、owner、writeScopes 警告 | 避免过期认领覆盖；识别路径争抢 | 同一 checkout，无 worktree 隔离、自动 owner 回收或跨进程锁 |
| Pre-push | change-scope 明确收集 committed/staged/unstaged/untracked；选相关检查 | 不漏掉未提交或未跟踪文件 | 本地 hook 只做轻量检查；全面验证在 CI |
| PR 内容 | dsh-pr-description 规范 Motivation、Changes、Testing、AI Usage，要求 PR 随后续改动更新 | 测试和变化与真实 diff 对齐 | PR 描述仍需 Reviewer 验证 |
| 独立 Review | dsh-code-review 读取当下 base/head、文件作用域、规则和源码 | 防止用旧 diff 评审新修改 | 自动检查不能替代语义审查 |
| 分层交付 | dsh-merging-stacked-prs 强制验证 GitHub 原生 Stack 对象、依赖、审查和重新同步 | 大功能分层，每层独立审查 | 仅在官方 Stack 可用时采用；不做私有模拟协议 |

### DSH 直接证据

- [Root AGENTS.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/AGENTS.md)
- [Package AGENTS.md：same commit 文档规则](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/AGENTS.md)
- [Documentation AGENTS.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/AGENTS.md)
- [dsh-doc-writing](https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/skills/dsh-doc-writing/SKILL.md)
- [dsh-prose-standard](https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/skills/dsh-prose-standard/SKILL.md)
- [文档检查聚合 runner](https://github.com/deepseek-ai/deepseek-harness/blob/master/scripts/run-gates.ts)
- [verify-md-links](https://github.com/deepseek-ai/deepseek-harness/blob/master/scripts/verify-md-links.ts)
- [verify-export-jsdoc](https://github.com/deepseek-ai/deepseek-harness/blob/master/scripts/verify-export-jsdoc.ts)
- [doc-standard tests](https://github.com/deepseek-ai/deepseek-harness/blob/master/scripts/doc-standard.spec.ts)
- [Lefthook（staged checks）](https://github.com/deepseek-ai/deepseek-harness/blob/master/lefthook.yml)
- [开发文档中的 Git hook 边界](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/development.md)
- [change-scope](https://github.com/deepseek-ai/deepseek-harness/blob/master/scripts/change-scope.ts)
- [dsh-pre-push-checks](https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/skills/dsh-pre-push-checks/SKILL.md)
- [dsh-code-review](https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/skills/dsh-code-review/SKILL.md)
- [dsh-pr-description](https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/skills/dsh-pr-description/SKILL.md)
- [dsh-merging-stacked-prs](https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/skills/dsh-merging-stacked-prs/SKILL.md)
- [Team 运行时契约与限制](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/team/agent-team/README.md)
- [Todo 单 Session 所有权](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/todo/tool-todo/README.md)
- [Workflow 生命周期与取消](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/workflow/tool-workflow/README.md)

### “DSH 文档一直同步得很好”的证据范围

上述文件可以证明 DSH **设计并维护了一套强约束的协作机制**，不能从中直接证明所有历史 PR 从未漏文档、从未出现过大提交，也不能把未做过的运行时测试表述为 PASS。

## 3. 模板 v2.6 的实际差距

| 模板现状 | 已存在的内容 | 缺口（不是重写文案能解决的） |
|---|---|---|
| root AGENTS 与 docs/AGENTS | 文档与测试同步要求、单一事实来源 | 没有确定“这次变更属于哪个文档 owner”的结构化证据 |
| project-implement / project-doc-writing | 提醒写文档和核对示例 | 没有 Task Completion / PR Gate 检查是否完成 |
| project-pre-pr | 人工检查 docs / tests / PR 完整性 | 没有针对源文件改变的文档 Impact 报告或负向测试 |
| docs/git-workflow.md | 单一逻辑变更、Reviewable commits、保护操作 | 缺少可执行的原子变更识别、PR 拆分标准和合并历史选择说明 |
| scripts/run_quality.py | BASE...HEAD 路径选择，source 变更必须选测试 | 只覆盖 committed；无统一 staged/unstaged/untracked 预检 |
| quality.yml | 模板契约测试、治理检查、项目质量命令 | 消费项目文档与 API 的专项 gate 需要额外配置 |
| PR template | 动机、范围、测试设计、证据、AI 援助声明 | 缺文档 owner 的变更矩阵、PR 拆分说明与交接证据 |
| Agent 执行管理 | 通用 Skills 可被多宿主读取 | 没有统一 Task Handoff 合约、host capability 级别或 worktree 冲突隔离 |

核对位置：
[当前 AGENTS.md](https://github.com/SophiaData/agent-project-template/blob/master/AGENTS.md)、
[project-implement](https://github.com/SophiaData/agent-project-template/blob/master/.agents/skills/project-implement/SKILL.md)、
[project-doc-writing](https://github.com/SophiaData/agent-project-template/blob/master/.agents/skills/project-doc-writing/SKILL.md)、
[project-pre-pr](https://github.com/SophiaData/agent-project-template/blob/master/.agents/skills/project-pre-pr/SKILL.md)、
[docs/git-workflow.md](https://github.com/SophiaData/agent-project-template/blob/master/docs/git-workflow.md)、
[run_quality.py](https://github.com/SophiaData/agent-project-template/blob/master/scripts/run_quality.py)、
[quality.yml](https://github.com/SophiaData/agent-project-template/blob/master/.github/workflows/quality.yml)。

## 4. 新项目交付生命周期（目标设计）

一个任务从 Issue 到 Merge，必须有明确的责任人、验证证据和状态边界。步骤如下。

### 4.1 Requirement & Planning

输入：Issue、用户需求、现有架构及约束。

必须输出：
- Scope / Non-goals / Acceptance Criteria；
- 受影响的模块与数据/接口边界；
- Documentation Impact：准确指出文档 owner，或给出不需要文档更新的依据；
- Test Plan：能发现回归的测试类型及环境；
- Delivery Units：需要单 PR、多个独立 PR，还是原生 Stack；
- 并行任务及写入范围/依赖关系；
- 需要人工批准的危险操作。

没有 Document Impact 的计划视为未完成；但“没有文档变更”可以是合理结果，必须有具体理由。

### 4.2 Task Assignment & Ownership

每个委派任务具有：
- task_id、parent_issue、objective、acceptance、depends_on；
- owner/agent_id、host、status；
- exclusive 或 advisory write_scopes；
- branch/worktree 身份及基线 Commit SHA；
- documentation_owner、tests_owned；
- handoff_revision 与交接证据位置。

若宿主提供 DSH Team，可使用其 expectedRevision Task CAS；若宿主不提供，共享任务更新不能假装原子，需要明确的协调者或外部任务服务；没有隔离能力时采用同一模块串行交付。

**保护边界：**
- writeScopes 提示不等于文件系统访问控制；
- 不允许多个 Agent 同时独立提交同一 checkout 内的同一文件；
- 子 Agent 交接不等于自动授权 commit/push/merge；
- Agent 自述任务完成不足以证明产物存在，协调者必须回读文件、diff、测试结果。

### 4.3 Implementation & Documentation in the Same Change

每一个可以审查的行为单元应按以下顺序完成：

1. 在模块边界内实现代码及回归测试；
2. 判断 public API/config/schema/tool/CLI/runtime 行为是否变化；
3. 对照源码事实同步 README、API Reference、JSDoc/Docstring、架构或升级文档；
4. 执行相关生成器并比对派生文档；不得手改自动生成文档；
5. 运行聚焦测试和文档检查；
6. 查看 staged diff，仅提交同一逻辑单元涉及的文件；
7. 向协调者报告文件路径、Commit SHA（若有）、检查证据和未解决风险。

继承 DSH 的 “same commit” 精神：**某一个 Commit 改变了对外合同，原则上该 Commit 包含对应文档**。纯内部重构不强制生成无意义 README 修改。若某项目允许 PR 级文档更新而非逐 Commit 同步，应在策略中显式声明并接受历史层面的可追溯性差异。

### 4.4 Local Pre-push

- Fetch/确认真实 base 和当前 head；
- 同时读取 committed、staged、unstaged、untracked 四个 Git 平面；
- 排查未跟踪的业务文件、敏感信息、冲突标记及生成内容；
- 按行为变更选择 tests/typecheck/docs/schema 等最小必要 Gate；
- 明确区分 PASS / FAIL / NOT RUN / BLOCKED；
- Hook 应保持快速，完整验证仍由 CI 负责；
- 后续代码变更导致证据失效时只重新运行相关检查。

### 4.5 PR & Review

每层 PR 都必须能独立说明：
- Issue 与验收目标；
- Changed behavior / API / Config / Schema；
- Documentation Impact：Updated 或 No update required + reason；
- Test design 与可复核运行证据；
- Agent/人类任务所有权和实际写入范围；
- Compatibility / rollback；
- 明确已知限制和剩余人工验收。

Reviewer 以**当前** base/head 评审实际 diff，先读文档 owner 和测试证据，再核对行为是否正确、遗漏 doc 是否真实存在。PR 后续修改须同步更新描述。Review 不是检查每个目录都有 README，而是检查本次变化的用户/开发者可观察合同是否得到准确描述。

### 4.6 Merge & Post-merge

- 分层 PR 只有在下层依赖已满足、对应 CI/Review 均新鲜时才可合并；
- 原生 Stack 可用时按 GitHub 原生语义检查；不可用时明确降级为普通聚焦 PR，不伪造 Stack；
- 合并前刷新 base/head SHA、未解决 Review Threads、权限和 Required Checks；
- Squash / Rebase / Merge Commit 的选择是**仓库历史策略**，不能用 Commit 数量评判工程质量；
- Merge 后核对主分支提交、CI 与文档投影；生产部署和 DataWorks 节点提交/发布仍需人工授权。

## 5. 可执行门禁设计（下一阶段实现，而非本 PR 的功能）

### 5.1 Documentation Impact Contract

**设计原则**：先建立代码路径到“权威文档 owner”的可配置映射，再选择有事实支持的守卫。

建议新增独立的 docs-impact 配置（示意格式，不是已经发布的 schema）：

~~~json
{
  "version": 1,
  "rules": [
    {
      "id": "public-api",
      "sourcePaths": ["src/api/**", "packages/*/src/**"],
      "ownerPaths": ["docs/api/**", "packages/*/README.md"],
      "severity": "review"
    },
    {
      "id": "configuration",
      "sourcePaths": ["config/**", "schemas/**"],
      "ownerPaths": ["docs/configuration/**", "docs/compatibility.md"],
      "severity": "review"
    }
  ]
}
~~~

此 JSON 是实现讨论用的示意，真实设计必须解决参数化路径映射、重命名、文档不存在、owner 优先级和异常语义；不能直接以任意 Markdown 修改满足任意 API 变更。

**初始实现：**
- 先生成 Doc Impact 报告与可能过期的 owner 文件；
- 若 source 变化匹配规则但无 owner 更新，要求 PR 明确“确实无行为改变”的具体证据；
- 可机械证明的文档约束（链接、标题、元数据、生成文件一致性）设为 blocking；
- 语义完整性采用 Reviewer Gate，不能假装 grep 或 LLM 自评能够证明；
- 避免简单“每个代码 PR 必须改 Markdown”的形式主义；
- 对 README/JSDoc 同 Commit 的强化模式仅在项目明确采用时启用，不设为所有技术栈通用默认。

### 5.2 Scope & Commit Review

工具输出应包含：
- baseSha、headSha、mergeBaseSha；
- committed、staged、unstaged、untracked；
- 每个提交触及的文件集合与说明；
- module/Issue/scope 归属提示；
- 文件大范围修改与文档/测试缺口候选项。

门禁不应以“超过 N 行或只有一个 Commit”为阻断条件，因为自动生成文件、版本迁移、大规模可证明机械改动都可能合理。

推荐两个等级：
- **warn**：一个 PR 触及多个互不相干的业务模块、多个 Issue 或同时改变无关配置和逻辑；
- **block**：超出明确允许的写入范围、混入凭据、来自不可信 PR 的发布命令、损坏的格式/链接、缺失 Required Tests、错误地声称 Docs/Gate PASS。

原子性由“一个变更单元是否有可理解的目的、可观察的测试和回滚边界”判断，而非单凭提交数。

### 5.3 Agent Handoff Contract

标准化完成报告字段：
- task_id、owner、base/head、files_changed、docs_changed、tests_executed；
- result: PASS/FAIL/NOT RUN/BLOCKED；
- known_risks、conflict_with、next_owner；
- evidence links；
- 不做任何未经授权的 push/merge/deploy。

Host adapter 只需能提供任务状态和工具执行证据即可；DSH Team、Claude Code、Codex、Cursor 可以有不同底层实现。缺少可靠并行隔离能力时强制串行执行，不用 Markdown 模拟共享锁。

### 5.4 可靠性与负向控制

| 场景 | 预期 |
|---|---|
| API 字段变化但 owner 文档缺失 | Doc Impact warning / blocking（按规则）并给出精确 owner |
| API 变化但提交任意 README 凑数 | 仍报告 owner 未满足 |
| 纯内部优化且无文档影响 | 合法 No update required，不强制文档改动 |
| 生成文档落后于源码 | generator freshness Gate FAIL |
| Markdown 目标存在但 fragment 不存在 | link Gate FAIL |
| 代码改变、Docs 检查未执行 | NOT RUN，不能声明 PASS |
| 多个 Agent 认领同一 task 版本 | 过期 revision 操作被拒绝 / 需要人工协调 |
| Agent 重叠写入同一 checkout | 报警并避免无隔离的并行写入 |
| 修改 PR 后仍引用旧 CI 结果 | 审查新鲜度复核失败 |
| 错误的 Git base/不完整历史 | fail closed，不当成空 diff |
| 故障中断/重复执行检查 | 可重入、幂等、保留可审计结果 |
| 一个聚焦功能只有一个 Commit | 合法，不应凭数量拒绝 |
| 单 PR 包含无关联 Issue 与跨模块变更 | Review 提醒拆分/改用 PR Stack |
| 主分支启用 Squash | 说明历史策略，不错误指责 Agent |

## 6. 分阶段 PR 路线图

### P0：可靠性基础（建议下一轮优先）

**PR-A：Development Scope + Handoff Contract**
- 为当前 project-implement、project-plan、project-pre-pr 增加统一交接契约；
- 规范 committed/staged/unstaged/untracked 的变更报告；
- 与当前 run_quality.py 的 --base 行为兼容，不替换现有 schema V2；
- 对不可信路径、错误 base、空测试集增加负向控制。

**PR-B：Documentation Impact v1（report-only）**
- 新建可配置 doc owner 映射；
- 输出机器可读 JSON + 人类可读摘要；
- GitHub Actions 生成 warning，而非误报阻断；
- 新建测试覆盖公共 API/配置变更、无影响、错 owner、重命名和删除；
- 先针对消费项目的约定路径，不修改 DSH/Agent 宿主内核。

### P1：文档与 PR 质量

**PR-C：Focused Docs Gates**
- 为 TypeScript/Python/Java/SQL 或 dbt 选择对应的公开契约/Schema 检测器；
- 增加链接 fragment / README metadata / generated artifact freshness 等可确定的 Gate；
- 模板只提供规范和扩展点，消费项目按技术栈声明实际命令；
- Docs Impact Gate 从 warning 升级到“owner 更新或有可审查例外”的阻断，例外本身必须说明理由。

**PR-D：Atomic Change + PR Scope Governance**
- 变更范围归属和 PR 交付单元审查；
- PR 描述中的文档和测试矩阵；
- 模板规定 Merge Commit / Rebase / Squash 的可配置历史策略；
- 优先提示而非依据行数/Commit 数硬阻断；
- 每层 PR 独立审查，可选 GitHub 原生 Stack，不自行实现变基协议。

### P2：跨 Agent 协作可靠性

**PR-E：Task Ownership & Worktree Adapter Contract**
- 定义 Task/Agent/WriteScope/Revision/Dependency 协作契约；
- 宿主能力声明：native / adapter / unsupported；
- DSH Team 的任务 CAS 与实际文件隔离分别标记；
- 宿主不支持可靠任务认领或隔离时自动退回串行调度，而不是假装安全并行；
- 通过实际 DSH、Claude Code、Codex、Cursor 运行时验收之后，再声明具体适配已经支持。

**PR-F：Reliability & Recovery**
- 任务交接与 PR 证据完整性；
- 多 Agent 竞态、文件覆盖、过期状态、部分提交、失联与重试；
- 重新读取 Git/文件最终状态，不依赖 Agent 自报成功；
- 不提供自动合并/部署/生产发布。

## 7. 可靠性设计底线

1. **事实唯一归属**：源代码、机器生成 API Reference、README、Agent Notes 分工；不得维护多个手写重复事实源。
2. **约束靠所有者执行**：文档检查属于项目 CI；提交范围属于 Git；Team owner 属于宿主任务服务；权限属于真实 OS/仓库设置。Prompt 本身不是强制隔离。
3. **Fail closed 只针对可验证关键风险**：不可信 Git ref、缺少必需测试、权限越界应拒绝；语义是否要改文档需要提示并由 Reviewer 判定，不允许粗暴误封。
4. **最小可行检查**：本地 hook 轻量；CI 更完整；没有必要因每次 push 重新执行无关、已证实有效的耗时测试。
5. **证据新鲜度**：Commit SHA、PR head/base 和 Gate 结果成组记录；代码或依赖变化导致相关证据过期必须重新验收。
6. **安全边界**：不允许运行来自 PR 分支的不可信脚本并同时持有写 token；不允许自动合并和任何生产发布。
7. **历史可追溯**：保留或 Squash 的权衡由仓库政策决定；每个 PR 必须具备独立可审查/回滚范围。
8. **兼容性优先**：project-policy.json schema V2 不强制迁移；从报告模式逐步启用阻断，支持旧项目有控制地升级。

## 8. 明确不复制 DSH 的部分

- 不强迫每个新项目采用 DSH 的 TypeScript JSDoc / 中英 YAML 配对 / 完全相同 README 模板。
- 不把 GitHub 官方 Stacked PR 当成所有 Git 平台都有的原生能力。
- 不把 Team writeScopes 警告当成工作区锁，也不把 Session Todo 当成 Team Board。
- 不规定一个 PR 必须有多个 Commit，不因 Squash Merge 直接否定 Agent 的代码质量。
- 不靠文档计数来定义“文档同步”，不靠 Markdown 修饰掩盖文档语义过期。
- 不因为“模板规范已经写了”就认为所有 Agent 或 SubAgent 都已经执行。

## 9. 最终交付结论

当前模板已经具备通用工程规范框架；下一阶段最值得学习的是 DSH 的**文档 owner + 同步变更 + 分层检查 + 独立审查**以及**任务 owner + 增量验证 + 聚焦 PR**组合，而不是复制 DSH 内核。

建议先实现 P0 的 Scope/Handoff Contract 与 Documentation Impact report-only，配套真实负向控制与 CI 证据；再逐步升级为 blocking Gate，最后才扩展跨 Agent 并发和失败恢复。

**本文件是专项审计与设计，不是已实施功能说明。** CI 能验证文件格式与现有仓库约束，但不证明这些提议已经投入运行。
