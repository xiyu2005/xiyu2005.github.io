列访问表

【2017PV大题】请添加必要的信号量和 P、V（或`wait()`、`signal()`）操作，要求确保线程互斥访问临界资源，并且最大限度地并发执行。
```c
// 复数的结构类型定义
typedef struct {
    float a;
    float b;
} cnum;

cnum x, y, z; // 全局变量

// 计算两个复数之和
cnum add(cnum p, cnum q) {
    cnum s;
    s.a = p.a + q.a;
    s.b = p.b + q.b;
    return s;
}

thread1() {
    cnum w;
    w = add(x, y);
    ...
}

thread2() {
    cnum w;
    w = add(y, z);
    ...
}

thread3() {
    cnum w;
    w.a = 1;
    w.b = 1;
    z = add(z, w);
    y = add(y, w);
    ...
}
```


## 1. 最优性的定义

在本题条件下，“最优解”通常同时满足：

1. **正确性**：所有对共享变量 `y`、`z` 的读写互斥关系得到保证。
2. **最大并发性**：只有真正冲突的操作才互斥，不冲突的操作可以同时执行。
3. **信号量数量最少**：在满足前两条的前提下，使用的信号量个数达到下界。


```c
thread1() {
    cnum w;
    P(mutex_y_13);  // thread1 和 thread3 互斥访问 y
    w = add(x, y);
    V(mutex_y_13);
    ...
}

thread2() {
    cnum w;
    P(mutex_y_23);  // thread2 和 thread3 互斥访问 y
    P(mutex_z_23);  // thread2 和 thread3 互斥访问 z
    w = add(y, z);
    V(mutex_z_23);
    V(mutex_y_23);
    ...
}

thread3() {
    cnum w;
    w.a = 1;
    w.b = 1;
    P(mutex_z_23);  // thread2 和 thread3 互斥访问 z
    z = add(z, w);
    V(mutex_z_23);
    
    P(mutex_y_13);  // thread1 和 thread3 互斥访问 y
    P(mutex_y_23);  // thread2 和 thread3 互斥访问 y
    y = add(y, w);
    V(mutex_y_23);
    V(mutex_y_13);
    ...
}


```
下面证明用户提出的三信号量方案同时满足以上三点。

---

## 2. 方案的正确性

列出三个线程对共享变量的访问：

| 线程      | 对 `y` | 对 `z` |
| ------- | ----- | ----- |
| thread1 | 读     | 不访问   |
| thread2 | 读     | 读     |
| thread3 | 写     | 写     |

必须互斥的冲突对有：
- thread1 读 `y` 与 thread3 写 `y`
- thread2 读 `y` 与 thread3 写 `y`
- thread2 读 `z` 与 thread3 写 `z`
方案中：
- `mutex_y_13`：正好覆盖 thread1 与 thread3 在 `y` 上的冲突。
- `mutex_y_23`：正好覆盖 thread2 与 thread3 在 `y` 上的冲突。
- `mutex_z_23`：正好覆盖 thread2 与 thread3 在 `z` 上的冲突。

thread3 写 `y` 时同时持有 `mutex_y_13` 和 `mutex_y_23`，因此可以同时阻止 thread1 和 thread2 读 `y`；写 `z` 时持有 `mutex_z_23`，可以阻止 thread2 读 `z`。各线程的锁顺序无环，**无死锁**。

因此，所有必要的互斥关系都得到满足，正确性成立。


## 3. 并发性最优的证明

“最大并发”要求：**不冲突的操作不应被互斥信号量阻塞**。

该方案中：

- thread1 读 `y` 和 thread2 读 `y` 是读—读，不冲突，分别只获取 `mutex_y_13` 和 `mutex_y_23`，互不影响，可以同时执行。
- thread1 读 `y` 和 thread2 读 `z` 访问不同变量，不冲突，使用的信号量也不同，可以同时执行。
- thread1 读 `y` 和 thread3 写 `z` 访问不同变量，不冲突，thread3 写 `z` 只获取 `mutex_z_23`，不阻塞 thread1，可以同时执行。

也就是说，所有可能并发的不冲突操作，在该方案中都没有被不必要的串行化。因此并发性已经达到最大，无法再减少任何互斥而不破坏正确性。

---

## 4. 信号量数量最少的证明

在最大并发前提下，至少需要 **3 个**信号量。

理由如下：

三对必须互斥的冲突关系：

1. thread1 读 `y` ↔ thread3 写 `y`
2. thread2 读 `y` ↔ thread3 写 `y`
3. thread2 读 `z` ↔ thread3 写 `z`

