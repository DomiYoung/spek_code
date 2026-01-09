# PROJECT_CONVENTIONS.md - 项目规范约束系统

动态项目规范检测和约束执行系统，确保所有生成内容符合当前项目标准。

## 🎯 核心约束原则

**首要原则**: 在执行任何文件创建、代码生成、文档编写操作前，必须检测并遵守当前项目的规范约束。

## 🔍 项目规范检测流程

### 自动检测机制
```yaml
检测优先级:
  1. 项目根目录结构分析
  2. docs/ 目录组织模式识别
  3. 现有文件命名规范提取
  4. 代码架构模式学习
  5. 配置文件规范解析
```

### 规范提取算法
```typescript
// 伪代码：项目规范检测
const detectProjectConventions = (projectRoot: string) => {
  // 1. 分析文档结构
  const docsStructure = analyzeDocsDirectory(projectRoot + '/docs/');
  
  // 2. 提取命名模式
  const namingPatterns = extractNamingPatterns(docsStructure);
  
  // 3. 检测架构约束
  const archConstraints = detectArchitectureConstraints(projectRoot);
  
  // 4. 学习代码风格
  const codeStyle = learnCodeStyle(projectRoot + '/apps/');
  
  return {
    documentConventions: namingPatterns,
    architectureRules: archConstraints,
    codeStandards: codeStyle,
    qualityGates: extractQualityGates(projectRoot)
  };
};
```

## 📁 CreativePro Studio 特定规范

### 文档管理约束
```yaml
位置规范:
  docs/architecture/: 技术架构、系统设计、代码分析
  docs/project_management/: 项目管理、进度报告、状态总结
  docs/deployment/: 部署文档、运维指南
  docs/development/: 开发文档、环境配置、故障排查
  docs/features/: 功能文档、用户指南

命名规范:
  格式: [TYPE]_[NAME]_[DATE].md
  示例: CODE_ANALYSIS_SUMMARY_2025-01-01.md
  类型: ANALYSIS, SUMMARY, PLAN, GUIDE, REPORT, SPEC

结构模板:
  头部: 🔍 标题 | 日期 | 作者 | 版本 | 状态
  章节: 📊 摘要 → 🔍 分析 → 🚀 计划 → 📋 清单 → 🏁 结论
```

### 代码组织约束
```yaml
目录结构:
  apps/web/src/: 前端代码
    components/: 可复用组件
    pages/: 路由页面  
    services/: API服务层
    utils/: 工具函数
    
  apps/apis/src/: 后端代码
    [module]/: 功能模块
    shared/: 共享组件

禁止模式:
  ❌ 根目录散落文件
  ❌ 测试/临时代码 (test_, demo_, temp_)
  ❌ 硬编码配置
  ❌ Console.log调试语句
  ❌ 未完成的TODO标记
```

### 质量门禁
```yaml
生产级要求:
  ✅ 完整错误处理
  ✅ TypeScript类型定义
  ✅ 输入验证清理
  ✅ 安全防护措施
  ✅ 性能优化实现
  ✅ 完整文档注释

安全约束:
  ✅ XSS防护 (DOMPurify)
  ✅ SQL注入防护
  ✅ 敏感数据加密
  ❌ localStorage存储token
  ❌ 硬编码凭据
  ❌ HTTP明文传输

性能要求:
  - API响应 <200ms
  - 首屏加载 <3s  
  - Bundle大小 <2MB
  - 测试覆盖 >80%
```

## 🚀 执行约束机制

### 文件创建前检查
```yaml
必执行步骤:
  1. 检测目标位置是否符合项目结构
  2. 验证文件命名是否遵循规范
  3. 确认文档模板和格式要求
  4. 搜索现有类似功能避免重复
  5. 评估质量和安全要求合规性
```

### 动态规范适配
```yaml
适配机制:
  - 自动检测当前项目根目录
  - 分析现有文档命名模式
  - 学习代码组织结构
  - 提取质量标准配置
  - 应用项目特定约束
```

### 违规预防系统
```yaml
预防措施:
  1. 文件创建位置验证
  2. 命名规范实时检查
  3. 代码质量门禁验证
  4. 重复功能冲突检测
  5. 安全风险模式识别
```

## 🎛️ 自适应规范引擎

### 项目类型识别
```typescript
const identifyProject = (structure: ProjectStructure) => {
  if (hasReactApp(structure) && hasFastAPI(structure)) {
    return 'creativepro-studio'; // 应用CreativePro Studio规范
  }
  if (hasNextJS(structure)) {
    return 'nextjs-project'; // 应用Next.js规范
  }
  // ... 其他项目类型
  return 'generic'; // 应用通用规范
};
```

### 规范配置加载
```yaml
配置来源优先级:
  1. 项目根目录 .claude-project.yml
  2. docs/README.md 约定提取
  3. package.json 项目配置
  4. 现有文件模式学习
  5. 默认最佳实践规范
```

## 📋 操作检查清单

### 创建文档时
- [ ] 识别文档类型和目标受众
- [ ] 确定正确的docs/子目录
- [ ] 应用项目命名规范
- [ ] 使用标准文档模板
- [ ] 包含完整元信息头部
- [ ] 添加相关文档交叉引用

### 生成代码时  
- [ ] 搜索现有类似功能避免重复
- [ ] 确认代码放置位置正确
- [ ] 遵循项目命名约定
- [ ] 满足生产级质量要求
- [ ] 实现必要的安全防护
- [ ] 包含完整的错误处理

### 修改项目文件时
- [ ] 保持现有项目结构完整性
- [ ] 遵循已建立的代码风格
- [ ] 确保向后兼容性
- [ ] 更新相关文档和测试
- [ ] 验证不破坏现有功能

## ⚡ 智能约束执行

### 上下文感知约束
```yaml
约束应用逻辑:
  if 当前项目 == 'CreativePro Studio':
    apply CreativeProStudioConventions()
  elif 检测到React项目:
    apply ReactProjectConventions()  
  elif 检测到Python项目:
    apply PythonProjectConventions()
  else:
    apply GenericBestPractices()
```

### 违规自动修正
```yaml
修正能力:
  - 文档位置错误 → 自动移动到正确目录
  - 命名不规范 → 提供正确命名建议
  - 模板不完整 → 补充缺失的标准章节
  - 质量不达标 → 提供改进方案
```

## 🔄 持续学习和改进

### 规范进化机制
```yaml
学习源:
  - 项目现有文件模式分析
  - 团队代码审查反馈
  - 行业最佳实践更新
  - 安全和性能标准演进
```

### 约束优化
```yaml
优化策略:
  - 基于违规频率调整检查严格度
  - 根据项目成熟度调整质量要求
  - 结合团队反馈优化规范合理性
  - 定期更新最佳实践标准
```

---

**约束系统状态**: ✅ 已激活  
**适用范围**: 所有文件创建、代码生成、文档编写操作  
**更新频率**: 每次项目切换时自动重新检测和应用