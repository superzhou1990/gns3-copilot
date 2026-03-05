# 技术文档

本部分包含 GNS3 Copilot 的技术规范和实现细节。

## 可用文档

### GNS3 绘图 SVG 格式
- [GNS3 Drawing SVG Format Guide (English)](gns3-drawing-svg-format-guide.md) - SVG 绘图格式规范
- [GNS3 绘图 SVG 格式指南 (中文)](gns3-drawing-svg-format-guide_zh.md) - SVG 绘图格式规范

## 技术概览

### GNS3 绘图格式

GNS3 使用 SVG（可缩放矢量图形）来渲染网络拓扑图。理解 SVG 格式对于以下工作至关重要：

- **自动拓扑生成**：以编程方式创建网络拓扑的可视化表示
- **绘图区域管理**：创建可视化区域以组织拓扑组件（例如 OSPF 区域圆圈）
- **拓扑可视化**：在 GNS3 Web UI 中渲染网络图

### SVG 绘图组件

GNS3 绘图支持以下 SVG 元素：

| 元素 | 用途 |
|---------|-------|
| `<rect>` | 矩形区域和区域划分 |
| `<circle>` | 圆形区域（例如 OSPF 区域） |
| `<line>` | 连接线和注释 |
| `<path>` | 复杂形状和路由 |
| `<text>` | 标签和注释 |

### GNS3 绘图 API

GNS3 提供用于管理绘图的 REST API 端点：

- **创建绘图**: `POST /v2/projects/{project_id}/drawings`
- **更新绘图**: `PUT /v2/projects/{project_id}/drawings/{drawing_id}`
- **删除绘图**: `DELETE /v2/projects/{project_id}/drawings/{drawing_id}`
- **获取绘图**: `GET /v2/projects/{project_id}/drawings`

### 示例：创建圆形绘图

```json
{
  "type": "ellipse",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 200,
  "rotation": 0,
  "svg": "<svg width='200' height='200'><ellipse cx='100' cy='100' rx='100' ry='100' style='fill:none;stroke:#ff0000;stroke-width:2'/></svg>"
}
```

## 相关资源

- [GNS3 API 文档](https://api.gns3.net/)
- [SVG 规范](https://www.w3.org/TR/SVG/)
- [项目文档](https://yueguobin.github.io/gns3-copilot/)
