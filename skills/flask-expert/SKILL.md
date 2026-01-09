---
name: flask-expert
description: "Flask 框架专家。当用户需要：(1) 构建 Flask API (2) 配置蓝图和路由 (3) 处理请求和响应 (4) 集成数据库 ORM (5) 部署 Flask 应用时触发。确保 API 设计符合 RESTful 规范。"
---

# Flask Expert

> **核心理念**：简洁 > 灵活 > 性能

## 触发条件

当用户说以下任何一句时激活：
- "Flask 应用"
- "API 路由"
- "蓝图"
- "后端开发"（且项目使用 Flask）

## 项目结构

```
backend/
├── app/
│   ├── __init__.py          # 应用工厂
│   ├── config.py             # 配置类
│   ├── models/               # 数据模型
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routes/               # 路由蓝图
│   │   ├── __init__.py
│   │   ├── api.py
│   │   └── auth.py
│   ├── services/             # 业务逻辑
│   │   └── user_service.py
│   └── utils/                # 工具函数
├── tests/
├── requirements.txt
└── run.py
```

## 应用工厂模式

```python
# app/__init__.py
from flask import Flask
from flask_cors import CORS

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 扩展初始化
    CORS(app)
    
    # 注册蓝图
    from .routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
```

## 蓝图模式

```python
# app/routes/api.py
from flask import Blueprint, jsonify, request

api_bp = Blueprint('api', __name__)

@api_bp.route('/items', methods=['GET'])
def get_items():
    """获取所有项目"""
    return jsonify({'items': [], 'total': 0})

@api_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """获取单个项目"""
    return jsonify({'id': item_id, 'name': 'Example'})

@api_bp.route('/items', methods=['POST'])
def create_item():
    """创建项目"""
    data = request.get_json()
    # 验证 & 创建逻辑
    return jsonify({'id': 1, **data}), 201
```

## 错误处理

```python
# app/utils/errors.py
from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad Request', 'message': str(error)}), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not Found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal Server Error'}), 500
```

## 请求验证

```python
from functools import wraps
from flask import request, jsonify

def validate_json(*required_fields):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            if not data:
                return jsonify({'error': 'JSON body required'}), 400
            missing = [f for f in required_fields if f not in data]
            if missing:
                return jsonify({'error': f'Missing fields: {missing}'}), 400
            return f(*args, **kwargs)
        return wrapper
    return decorator

# 使用
@api_bp.route('/items', methods=['POST'])
@validate_json('name', 'description')
def create_item():
    data = request.get_json()
    # ...
```

## 数据库集成 (SQLAlchemy)

```python
# app/models/user.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }
```

## 部署配置 (Gunicorn)

```bash
# 生产环境启动
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app('production')"

# 配合 gevent
gunicorn -w 4 -k gevent -b 0.0.0.0:8000 "app:create_app('production')"
```

## 常见陷阱

| ❌ 避免 | ✅ 正确做法 |
|:---|:---|
| 在路由中写业务逻辑 | 抽取到 services 层 |
| 硬编码配置 | 使用环境变量 + config 类 |
| 不处理异常 | 使用 errorhandler 统一处理 |
| 返回字典直接用 json.dumps | 使用 jsonify() |
| 忽略 CORS | 使用 flask-cors |

---

## 进化日志

| 日期 | 更新内容 | 来源 |
|:---|:---|:---|
| 2025-12-27 | 初始版本 | ContentRSS 项目需求 |
