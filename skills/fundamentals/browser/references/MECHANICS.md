# 浏览器底层原理 - 深度诊断手册

> **用途**：遇到浏览器相关问题时，提供可执行的诊断路径和根因定位。

---

## 1. 事件循环（Event Loop）

### 核心模型

```
┌─────────────────────────────────────────────────────────────┐
│                     浏览器主线程                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────────┐                                          │
│   │  Call Stack  │  ← 同步代码在这里执行                      │
│   └──────┬───────┘                                          │
│          │ 清空后                                            │
│          ▼                                                   │
│   ┌──────────────┐                                          │
│   │ Microtask Q  │  ← Promise.then / queueMicrotask         │
│   │  (全部执行)   │     MutationObserver                     │
│   └──────┬───────┘                                          │
│          │ 清空后                                            │
│          ▼                                                   │
│   ┌──────────────┐                                          │
│   │ 渲染机会?     │  ← 浏览器判断是否需要渲染（通常 16.6ms）    │
│   └──────┬───────┘                                          │
│          │ 如果渲染                                          │
│          ▼                                                   │
│   ┌──────────────┐                                          │
│   │ rAF 回调     │  ← requestAnimationFrame                 │
│   │ Style/Layout │                                          │
│   │ Paint/Comp   │                                          │
│   └──────┬───────┘                                          │
│          │                                                   │
│          ▼                                                   │
│   ┌──────────────┐                                          │
│   │ Macrotask Q  │  ← setTimeout / setInterval / I/O        │
│   │  (取一个)     │     MessageChannel / postMessage        │
│   └──────────────┘                                          │
│                                                              │
│   → 回到 Call Stack，循环继续                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 诊断：页面卡顿/输入无响应

**症状**：点击按钮没反应、输入框延迟、滚动卡顿

**根因定位**：
```javascript
// 1. 检查是否有长任务（> 50ms）
// Performance 面板 → Main → 红色三角标记

// 2. 代码层面检测
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.warn('Long Task:', {
      duration: entry.duration,
      startTime: entry.startTime,
      name: entry.name
    });
  }
});
observer.observe({ entryTypes: ['longtask'] });
```

**常见根因**：
| 现象 | 根因 | 验证方法 |
|------|------|---------|
| 长任务 > 50ms | 同步循环/大数据处理 | Performance 面板看 Main Thread |
| 微任务堆积 | Promise 链过深 | 断点看 Microtask Queue |
| 频繁 GC | 大量临时对象分配 | Performance → Memory |

**修复模式**：
```javascript
// ❌ 阻塞主线程
function processLargeArray(items) {
  items.forEach(item => heavyWork(item)); // 可能 > 50ms
}

// ✅ 分片执行
async function processLargeArrayAsync(items, chunkSize = 100) {
  for (let i = 0; i < items.length; i += chunkSize) {
    const chunk = items.slice(i, i + chunkSize);
    chunk.forEach(item => heavyWork(item));
    // 让出主线程
    await new Promise(resolve => setTimeout(resolve, 0));
  }
}

// ✅ 使用 scheduler.yield()（Chrome 115+）
async function processWithYield(items) {
  for (const item of items) {
    heavyWork(item);
    if (scheduler.yield) {
      await scheduler.yield();
    }
  }
}

// ✅ 移到 Web Worker
const worker = new Worker('heavy-work.js');
worker.postMessage(items);
worker.onmessage = (e) => updateUI(e.data);
```

---

## 2. 渲染流水线（Rendering Pipeline）

### 核心模型

```
┌─────────────────────────────────────────────────────────────┐
│                      渲染流水线                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  JavaScript → Style → Layout → Paint → Composite            │
│      │          │        │        │         │               │
│      │          │        │        │         └─ GPU 合成     │
│      │          │        │        └─ 绘制像素               │
│      │          │        └─ 计算几何位置                     │
│      │          └─ 计算最终样式                              │
│      └─ 执行脚本                                             │
│                                                              │
│  触发关系：                                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 改 width/height/top/left → Layout → Paint → Comp   │    │
│  │ 改 color/background      →         Paint → Comp   │    │
│  │ 改 transform/opacity     →                  Comp   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 诊断：动画卡顿/滚动掉帧

