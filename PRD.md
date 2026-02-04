# PRD：TRON MCP Server（更新版）

## 1. 项目背景
构建面向 AI Agent 的 TRON 区块链 MCP 服务器，将 TRONSCAN REST API 封装为 MCP 工具。系统需提供结构化输出与中文摘要，便于 AI 直接面向用户交互。

## 2. 目标
- 通过 MCP 工具提供 TRON 余额、网络状态、交易状态、Gas 参数、未签名交易构建能力。
- 输出结构化字段与可读摘要。
- 支持环境变量配置与鉴权（TRONSCAN API Key）。

## 3. 功能范围（当前版本）
### 3.1 必须支持
- `tron_get_usdt_balance(address)`：USDT 余额查询
- `tron_get_balance(address)`：TRX 余额查询
- `tron_get_gas_parameters()`：Gas/能量价格参数
- `tron_get_transaction_status(txid)`：交易状态查询（含 pending）
- `tron_get_network_status()`：最新区块高度
- `tron_build_tx(from_address, to_address, amount, token=USDT|TRX)`：构建未签名交易

### 3.2 兼容入口
- `call(action, params)`：单入口路由，支持 `skills` 返回技能清单

## 4. 数据与输出规范
- 余额单位：
  - TRX/SUN 转换（1 TRX = 1,000,000 SUN）
  - USDT 使用 6 位小数
- 交易状态输出：`status`（成功/失败/pending）、`success`、`block_number`、`confirmations`
- 统一错误格式：`error` + `summary`

## 5. 地址与参数校验
- 地址支持 Base58（T 开头 34 位）或 Hex（0x41 开头 44 位）
- txid 支持 64 位 hex（可带 0x 前缀）
- 金额必须为正数

## 6. 技术实现要求
- 访问 TRONSCAN REST API（account、transaction-info、chain/parameters、block）
- 支持超时与异常处理
- 结构化输出与摘要由 formatter 层统一生成

## 7. 非功能需求
- 可维护性：模块化结构（client / validators / formatters / router / server）
- 稳定性：异常可读、超时可控
- 可扩展性：易于新增链上查询工具

## 8. 验收标准
- 所有核心工具可被 MCP 正常调用
- 返回结果包含结构化字段与中文摘要
- 错误场景有明确可读提示
