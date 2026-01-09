# 算法优化模式库（LeetCode 实战版）

> **核心原则**: 选择正确的算法比微优化代码更重要
> **来源**: [LeetCode](https://leetcode.com) 高频题解 + [Big-O Cheat Sheet](https://www.bigocheatsheet.com/)

---

## 复杂度速查表

### 时间复杂度排名

```
最优 ──────────────────────────────────────────────▶ 最差

O(1) → O(log n) → O(n) → O(n log n) → O(n²) → O(2^n) → O(n!)

常数    对数      线性    线性对数     平方      指数      阶乘
```

### 实际运行时间估算（n = 10^6）

| 复杂度 | 操作次数 | 实际耗时 | 可接受? |
|--------|---------|---------|--------|
| O(1) | 1 | < 1ms | ✅ |
| O(log n) | 20 | < 1ms | ✅ |
| O(n) | 10^6 | ~10ms | ✅ |
| O(n log n) | 2×10^7 | ~200ms | ✅ |
| O(n²) | 10^12 | ~3 小时 | ❌ |
| O(2^n) | 10^301029 | ∞ | ❌ |

---

## LeetCode 高频算法模式

### 1. HashMap/HashSet 查找优化

**适用场景**: Two Sum、统计频次、查找重复、O(n) 降到 O(1) 查找

**LeetCode 原题**: [1. Two Sum](https://leetcode.com/problems/two-sum/)

```typescript
// ❌ 暴力解法 O(n²)
function twoSum_brute(nums: number[], target: number): number[] {
  for (let i = 0; i < nums.length; i++) {
    for (let j = i + 1; j < nums.length; j++) {
      if (nums[i] + nums[j] === target) return [i, j];
    }
  }
  return [];
}

// ✅ HashMap 一遍扫描 O(n)
function twoSum(nums: number[], target: number): number[] {
  const map = new Map<number, number>(); // 值 -> 索引
  for (let i = 0; i < nums.length; i++) {
    const complement = target - nums[i];
    if (map.has(complement)) {
      return [map.get(complement)!, i];
    }
    map.set(nums[i], i);
  }
  return [];
}
```

```python
# Python 版本
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}  # 值 -> 索引
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

**前端实战应用**:

```typescript
// 用户列表查找优化
// ❌ O(n) - 每次查找都遍历
const users = [{ id: 1, name: 'Alice' }, { id: 2, name: 'Bob' }];
const findUser = (id: number) => users.find(u => u.id === id);

// ✅ O(1) - HashMap 查找
const userMap = new Map(users.map(u => [u.id, u]));
const findUser = (id: number) => userMap.get(id);

// 什么时候建立 HashMap?
// 规则: 查找次数 > 1 && 数据量 > 100 → 建立 HashMap
```

---

### 2. 双指针 (Two Pointers)

**适用场景**: 有序数组、链表、回文检测、O(n²) 降到 O(n)

**LeetCode 原题**: [11. Container With Most Water](https://leetcode.com/problems/container-with-most-water/)

```typescript
// ❌ 暴力解法 O(n²)
function maxArea_brute(height: number[]): number {
  let max = 0;
  for (let i = 0; i < height.length; i++) {
    for (let j = i + 1; j < height.length; j++) {
      const area = Math.min(height[i], height[j]) * (j - i);
      max = Math.max(max, area);
    }
  }
  return max;
}

// ✅ 双指针 O(n)
function maxArea(height: number[]): number {
  let left = 0, right = height.length - 1;
  let max = 0;

  while (left < right) {
    const area = Math.min(height[left], height[right]) * (right - left);
    max = Math.max(max, area);

    // 移动较小的那边
    if (height[left] < height[right]) {
      left++;
    } else {
      right--;
    }
  }
  return max;
}
```

```python
# Python 版本
def max_area(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    max_area = 0

    while left < right:
        area = min(height[left], height[right]) * (right - left)
        max_area = max(max_area, area)

        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_area
```

**双指针变体**:

| 类型 | 特征 | 典型问题 |
|------|------|---------|
| 对向双指针 | 左右向中间靠拢 | Two Sum II, Container With Most Water |
| 同向双指针 | 快慢指针 | 链表环检测, 移除重复元素 |
| 滑动窗口 | 维护区间条件 | 最长无重复子串, 最小覆盖子串 |

---

### 3. 滑动窗口 (Sliding Window)

**适用场景**: 连续子数组/子串问题、O(n²) 降到 O(n)

**LeetCode 原题**: [3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

```typescript
// ❌ 暴力解法 O(n³) - 检查所有子串
function lengthOfLongestSubstring_brute(s: string): number {
  let max = 0;
  for (let i = 0; i < s.length; i++) {
    for (let j = i; j < s.length; j++) {
      const substring = s.slice(i, j + 1);
      if (new Set(substring).size === substring.length) {
        max = Math.max(max, substring.length);
      }
    }
  }
  return max;
}

// ✅ 滑动窗口 + HashMap O(n)
function lengthOfLongestSubstring(s: string): number {
  const charIndex = new Map<string, number>(); // 字符 -> 最近索引
  let left = 0;
  let max = 0;

  for (let right = 0; right < s.length; right++) {
    const char = s[right];

    // 如果字符已存在且在窗口内，收缩左边界
    if (charIndex.has(char) && charIndex.get(char)! >= left) {
      left = charIndex.get(char)! + 1;
    }

    charIndex.set(char, right);
    max = Math.max(max, right - left + 1);
  }

  return max;
}
```

```python
# Python 版本
def length_of_longest_substring(s: str) -> int:
    char_index = {}  # 字符 -> 最近索引
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1

        char_index[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len
```

**滑动窗口模板**:

```typescript
function slidingWindowTemplate<T>(arr: T[], condition: Function): number {
  const window = new Map<T, number>(); // 窗口状态
  let left = 0;
  let result = 0;

  for (let right = 0; right < arr.length; right++) {
    // 1. 扩展右边界
    const rightItem = arr[right];
    window.set(rightItem, (window.get(rightItem) || 0) + 1);

    // 2. 收缩左边界直到满足条件
    while (!condition(window)) {
      const leftItem = arr[left];
      window.set(leftItem, window.get(leftItem)! - 1);
      if (window.get(leftItem) === 0) window.delete(leftItem);
      left++;
    }

    // 3. 更新结果
    result = Math.max(result, right - left + 1);
  }

  return result;
}
```

---

### 4. 记忆化 (Memoization)

**适用场景**: 重叠子问题、递归优化、O(2^n) 降到 O(n)

**LeetCode 原题**: [70. Climbing Stairs](https://leetcode.com/problems/climbing-stairs/)

```typescript
// ❌ 朴素递归 O(2^n) - 指数级
function climbStairs_naive(n: number): number {
  if (n <= 2) return n;
  return climbStairs_naive(n - 1) + climbStairs_naive(n - 2);
}
// climbStairs_naive(40) 需要约 10 亿次递归

// ✅ 记忆化递归 O(n)
function climbStairs_memo(n: number, memo = new Map<number, number>()): number {
  if (n <= 2) return n;
  if (memo.has(n)) return memo.get(n)!;

  const result = climbStairs_memo(n - 1, memo) + climbStairs_memo(n - 2, memo);
  memo.set(n, result);
  return result;
}

// ✅ 动态规划迭代 O(n) 空间 O(1)
function climbStairs(n: number): number {
  if (n <= 2) return n;
  let prev = 1, curr = 2;

  for (let i = 3; i <= n; i++) {
    const next = prev + curr;
    prev = curr;
    curr = next;
  }

  return curr;
}
```

```python
# Python 版本 - 使用 @lru_cache
from functools import lru_cache

@lru_cache(maxsize=None)
def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    return climb_stairs(n - 1) + climb_stairs(n - 2)

# 或者迭代版本
def climb_stairs_iter(n: int) -> int:
    if n <= 2:
        return n
    prev, curr = 1, 2
    for _ in range(3, n + 1):
        prev, curr = curr, prev + curr
    return curr
```

**React 中的记忆化**:

```typescript
// useMemo - 缓存计算结果
const expensiveValue = useMemo(() => {
  return items.filter(i => i.active).map(i => heavyTransform(i));
}, [items]);

// useCallback - 缓存函数引用
const handleClick = useCallback((id: string) => {
  dispatch(selectItem(id));
}, [dispatch]);

// React.memo - 缓存组件
const ExpensiveList = React.memo(({ items }) => {
  return items.map(item => <ExpensiveItem key={item.id} item={item} />);
});
```

---

### 5. 扁平化 + 索引

**适用场景**: 树形结构频繁查找、O(n×深度) 降到 O(1)

**前端实战应用**:

```typescript
// ❌ 递归查找节点 O(n×depth)
interface TreeNode {
  id: string;
  children: TreeNode[];
}

function findNode(tree: TreeNode, id: string): TreeNode | null {
  if (tree.id === id) return tree;
  for (const child of tree.children) {
    const found = findNode(child, id);
    if (found) return found;
  }
  return null;
}

// ✅ 扁平化 + 索引 O(1) 查找
function buildIndex(root: TreeNode): Map<string, TreeNode> {
  const index = new Map<string, TreeNode>();

  const traverse = (node: TreeNode) => {
    index.set(node.id, node);
    node.children.forEach(traverse);
  };

  traverse(root);
  return index;
}

const nodeIndex = buildIndex(tree);
const findNode = (id: string) => nodeIndex.get(id); // O(1)
```

```python
# Python 版本
def build_index(root: dict) -> dict:
    index = {}

    def traverse(node):
        index[node['id']] = node
        for child in node.get('children', []):
            traverse(child)

    traverse(root)
    return index

# 使用
node_index = build_index(tree)
find_node = lambda id: node_index.get(id)  # O(1)
```

**ReactFlow 节点索引示例**:

```typescript
// ReactFlow 节点快速查找
const useNodeIndex = (nodes: Node[]) => {
  return useMemo(() => {
    return new Map(nodes.map(node => [node.id, node]));
  }, [nodes]);
};

// 使用
const nodeIndex = useNodeIndex(nodes);
const getNode = (id: string) => nodeIndex.get(id);
```

---

### 6. 二分查找

**适用场景**: 有序数组查找、O(n) 降到 O(log n)

**LeetCode 原题**: [704. Binary Search](https://leetcode.com/problems/binary-search/)

```typescript
// ❌ 线性查找 O(n)
function search_linear(nums: number[], target: number): number {
  return nums.indexOf(target);
}

// ✅ 二分查找 O(log n)
function search(nums: number[], target: number): number {
  let left = 0, right = nums.length - 1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);

    if (nums[mid] === target) {
      return mid;
    } else if (nums[mid] < target) {
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }

  return -1;
}
```

```python
# Python 版本 - 使用 bisect 模块
import bisect

def search(nums: list[int], target: int) -> int:
    i = bisect.bisect_left(nums, target)
    if i < len(nums) and nums[i] == target:
        return i
    return -1

# 手写版本
def binary_search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

---

### 7. 虚拟滚动

**适用场景**: 大列表渲染、O(n) DOM 节点降到 O(k) 可视区

```typescript
// ❌ 渲染所有项 O(n) - 10000 项 = 10000 个 DOM 节点
{items.map(item => <ListItem key={item.id} item={item} />)}

// ✅ 虚拟滚动 O(k) - 只渲染可视区 ~20 个 DOM 节点
import { Virtuoso } from 'react-virtuoso';

<Virtuoso
  data={items}
  itemContent={(index, item) => <ListItem item={item} />}
/>

// 或使用 react-window
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={400}
  itemCount={items.length}
  itemSize={50}
>
  {({ index, style }) => (
    <div style={style}>
      <ListItem item={items[index]} />
    </div>
  )}
</FixedSizeList>
```

---

### 8. 防抖与节流

**适用场景**: 高频事件处理、降低调用频率

```typescript
// 防抖 - 停止触发后才执行 (搜索输入)
function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timer: ReturnType<typeof setTimeout>;

  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

// 节流 - 固定频率执行 (滚动事件)
function throttle<T extends (...args: any[]) => any>(
  fn: T,
  interval: number
): (...args: Parameters<T>) => void {
  let lastTime = 0;

  return (...args) => {
    const now = Date.now();
    if (now - lastTime >= interval) {
      lastTime = now;
      fn(...args);
    }
  };
}
```

```python
# Python 版本
import time
from functools import wraps

def debounce(delay: float):
    def decorator(fn):
        timer = [None]

        @wraps(fn)
        def wrapper(*args, **kwargs):
            if timer[0]:
                timer[0].cancel()
            timer[0] = threading.Timer(delay, fn, args, kwargs)
            timer[0].start()

        return wrapper
    return decorator

def throttle(interval: float):
    def decorator(fn):
        last_time = [0]

        @wraps(fn)
        def wrapper(*args, **kwargs):
            now = time.time()
            if now - last_time[0] >= interval:
                last_time[0] = now
                return fn(*args, **kwargs)

        return wrapper
    return decorator
```

---

### 9. 分批处理 (Chunking)

**适用场景**: 大数据处理、避免阻塞主线程

```typescript
// ❌ 同步处理 - 阻塞主线程
function processAll(items: Item[]) {
  items.forEach(item => heavyProcessing(item));
}

// ✅ 分批处理 - 保持响应
async function processInChunks(
  items: Item[],
  chunkSize = 100
): Promise<void> {
  for (let i = 0; i < items.length; i += chunkSize) {
    const chunk = items.slice(i, i + chunkSize);
    chunk.forEach(item => heavyProcessing(item));

    // 让出主线程
    await new Promise(resolve => setTimeout(resolve, 0));
  }
}

// ✅ 使用 requestIdleCallback
function processWhenIdle(items: Item[], index = 0) {
  requestIdleCallback((deadline) => {
    while (deadline.timeRemaining() > 0 && index < items.length) {
      heavyProcessing(items[index]);
      index++;
    }

    if (index < items.length) {
      processWhenIdle(items, index);
    }
  });
}
```

```python
# Python 版本 - 使用生成器
def process_in_chunks(items: list, chunk_size: int = 100):
    for i in range(0, len(items), chunk_size):
        chunk = items[i:i + chunk_size]
        for item in chunk:
            heavy_processing(item)
        yield i + len(chunk)  # 进度

# 使用
for progress in process_in_chunks(items):
    print(f"Processed: {progress}/{len(items)}")
```

---

## React 特定优化

### 避免不必要的重渲染

```typescript
// ❌ 内联对象 - 每次渲染创建新对象
<Component style={{ color: 'red' }} />

// ✅ 提取到组件外或 useMemo
const style = { color: 'red' };
<Component style={style} />

// ❌ 内联回调 - 每次渲染创建新函数
<Button onClick={() => handleClick(id)} />

// ✅ useCallback 缓存
const handleClickMemo = useCallback(() => handleClick(id), [id]);
<Button onClick={handleClickMemo} />

// ❌ 派生数据未缓存
<List items={items.filter(i => i.active)} />

// ✅ useMemo 缓存派生数据
const activeItems = useMemo(() => items.filter(i => i.active), [items]);
<List items={activeItems} />
```

### React.memo 使用指南

```typescript
// ✅ 适合 memo 的场景
// - 渲染开销大 (复杂组件/大列表项)
// - props 变化不频繁
// - 父组件频繁重渲染
const ExpensiveComponent = React.memo(({ data }) => {
  return <ComplexVisualization data={data} />;
});

// ❌ 不适合 memo 的场景
// - 简单组件 (比较开销 > 渲染开销)
// - props 每次都变
// - 子组件很少
const SimpleLabel = React.memo(({ text }) => <span>{text}</span>); // 过度优化
```

---

## 算法模式选择指南

| 问题特征 | 推荐模式 | 复杂度改进 |
|---------|---------|-----------|
| 查找配对/求和 | HashMap | O(n²) → O(n) |
| 有序数组处理 | 双指针 | O(n²) → O(n) |
| 连续子数组/子串 | 滑动窗口 | O(n²) → O(n) |
| 重叠子问题 | 记忆化/DP | O(2^n) → O(n) |
| 树形结构查找 | 扁平化索引 | O(n×d) → O(1) |
| 有序查找 | 二分查找 | O(n) → O(log n) |
| 大列表渲染 | 虚拟滚动 | O(n) → O(k) |
| 高频事件 | 防抖/节流 | 降低调用频率 |
| 长任务 | 分批处理 | 阻塞 → 非阻塞 |

---

## 性能检测

### 识别复杂度问题

```typescript
// 使用 Performance API 检测
const measurePerformance = <T>(fn: () => T, label: string): T => {
  const start = performance.now();
  const result = fn();
  const end = performance.now();
  console.log(`${label}: ${(end - start).toFixed(2)}ms`);
  return result;
};

// 不同数据量测试 - 判断复杂度
[100, 1000, 10000].forEach(n => {
  const data = generateData(n);
  measurePerformance(() => processData(data), `n=${n}`);
});

// 结果分析:
// - 耗时与 n 成正比 → O(n)
// - 耗时与 n² 成正比 → O(n²)
// - 耗时翻倍时 n 翻 10 倍 → O(log n)
```

---

**来源参考**:
- [LeetCode](https://leetcode.com) 高频题解
- [NeetCode Roadmap](https://neetcode.io/roadmap)
- [Medium - Algorithm Patterns](https://medium.com)

**记住**: 过早优化是万恶之源。先测量，确认是瓶颈，再优化。

