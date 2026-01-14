# GNS3 Copilot 文档

本目录包含 GNS3 Copilot 项目的所有文档。

## 目录结构

```
docs/
├── README.md                                # 本文件 - 文档索引
├── README_ZH.md                             # 本文件（中文）
├── project-announcement.md                  # 项目公告和路线图
├── project-announcement_ZH.md               # 项目公告和路线图（中文）
├── index.md                                 # 文档首页
├── index_ZH.md                              # 文档首页（中文）
├── architecture/                            # 架构文档
│   ├── README.md                            # 架构索引
│   ├── README_ZH.md                         # 架构索引（中文）
│   ├── system-architecture.md               # 系统架构概览
│   ├── system-architecture_ZH.md            # 系统架构概览（中文）
│   ├── core-framework-design.md             # 核心框架设计
│   ├── core-framework-design_ZH.md          # 核心框架设计（中文）
│   └── images/                             # 架构图
│       ├── gns3_copilot_architecture.svg
│       ├── framework-data-flow.svg
│       ├── langchain-tools.svg
│       ├── langgraph-agent.svg
│       ├── multi-agent.svg
│       ├── config-first-party.jpeg
│       ├── config-third-party.jpeg
│       └── gns3-select-project.jpeg
├── user/                                    # 面向用户的文档
│   ├── FAQ.md                               # 常见问题
│   ├── FAQ_ZH.md                            # 常见问题（中文）
│   ├── llm-quick-configuration-guide.md     # LLM 快速设置指南
│   ├── llm-quick-configuration-guide_zh.md  # LLM 快速设置指南（中文）
│   ├── checkpoint-import-export-guide.md    # 检查点导入/导出指南
│   └── checkpoint-import-export-guide_ZH.md # 检查点导入/导出指南（中文）
├── development/                             # 开发文档
│   ├── testing/                             # 测试指南和报告
│   │   ├── manual_testing_guide.md          # 手动测试说明
│   │   ├── manual_testing_guide_zh.md       # 手动测试说明（中文）
│   │   ├── TEST_COVERAGE_REPORT.md          # 测试覆盖率统计
│   │   └── TEST_COVERAGE_REPORT_ZH.md       # 测试覆盖率统计（中文）
│   ├── automation/                          # 自动化工具文档
│   │   ├── auto-commit-usage-guide.md       # 自动提交脚本指南
│   │   ├── auto-commit-usage-guide_zh.md    # 自动提交脚本指南（中文）
│   │   ├── auto-doc-automation-guide.md     # 自动文档生成指南
│   │   ├── auto-doc-automation-guide_zh.md  # 自动文档生成指南（中文）
│   │   ├── doc-update-improvements.md       # 文档改进
│   │   └── doc-update-improvements_zh.md    # 文档改进（中文）
│   └── evolution/                           # 项目演进规划
│       ├── GNS3-Copilot Backend Evolution Plan.md    # 后端演进路线图
│       └── GNS3-Copilot-Backend-Evolution-Plan_ZH.md # 后端演进路线图（中文）
└── technical/                               # 技术文档
    ├── gns3-drawing-svg-format-guide.md     # GNS3 绘图格式指南
    └── gns3-drawing-svg-format-guide_zh.md  # GNS3 绘图格式指南（中文）
```

## 快速开始

### 面向用户

如果您想要使用 GNS3 Copilot，请从以下内容开始：
- [项目公告](project-announcement_ZH.md) - 项目概述、功能和路线图
- [常见问题](user/FAQ_ZH.md) - 常见问题和故障排查
- [LLM 快速配置指南](user/llm-quick-configuration-guide_zh.md) - 设置您的 LLM 提供商

### 面向开发者

如果您想要贡献或了解代码库：
- [手动测试指南](development/testing/manual_testing_guide_zh.md) - 如何测试应用程序
- [测试覆盖率报告](development/testing/TEST_COVERAGE_REPORT_ZH.md) - 测试统计
- [自动提交使用指南](development/automation/auto-commit-usage-guide_zh.md) - 自动化提交消息
- [后端演进计划](development/evolution/GNS3-Copilot-Backend-Evolution-Plan_ZH.md) - 项目路线图

### 面向技术细节

如果您需要技术规范：
- [系统架构](architecture/system-architecture_ZH.md) - 系统架构概览（7 层设计）
- [核心框架设计](architecture/core-framework-design_ZH.md) - 详细的 LangGraph 和 LangChain 框架设计
- [GNS3 绘图 SVG 格式指南](technical/gns3-drawing-svg-format-guide_zh.md) - 绘图格式规范

### 面向架构文档

如果您想了解系统架构：
- [架构索引](architecture/README_ZH.md) - 完整的架构文档
- [系统架构](architecture/system-architecture_ZH.md) - 中文版系统架构
- [核心框架设计](architecture/core-framework-design_ZH.md) - 中文版框架设计

## 文档语言

大多数文档都有英文和中文（简体）版本。中文版本以 `_ZH.md` 或 `_zh.md` 为后缀。

## 相关资源

- [架构文档](architecture/) - 系统架构图和设计文档
- [源代码](../src/gns3_copilot/) - 应用程序源代码
- [测试文件](../tests/) - 测试套件和测试文件
