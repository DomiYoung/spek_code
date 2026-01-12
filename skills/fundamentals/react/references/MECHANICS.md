# React 机制扩展

## Fiber 与调度
- Fiber 支持可中断渲染与优先级调度。
- commit 阶段不可中断。

## Reconciliation
- key 决定节点复用，错误 key 会触发重建。
- props 引用变化会导致子树更新。

## Effects 时序
- useEffect 在 commit 后执行。
- useLayoutEffect 在 commit 前同步执行。

## StrictMode
- 开发环境双调用用于检测副作用。
