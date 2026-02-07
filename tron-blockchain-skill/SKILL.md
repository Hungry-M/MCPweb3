---
name: tron-blockchain
description: 与 TRON 区块链交互的技能。通过 tron-mcp-server 的 call(action, params) 调用。用于查询 USDT/TRX 余额、获取 Gas 参数、检查交易状态、构建未签名交易。
---

# TRON 区块链操作技能

## 概述

此技能使你能够与 TRON 区块链进行交互，完成常见的链上操作任务。

**关键词**: TRON, TRX, USDT, TRC20, 余额查询, Gas, 交易状态, 转账, 区块链

---

## 可用工具

此技能通过 `tron-mcp-server` MCP 服务器提供以下动作（通过 `call(action, params)` 调用）：

### 0. `skills`
获取当前服务器支持的所有技能清单。

**参数:** 无

**返回:**
- `skills`: 包含所有可用动作、描述和参数的列表
- `summary`: 技能加载摘要

---

### 1. `get_usdt_balance`
查询指定地址的 USDT (TRC20) 余额。

**参数:**
- `address` (必填): TRON 地址，支持两种格式：
  - Base58: 以 `T` 开头，34 字符（如 `TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf`）
  - Hex: 以 `0x41` 开头，44 字符

**返回:**
- `address`: 查询地址
- `balance_usdt`: USDT 余额（浮点数，6 位小数）
- `balance_raw`: 原始余额（最小单位）
- `summary`: 人类可读的摘要

**示例:**
```
查询 TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf 的 USDT 余额
→ 返回: "地址 TXYZ... 当前 USDT 余额为 1,234.567890 USDT。"
```

---

### 2. `get_balance`
查询指定地址的 TRX 原生代币余额。

**参数:**
- `address` (必填): TRON 地址

**返回:**
- `address`: 查询地址
- `balance_trx`: TRX 余额
- `balance_sun`: SUN 单位余额（1 TRX = 1,000,000 SUN）
- `summary`: 人类可读的摘要

---

### 3. `get_gas_parameters`
获取当前网络的 Gas/能量价格参数。

**参数:** 无

**返回:**
- `gas_price_sun`: Gas 价格（SUN）
- `gas_price_trx`: Gas 价格（TRX）
- `summary`: 人类可读的摘要

**使用场景:**
- 在构建交易前评估手续费
- 监控网络拥堵状况

---

### 4. `get_transaction_status`
查询交易的确认状态。

**参数:**
- `txid` (必填): 交易哈希，64 位十六进制字符串（可带 `0x` 前缀）

**返回:**
- `status`: "成功" 或 "失败" 或 "pending"
- `confirmed`: 布尔值
- `block_number`: 所在区块高度（成功/失败时）
- `confirmations`: 确认次数（如服务端提供）
- `summary`: 人类可读的摘要

**示例:**
```
查询交易 abc123...def 的状态
→ 返回: "交易 abc123... 状态：成功，所在区块 12,345,678，已确认 20 次。"
```

---

### 5. `get_network_status`
获取 TRON 网络当前状态。

**参数:** 无

**返回:**
- `latest_block`: 最新区块高度
- `chain`: 链名称 (TRON Nile Testnet)
- `summary`: 人类可读的摘要

---

### 6. `build_tx`
构建未签名的转账交易。

**参数:**
- `from` (必填): 发送方地址
- `to` (必填): 接收方地址
- `amount` (必填): 转账金额（正数）
- `token` (可选): 代币类型，`USDT` 或 `TRX`，默认 `USDT`

**返回:**
- `unsigned_tx`: 未签名交易结构，包含：
  - `txID`: 交易 ID
  - `raw_data`: 交易原始数据
- `summary`: 人类可读的摘要

**重要提示:**
- 此工具仅构建交易，**不执行签名和广播**
- 用户需要使用私钥在本地签名后广播
- 交易有效期为 1 分钟

**示例:**
```
从 Txxxx 向 Tyyyy 转账 100 USDT
→ 返回: "已生成从 Txxxx... 到 Tyyyy... 转账 100 USDT 的未签名交易。"
```

---

## 工作流程指南

### 查询余额

```
用户: "查一下这个地址有多少 USDT: TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf"

步骤:
1. 调用 get_usdt_balance(address="TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf")
2. 返回余额信息给用户
```

### 检查交易状态

```
用户: "我的转账到账了吗？交易哈希是 abc123..."

步骤:
1. 调用 get_transaction_status(txid="abc123...")
2. 如果状态是 pending，建议用户稍后再查
3. 如果状态是成功/失败，告知用户结果
```

### 构建转账交易

```
用户: "帮我生成一个转账交易，从我的地址转 50 USDT 到 Tyyyy"

步骤:
1. 先调用 get_usdt_balance 检查发送方余额是否足够
2. 调用 get_gas_parameters 获取当前 Gas 价格
3. 调用 build_tx(from="Txxxx", to="Tyyyy", amount=50, token="USDT")
4. 返回未签名交易，提醒用户需要签名后广播
```

---

## 错误处理

### 常见错误

| 错误类型 | 描述 | 处理建议 |
|---------|------|---------|
| `invalid_address` | 地址格式无效 | 请用户检查地址格式，应以 T 开头且 34 字符 |
| `invalid_txid` | 交易哈希格式无效 | 交易哈希应为 64 位十六进制字符 |
| `missing_param` | 缺少必填参数 | 提示用户提供所需参数 |
| `rpc_error` | 网络请求失败 | 建议用户稍后重试 |
| `timeout` | 请求超时 | 网络可能拥堵，建议稍后重试 |
| `invalid_amount` | 金额不合法 | 金额必须为正数 |
| `build_error` | 构建交易失败 | 检查参数或稍后重试 |
| `unknown_action` | 未知动作 | 使用 skills 或核对 action 名称 |

### 错误响应格式

所有错误响应包含：
- `error`: 错误类型代码
- `summary`: 人类可读的错误描述

---

## 安全注意事项

1. **不处理私钥**: 此技能不接触用户私钥，仅构建未签名交易
2. **地址验证**: 所有地址在使用前都会进行格式验证
3. **金额验证**: 转账金额必须为正数
4. **只读优先**: 查询操作不会修改链上状态

---

## 技术细节

- **USDT 合约**: `TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf` (Nile 测试网 TRC20, 6 位小数)
- **精度**: USDT 和 TRX 均使用 6 位小数
- **API**: 通过 TRONSCAN REST API 与 TRON Nile 测试网通信
- **接口来源**: account, transaction-info, chain/parameters, block