如果只使用 2 个信号量，则必须存在至少一个信号量同时负责两个不同的冲突关系。

例如：

- 若用一个信号量同时保护 `y` 的两次读与写，则 thread1 和 thread2 读 `y` 会互相阻塞，违反最大并发。
- 若用一个信号量同时保护 thread2 读 `z` 和 thread2 读 `y`，则 thread1 读 `y` 与 thread2 读 `z` 可能被不必要的串行化。

由于存在三对独立的互斥需求，且其中任意两对共享同一信号量都会导致不冲突操作被阻塞，因此在保证最大并发的前提下，信号量数量不能少于 3 个。

用户方案恰好使用了 3 个信号量，达到了下界。

---

## 5. 结论

在本题给定的三个线程场景下，用户提出的三信号量方案是**最优解**：

- 正确性：所有读写冲突对都被正确互斥。
- 最大并发：所有不冲突的操作都可以并行执行。
- 最少信号量：3 个信号量已达到该并发要求下的下界。

该方案属于“为每个读者实例分配独立锁”的策略，适用于线程数量固定且较少的情况。如果读者线程数量不固定，通用读写锁方案更具扩展性，但在本题条件下，定制方案更简洁且最优。



## 改编题目

在原复数计算问题的基础上，增加一条**顺序要求**：

> thread3 对 `z` 和 `y` 的写操作，必须等到 thread1 和 thread2 都完成各自的读操作之后才能开始。

线程访问方式不变：

- `thread1`：读 `x, y`
- `thread2`：读 `y, z`
- `thread3`：先写 `z`，再写 `y`

要求：  
1. 保证对 `y, z` 的读写互斥，且不冲突的读操作可并发；  
2. 满足上述顺序限制。

---

## 信号量定义及初值

| 信号量 | 作用 | 初值 |
|--------|------|------|
| `mutex_y_13` | 互斥 `thread1` 读 `y` 与 `thread3` 写 `y` | 1 |
| `mutex_y_23` | 互斥 `thread2` 读 `y` 与 `thread3` 写 `y` | 1 |
| `mutex_z_23` | 互斥 `thread2` 读 `z` 与 `thread3` 写 `z` | 1 |
| `done1` | 表示 `thread1` 已完成读操作 | 0 |
| `done2` | 表示 `thread2` 已完成读操作 | 0 |

---

## 代码实现

```c
semaphore mutex_y_13 = 1, mutex_y_23 = 1, mutex_z_23 = 1;
semaphore done1 = 0, done2 = 0;

thread1() {
    cnum w;
    P(mutex_y_13);          // 与 thread3 互斥访问 y
    w = add(x, y);
    V(mutex_y_13);
    signal(done1);          // 通知 thread3：thread1 已完成读操作
}

thread2() {
    cnum w;
    P(mutex_y_23);          // 与 thread3 互斥访问 y
    P(mutex_z_23);          // 与 thread3 互斥访问 z
    w = add(y, z);
    V(mutex_z_23);
    V(mutex_y_23);
    signal(done2);          // 通知 thread3：thread2 已完成读操作
}

thread3() {
    cnum w;
    w.a = 1;
    w.b = 1;

    wait(done1);            // 等待 thread1 完成
    wait(done2);            // 等待 thread2 完成

    P(mutex_z_23);          // 写 z，与 thread2 互斥
    z = add(z, w);
    V(mutex_z_23);

    P(mutex_y_13);          // 写 y，与 thread1、thread2 互斥
    P(mutex_y_23);
    y = add(y, w);
    V(mutex_y_23);
    V(mutex_y_13);
}
```

---

## 解释

- `done1`、`done2` 实现**顺序同步**：  
  thread3 必须等待两个 `done` 信号量都被 `signal` 后，才能开始写操作，满足“thread3 写之前，thread1 和 thread2 已完成读”的要求。

- `mutex_*` 信号量负责**互斥**：  
  - `thread1` 和 `thread2` 都是 `y` 的读者，互不影响；  
  - `thread3` 写 `y` 时同时持有 `mutex_y_13` 和 `mutex_y_23`，阻止两个读者；  
  - `thread3` 写 `z` 时持有 `mutex_z_23`，阻止 thread2 读 `z`。

- 前驱关系可表示为：  
  ```
  thread1 读 y ──┐
                 ├──→ thread3 写 z ──→ thread3 写 y
  thread2 读 y,z ┘
  ```
  这体现了顺序要求，而互斥关系仍通过访问表设计。