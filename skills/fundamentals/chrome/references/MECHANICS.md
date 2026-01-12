# Chrome/Chromium 架构扩展

## 多进程模型
- Browser/Renderer/GPU/Network Service/Utility 等分工。
- Site Isolation 将不同站点隔离到不同渲染进程。

## Blink 渲染流水线
- 解析 → 样式计算 → 布局 → 绘制 → 合成。
- 合成层过多会增加 GPU 负担。

## 安全与沙箱
- 渲染进程受沙箱限制，权限由 Browser 进程代理。
- 扩展与策略可能改变默认隔离行为。

## 诊断入口
- `chrome://gpu`、`chrome://process-internals`
- `chrome://net-export` 导出网络日志
