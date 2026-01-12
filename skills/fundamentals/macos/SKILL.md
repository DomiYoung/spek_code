---
name: fundamentals-macos
description: |
  macOS 底层原理诊断 - XNU/launchd/权限与安全/文件系统/进程模型。
  Use when:
  - 应用无法启动/被阻止/签名问题
  - 权限/沙箱/Keychain 访问异常
  - 系统级资源限制/性能问题
  触发词：macOS、XNU、launchd、SIP、codesign、notarization、sandbox、keychain、entitlements
  Related Skills: fundamentals/unix
allowed-tools: "*"
---

# macOS Fundamentals（macOS 底层原理）

> **目标**：把问题定位到系统安全、签名与进程管理机制。

## 诊断路径
1. 确认系统版本与架构（`sw_vers`/`uname -m`）。
2. 检查 Gatekeeper/签名/公证状态（`spctl`/`codesign`）。
3. 核对沙箱与权限（TCC/entitlements/Keychain）。
4. 追踪 launchd/系统日志（`launchctl`/`log show`）。

## 症状 → 机制速查
- **无法打开应用** → Gatekeeper/公证/签名校验失败
- **Operation not permitted** → SIP/TCC 权限限制
- **Keychain 访问失败** → entitlements 缺失或访问组错误
- **后台进程异常** → launchd 配置/权限问题

## 关键机制速记
- **Gatekeeper**：签名与公证检查
- **SIP/TCC**：系统保护与隐私权限控制
- **Entitlements**：能力声明，影响沙箱访问
- **launchd**：系统级进程管理与服务启动

## 证据采集要点
- `codesign -dv --verbose=4 <app>`
- `spctl --assess --verbose <app>`
- 系统日志中的拒绝原因
- 可选：运行 `scripts/diagnose.sh` 输出系统信息与签名检查提示

## 常见根因清单
- 缺失 entitlements 或签名不匹配
- 应用仍带有 quarantine 属性
- SIP/TCC 未授权导致访问被拒
- Keychain access group 配置错误
- launchd plist 权限/路径异常

## 快速验证
- `xattr -l <app>` 检查 quarantine
- `spctl --assess --verbose <app>`
- `codesign -dv --verbose=4 <app>`

## 输出模板（固定顺序）
1. 症状：描述可观测现象与影响范围。
2. 机制：指出机制级根因。
3. 证据：列出采集到的指标/日志/截图/命令输出。
4. 修复：给出最小可行修复与替代方案（如有）。
5. 验证：说明如何确认改善（对比指标/复现/回归）。

## 深入阅读（按需加载）
- `references/MECHANICS.md`：Gatekeeper/SIP/TCC/签名与沙箱机制
