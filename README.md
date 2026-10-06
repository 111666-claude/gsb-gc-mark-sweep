# gc-mark-sweep

对象图上的标记清除回收。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m heapgc --sample=chain
python3 -m heapgc --sample=dup
python3 -m heapgc --sample=gen
python3 -m heapgc --sample=work
```

## 口径

- **可达**：从根集合沿引用**传递地**标记，链子中间任何一环都不能漏。
- **释放**：不可达对象的代数加一，只有代数超过 `gen_limit` 才真正回收并在释放列表里出现。
- **代数**：可达对象回到年轻代。

## 不变量

- 可达对象一定不出现在释放列表里。
- 每个对象每轮只判一次，释放列表无重复。
- `scanned` 不随对象数平方级放大：两千个对象的 `scanned` 不超过 6000。

## 输出契约

每个场景打印一行 JSON，`freed` 是释放的对象 id 列表；
`--sample=work` 只打印 `{"objects": N, "scanned": N}`。
