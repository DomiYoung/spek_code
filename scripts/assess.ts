/**
 * 工作流路由评估器
 * 两段式路由：Stage A (决策树硬门槛) + Stage B (打分路由)
 */

// ============================================
// 类型定义
// ============================================

export type Flags = {
  // Stage A: 强制升级标记
  breaking_change?: boolean;
  schema_migration?: boolean;
  external_api_contract?: boolean;
  auth_audit_compliance?: boolean;
  money_core_business?: boolean;
  cross_service_chain?: boolean;
  multi_tool_calls?: boolean;
  multi_stage_execution?: boolean;
  need_persistent_progress?: boolean;
  analysis_only?: boolean;
  docs_or_style_only?: boolean;

  // Stage B: 复杂度标记
  new_feature?: boolean;
  major_refactor?: boolean;
  api_change?: boolean;
  schema_change?: boolean;
  arch_change?: boolean;
  bug_fix?: boolean;
  docs_only?: boolean;
  style_only?: boolean;

  // Stage B: 风险标记
  concurrency_tx?: boolean;

  // Task Master 标记
  need_rollback_or_gray?: boolean;
  cross_module_validation?: boolean;
  multi_role_collab?: boolean;
  has_acceptance_checklist?: boolean;

  // Mode 标记
  need_external_evidence?: boolean;
  need_comparison?: boolean;
  time_sensitive_info?: boolean;
  design_tradeoff?: boolean;
  arch_decision?: boolean;

  // 噪音过滤标记
  auto_generated?: boolean;
  format_only?: boolean;
  dependency_update_minor?: boolean;
  lock_file_only?: boolean;
};

export type Input = {
  changedFiles: number;
  changedLines: number;
  flags: Flags;
  subtasks?: number;
};

export type Workflow = 'Spec-Kit' | 'planning-with-files' | 'planning-with-files-lite' | 'TodoWrite';
export type Mode = '--research' | '--think' | '默认';

export type Result = {
  // 路由结果
  workflow: Workflow;
  dir: string;
  taskMaster: boolean;
  mode: Mode;

  // 评估详情
  stage: 'A' | 'B';
  complexityScore: number;
  riskScore: number;
  totalScore: number;

  // 可解释性
  reasons: string[];
  path: string;
};

// ============================================
// 工具函数
// ============================================

function clamp(n: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, n));
}

// ============================================
// Stage A: 决策树硬门槛
// ============================================

function stageA(input: Input): { workflow: Workflow; dir: string; reason: string } | null {
  const f = input.flags;

  // 1. 强制升级到 Spec-Kit
  if (f.breaking_change) return { workflow: 'Spec-Kit', dir: '.specify/specs/{feature}/', reason: 'Breaking Change' };
  if (f.schema_migration) return { workflow: 'Spec-Kit', dir: '.specify/specs/{feature}/', reason: 'Schema/数据迁移' };
  if (f.external_api_contract) return { workflow: 'Spec-Kit', dir: '.specify/specs/{feature}/', reason: '对外 API 契约变化' };
  if (f.auth_audit_compliance) return { workflow: 'Spec-Kit', dir: '.specify/specs/{feature}/', reason: '权限/鉴权/审计/合规' };
  if (f.money_core_business) return { workflow: 'Spec-Kit', dir: '.specify/specs/{feature}/', reason: '资金/结算/订单等高风险' };
  if (f.cross_service_chain) return { workflow: 'Spec-Kit', dir: '.specify/specs/{feature}/', reason: '跨服务/跨模块链路' };

  // 2. 强制升级到 planning-with-files
  if (f.multi_tool_calls) return { workflow: 'planning-with-files', dir: '.planning/', reason: '需要 >5 次工具调用' };
  if (f.multi_stage_execution) return { workflow: 'planning-with-files', dir: '.planning/', reason: '多阶段执行' };
  if (f.need_persistent_progress) return { workflow: 'planning-with-files', dir: '.planning/', reason: '需要持久化进度' };

  // 3. 强制降级到 TodoWrite
  if (f.analysis_only) return { workflow: 'TodoWrite', dir: '', reason: '纯代码分析/理解' };
  if (f.docs_or_style_only) return { workflow: 'TodoWrite', dir: '', reason: '纯文档/样式' };

  // 未命中任何硬门槛
  return null;
}

// ============================================
// Stage B: 打分路由
// ============================================

