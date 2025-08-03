# A2A Server Communication Demo

这是一个演示两个A2A（Agent-to-Agent）服务器之间通信的项目。项目包含两个服务器：
- **Server 1 (Passive)**: 被动服务器，只响应来自Server 2的请求
- **Server 2 (Active)**: 主动服务器，向Server 1发送消息并等待响应

## 项目结构

```
pydantic_ai_a2a_demo/
├── server1.py          # 被动A2A服务器 (端口8000)
├── server2.py          # 主动A2A服务器 (端口8001)
├── requirements.txt    # Python依赖
├── .env               # 环境变量配置
└── README.md          # 项目说明
```

## 技术栈

- **Pydantic AI**: 用于创建AI代理
- **FastA2A**: 将Pydantic AI代理暴露为A2A服务器
- **Uvicorn**: ASGI服务器
- **Httpx**: 异步HTTP客户端
- **Python-dotenv**: 环境变量管理

## 安装和设置

### 1. 克隆项目
```bash
git clone <repository-url>
cd pydantic_ai_a2a_demo
```

### 2. 创建虚拟环境
```bash
conda create -n py313 python=3.13
conda activate py313
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置环境变量
创建 `.env` 文件并添加你的OpenAI API密钥：
```
OPENAI_API_KEY=your_openai_api_key_here
```

## 使用方法

### 方法1: 分别启动两个服务器

#### 启动被动服务器 (Server 1)
```bash
python server1.py
```
Server 1 将在 http://localhost:8000 启动，并等待来自Server 2的消息。

#### 启动主动服务器 (Server 2)
```bash
python server2.py
```
Server 2 将在 http://localhost:8001 启动，并自动向Server 1发送消息。

### 方法2: 使用演示脚本

创建一个简单的演示脚本：

```python
# demo.py
import asyncio
import subprocess
import sys

async def run_demo():
    print("=== A2A Server Communication Demo ===")
    
    # 启动Server 1
    server1 = subprocess.Popen([sys.executable, "server1.py"])
    await asyncio.sleep(3)
    
    # 启动Server 2
    server2 = subprocess.Popen([sys.executable, "server2.py"])
    
    # 等待完成
    server1.wait()
    server2.wait()

if __name__ == "__main__":
    asyncio.run(run_demo())
```

然后运行：
```bash
python demo.py
```

## 通信流程

1. **Server 1 启动**: 在端口8000启动，等待消息
2. **Server 2 启动**: 在端口8001启动，等待5秒让Server 1准备就绪
3. **第一轮通信**: Server 2 向 Server 1 询问关于人工智能的问题
4. **第二轮通信**: Server 2 向 Server 1 询问关于深度学习和神经网络的问题
5. **第三轮通信**: Server 2 向 Server 1 询问关于监督学习和无监督学习的区别
6. **完成**: 两个服务器完成通信并自动关闭

## 服务器配置

### Server 1 (Passive)
- **端口**: 8000
- **角色**: 被动响应
- **功能**: 回答来自Server 2的问题
- **指令**: 作为Server 1，与Server 2友好交流

### Server 2 (Active)
- **端口**: 8001
- **角色**: 主动发起
- **功能**: 向Server 1发送问题并等待响应
- **指令**: 作为Server 2，与Server 1友好交流

## API端点

两个服务器都使用标准的A2A协议：

- **POST /** - 发送JSON-RPC消息
- **GET /.well-known/agent.json** - 获取代理信息
- **POST /** - 查询任务状态 (使用 `tasks/get` 方法)

## 消息格式

使用JSON-RPC 2.0格式：

```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [{"kind": "text", "text": "Hello!"}],
      "kind": "message",
      "messageId": "unique-id"
    }
  },
  "id": "unique-id"
}
```

## 故障排除

### 常见问题

1. **连接错误**: 确保两个服务器都在运行
2. **API密钥错误**: 检查 `.env` 文件中的 `OPENAI_API_KEY`
3. **端口冲突**: 确保端口8000和8001没有被其他程序占用

### 调试

- 检查服务器日志输出
- 使用 `curl` 测试API端点
- 确保网络连接正常

## 扩展

你可以通过以下方式扩展这个项目：

1. **添加更多服务器**: 创建更多A2A服务器进行多对多通信
2. **自定义工具**: 为代理添加特定的工具和功能
3. **持久化存储**: 添加数据库来存储对话历史
4. **负载均衡**: 使用多个服务器实例处理高负载
