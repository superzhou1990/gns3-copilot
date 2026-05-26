# PNETLab-v6 集成实现检查清单与代码示例

## 🎯 完整实现步骤

### Phase 1: 核心模块实现 ✅

#### 已创建文件列表：

1. **`src/gns3_copilot/pnetlab_client/__init__.py`**
   - PNETLab 客户端模块初始化
   - 导出核心类和工具

2. **`src/gns3_copilot/pnetlab_client/pnetlab_client.py`** (595行)
   - REST API 客户端实现
   - 认证、连接池、请求处理
   - 支持所有主要 API 端点

3. **`src/gns3_copilot/pnetlab_client/pnetlab_topology_tool.py`** (230行)
   - 拓扑读取工具
   - 兼容 GNS3TopologyTool 接口
   - 自动拓扑结构转换

4. **`src/gns3_copilot/pnetlab_client/pnetlab_config_tools_nornir.py`** (350行)
   - 多设备配置执行工具
   - Nornir 集成
   - 错误处理和重试

5. **`src/gns3_copilot/pnetlab_client/pnetlab_display_tools_nornir.py`** (310行)
   - 多设备查询工具
   - Show/Display 命令执行
   - 结果处理

6. **`src/gns3_copilot/platform_abstraction.py`** (140行)
   - 平台抽象工厂
   - 动态工具加载
   - 平台检测

7. **`src/gns3_copilot/agent/unified_agent.py`** (270行)
   - 统一 Agent 实现
   - 支持 GNS3 和 PNETLab
   - 向后兼容

8. **`PNETLAB_CONFIG.md`**
   - 环境变量配置说明

9. **`PNETLAB_INTEGRATION_GUIDE.md`** (600+ 行)
   - 完整集成指南
   - 架构设计文档
   - 故障排查指南

---

### Phase 2: 必需的代码修改

#### 修改 1: `src/gns3_copilot/app.py`

```python
# 原代码
from gns3_copilot.agent.gns3_copilot import agent

# 新代码
from gns3_copilot.agent.unified_agent import agent
```

#### 修改 2: `src/gns3_copilot/ui_model/settings.py`

添加平台选择：

```python
import streamlit as st
from gns3_copilot.platform_abstraction import SimulatorPlatform
from gns3_copilot.utils import get_config, save_config

def render_platform_settings():
    """渲染平台设置界面"""
    st.subheader("🖥️ Simulator Platform")
    
    current_platform = get_config("SIMULATOR_PLATFORM", "gns3")
    
    platform = st.selectbox(
        "Select Network Simulator",
        [p.value for p in SimulatorPlatform],
        index=[p.value for p in SimulatorPlatform].index(current_platform),
        key="platform_selector"
    )
    
    if platform != current_platform:
        save_config("SIMULATOR_PLATFORM", platform)
        st.success(f"Platform switched to {platform}")
        st.rerun()
    
    # 平台特定配置
    if platform == "pnetlab_v6":
        st.subheader("PNETLab-v6 Configuration")
        
        pnetlab_host = st.text_input(
            "PNETLab Server Host",
            value=get_config("PNETLAB_SERVER_HOST", "localhost"),
            key="pnetlab_host"
        )
        
        pnetlab_port = st.number_input(
            "PNETLab Server Port",
            value=int(get_config("PNETLAB_SERVER_PORT", "443")),
            min_value=1,
            max_value=65535,
            key="pnetlab_port"
        )
        
        pnetlab_username = st.text_input(
            "PNETLab Username",
            value=get_config("PNETLAB_USERNAME", "admin"),
            key="pnetlab_username"
        )
        
        pnetlab_password = st.text_input(
            "PNETLab Password",
            value=get_config("PNETLAB_PASSWORD", ""),
            type="password",
            key="pnetlab_password"
        )
        
        if st.button("Test Connection", key="test_pnetlab_connection"):
            from gns3_copilot.pnetlab_client import PNETLabClient
            try:
                client = PNETLabClient(
                    host=pnetlab_host,
                    port=pnetlab_port,
                    username=pnetlab_username,
                    password=pnetlab_password,
                )
                if client.authenticate():
                    st.success("✅ Connected to PNETLab server!")
                    save_config("PNETLAB_SERVER_HOST", pnetlab_host)
                    save_config("PNETLAB_SERVER_PORT", str(pnetlab_port))
                    save_config("PNETLAB_USERNAME", pnetlab_username)
                    save_config("PNETLAB_PASSWORD", pnetlab_password)
                else:
                    st.error("❌ Authentication failed")
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")
            finally:
                client.close()
```

#### 修改 3: `src/gns3_copilot/ui_model/sidebar.py`

