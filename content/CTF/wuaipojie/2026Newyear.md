## WindowsEZ

本程序为 CrackMe 挑战，核心逻辑位于 `sub_4CD130` 函数中。通过静态分析可知，Flag 的验证需满足三个硬性条件：长度必须为 31 字节，核心函数 `sub_4016D0` 验证需通过，且满足累加校验和 $\sum_{i=0}^{30} (i+1) \times \text{char}[i] = 44709$。进入分析 `sub_4016D0` 发现，程序调用 `sub_401620` 在内存中生成了一个标准序列并与输入进行逐位比对。在 `sub_401620` 函数内，程序先通过小端序方式在栈上布置了一系列 `DWORD`、`WORD` 及 `BYTE` 类型的 16 进制常数，随后利用循环将这些字节与 `0x42` 进行异或运算。通过 Python 脚本还原该内存布局并执行异或逆运算，可解密出原始字符串为 `52pojie!!!_2026_Happy_new_year!`。经计算，该字符串的加权校验和恰好等于 44709，完全符合所有验证逻辑，确认为最终正确的 Flag。

start函数中进入入口sub_4CD130

```
if ( strlen(Str) != 31 ) {
    // 提示长度不正确
    goto LABEL_9;
}
```
说明长度31位
4016D0
```
bool __cdecl sub_4016D0(int a1, int a2)
{
  unsigned __int8 *Block; // ebp
  int v3; // eax
  int v4; // ebx
  bool v5; // dl

  Block = (unsigned __int8 *)sub_4CB710(0x64u);
  sub_401620((int)Block);
  if ( a2 <= 0 )
  {
    v4 = 0;
  }
  else
  {
    v3 = 0;
    v4 = 0;
    do
    {
      v5 = *(char *)(a1 + v3) == Block[v3];
      ++v3;
      v4 += v5;
    }
    while ( a2 != v3 );
  }
  j_j_free(Block);
  return a2 == v4;
}


_BYTE *__cdecl sub_401620(int a1)
{
  _BYTE *result; // eax

  *(_DWORD *)a1 = 758280311;
  *(_DWORD *)(a1 + 4) = 1663511336;
  *(_DWORD *)(a1 + 8) = 1880974179;
  *(_DWORD *)(a1 + 12) = 494170226;
  *(_DWORD *)(a1 + 16) = 842146570;
  *(_DWORD *)(a1 + 20) = 657202491;
  *(_DWORD *)(a1 + 24) = 658185525;
  *(_BYTE *)(a1 + 30) = 99;
  *(_WORD *)(a1 + 28) = 12323;
  result = (_BYTE *)a1;
  do
    *result++ ^= 0x42u;
  while ( result != (_BYTE *)(a1 + 31) );
  *(_BYTE *)(a1 + 31) = 0;
  return result;
}
```