**症状**：动画不流畅、滚动时抖动、FPS < 60

**证据采集**：
```
1. DevTools → Performance → Record
2. 操作页面（滚动/动画）
3. 查看：
   - Frames：是否有红色帧（掉帧）
   - Main：Layout/Paint 占比
   - GPU：合成时间
```

**常见根因**：

| 现象 | 根因 | 验证 |
|------|------|------|
| Layout 频繁触发 | 读写交错（Layout Thrashing） | Performance 看紫色 Layout 条 |
| Paint 过重 | 大面积重绘/复杂阴影 | Rendering → Paint flashing |
| 层爆炸 | 过多 will-change/transform | Layers 面板看层数 |

**Layout Thrashing 诊断**：
```javascript
// ❌ 强制同步布局（每次读取都触发 Layout）
elements.forEach(el => {
  const width = el.offsetWidth;      // 读 → 触发 Layout
  el.style.width = width * 2 + 'px'; // 写 → 标记脏
  // 下一次循环的读又触发 Layout！
});

// ✅ 批量读，批量写
const widths = elements.map(el => el.offsetWidth); // 一次性读
elements.forEach((el, i) => {
  el.style.width = widths[i] * 2 + 'px'; // 批量写
});

// ✅ 使用 requestAnimationFrame 分离读写
function optimizedUpdate() {
  // 读
  const measurements = elements.map(el => el.getBoundingClientRect());
  
  requestAnimationFrame(() => {
    // 写（下一帧）
    elements.forEach((el, i) => {
      el.style.transform = `translateX(${measurements[i].width}px)`;
    });
  });
}
```

**高性能动画**：
```css
/* ❌ 触发 Layout */
.animate-bad {
  transition: left 0.3s, width 0.3s;
}

/* ✅ 只触发 Composite（GPU 加速） */
.animate-good {
  transition: transform 0.3s, opacity 0.3s;
  will-change: transform; /* 提前告知浏览器 */
}
```

---

## 3. 内存管理与泄漏

### 诊断：页面越来越慢/崩溃

**症状**：使用一段时间后卡顿、标签页崩溃、内存占用持续上涨

**证据采集**：
```
1. DevTools → Memory → Heap Snapshot
2. 操作页面（切换路由/打开关闭弹窗）
3. 再次 Heap Snapshot
4. 对比 → 查看 Delta（增量对象）
5. 查找 Detached DOM tree
```

**常见泄漏模式**：

```javascript
// ❌ 1. 事件监听未清理
useEffect(() => {
  window.addEventListener('resize', handleResize);
  // 忘记 return cleanup！
}, []);

// ✅ 修复
useEffect(() => {
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);

// ❌ 2. 定时器未清理
useEffect(() => {
  setInterval(pollData, 1000);
  // 组件卸载后仍在运行！
}, []);

// ✅ 修复
useEffect(() => {
  const timer = setInterval(pollData, 1000);
  return () => clearInterval(timer);
}, []);

// ❌ 3. 闭包持有大对象
function createHandler() {
  const hugeData = new Array(1000000).fill('x');
  return () => {
    console.log('handler called');
    // hugeData 永远不会被回收
  };
}

// ✅ 修复：只保留需要的
function createHandler() {
  const hugeData = new Array(1000000).fill('x');
  const summary = hugeData.length; // 只取需要的
  return () => {
    console.log('count:', summary);
  };
}

// ❌ 4. DOM 引用未释放
class Component {
  constructor() {
    this.element = document.querySelector('.target');
  }
  destroy() {
    // this.element 仍持有 DOM 引用
  }
}

// ✅ 修复
destroy() {
  this.element = null;
}
```

**内存泄漏检测脚本**：
```javascript
// 在 Console 执行，监控内存变化
let lastHeap = 0;
setInterval(() => {
  if (performance.memory) {
    const heap = performance.memory.usedJSHeapSize;
    const delta = heap - lastHeap;
    if (delta > 1000000) { // 增长 > 1MB
      console.warn('内存增长:', (delta / 1024 / 1024).toFixed(2), 'MB');
    }
    lastHeap = heap;
  }
}, 5000);
```

