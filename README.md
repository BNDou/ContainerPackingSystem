<!--
 * @FilePath     : /ContainerPackingSystem/README.md
 * @Description  :  装箱记录管理系统
 * @Author       : BNDou
 * @Date         : 2024-12-14 01:27:05
 * @LastEditTime : 2025-01-03 22:40:00
-->
# 装箱记录管理系统

一个基于 Flask 的装箱记录管理系统，用于记录、删除和查询装箱信息。

## 功能特点

- 查询月度装箱记录
  - 按月份查询装箱记录
  - 显示每条记录的箱数统计
  - 显示月度总箱数和记录数
  - 日期显示采用中文格式
- 添加新的装箱记录
  - 支持日期选择
  - 支持箱号区间输入
  - 自动生成唯一记录ID
  - 自动记录创建时间
- 删除装箱记录
  - 支持删除指定记录ID的装箱记录
- 现代化UI界面
  - 优雅的渐变色主题
  - 响应式卡片设计
  - 平滑的动画效果
  - 美化的确认弹窗
  - 统一的设计语言

## 技术框架

- 后端框架：Flask 3.x
- 数据存储：SQLite（通过SQLAlchemy ORM）
- 前端框架：
  - Bootstrap 5（布局和基础组件）
  - SweetAlert2（美化的弹窗）
  - Font Awesome 6（图标库）
- 数据处理：Pandas
- 日期处理：Python-dateutil

## 界面特性

- 配色方案：
  - 主色调：现代感绿色和蓝色渐变
  - 强调色：优雅的深色调
  - 统一的阴影效果
- 交互设计：
  - 卡片悬浮效果
  - 按钮点击反馈
  - 平滑的状态转换
- 响应式布局：
  - 完美适配移动设备
  - 自适应的字体大小
  - 优化的移动端间距

## 项目结构

```
project/
├── app/
│   ├── static/
│   │   └── style.css
│   ├── templates/
│   │   ├── base.html
│   │   └── index.html
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   └── utils.py
├── logs/
├── config.py
├── package_config.py
├── requirements.txt
├── run.py
├── migrate_data.py
└── app.db
```

## 数据存储

系统使用 SQLite 数据库进行数据存储，主要优势：
- 更好的数据一致性和完整性
- 更高效的查询性能
- 更好的并发处理能力
- 更容易进行数据备份和恢复

### 数据迁移

如果你之前使用的是CSV存储，可以使用数据迁移脚本进行迁移：

```bash
python migrate_data.py
```

迁移脚本会：
1. 读取原有的CSV文件
2. 将所有记录迁移到SQLite数据库
3. 保持原有的ID和创建时间
4. 验证数据的完整性

## 运行方法

### 开发环境
```bash
python run.py
```

### 生产环境
1. 修改 run.py 中的 host 和 port
2. 关闭 debug 模式
3. 运行程序

## 使用说明

1. 查询记录：
   - 选择月份（格式：YYYY-MM）
   - 点击查询按钮
   - 查看结果表格和统计信息

2. 添加记录：
   - 选择日期
   - 输入箱号区间（格式：A001-A100）
   - 点击添加按钮

3. 删除记录：
   - 选择月份
   - 点击删除按钮

## 打包说明

使用 auto-py-to-exe 打包：

1. 安装打包工具
```bash
pip install auto-py-to-exe
```

2. 安装 UPX 压缩工具（用于减小程序体积）
   - 下载 UPX: https://github.com/upx/upx/releases
   - 将 upx.exe 放入系统 PATH 或与打包程序同目录

3. 配置打包选项
- Script Location: run.py
- Onefile: One Directory
- Console Window: Console Based
- Additional Files:
  - app/templates -> templates
  - app/static -> static
  - config.py -> .
  - package_config.py -> .
- Advanced Options:
  - --upx-dir: UPX可执行文件所在目录
  - --clean: 清理打包目录
  - --strip: 移除调试符号

4. 打包优化
- 使用 UPX 压缩可以显著减小程序体积
- 压缩后的程序运行速度基本不受影响
- 支持的文件类型：EXE、DLL、SYS 等
- 压缩率通常可达到 50%-70%

5. 打包后注意事项
- 数据库文件（app.db）将在程序所在目录创建
- 日志文件将在程序所在目录的 logs 文件夹中创建
- 首次运行时会自动初始化数据库和日志目录
- 如需迁移数据，请将 migrate_data.py 和原 CSV 文件复制到程序目录运行

## 注意事项

1. 确保 logs 目录存在且有写入权限
2. 箱号区间格式必须统一（如：A001-A100）
3. 日期选择不能为空
4. 数据库文件（app.db）会自动创建

## 系统要求

- Python 3.7+
- 支持现代浏览器
- 操作系统：Windows/Linux/MacOS

## 日志记录

- 位置：logs/app.log
- 记录内容：操作日志和错误信息
- 格式：时间 - 名称 - 级别 - 消息