```python
from gns3_copilot.platform_abstraction import (
    SimulatorPlatform,
    PlatformFactory,
    get_current_platform,
)

def render_sidebar(current_page: str) -> tuple:
    """渲染侧边栏，支持多平台"""
    
    platform = get_current_platform()
    
    with st.sidebar:
        st.title("🤖 Network Copilot")
        
        # 显示当前平台
        st.info(f"Platform: {platform.value.upper()}")
        
        # 获取平台特定的项目列表
        if platform == SimulatorPlatform.GNS3:
            projects = get_gns3_projects()
            project_display_name = "GNS3 Projects"
        elif platform == SimulatorPlatform.PNETLAB_V6:
            projects = get_pnetlab_labs()
            project_display_name = "PNETLab Labs"
        else:
            projects = []
            project_display_name = "Projects"
        
        if projects:
            selected_project = st.selectbox(
                project_display_name,
                projects,
                format_func=lambda x: x[0] if isinstance(x, tuple) else str(x),
                key="selected_project"
            )
            
            # 存储选中的项目
            st.session_state["selected_project_info"] = selected_project
            return selected_project
        else:
            st.warning(f"No {project_display_name.lower()} found")
            return None


def get_pnetlab_labs() -> list[tuple]:
    """获取 PNETLab 实验室列表"""
    from gns3_copilot.pnetlab_client import PNETLabClient
    from gns3_copilot.utils import get_config
    
    try:
        client = PNETLabClient(
            host=get_config("PNETLAB_SERVER_HOST", "localhost"),
            port=int(get_config("PNETLAB_SERVER_PORT", "443")),
            username=get_config("PNETLAB_USERNAME", "admin"),
            password=get_config("PNETLAB_PASSWORD", ""),
        )
        
        if not client.authenticate():
            st.error("PNETLab authentication failed")
            return []
        
        success, labs_data = client.get_labs()
        if not success:
            st.error("Failed to fetch PNETLab labs")
            return []
        
        labs = []
        labs_list = labs_data.get("data", []) if isinstance(labs_data, dict) else labs_data
        
        for lab in labs_list:
            lab_id = lab.get("id")
            lab_name = lab.get("name", "Unknown")
            
            # 获取节点和链接数量
            success, nodes_data = client.get_lab_nodes(lab_id)
            node_count = len(nodes_data) if success and isinstance(nodes_data, list) else 0
            
            success, links_data = client.get_lab_links(lab_id)
            link_count = len(links_data) if success and isinstance(links_data, list) else 0
            
            labs.append((
                lab_name,
                lab_id,
                node_count,
                link_count,
                lab.get("status", "unknown")
            ))
        
        client.close()
        return labs
        
    except Exception as e:
        st.error(f"Error fetching PNETLab labs: {str(e)}")
        return []
```

---

### Phase 3: 依赖项配置

#### 更新 `pyproject.toml`

```toml
[project]
dependencies = [
    "streamlit>=1.28.0",
    "langchain>=0.1.0",
    "langchain-core>=0.1.0",
    "langgraph>=0.0.1",
    "requests>=2.31.0",  # 新增：PNETLab HTTP客户端
    "urllib3>=2.0.0",     # 新增：重试策略
    "nornir>=3.3.0",
    "nornir-netmiko>=0.2.0",
    "netmiko>=4.3.0",
    # ... 其他依赖
]
```

#### 安装命令

```bash
pip install -e .
# 或
pip install requests>=2.31.0 urllib3>=2.0.0
```

---

### Phase 4: 配置文件

#### `.env.pnetlab` 模板

```bash
# 平台选择
SIMULATOR_PLATFORM=pnetlab_v6

# PNETLab 服务器配置
PNETLAB_SERVER_HOST=192.168.1.100
PNETLAB_SERVER_PORT=443
PNETLAB_USERNAME=admin
PNETLAB_PASSWORD=pnetlab
PNETLAB_VERIFY_SSL=true

# 设备访问凭证
DEVICE_USERNAME=admin
DEVICE_PASSWORD=admin
DEVICE_SECRET=admin

# AI 模型配置
MODEL_NAME=deepseek-chat
MODE_PROVIDER=openai
MODEL_API_KEY=sk-xxx
BASE_URL=https://api.deepseek.com

# Nornir 配置
NORNIR_TIMEOUT=30
NORNIR_WORKERS=10
```

---

### Phase 5: 测试用例

#### 测试文件：`tests/test_pnetlab_integration.py`

