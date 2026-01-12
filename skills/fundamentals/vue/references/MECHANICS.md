# Vue 响应式与渲染扩展

## 依赖追踪
- `reactive`/`ref` 通过 Proxy 收集依赖，`track/trigger` 维护关系图。
- 解构/浅拷贝会丢失响应性。

## 调度与批处理
- 更新进入调度队列，`nextTick` 在 flush 后执行。
- 关注 `flush: pre/post/sync` 的时序差异。

## computed 与 watch
- computed 具备缓存与惰性求值；watch 关注副作用清理。
- watchEffect 会自动追踪依赖但更易过度触发。

## SSR 与 Hydration
- 服务端与客户端渲染输出必须一致。
- 依赖随机数/时间等非确定值易导致 mismatch。