---

## 4. 安全模型（CORS/CSP）

### 诊断：跨域请求失败

**症状**：Console 报 CORS 错误、请求被阻止

**错误类型速查**：

| 错误信息 | 根因 | 修复方向 |
|---------|------|---------|
| `No 'Access-Control-Allow-Origin'` | 服务端未配置 CORS | 服务端加响应头 |
| `Preflight response is not successful` | OPTIONS 请求失败 | 检查服务端 OPTIONS 处理 |
| `Credentials flag is true, but...` | credentials 与 Origin 冲突 | 不能用 `*`，需具体域名 |
| `Refused to execute script from...` | CSP 阻止 | 检查 CSP 策略 |

**CORS 诊断流程**：
```javascript
// 1. 简单请求 vs 预检请求
// 简单请求条件：
// - GET/HEAD/POST
// - 只有 Accept/Content-Type 等安全头
// - Content-Type 只能是 text/plain, multipart/form-data, application/x-www-form-urlencoded

// 2. 预检请求（OPTIONS）触发条件：
// - 自定义头（Authorization, X-Custom-Header）
// - Content-Type: application/json
// - PUT/DELETE/PATCH

// 3. 服务端配置示例（Express）
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', 'https://your-app.com');
  res.header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE');
  res.header('Access-Control-Allow-Headers', 'Content-Type,Authorization');
  res.header('Access-Control-Allow-Credentials', 'true');
  
  if (req.method === 'OPTIONS') {
    return res.sendStatus(204);
  }
  next();
});
```

**开发环境代理绕过 CORS**：
```javascript
// vite.config.js
export default {
  server: {
    proxy: {
      '/api': {
        target: 'https://api.example.com',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
}
```

---

## 5. 诊断命令速查

### Performance 面板

```
录制 → 操作 → 停止 → 分析：
- Summary：各阶段时间占比
- Main：主线程活动（找红色三角 = 长任务）
- Frames：帧率（红色 = 掉帧）
- Network：资源加载时序
```

### Memory 面板

```
Heap Snapshot：
- 操作前快照 → 操作 → 操作后快照
- Comparison 视图看 Delta
- 搜索 "Detached" 找未释放 DOM

Allocation Timeline：
- 录制期间的内存分配
- 蓝色条 = 仍在内存中
```

### Rendering 面板

```
勾选：
- Paint flashing：绿色闪烁 = 重绘区域
- Layout Shift Regions：蓝色 = 布局偏移
- Layer borders：橙色边框 = 合成层
- FPS meter：实时帧率
```

### Console 命令

```javascript
// 检测长任务
new PerformanceObserver((list) => {
  list.getEntries().forEach(e => console.log('Long task:', e.duration));
}).observe({ entryTypes: ['longtask'] });

// 检测布局偏移
new PerformanceObserver((list) => {
  list.getEntries().forEach(e => {
    if (!e.hadRecentInput) console.log('CLS:', e.value);
  });
}).observe({ entryTypes: ['layout-shift'] });

// 内存使用
console.log(performance.memory);

// 资源加载
performance.getEntriesByType('resource').forEach(r => {
  console.log(r.name, r.duration);
});
```

---

## 6. 快速诊断清单

```markdown
## 浏览器问题诊断

### 卡顿/无响应
- [ ] Performance 面板查长任务 (> 50ms)
- [ ] 是否有同步大循环？
- [ ] 是否有 Layout Thrashing？
- [ ] 微任务是否堆积？

### 动画掉帧
- [ ] 动画属性是否只用 transform/opacity？
- [ ] 是否有强制同步布局？
- [ ] Layers 面板层数是否合理？
- [ ] will-change 是否过度使用？

### 内存泄漏
- [ ] Heap Snapshot 对比有无 Detached DOM？
- [ ] 事件监听器是否清理？
- [ ] 定时器是否清理？
- [ ] 闭包是否持有大对象？

### 跨域问题
- [ ] 服务端 CORS 头是否正确？
- [ ] 是否触发了预检请求？
- [ ] credentials 与 Origin 是否冲突？
- [ ] CSP 是否阻止资源？
```