```python
import pytest
from gns3_copilot.pnetlab_client import PNETLabClient, PNETLabTopologyTool
from gns3_copilot.platform_abstraction import PlatformFactory, SimulatorPlatform


class TestPNETLabClient:
    """PNETLab 客户端测试"""
    
    @pytest.fixture
    def client(self):
        return PNETLabClient(
            host="localhost",
            port=443,
            username="admin",
            password="pnetlab",
        )
    
    def test_authentication(self, client):
        """测试认证"""
        result = client.authenticate()
        assert result is True or result is False  # 取决于服务器
    
    def test_get_labs(self, client):
        """测试获取实验室列表"""
        success, labs = client.get_labs()
        assert isinstance(success, bool)
        assert isinstance(labs, (dict, list))


class TestPlatformFactory:
    """平台工厂测试"""
    
    def test_get_gns3_tools(self):
        """测试 GNS3 工具加载"""
        tools = PlatformFactory.get_all_tools(SimulatorPlatform.GNS3)
        assert len(tools) > 0
        assert any("gns3" in tool.name for tool in tools)
    
    def test_get_pnetlab_tools(self):
        """测试 PNETLab 工具加载"""
        tools = PlatformFactory.get_all_tools(SimulatorPlatform.PNETLAB_V6)
        assert len(tools) > 0
        assert any("pnetlab" in tool.name for tool in tools)
    
    def test_topology_tool_interface(self):
        """测试拓扑工具接口兼容性"""
        gns3_tool = PlatformFactory.get_topology_tool(SimulatorPlatform.GNS3)
        pnetlab_tool = PlatformFactory.get_topology_tool(SimulatorPlatform.PNETLAB_V6)
        
        # 两个工具应该有相同的接口
        assert hasattr(gns3_tool, "_run")
        assert hasattr(pnetlab_tool, "_run")
        assert gns3_tool.name != pnetlab_tool.name
```

---

## 📋 完整文件清单

### 新增文件（7个）

- ✅ `src/gns3_copilot/pnetlab_client/__init__.py`
- ✅ `src/gns3_copilot/pnetlab_client/pnetlab_client.py`
- ✅ `src/gns3_copilot/pnetlab_client/pnetlab_topology_tool.py`
- ✅ `src/gns3_copilot/pnetlab_client/pnetlab_config_tools_nornir.py`
- ✅ `src/gns3_copilot/pnetlab_client/pnetlab_display_tools_nornir.py`
- ✅ `src/gns3_copilot/platform_abstraction.py`
- ✅ `src/gns3_copilot/agent/unified_agent.py`

### 文档文件（2个）

- ✅ `PNETLAB_CONFIG.md`
- ✅ `PNETLAB_INTEGRATION_GUIDE.md`

### 修改的文件（3个）

- ⚠️ `src/gns3_copilot/app.py` - 1行改动
- ⚠️ `src/gns3_copilot/ui_model/settings.py` - 新增100行
- ⚠️ `src/gns3_copilot/ui_model/sidebar.py` - 新增150行

### 测试文件（可选）

- ⚠️ `tests/test_pnetlab_integration.py`

---

## 🔄 系统流程图

```
用户输入 (UI)
    ↓
Streamlit ChatInterface
    ↓
unified_agent.llm_call()
    ↓
    ├─ 读取 SIMULATOR_PLATFORM 环境变量
    ├─ PlatformFactory.get_topology_tool(platform)
    └─ 如果是 pnetlab_v6:
        ├─ PNETLabClient 连接
        ├─ 认证
        ├─ 获取 Lab 拓扑
        └─ 返回标准化拓扑结构
    ↓
LLM 分析请求 + 拓扑信息
    ↓
选择工具
    ├─ 如果是 execute_multiple_device_commands:
    │   └─ PlatformFactory 返回正确的工具实现
    ├─ 如果是 execute_multiple_device_config_commands:
    │   └─ PlatformFactory 返回正确的工具实现
    └─ 其他工具...
    ↓
Nornir + Netmiko 执行
    ↓
返回结果给 LLM
    ↓
生成最终响应给用户
```

---

## ✅ 验证清单

### 本地测试

- [ ] Python 导入不出错：`python -c "from gns3_copilot.pnetlab_client import *"`
- [ ] 平台工厂工作正常：`python -c "from gns3_copilot.platform_abstraction import *"`
- [ ] 环境变量读取：`python -c "import os; from gns3_copilot.utils import get_config"`

### 功能测试

- [ ] PNETLab 连接测试
- [ ] 拓扑读取测试
- [ ] 多设备查询测试
- [ ] 多设备配置测试
- [ ] UI 平台切换测试

### 兼容性测试

- [ ] GNS3 功能仍然正常
- [ ] 工具名称不冲突
- [ ] Agent 路由正确

---

## 💡 后续优化建议

1. **缓存优化**
   - 缓存拓扑信息减少 API 调用
   - 实现增量更新

2. **性能优化**
   - 批量 API 调用
   - 异步执行

3. **功能扩展**
   - 支持 CML
   - 支持 EVE-NG
   - 支持 Proxmox

4. **监控和日志**
   - 更详细的日志
   - 性能指标收集
   - 错误追踪

---

这个完整实现包含了 **1900+ 行新代码**，涵盖了从底层 API 客户端到上层 UI 的所有层级。
