# API 文档

## POST /api/recognize

上传图片并返回识别到的物品名称与参考回收价。

### 请求

- Content-Type: multipart/form-data
- 字段：
  - file: 图片文件

示例：

```bash
curl -X POST "http://localhost:8000/api/recognize" \
  -H "Origin: http://localhost:5173" \
  -F "file=@./sample.jpg"
```

### 成功响应

- HTTP 200

```json
{
  "item": "纸箱",
  "price": 1.2,
  "currency": "CNY"
}
```

### 失败响应（统一格式）

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "文件为空",
    "details": {}
  }
}
```

### 错误码与状态码

- INVALID_REQUEST (400)：参数不合法、文件为空、文件过大等
- UNSUPPORTED_FILE (415)：上传非图片类型文件
- UNAUTHORIZED (401)：未登录/登录失效
- FORBIDDEN (403)：无权限
- NOT_FOUND (404)：资源不存在
- CONFLICT (409)：资源冲突（例如商品已售出、用户名已存在）
- AI_PROVIDER_ERROR (502)：第三方识别服务调用失败/鉴权失败
- INTERNAL_ERROR (500)：未预期错误

## 认证

### POST /api/auth/register

```json
{ "username": "user1", "password": "secret1", "display_name": "昵称(可选)" }
```

成功：

```json
{ "access_token": "...", "token_type": "bearer" }
```

### POST /api/auth/login

```json
{ "username": "user1", "password": "secret1" }
```

成功：

```json
{ "access_token": "...", "token_type": "bearer" }
```

### Authorization Header

需要登录的接口使用：

```text
Authorization: Bearer <access_token>
```

## 用户

### GET /api/me

返回当前用户信息。

### PATCH /api/me

```json
{ "display_name": "新的昵称" }
```

## 商品

### GET /api/listings

- Query: `include_sold=false|true`（默认 false）

### GET /api/listings/{id}

返回商品详情（用于商品详情页）。

### POST /api/listings

上传图片并自动识别物品名称，使用价格库返回默认价格；可传 `price` 覆盖默认值。

- Content-Type: multipart/form-data
- 字段：
  - file: 图片文件
  - description: 文本（可选）
  - price: 数字（可选，空值等价于不传）

### POST /api/listings/{id}/purchase

购买指定商品（演示用：创建订单并将商品标记为已售）。

## 历史

### GET /api/history

返回：

- recognitions：识别记录
- purchases：购买记录
- sales：卖出记录
- my_listings：我的上架
