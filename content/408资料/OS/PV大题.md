
2、【11-45】(8分) 某银行提供 1 个服务窗口和 10 个供顾客等待的座位。顾客到达银行时，若有空座位，则到取号机上领取一个号，等待叫号。取号机每次仅允许一位顾客使用。当营业员空闲时，通过叫号选取一位顾客，并为其服务。顾客和营业员的活动过程描述如下：

```c
cobegin {
    process 顾客 i {
        从取号机获取一个号码;
        等待叫号;
        获取服务;
    }

    process 营业员 {
        while (TRUE) {
            叫号;
            为客户服务;
        }
    }
} coend
```

请添加必要的信号量和 P、V (或 wait()、signal()) 操作，实现上述过程中的互斥与同步。要求写出完整的过程，说明信号量的含义并赋初值。



```
#define MAXN 100   // 最大顾客数

semaphore mutex = 1;               // 取号机互斥
semaphore seats_empty = 10;        // 空座位数
semaphore waiting_customers = 0;   // 等待服务的顾客数
semaphore service[MAXN] = {0};     // 每个顾客的叫号信号
semaphore done[MAXN] = {0};        // 每个顾客的服务完成信号

cobegin {
    process 顾客i {
        P(seats_empty);            // 申请座位（无空位则阻塞）
        P(mutex);                  // 申请取号机
        从取号机获取一个号码;
        V(mutex);                  // 释放取号机
        V(waiting_customers);      // 通知营业员有顾客等待
        P(service[i]);             // 等待营业员叫自己的号
        V(seats_empty);            // 被叫到，起身让座
        获取服务;
        P(done[i]);                // 等待服务完成
        // 顾客离开
    }

    process 营业员 {
        int i;
        while (TRUE) {
            P(waiting_customers);  // 有顾客等待才叫号
            叫号;// 从等待队列中选一位顾客，得到其编号 i
            V(service[i]);         // 叫号，唤醒该顾客
            为客户服务;           // 服务过程（耗时操作）
            V(done[i]);            // 通知该顾客服务结束
        }
    }
} coend
```

```
semaphore done[N] = {0};   // 服务完成信号

顾客 i {
    P(empty);
    P(mutex);
    取号;
    V(mutex);
    V(full);
    P(service);        // 等待叫号
    // 被叫到后，不立即获取服务，而是等待服务完成
    P(done[i]);        // 等待服务结束
    // 服务完成，离开
}


营业员 {
    while(1) {
        P(full);
        V(service);          // 叫号，唤醒一个顾客（顾客会阻塞在 done[i] 上）
        // 注意：此时顾客被唤醒后执行 P(done[i]) 会阻塞
        为客户服务;          // 服务过程
        V(done[i]);          // 服务结束，通知该顾客
        V(empty);            // 释放座位（可以在服务结束后释放，也可提前释放，两种均可）
    }
}
```