function stageB(input: Input): {
  workflow: Workflow;
  dir: string;
  complexityScore: number;
  riskScore: number;
  totalScore: number;
  reasons: string[];
} {
  const f = input.flags;
  const reasons: string[] = [];

  // --- 复杂度评分（只取最高项）---
  const complexityCandidates: Array<{ label: string; score: number; match: boolean }> = [
    { label: '新功能/重构/Breaking Change', score: 10, match: !!(f.breaking_change || f.new_feature || f.major_refactor) },
    { label: '>5 文件 或 >200 行', score: 8, match: input.changedFiles > 5 || input.changedLines > 200 },
    { label: 'API/架构/Schema 变更', score: 7, match: !!(f.api_change || f.schema_change || f.arch_change) },
    { label: '3-5 文件功能变更', score: 5, match: input.changedFiles >= 3 && input.changedFiles <= 5 },
    { label: '简单 Bug (<3 文件)', score: 2, match: input.changedFiles < 3 && !!f.bug_fix },
    { label: '纯样式/文档', score: 1, match: !!(f.docs_only || f.style_only) },
    { label: '代码分析/理解', score: 0, match: !!f.analysis_only },
  ];

  const matchedComplexity = complexityCandidates.filter(c => c.match);
  const complexityScore = matchedComplexity.length > 0
    ? Math.max(...matchedComplexity.map(c => c.score))
    : 0;

  const topComplexity = matchedComplexity.find(c => c.score === complexityScore);
  if (topComplexity && topComplexity.score > 0) {
    reasons.push(`复杂度: ${topComplexity.label} (+${topComplexity.score})`);
  }

  // --- 风险评分（可叠加，封顶 10）---
  const riskItems: Array<{ label: string; score: number; match: boolean }> = [
    { label: '权限/鉴权/审计/合规', score: 7, match: !!f.auth_audit_compliance },
    { label: 'Schema/迁移/数据修复', score: 7, match: !!f.schema_migration },
    { label: '对外 API 契约变化', score: 7, match: !!f.external_api_contract },
    { label: '资金/结算/订单等高风险', score: 7, match: !!f.money_core_business },
    { label: '并发/事务/幂等/消息可靠性', score: 5, match: !!f.concurrency_tx },
  ];

  const riskRaw = riskItems.reduce((sum, r) => sum + (r.match ? r.score : 0), 0);
  const riskScore = clamp(riskRaw, 0, 10);

  riskItems.filter(r => r.match).forEach(r => {
    reasons.push(`风险: ${r.label} (+${r.score})`);
  });

  if (riskRaw !== riskScore) {
    reasons.push(`风险分封顶: ${riskRaw} → ${riskScore}`);
  }

  // --- 最终总分：max(复杂度, 风险) ---
  const totalScore = Math.max(complexityScore, riskScore);

  // --- 路由 workflow ---
  let workflow: Workflow;
  let dir: string;

  if (totalScore >= 7) {
    workflow = 'Spec-Kit';
    dir = '.specify/specs/{feature}/';
  } else if (totalScore >= 5) {
    workflow = 'planning-with-files';
    dir = '.planning/';
  } else if (totalScore >= 3) {
    workflow = 'planning-with-files-lite';
    dir = '.planning/';
  } else {
    workflow = 'TodoWrite';
    dir = '';
  }

  return { workflow, dir, complexityScore, riskScore, totalScore, reasons };
}

// ============================================
// Task Master 判定
// ============================================

function shouldEnableTaskMaster(input: Input): boolean {
  const f = input.flags;
  const subtasks = input.subtasks ?? 0;

  return (
    subtasks >= 5 ||
    !!f.need_rollback_or_gray ||
    !!f.cross_module_validation ||
    !!f.multi_role_collab ||
    !!f.has_acceptance_checklist
  );
}

// ============================================
// Mode 判定
// ============================================

function determineMode(input: Input): Mode {
  const f = input.flags;

  if (f.need_external_evidence || f.need_comparison || f.time_sensitive_info) {
    return '--research';
  }

  if (f.design_tradeoff || f.arch_decision) {
    return '--think';
  }

  return '默认';
}

// ============================================
// 噪音过滤
// ============================================

function isNoise(input: Input): boolean {
  const f = input.flags;
  return !!(f.auto_generated || f.format_only || f.dependency_update_minor || f.lock_file_only);
}

// ============================================
// 主入口：评估函数
// ============================================

export function assess(input: Input): Result {
  // 噪音过滤
  if (isNoise(input)) {
    return {
      workflow: 'TodoWrite',
      dir: '',
      taskMaster: false,
      mode: '默认',
      stage: 'A',
      complexityScore: 0,
      riskScore: 0,
      totalScore: 0,
      reasons: ['噪音过滤: 自动生成/格式化/依赖更新'],
      path: 'noise-filter → TodoWrite',
    };
  }

  // Stage A: 决策树硬门槛
  const stageAResult = stageA(input);

  if (stageAResult) {
    return {
      workflow: stageAResult.workflow,
      dir: stageAResult.dir,
      taskMaster: shouldEnableTaskMaster(input),
      mode: determineMode(input),
      stage: 'A',
      complexityScore: 0,
      riskScore: 0,
      totalScore: stageAResult.workflow === 'Spec-Kit' ? 10 : stageAResult.workflow === 'TodoWrite' ? 0 : 5,
      reasons: [`硬门槛命中: ${stageAResult.reason}`],
      path: `Stage A → ${stageAResult.reason} → ${stageAResult.workflow}`,
    };
  }

  // Stage B: 打分路由
  const stageBResult = stageB(input);

  return {
    workflow: stageBResult.workflow,
    dir: stageBResult.dir,
    taskMaster: shouldEnableTaskMaster(input),
    mode: determineMode(input),
    stage: 'B',
    complexityScore: stageBResult.complexityScore,
    riskScore: stageBResult.riskScore,
    totalScore: stageBResult.totalScore,
    reasons: stageBResult.reasons,
    path: `Stage B → 总分 ${stageBResult.totalScore} → ${stageBResult.workflow}`,
  };
}

// ============================================
// 使用示例
// ============================================

/*
const input: Input = {
  changedFiles: 2,
  changedLines: 80,
  flags: {
    bug_fix: true,
    auth_audit_compliance: true,  // 即使 2 文件也会升级
  },
  subtasks: 6,
};

console.log(assess(input));
// 输出:
// {
//   workflow: 'Spec-Kit',
//   dir: '.specify/specs/{feature}/',
//   taskMaster: true,
//   mode: '默认',
//   stage: 'A',
//   reasons: ['硬门槛命中: 权限/鉴权/审计/合规'],
//   path: 'Stage A → 权限/鉴权/审计/合规 → Spec-Kit',
//   ...
// }
*/

export default assess;
