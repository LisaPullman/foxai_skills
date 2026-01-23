# Agent Skills (智能体技能)

这个仓库包含了一系列 Anthropic 的 "Agent Skills"（智能体技能）。这些技能由指令、脚本和资源组成，旨在动态加载给 Claude，以赋予其处理特定专业任务的能力。

简单来说，这里是 Claude 的“技能包”库，涵盖了从办公文档处理、创意设计到专业代码开发的多种能力。

## 技能分类概览

### 📝 办公与文档 (Productivity & Documents)
这些技能赋予 Claude 强大的文档处理能力，支持创建、编辑和分析主流办公文件格式。

*   **[docx](./skills/docx)**: Word 文档全能助手。支持创建新文档、编辑内容、处理修订模式、添加评论以及提取文本。底层处理复杂的 XML 结构。
*   **[xlsx](./skills/xlsx)**: Excel 表格专家。支持创建电子表格、公式计算、数据分析、格式化以及可视化图表。
*   **[pptx](./skills/pptx)**: PPT 演示文稿大师。支持创建幻灯片、修改布局、编辑内容以及处理演讲者备注。
*   **[pdf](./skills/pdf)**: PDF 处理工具箱。支持 PDF 表单填写、文本与表格提取、文档合并/拆分以及生成新 PDF。
*   **[doc-coauthoring](./skills/doc-coauthoring)**: 文档共创工作流。引导用户进行结构化的文档编写（如技术规范、提案），包含从草稿到审阅的全流程。
*   **[internal-comms](./skills/internal-comms)**: 内部沟通助手。帮助编写标准化的公司内部文档，如项目周报、FAQ、通讯稿等。

### 🎨 创意与设计 (Creative & Design)
这些技能让 Claude 具备设计师的眼光和能力，能够生成视觉作品、应用品牌规范。

*   **[algorithmic-art](./skills/algorithmic-art)**: 算法生成艺术。使用 p5.js 代码生成具有随机性和参数化探索特性的数字艺术作品。
*   **[canvas-design](./skills/canvas-design)**: 平面视觉设计。用于设计海报、艺术图或其他静态视觉作品，强调设计美学。
*   **[infographic-creation](./skills/infographic-creation)**: 信息图表生成。根据文本内容自动设计美观的信息图表。
*   **[frontend-design](./skills/frontend-design)**: 前端 UI 设计。生成高质量、生产级的前端界面代码，注重设计感，避免 AI 生成的廉价感。
*   **[slack-gif-creator](./skills/slack-gif-creator)**: Slack 动图制作。专门生成适用于 Slack 的优化 GIF 动画。
*   **[theme-factory](./skills/theme-factory)**: 主题工厂。提供预设或自定义的主题（配色、字体），可一键应用到文档、幻灯片或网页中。
*   **[brand-guidelines](./skills/brand-guidelines)**: 品牌指南库。定义了 Anthropic 的官方品牌色彩、排版和视觉规范。
*   **[applying-brand-guidelines](./skills/applying-brand-guidelines)**: 品牌一致性应用。确保生成的所有文档和设计符合公司的品牌视觉规范。

### 💻 开发与技术 (Development & Technical)
这些技能辅助开发者进行代码生成、测试和工具构建。

*   **[mcp-builder](./skills/mcp-builder)**: MCP 服务器构建指南。教 Claude 如何构建 Model Context Protocol (MCP) 服务器，以连接外部工具和数据。
*   **[web-artifacts-builder](./skills/web-artifacts-builder)**: Web 制品构建器。构建基于 React、Tailwind CSS 和 shadcn/ui 的复杂 Web 应用组件。
*   **[webapp-testing](./skills/webapp-testing)**: Web 应用测试。使用 Playwright 对本地 Web 应用进行自动化测试、截图和调试。
*   **[skill-creator](./skills/skill-creator)**: 技能生成向导。帮助用户创建新的自定义技能或更新现有技能。
*   **[gemini](./skills/gemini)**: Gemini 集成。调用 Google Gemini 模型处理复杂的推理任务。
*   **[codex](./skills/codex)**: Codex 集成。调用 Codex 模型进行代码重构和自动化修改。

### 📊 金融与数据分析 (Finance & Data)
专为金融领域设计的分析工具。

*   **[analyzing-financial-statements](./skills/analyzing-financial-statements)**: 财报分析。从财务报表中提取数据并计算关键财务比率，辅助投资分析。
*   **[creating-financial-models](./skills/creating-financial-models)**: 财务建模。提供 DCF 估值、敏感性分析、蒙特卡洛模拟等高级财务建模功能。

## 如何使用

要使用这些技能，通常需要将其加载到 Claude 的上下文中。具体方式取决于你使用的平台（Claude Code, Claude.ai 或 API）。

每个技能文件夹下都有一个 `SKILL.md` 文件，其中包含了详细的指令。你可以参考这些文件来了解每个技能的具体用法。

## 关于本项目

本项目展示了 Claude 技能系统的潜力。虽然部分技能（如文档处理）是 source-available 的参考实现，但大部分都是开源的 (Apache 2.0)。

> **免责声明**: 这些技能仅供演示和教育目的。在生产环境中使用前请务必进行充分测试。
