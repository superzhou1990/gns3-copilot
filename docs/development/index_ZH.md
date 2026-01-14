# 开发指南

本部分包含为 GNS3 Copilot 贡献者和开发者准备的开发资源。

## 快速开始

如果您是第一次为 GNS3 Copilot 做贡献，请参考：

1. **[测试指南](testing/manual_testing_guide_zh.md)** - 手动测试程序
2. **[自动提交指南](automation/auto-commit-usage-guide_zh.md)** - 自动提交工作流
3. **[自动文档指南](automation/auto-doc-automation-guide_zh.md)** - 文档自动化

## 分支策略

我们使用以下分支策略：

```
master (生产环境)
    ↑
Development (主开发分支)
    ↑
feature/* (功能分支)
```

- **master**: 稳定的生产版本
- **Development**: 主开发分支 - 将所有 PR 合并到此分支
- **feature/***: 从 Development 创建的功能分支

## 可用文档

### 测试
- [Manual Testing Guide (English)](testing/manual_testing_guide.md) - 手动测试程序
- [手动测试指南 (中文)](testing/manual_testing_guide_zh.md) - 手动测试程序
- [Test Coverage Report (English)](testing/TEST_COVERAGE_REPORT.md) - 代码覆盖率统计
- [测试覆盖率报告 (中文)](testing/TEST_COVERAGE_REPORT_ZH.md) - 代码覆盖率统计

### 自动化
#### 自动提交
- [Auto Commit Usage Guide (English)](automation/auto-commit-usage-guide.md) - 使用自动提交工作流
- [自动提交使用指南 (中文)](automation/auto-commit-usage-guide_zh.md) - 使用自动提交工作流

#### 自动文档
- [Auto Documentation Guide (English)](automation/auto-doc-automation-guide.md) - 文档自动化流程
- [自动文档指南 (中文)](automation/auto-doc-automation-guide_zh.md) - 文档自动化流程

#### 文档改进
- [Documentation Improvements (English)](automation/doc-update-improvements.md) - 文档更新改进
- [文档更新改进 (中文)](automation/doc-update-improvements_zh.md) - 文档更新改进

### 演进
- [Backend Evolution Plan (English)](evolution/GNS3-Copilot%20Backend%20Evolution%20Plan.md) - 未来开发路线图
- [后端演进计划 (中文)](evolution/GNS3-Copilot-Backend-Evolution-Plan_ZH.md) - 未来开发路线图

## 开发命令

```bash
# 安装开发依赖
pip install -e ".[dev,docs]"

# 运行测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=gns3_copilot --cov-report=html

# 代码检查
ruff check src/

# 代码格式化
ruff format src/

# 类型检查
mypy src/

# 安全检查
safety scan

# 本地构建文档
mkdocs serve
```

## 代码风格指南

我们遵循以下代码风格标准：

- **PEP 8** - Python 代码风格
- **类型提示** - 公共函数必须有类型注解
- **文档字符串** - Google 或 NumPy 风格的文档字符串
- **行长度** - 最多 88 个字符（Black 格式化）

## 提交更改

1. 从 Development 创建功能分支：
   ```bash
   git checkout -b feature/your-feature Development
   ```

2. 进行更改并提交

3. 推送您的分支：
   ```bash
   git push origin feature/your-feature
   ```

4. 创建 Pull Request 到 **Development** 分支

5. 在请求审查之前确保所有 CI 检查通过

## CI/CD 流水线

我们的 CI/CD 流水线包括：

- **代码检查** - Ruff 代码风格检查
- **类型检查** - Mypy 静态类型检查
- **安全扫描** - Safety 依赖扫描
- **测试** - Pytest 测试和覆盖率报告
- **文档** - 在 PR 上自动更新文档
- **发布** - 在版本标签上自动发布到 PyPI
