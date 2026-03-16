# 部署与运行

## 环境准备

- Python 3.9+
- Node 18+（前端构建与运行）
- 建议使用 Linux/macOS 或 Windows 的 Git Bash/WSL 执行 `.sh` 脚本

## 配置（AI 识别）

后端支持两种模式：

- Mock（默认）：无需密钥，离线可用
- 百度通用图像识别：需要配置 `BAIDU_API_KEY` 与 `BAIDU_SECRET_KEY`

在项目根目录创建 `.env`（或导出环境变量）：

```ini
AI_MOCK=false
AI_PROVIDER=baidu
BAIDU_API_KEY=your_api_key
BAIDU_SECRET_KEY=your_secret_key
```

可选项：

```ini
BAIDU_ENDPOINT=https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general
BAIDU_OAUTH_ENDPOINT=https://aip.baidubce.com/oauth/2.0/token
AI_TIMEOUT_SECONDS=15
MAX_UPLOAD_BYTES=8388608
CORS_ALLOW_ORIGINS=http://localhost:5173
PRICING_PATH=./shared/pricing.json
DB_PATH=./shared/app.db
UPLOAD_DIR=./shared/uploads
JWT_SECRET=dev-secret-change-me
JWT_EXPIRE_MINUTES=10080
```

## 端口说明

- 前端 dev server：5173
- 后端 API：8000
- CORS 默认仅允许：`http://localhost:5173`

## 本地开发（双进程）

```bash
./setup.sh
./scripts/start-dev.sh
```

或分别启动：

```bash
cd backend
uvicorn main:app --reload --port 8000
```

```bash
cd frontend
npm run dev
```

## 生产启动（pm2 + gunicorn）

```bash
./setup.sh
./scripts/start-prod.sh
```

日志默认写入：

- `logs/backend-access.log`
- `logs/backend-error.log`

## 常见故障排查

- 前端请求被 CORS 拦截：确认前端来源是 `http://localhost:5173`，或在 `.env` 设置 `CORS_ALLOW_ORIGINS`
- 百度鉴权失败：检查 `BAIDU_API_KEY/BAIDU_SECRET_KEY` 是否正确，以及账号权限是否开通通用物体识别
- 上传失败/文件过大：调整 `MAX_UPLOAD_BYTES` 或压缩图片
- 登录/注册后数据存哪：默认 SQLite 文件在 `shared/app.db`（可用 `DB_PATH` 修改）
