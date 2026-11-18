# DSH 工程治理成熟度对标审计

- 审计日期：2026-11-18
- 对标仓库：[deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)
- 被审计仓库：[SophiaData/agent-project-template](https://github.com/SophiaData/agent-project-template)
- 被审计版本：2.6.0
- 范围：仓库工程管理、Agent 开发流程、通用工程治理与可靠性
- 性质：代码/文档/测试/Workflow 静态审计；不是线上 GitHub Project、分支保护或 Agent 宿主行为的实测报告

## 1. 执行摘要

结论：当前模板已经建立了可复用的工程规范基础，但还没有形成 DSH 水平的项目生命周期管理、PR 审批治理、决策知识生命周期和多 Agent 执行追踪。

最重要的发现不是“少几个 Skill”，而是两者承担的产品职责不同：

1. agent-project-template 是一个项目工程治理模板。它告诉项目和 Agent 应该遵循什么规则，并提供有限的本地/CI 验证工具。
2. DSH 同时是一个大型 Agent Harness 产品，以及一个有成熟 GitHub 工程流程的产品仓库。它既有仓库级 Issue/PR/CI/Notes 治理，也有运行时 Plan、Todo、Goal、Team、Workflow、Jobs 等能力。
3. 不应该把 DSH 的运行时功能伪装成模板 Skill，也不应该为了通用性重新实现一个 Agent Harness。应通过宿主能力适配契约使用已有能力。

因此，之前提出的“40%”不作为本次结论。本报告不使用单一百分比，而采用“已具备 / 部分具备 / 缺失 / 宿主提供 / 未验证”分类。

### 核心结论

- **工程规范：已有较好的通用基础。** AGENTS、架构、编码、测试、防御性模式、错误处理、兼容性、Skills 和 PR 模板已经存在。
- **项目管理：差距最大。** 没有 Issue taxonomy、GitHub Project 状态模型、Issue/PR 生命周期自动化、审计和对账。
- **PR 治理：只有流程指导，缺少机器强制。** 还没有 DSH 式的审批策略、审查新鲜度、Stacked PR 管理和合并前策略验证。
- **CI：有通用基础，但执行引擎较简单。** 当前质量检查是路径选择 + 顺序执行；没有 DSH 那样的变更范围完整采集和依赖 DAG 调度。
- **知识治理：有 ADR，但没有完整生命周期。** 缺少提案/实施/拒绝/归档的结构化校验、自动 supersession 检查和不可变归档封存。
- **Agent 执行管理：模板不负责实现。** 应定义 DSH、Claude Code、Codex、Cursor 的能力适配接口和降级规则，不复制其内部状态机。

## 2. 审计方法与证据边界

本次以两个仓库在审计时可读取的 master 文件树和实际源文件为依据。重点检查 DSH 的 Issue policy/lifecycle、PR approval、pre-push/CI、Agent Notes、Plan/Todo/Goal/Team/Workflow/Jobs，以及模板中的 AGENTS、Skills、project-policy、验证器、质量执行器和 GitHub Actions。

仓库规模仅用于理解职责范围，不作为成熟度评分。DSH 是完整产品代码库，模板是轻量复用起点，不能用文件数量直接比较质量。

### 未验证项

以下需要仓库管理权限或真实运行环境，不能从公开文件树得出结论：

- agent-project-template 的 master 分支保护、Required Status Checks、Required Reviewers、Merge Queue 实际配置。
- 组织级 GitHub Projects 是否存在、字段权限、App 安装范围和 token 实际权限。
- DSH Workflow 的真实事件投递延迟、GitHub App 安装健康度、Actions 成本与线上失败率。
- DSH、Claude Code、Codex、Cursor 在具体项目中的真实指令加载、Session 恢复和 SubAgent 行为。
- 本报告未修改任何 GitHub Project、分支保护、生产系统或 DataWorks 节点。

## 3. 能力成熟度矩阵

| 能力域 | 当前模板状态 | DSH 对标证据 | 主要差距 |
|---|---|---|---|
| AGENTS / 指令链 | 部分具备 | 分层指令、宿主加载约定、目录作用域规则 | v2.6 是静态预检，不证明真实宿主注入或 Agent 遵守 |
| 架构 / 编码规范 | 已具备基础 | 分层架构、Defensive Patterns、模块所有权 | 模板验证器主要验证文档结构，消费项目仍需项目级架构守卫 |
| Skills | 部分具备 | 22 个专项 Skill，按场景路由 | 目前 9 个通用 Skill，缺少 Issue 生命周期、CI 可靠性、Notes 归档、Stacked PR 等专项流程 |
| Issue / Project 管理 | 缺失 | Issue taxonomy、7 状态 Project、类型/优先级/Area 约束 | 没有 Issue 模板、字段模型、状态转换、Project 自动化 |
| Issue 生命周期 | 缺失 | 事件驱动的 Project 状态更新、标签修复、审计评论 | 没有事件入口、幂等账本、重试、对账或修复机制 |
| PR 元数据治理 | 部分具备 | PR 引用 Issue、kind/area/priority 校验 | 只有 PR 文档模板，没有机器校验 |
| PR 审批 / Review | 部分具备 | Weighted approval、Changes requested 阻断、状态发布 | 没有审批策略、Reviewer 权限判断、审批过期/新提交后重审规则 |
| Merge / Stacked PR | 缺失 | 专用 Stack Skill、原生 gh stack 流程、逐层检查 | 没有 Stack 依赖图、层级合并与重写后复验 |
| CI / 质量门禁 | 部分具备 | 多层 CI、Gate DAG、平台矩阵、性能与 Snapshot 门禁 | 当前单 Job、顺序执行、无 Gate 依赖图和统一资源调度 |
| 变更范围识别 | 部分具备 | change-scope 同时采集 committed/staged/unstaged/untracked | 当前 run_quality 只根据 BASE...HEAD 已提交差异选择 |
| 测试可靠性 | 部分具备 | 测试隔离、资源恢复、并发、取消、真实 API、负向控制 | 模板有测试原则和负向控制，但缺少通用测试可靠性专项 Skill/执行契约 |
| 决策知识生命周期 | 部分具备 | Agent Notes proposed/implemented/rejected/archived、封存清单 | 当前 ADR 仅有状态约定，没有结构验证、归档封存和 supersession 自动审查 |
| Agent 任务状态 | 宿主提供 / 模板缺失 | DSH Todo、Plan、Goal | 模板没有宿主能力契约和统一状态映射 |
| 多 Agent 协作 | 宿主提供 / 模板缺失 | DSH Team、Workflow、Subagent | 模板没有任务所有权、共享状态、冲突和工作区隔离适配规范 |
| 后台任务 / 恢复 | 宿主提供 / 模板缺失 | DSH Jobs、Session 持久化、取消和完成通知 | 没有跨宿主 Job 状态映射和异常恢复契约 |
| 安全与权限 | 部分具备 | trusted default-branch checkout、最小权限、App token 分权 | 当前只有只读 CI；未来写入型自动化必须先建立权限和信任边界规范 |
| 状态一致性与恢复 | 缺失 | DSH 明确记录事件驱动与无 CAS 的限制 | 需要在 DSH 已有机制上增加 reconciliation、幂等和冲突保护 |

## 4. DSH 中值得继承的成熟设计

### 4.1 Issue / Project：把项目管理做成明确状态机

DSH 的 Issue 管理不是只有模板和标签。它定义了：

- Issue Type：Idea、Feature、Bug、Research、Task。
- Project Status：Inbox、Backlog、Ready、In progress、In review、Done、No action。
- PR 元数据：一个 canonical kind、至少一个 area、最多一个 priority。
- 同仓库 Issue 引用；Resolving reference 的优先级需要与 PR 规则一致。
- Issue 打开、关闭、重开、PR 打开、Review requested、Changes requested 等事件驱动状态变化。
- PR 打开时初始化 Start Date。
- Issue 标签违规修复和带稳定 Marker 的审计评论。

证据：
- [Issue management README](https://github.com/deepseek-ai/deepseek-harness/blob/master/.github/issue-management/README.md)
- [config.json](https://github.com/deepseek-ai/deepseek-harness/blob/master/.github/issue-management/config.json)
- [rules.mjs](https://github.com/deepseek-ai/deepseek-harness/blob/master/.github/issue-management/rules.mjs)
- [pull-request.mjs](https://github.com/deepseek-ai/deepseek-harness/blob/master/.github/issue-management/pull-request.mjs)
- [lifecycle.mjs](https://github.com/deepseek-ai/deepseek-harness/blob/master/.github/issue-management/lifecycle.mjs)
- [policy.test.mjs](https://github.com/deepseek-ai/deepseek-harness/blob/master/.github/issue-management/policy.test.mjs)

该 Issue policy 测试文件包含 48 个 Node test case。其规则逻辑、GitHub 传输、PR 只读快照和生命周期编排被拆分在不同模块中。这种模块所有权和纯规则测试方式值得直接借鉴。

### 4.2 DSH 自身也有已知限制，不能照搬为最终设计

DSH 的 Issue management README 明确承认：

- Lifecycle 是 event-driven，不是 reconciler；遗漏的事件不会自动修复 Project 状态。
- GitHub Project 并未提供这里需要的原子 compare-and-swap；并发状态修改存在竞态。
- Priority 是 Project custom field，手工维护，不自动同步原生 Issue Priority。
- selective preflight 不代表完整的 Required Check 权限模型，也不保证实际 Actions 成本下降。

lifecycle.mjs 中还留有明确 TODO：需要以 per-Issue serialization 或 conditional update 替代 latest-state guard。

**我们的目标应是继承 DSH 的状态机、模块拆分、最小权限和测试设计，同时增加事件去重、可恢复执行和定期对账。** 不能声称 GitHub Project 的字段写入具有 CAS；如果远端不提供原子条件写入，就需要用串行化写入、版本/租约、写后回读和冲突检测降低风险。

### 4.3 PR 审批：决策与状态发布分离

DSH 的 Weighted Approval workflow 值得研究的点：

- 每个 PR 独立并发组，避免同一 PR 多次评估相互覆盖。
- 先撤销旧的成功状态，再进行依赖安装和新一轮评估，避免失败后残留旧绿灯。
- 评估未完成时保持 pending；依赖安装或评估失败时发布 error。
- 审批决策由独立 GitHub App 发布稳定身份的 Check/Status。
- Draft、Changes requested、审批分数不足等状态都有明确结果。
- policy 从 trusted default branch 加载，不运行 PR 分支中的写状态代码。

证据：
- [weighted-approval.yml](https://github.com/deepseek-ai/deepseek-harness/blob/master/.github/workflows/weighted-approval.yml)
- [check-approval.mjs](https://github.com/deepseek-ai/deepseek-harness/blob/master/.github/review-ownership/check-approval.mjs)
- [approval policy README](https://github.com/deepseek-ai/deepseek-harness/blob/master/.github/review-ownership/README.md)

Reviewer 权重、团队成员名单和分数阈值是 DSH 自己的组织策略，不应复制到通用模板。我们应抽象审批接口、权限判定、审批失效规则和稳定状态发布机制。

### 4.4 CI：变更范围、依赖 DAG 和资源调度

DSH 的 pre-push Skill 使用 change-scope 工具读取：

- committed changes；
- staged changes；
- unstaged changes；
- untracked files。

模板的 run_quality.py 当前通过 BASE...HEAD 获取 committed changes。docs/testing.md 已说明未提交变更需要执行全量配置检查。这是可用但不够精细的本地工作流。

DSH 的 run-gates.ts 则提供 Gate DAG：
- needs / after 依赖；
- 有界并发；
- fail-fast；
- 可控 retry；
- 子进程输出和退出诊断；
- 取消和进程信号处理；
- 按 CI 模式配置资源预算。

证据：
- [change-scope.ts](https://github.com/deepseek-ai/deepseek-harness/blob/master/scripts/change-scope.ts)
- [dsh-pre-push-checks Skill](https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/skills/dsh-pre-push-checks/SKILL.md)
- [run-gates.ts](https://github.com/deepseek-ai/deepseek-harness/blob/master/scripts/run-gates.ts)
- [Testing policy](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/testing.md)

DSH 的测试分层还包括 Unit、Coverage、Real API E2E、Expected Output、Snapshot、Web Browser Snapshot 和 Performance。模板不应强制所有项目采用 DSH 的 100% per-file coverage；应按项目技术栈和风险配置可证明的质量门禁。

### 4.5 Agent Notes：从 ADR 升级为知识生命周期

DSH 的 Agent Notes 不只是决策文件目录：

- proposed：等待评审的方案；
- implemented：已经落地且需与代码事实保持一致；
- rejected：保留仍能防止重复踩坑的否决理由；
- archived：保留历史价值的冻结记录。

它还要求：
- 新增 Note 时检查重复与 supersession；
- 维护相对链接；
- 英文、中文和 sidecar 配套；
- 归档时保留完整 triplet；
- 使用 append-only manifest 对归档文件做内容封存；
- 归档后禁止修改。

证据：
- [Agent Notes README](https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/notes/README.md)
- [Agent Notes AGENTS.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/notes/AGENTS.md)
- [verify-archived-agent-notes.ts](https://github.com/deepseek-ai/deepseek-harness/blob/master/scripts/verify-archived-agent-notes.ts)
- [dsh-archive-agent-notes Skill](https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/skills/dsh-archive-agent-notes/SKILL.md)

模板现有 ADR 状态约定是好的起点，但没有对应的自动化验证和冻结归档能力。

## 5. DSH Agent 执行能力：必须与仓库治理分开

这些是 DSH Harness 的运行时能力，不等于 GitHub 项目管理：

| DSH 能力 | 实际职责 | 重要边界 |
|---|---|---|
| Plan | 执行前探索、设计、提交计划供人审批 | Plan guidance 本身不限制所有工具调用，不能替代 sandbox/approval |
| Todo | 当前 Agent Session 的任务清单，跨轮次和重开 Session 保留 | 单 Session 所有，整表替换，不是共享 Team Board |
| Goal | 单个持久化目标，支持暂停、恢复、阻塞、完成 | 一 Session 一个当前 Goal；Goal 状态与调度分离 |
| Team | Subagent 树共享任务板、依赖和 compare-and-set 任务认领 | 共享 checkout；不提供跨进程协调、worktree 隔离或自动释放 owner |
| Workflow | 模型编写编排脚本，fan-out 到多个 Subagent | 取消/异常时不把部分结果伪装成成功 |
| Jobs | 后台长任务的状态、输出、等待和取消 | Session owner 隔离，后台能力依赖具体宿主组合 |

证据：
- [Plan package](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/plan)
- [Todo package](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/todo)
- [Goal package](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/goal)
- [Team package](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/team)
- [Workflow package](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/workflow)
- [Jobs package](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/jobs)

通用模板应定义 Host Capability Contract，例如：
- plan approval：native / adapter / unsupported；
- persistent todo：native / adapter / unsupported；
- durable goal：native / adapter / unsupported；
- shared task board：native / adapter / unsupported；
- background job lifecycle：native / adapter / unsupported；
- isolated worktree：native / adapter / unsupported；
- cancellation and recovery：native / adapter / unsupported。

不支持的能力必须显式报告，不得把一个临时 Markdown checklist 包装成等价的 Team/Jobs 实现。Agent Runtime 由 DSH、Claude Code、Codex、Cursor 等宿主提供；模板只定义跨宿主的任务和交付契约。

## 6. 当前模板实现核查

审计到的主要事实：

- 版本为 2.6.0，project-policy.json schema_version 为 2。
- 9 个 Project Skills：plan、implement、review、pre-pr、docs、error-handling、simplification、upgrade、agent-governance。
- 一个 quality.yml Workflow，单个 quality Job。
- 两个模板测试模块；最近 v2.6 PR 的 CI 报告 58 个模板契约测试通过。
- project-policy.json 默认 quality_checks 为空，release_mode 为 manual。
- run_quality.py 以路径模式选择命令，按顺序运行；单条命令超时 600 秒。
- verify_project.py 检查根 AGENTS、CLAUDE 兼容入口、Skill 注册、文档结构和指令源安全。
- instruction_chain.py 输出静态项目文件来源图，并明确 host_verified=false。
- ADR README 定义 Proposed/Accepted/Rejected/Superseded，但没有 Agent Notes 那样的目录状态机、supersession 检查或 archive manifest。
- 未发现 .github/ISSUE_TEMPLATE、.github/issue-management、PR approval workflow、CODEOWNERS、Stacked PR workflow 或 Project lifecycle automation。
- configure_project.py 只配置项目名、技术栈和部分候选质量命令，不创建 GitHub Project、Issue 字段、标签、分支保护或 App 权限。

证据：
- [AGENTS.md](https://github.com/SophiaData/agent-project-template/blob/master/AGENTS.md)
- [project-policy.json](https://github.com/SophiaData/agent-project-template/blob/master/project-policy.json)
- [verify_project.py](https://github.com/SophiaData/agent-project-template/blob/master/scripts/verify_project.py)
- [run_quality.py](https://github.com/SophiaData/agent-project-template/blob/master/scripts/run_quality.py)
- [quality.yml](https://github.com/SophiaData/agent-project-template/blob/master/.github/workflows/quality.yml)
- [docs/testing.md](https://github.com/SophiaData/agent-project-template/blob/master/docs/testing.md)
- [docs/decisions/README.md](https://github.com/SophiaData/agent-project-template/blob/master/docs/decisions/README.md)

## 7. 目标架构建议

不要把 GitHub、DSH 或任何 Agent 的字段、事件和状态写死在核心规则中。建议按下面的边界演进。

### 7.1 Governance Core（平台无关）

拥有：
- 项目实体和任务类型；
- 生命周期状态机及合法转换；
- Priority、Area、Kind、依赖和验收条件；
- PR / Review 的通用策略；
- 决策记录状态和 supersession 规则；
- 测试质量策略；
- 能力声明、执行证据和审计事件格式。

核心只负责纯规则和数据契约，不直接调用 GitHub API，也不依赖某个 Agent CLI。

### 7.2 Provider Adapters（平台适配）

第一阶段只实现 GitHub Adapter，之后再考虑 GitLab 等：
- Issue / PR / Review 读取；
- GitHub Projects 字段和状态映射；
- Check / Status 发布；
- App token / permission scope；
- webhook event parsing；
- Project mutation。

适配层需要报告平台差异，不能静默改变核心策略。

### 7.3 Agent Host Adapters（Agent 宿主适配）

先做能力探测与契约，不急于做复杂运行时：
- DSH：Plan/Todo/Goal/Team/Workflow/Jobs；
- Claude Code：指令、Skills、Subagents、Hooks 等可验证能力；
- Codex：AGENTS、Skills、任务/工作区能力；
- Cursor：规则、Skills、Agent/后台任务能力。

每个能力都需要声明支持等级、持久性、可见性、取消语义、所有权和限制。禁止把宿主没有提供的能力伪造为已支持。

### 7.4 Reliable Workflow Runtime（可靠工作流）

自动化工作流应包含：
- durable event inbox 或等价的 delivery ledger；
- event delivery 去重和幂等 key；
- per-entity serialization / lease；
- bounded retry，仅重试明确可安全重复的操作；
- 状态写入后回读验证；
- 定期 reconciliation；
- 无法自动修复时进入可观测的人工处理队列；
- 审计日志保留 actor、event、旧值、新值、policy version 和执行结果。

GitHub Project API 没有提供的 CAS 保证必须如实标记。可用串行化写入和写后验证降低竞态，但不能声称实现了真正原子事务。

### 7.5 Security Plane（安全平面）

在加入任何写入型 GitHub 自动化之前必须先定义：
- 读取、状态发布、Project 写入使用不同权限；
- 需要写权限的 workflow 使用专用 GitHub App；
- Policy 从可信 default branch 加载；
- PR 分支内容只作为不可信数据读取，不能在持有写 token 的 job 中执行；
- 最小权限、明确 token scope、短生命周期 token；
- 第三方 Actions 对高权限工作流使用完整 commit SHA pin；
- 缺少权限、配置错误或校验失败时 fail closed；
- 生产发布、DataWorks 节点提交/发布保持人工操作。

## 8. 分阶段路线图

路线图按能力依赖排序，不以版本号驱动范围膨胀。每阶段可以拆成多个独立 PR。

### Phase 0 — 对标审计（本 PR）

- 固化 DSH 代码级证据和限制；
- 记录模板现状；
- 确认目标架构和阶段依赖；
- 不修改现有生产或项目管理设置。

### Phase 1 — Project Lifecycle Governance

优先级：最高。

建议拆分：
1. Project schema 与状态机：定义通用 Issue/Task 模型、Type、Priority、Area、合法状态转换和校验规则；纯函数 + 表驱动测试。
2. GitHub bootstrap/config：提供 Issue templates、label taxonomy、Project 字段/状态配置说明和只读 drift 检查；不自动更改组织设置。
3. PR/Issue read-only policy：校验 PR 引用、kind/area/priority、Issue 状态和 Project 字段；先只读，不做自动状态写入。
4. Lifecycle write adapter：专用 App、可信默认分支、按实体串行、幂等事件、回读验证和完整审计。
5. Reconciliation：先 dry-run 报告漂移，再开放白名单内的安全修复；终态、人工修改和歧义状态不得自动覆盖。

### Phase 2 — PR & Review Governance

- 标准化 PR 关联、风险、测试证据和兼容性信息；
- 定义 Reviewer 权限、审批门槛和 Changes requested 处理；
- 新提交、base 更新或关键文件变化后重新评估审批有效性；
- 使用稳定 Check identity；
- 对 Stack 提供可选适配，不强制所有项目采用 stacked workflow；
- 合并前检查准确的 base/head SHA、review threads、CI 和 mergeability。

### Phase 3 — Decision & Knowledge Lifecycle

- 将 ADR 演进为可验证的 Decision/Note lifecycle；
- 提案、实施、拒绝、superseded、归档；
- 新记录自动检查重复和 supersession；
- 活跃记录与已实现代码事实保持一致；
- 归档内容 append-only hash manifest；
- 通用语言策略，不强制所有消费项目都采用 DSH 的中英 triplet。

### Phase 4 — Engineering Quality Pipeline

- 把变更范围采集扩展到 committed/staged/unstaged/untracked；
- 将质量检查从简单命令列表升级为有界 Gate DAG；
- 支持依赖、取消、超时、可选安全重试、日志和诊断；
- 提供语言/项目类型 profile；
- 验证测试发现数量和空测试集；
- 根据风险选择 Unit/Integration/Contract/E2E/Performance/Resilience；
- 为新 Guard 保留 negative controls；
- 对大型项目增加多平台和构建产物验证。

### Phase 5 — Agent Execution Governance

- 先发布 Host Capability Contract 和 capability probe；
- 将 Plan、Todo、Goal、Team、Workflow、Jobs 映射到宿主能力；
- 任务、Session、PR、Branch、Worktree 建立可追踪关联；
- 定义任务 owner、锁、取消、超时、重试和 abandoned work 恢复；
- 只在宿主不具备关键能力且有明确需求时开发 adapter；不在模板中复制 DSH Harness。

## 9. 每个治理能力的验收标准

每个阶段都必须通过以下验收，而不只是文档和 happy path：

1. **规则测试**：正常、非法、边界、重复和状态转换覆盖。
2. **负向控制**：故意制造不合法配置/事件/依赖，确认守卫以正确原因失败。
3. **幂等测试**：同一事件执行两次，最终状态与副作用不重复。
4. **并发测试**：同一 Issue/PR 并发事件、乱序事件、过期快照和并行写入。
5. **故障恢复**：API 超时、429、5xx、权限撤销、部分写成功、回读失败、workflow 被取消。
6. **安全测试**：来自 fork/PR 的不可信内容不能在持有写权限的执行上下文中运行。
7. **回读验证**：不能只验证 API 返回成功，必须重新读取远端最终状态。
8. **对账验证**：漏事件后 reconciliation 能检测漂移；只自动修复无歧义且白名单允许的情况。
9. **真实平台验收**：使用专用测试仓库/GitHub App 验证 webhook、Project 字段和 Check identity。
10. **兼容性验收**：旧 project-policy schema、旧 ADR 和现有项目自定义配置不被静默覆盖。

## 10. 优先级结论

| 优先级 | 建设项 | 原因 |
|---|---|---|
| P0 | Project/Issue 状态机与策略模型 | 没有任务状态源，就无法形成项目管理闭环 |
| P0 | GitHub 只读 Issue/PR Policy | 先验证规则，避免一开始引入写入风险 |
| P1 | 可靠 Lifecycle + reconciliation | 解决漏事件、重复事件、并发与状态漂移 |
| P1 | PR 审批与合并门禁 | 防止“CI 绿了就等于可以合并” |
| P1 | Decision/Notes lifecycle | 让知识长期可维护、可审计 |
| P2 | Gate DAG 与测试可靠性 | 让质量门禁能扩展到真实多技术栈项目 |
| P2 | Host Capability Adapter | 在不复制 Harness 的前提下跨 Agent 追踪执行 |
| P3 | 可选 Stack / 多 Provider | 先验证主链路，再扩展平台和协作模式 |

## 11. 不应照搬的内容

- 不照搬 DSH 的具体 Reviewer 名单、加权分数和组织 Project ID。
- 不强制每个项目都使用 DSH 的七个状态、五种 Issue Type；状态映射必须可配置，但必须有经过验证的有限状态机。
- 不强制所有语言/项目都采用 100% per-file coverage；质量门槛按风险和项目类型配置。
- 不把 DSH 的 Team/Jobs 运行时能力重新写成 Skills。
- 不把 GitHub event workflow 当成完整状态一致性方案；必须增加 reconciliation。
- 不把 GitHub Project 字段写入包装成 CAS/事务。
- 不为了跨平台而把所有平台能力降到最低公分母；使用 capability negotiation 和显式降级。
- 不增加自动 DataWorks 提交/发布、自动生产发布或未经授权的合并能力。

## 12. 最终判断

agent-project-template v2.6.0 已经有不错的工程规则和静态治理入口，但距离 DSH 级项目管理成熟度的主要差距，不在 AGENTS.md，而在：

1. 项目状态模型和自动生命周期；
2. 可靠的 PR/Review/合并治理；
3. 决策知识生命周期；
4. 可证明的增量质量执行；
5. Agent 宿主执行状态与项目交付之间的关联。

下一步应先实现 Phase 1 的纯规则与只读验证，再逐步引入写入型自动化和 reconciliation。这样可以先建立可测试、可审查、可回滚的基础，避免一开始就让 GitHub 自动化拥有过大的写权限。

**目标不是复刻 DSH，而是以 DSH 已经验证的工程机制作为质量基准，保留它的明确边界，并对其已知的事件丢失、并发写入和恢复限制做更可靠的通用设计。**
