
## 功能概述

这个Python脚本是一个用于自动生成UVM(Universal Verification Methodology)测试平台的工具，专门为数字设计单元(DUT)创建完整的验证环境。它可以根据用户提供的DUT接口定义，自动生成以下UVM组件：

- 事务(transaction)类
- 代理(agent)及其子组件(driver, monitor, sequencer)
- 环境(env)及其子组件(model, scoreboard)
- 测试用例(testcase)
- 序列(sequence)
- 顶层测试平台(top)和DUT包装

## 主要特点

- **模板化生成**：使用预定义的模板文件，确保生成的代码符合UVM标准
- **灵活配置**：通过JSON格式的变量列表定义DUT接口
- **自动化**：一键生成完整的UVM验证环境结构
- **可扩展**：易于添加新的模板或修改现有模板

## 使用方法

### 1. 配置DUT接口

在脚本中修改`variables_list`变量，定义DUT的接口信号。每个信号需要指定以下属性：

```python

variables_list = [
    {
        "is_clk": "1",          # 是否为时钟信号(可选)
        "is_rstn": "1",         # 是否为复位信号(可选)
        "direction": "input",   # 信号方向(input/output)
        "name": "signal_name",  # 信号名称
        "type": "bit",          # 信号类型
        "length": 1,            # 信号位宽(整数)
        "uvm_attr": "UVM_ALL_ON" # UVM字段属性
    },
    # 更多信号...
]

```

### 2. 设置DUT名称

修改`DEVICE_NAME`变量为您的DUT名称：

```python
DEVICE_NAME = "your_dut_name"
```

### 3. 运行脚本

直接执行脚本：

```bash
python uvm_tb_generator.py
```

### 4. 生成的文件结构

脚本将在当前目录下创建以下文件结构：

```
├─design_file
│  └─your_dut_name_ip
│      └── your_dut_name_dut.sv
└─your_dut_name_dv/
    ├── filelists/
    ├── script/
    └── verif/
        ├── agent/
        │   └── your_dut_name_agent/
        │       ├── your_dut_name_agent.sv
        │       ├── your_dut_name_driver.sv
        │       ├── your_dut_name_interface.sv
        │       ├── your_dut_name_monitor.sv
        │       ├── your_dut_name_sequencer.sv
        │       └── your_dut_name_transaction.sv
        ├── env/
        │   └── your_dut_name_env/
        │       ├── your_dut_name_env.sv
        │       ├── your_dut_name_model.sv
        │       └── your_dut_name_scoreboard.sv
        └── testbench/
            ├── sequences/
            │   └── your_dut_name_sequence.sv
            ├── tests/
            │   └── your_dut_name_testcase.sv
            └── hdl_top/
                └── your_dut_name_top.sv
```

## 自定义模板

如果需要修改生成的代码风格或添加新功能，可以编辑脚本中的`templates`字典变量。每个键对应一个UVM组件类型，值是该组件的模板字符串。

## 注意事项

1. 确保Python环境已安装(支持Python 3.x)
2. 生成的代码可能需要根据具体项目要求进行微调
3. 脚本假设使用SystemVerilog和UVM 1.2标准
4. 时钟和复位信号需要特别标记(`is_clk`和`is_rstn`)

## 示例

示例中展示了一个名为"float32_mac"的DUT的测试平台生成，包含多个输入输出信号和相应的UVM验证组件。