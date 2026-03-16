# AI-recycle

Recycle-AI 演示项目：上传旧物图片进行识别估价，并支持注册/登录、识别历史、旧物上架、浏览与购买（本地 SQLite 持久化）。

## 技术栈

- 前端：Vue 3 + Vite + Pinia + Vue Router
- 后端：FastAPI
- 数据：SQLite（默认 `shared/app.db`）+ 本地价格库 `shared/pricing.json`

## 一键启动（Windows）

双击运行：

- `scripts/start-dev.bat`

或 PowerShell 执行：

```powershell
.\scripts\start-dev.ps1
```

会分别打开前端/后端两个终端窗口，并自动打开：

- http://localhost:5173/

如果双击后窗口一闪而过，推荐用终端执行以便看到报错：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-dev.ps1
```

## 手动启动（开发）

### 1）启动后端

```powershell
cd backend
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

后端地址：

- http://127.0.0.1:8000

### 2）启动前端

另开一个终端：

```powershell
cd frontend
npm install
npm run dev
```

前端地址：

- http://localhost:5173

## 页面入口与登录规则

- 登录：`/login`
- 注册：`/register`

说明：除 `/login` 和 `/register` 外，其余页面需要先登录（未登录会自动跳转登录页）。

- 识别：首页 `/`
- 商城：`/market`（详情：`/market/:id`）
- 上架：`/sell`
- 记录：`/history`
- 我：`/me`

## 演示账号

- 用户名：`demo3`
- 密码：`demo123`

也可以在页面中自行注册新账号。

## 数据存储位置（本地）

- SQLite 数据库文件：`shared/app.db`（可通过环境变量 `DB_PATH` 修改）
- 上传图片保存目录：`shared/uploads/`（可通过环境变量 `UPLOAD_DIR` 修改）

## 识别模式（Mock vs 百度）

默认是 mock 识别（演示用，不是真实看图），能保证同一张图片结果稳定、不同图片结果通常不同。

若要使用百度通用图像识别，在项目根目录创建 `.env`：

```ini
AI_MOCK=false
AI_PROVIDER=baidu
BAIDU_API_KEY=your_api_key
BAIDU_SECRET_KEY=your_secret_key
```

更多部署与环境变量说明见：

- [deploy.md](file:///c:/Users/xhm/Documents/trae_projects/AI-recycle/docs/deploy.md)

## API 文档

- [api.md](file:///c:/Users/xhm/Documents/trae_projects/AI-recycle/docs/api.md)

## 测试

后端：

```powershell
python -m pip install -r backend/requirements.txt
python -m pytest -q backend/tests --cov=backend/app --cov-report=term
```

前端：

```powershell
cd frontend
npm ci
npm test
```
