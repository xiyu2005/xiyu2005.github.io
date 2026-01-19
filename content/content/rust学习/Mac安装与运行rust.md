下载
```
$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
```

创建
```rust
fn main() {
    println!("Hello, world!");
}
```



```
#编译
$ rustc main.rs
#运行
$ ./main
>>Hello, world!
```

安装cargo
```
$ cargo new get-dependencies
$ cd get-dependencies
$ cargo add rand@0.8.5 trpl@0.2.0

```

创建cargo项目
```
cargo new hello_cargo
cd hello_cargo
```

构建cargo项目
```
cargo build
   Compiling hello_cargo v0.1.0 (/Users/kaisenye/Desktop/chuangsai/Nirvana/rust/project/hello_cargo)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.50s
```
此命令在_target/debug/hello_cargo文件夹下创建了可执行文件
```
./target/debug/hello_cargo
Hello, world!
```
也可以cargo run来构建+运行
```
kaisenye@kaisendeMacBook-Air hello_cargo % cargo run
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/hello_cargo`
Hello, world!
```
检查代码正确性
```
cargo check
kaisenye@kaisendeMacBook-Air hello_cargo % cargo check
    Checking hello_cargo v0.1.0 (/Users/kaisenye/Desktop/chuangsai/Nirvana/rust/project/hello_cargo)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.27s
```