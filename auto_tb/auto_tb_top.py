# v1.2 2025/04/07
from template import *
# 设定dut的名称
DEVICE_NAME = "test1"
# 根据需求添加输入输出变量
variables_list = [
    {
        "is_clk": "1",
        "direction": "input",
        "name": "clk_i",
        "type": "bit",
        "length": 1,
        "uvm_attr": "UVM_ALL_ON"
    },
    {
        "is_rstn": "1",
        "direction": "input",
        "name": "rst_ni",
        "type": "bit",
        "length": 1,
        "uvm_attr": "UVM_ALL_ON"
    },
    {
        "direction": "input",
        "name": "en",
        "type": "rand bit",
        "length": 1,
        "uvm_attr": "UVM_ALL_ON"
    },
    {
        "direction": "input",
        "name": "din_i",
        "type": "rand bit",
        "length": 8,
        "uvm_attr": "UVM_ALL_ON"
    },
    {
        "direction": "output",
        "name": "dout_o",
        "type": "rand bit",
        "length": 8,
        "uvm_attr": "UVM_ALL_ON"
    }
    # 可以继续添加更多变量
]

# Get the current script's path
script_dir = os.path.dirname(os.path.abspath(__file__))
# Set the working directory to the script's location
os.chdir(script_dir)

# 生成变量定义和 `uvm_field` 部分
# transaction部分
trans_variables_code = ""
for var in variables_list:
    trans_str = ""
    if (var.get("is_clk") == "1"):
        continue
    else:
        if isinstance(var["length"], int):
            trans_str = f'{var["type"]} [{var["length"]-1}:0] {var["name"]};'
        else:
            trans_str = f'{var["type"]} [{var["length"]+"-1"}:0] {var["name"]};'
    trans_variables_code += f"{trans_str}\n    "

trans_uvm_fields_code = ""
for var in variables_list:
    trans_str = ""
    if (var.get("is_clk") == "1"):
        continue
    else:
        trans_str = f'`uvm_field_int({var["name"]}, {var["uvm_attr"]})'
    trans_uvm_fields_code += f"{trans_str}\n        "

trans_clear_code = ""
for var in variables_list:
    trans_str = ""
    if (var.get("is_clk") == "1"):
        continue
    else:
        if var["length"] == 1:
            trans_str = f'{var["name"]} = 1\'b0;'
        else:
            trans_str = f'{var["name"]} = {{{var["length"]}{{1\'b0}}}};'
    trans_clear_code += f"{trans_str}\n        "

trans_copy_output_code = ""
for var in variables_list:
    trans_str = ""
    if var["direction"] == "output":
        trans_str = f'{var["name"]} = tr.{var["name"]};'
    else:
        continue
    trans_copy_output_code += f"{trans_str}\n        "

trans_copy_input_code = ""
for var in variables_list:
    trans_str = ""
    if (var.get("is_clk") == "1"):
        continue
    else:
        if var["direction"] == "input":
            trans_str = f'{var["name"]} = tr.{var["name"]};'
        else:
            continue
    trans_copy_input_code += f"{trans_str}\n        "

trans_compare_code = ""
count = 0
for var in variables_list:
    trans_str = ""
    if (var.get("is_clk") == "1"):
        continue
    else:
        trans_str += f'if ({var["name"]} !== compare_tr.{var["name"]}) begin\n        '
        trans_str += f'    return {count};\n        '
        trans_str += f'end\n        '
        count = count + 1
    trans_compare_code += f"{trans_str}"

# driver部分
drv_init_code = ""
for var in variables_list:
    drv_str = ""
    if var["direction"] == "input":
        if (var.get("is_clk") == "1") or (var.get("is_rstn") == "1"):
            continue
        else:
            if var["length"] == 1:
                drv_str = f'vif.{var["name"]} <= 1\'b0;'
            else:
                drv_str = f'vif.{var["name"]} <= {{{var["length"]}{{1\'b0}}}};'
        drv_init_code += f"{drv_str}\n        "
    else:
        continue

drv_code = ""
for var in variables_list:
    drv_str = ""
    if (var.get("is_clk") == "1") or (var.get("is_rstn") == "1"):
        continue
    else:
        if (var["direction"] == "input"):
            drv_str = f'vif.{var["name"]} <= tr.{var["name"]};'
        else:
            continue
    drv_code += f"{drv_str}\n                "

clk_var = next((var for var in variables_list if (var.get("is_clk") == "1")), None)
rstn_var = next((var for var in variables_list if (var.get("is_rstn") == "1")), None)
delay = f'@(negedge vif.{clk_var["name"]});' if clk_var else "#1ns;"

drv_delay1 = delay
drv_delay2 = "" if delay == "#1ns;" else delay

#dut部分
dut_port_code = "\n    ".join([f'{var["name"]},' for var in variables_list])
dut_port_code = dut_port_code[:-1]
dut_dir_code = ""
for var in variables_list:
    dut_str = ""
    if isinstance(var["length"], int):
        dut_str = f'{var["direction"]} [{var["length"]-1}:0] {var["name"]};'
    else:
        dut_str = f'{var["direction"]} [{var["length"]+"-1"}:0] {var["name"]};'
    dut_dir_code += f"{dut_str}\n    "

#interface部分
intf_port_code = f'{clk_var["direction"]} bit {clk_var["name"]},\n' if clk_var else ""
intf_port_code += f'    {rstn_var["direction"]} bit {rstn_var["name"]}' if rstn_var else ""
intf_code = ""
for var in variables_list:
    intf_str = ""
    if (var.get("is_clk") == "1") or (var.get("is_rstn") == "1"):
        continue
    if isinstance(var["length"], int):
        intf_str = f'logic [{var["length"]-1}:0] {var["name"]};'
    else:
        intf_str = f'logic [{var["length"]+"-1"}:0] {var["name"]};'
    intf_code += f"{intf_str}\n    "

#model部分
mdl_code = "\n            ".join([f'tr_o.{var["name"]} = tr_i.{var["name"]};' for var in variables_list if var.get("is_clk") != "1"])

#monitor部分
mon_delay = delay
mon_code = "\n            ".join([f'tr.{var["name"]} = vif.{var["name"]};' for var in variables_list if var.get("is_clk") != "1"])

#top部分

top_if_ins = f'.{clk_var["name"]} ({clk_var["name"]}_top),' if clk_var else ""
top_if_ins += f'\n        .{rstn_var["name"]} ({rstn_var["name"]}_top),' if rstn_var else ""
top_if_ins = top_if_ins[:-1]

if clk_var:
    top_clk = f'reg {clk_var["name"]}_top;\n'
    top_clk += f'    shortreal half_period;\n'
    top_clk += f'    shortreal clk_freq;\n'
    top_clk += f'    initial begin\n'
    top_clk += f'        if ($value$plusargs("CLK_FREQ=%f", clk_freq)) begin\n'
    top_clk += f'            $display("clk_freq=%f(M)", clk_freq);\n'
    top_clk += f'        end\n'
    top_clk += f'        half_period = 500/clk_freq;\n'
    top_clk += f'        clk_i_top = 0;\n'
    top_clk += f'        forever begin\n'
    top_clk += f'            #half_period {clk_var["name"]}_top = ~{clk_var["name"]}_top;\n'
    top_clk += f'        end\n'
    top_clk += f'    end\n'
else:
    top_clk = ""

if rstn_var:
    top_rst = f'reg {rstn_var["name"]}_top;\n\n'
    top_rst += f'    initial begin\n'
    top_rst += f'        {rstn_var["name"]}_top = 0;\n'
    top_rst += f'        #100;\n'
    top_rst += f'        {rstn_var["name"]}_top = 1;\n'
    top_rst += f'    end\n'
else:
    top_rst = ""

top_str_i = ""
top_str_o = ""
top_dut_ins = ""
for var in variables_list:
    if (var.get("is_clk") == "1") or (var.get("is_rstn") == "1"):
        continue
    if var["direction"] == "input":
        top_str_i += f'\n        .{var["name"]}  (u_{DEVICE_NAME}_if.{var["name"]}),'
    else:
        top_str_o += f'\n        .{var["name"]}  (u_{DEVICE_NAME}_if.{var["name"]}),'
top_dut_ins = top_str_i + "\n" + top_str_o
top_dut_ins = top_dut_ins[:-1]

# 使用示例
if __name__ == "__main__":

    creator = FileStructureCreator(os.path.join(script_dir, f'{DEVICE_NAME}_dv', 'verif'))

    # 使用模板创建文件结构
    creator.add_structure(
        folder_name=os.path.join('testbench', 'sequences'),
        files={f'{DEVICE_NAME}_sequence.sv': templates['sequence'].format(DEVICE_NAME=DEVICE_NAME)},
    )
    creator.add_structure(folder_name=os.path.join('agent', f'{DEVICE_NAME}_agent'),
                          files={
                              f'{DEVICE_NAME}_agent.sv':
                              templates['agent'].format(DEVICE_NAME=DEVICE_NAME),
                              f'{DEVICE_NAME}_driver.sv':
                              templates['driver'].format(DEVICE_NAME=DEVICE_NAME, INIT=drv_init_code, DRV_CODE=drv_code, DRV_DELAY=drv_delay1, DRV_DELAY2=drv_delay2),
                              f'{DEVICE_NAME}_interface.sv':
                              templates['interface'].format(DEVICE_NAME=DEVICE_NAME, PORT=intf_port_code, CODE=intf_code),
                              f'{DEVICE_NAME}_monitor.sv':
                              templates['monitor'].format(DEVICE_NAME=DEVICE_NAME, DELAY=mon_delay, CODE=mon_code),
                              f'{DEVICE_NAME}_sequencer.sv':
                              templates['sequencer'].format(DEVICE_NAME=DEVICE_NAME),
                              f'{DEVICE_NAME}_transaction.sv':
                              templates['transaction'].format(DEVICE_NAME=DEVICE_NAME,
                                                              VARIABLES=trans_variables_code,
                                                              UVM_FIELDS=trans_uvm_fields_code,
                                                              CLEAR_VAR=trans_clear_code,
                                                              COPY_INPUT=trans_copy_input_code,
                                                              COPY_OUTPUT=trans_copy_output_code,
                                                              COMPARE_VAR=trans_compare_code),
                          })
    creator.add_structure(folder_name=os.path.join('env', f'{DEVICE_NAME}_env'),
                          files={
                              f'{DEVICE_NAME}_env.sv': templates['env'].format(DEVICE_NAME=DEVICE_NAME),
                              f'{DEVICE_NAME}_model.sv': templates['model'].format(DEVICE_NAME=DEVICE_NAME, CODE=mdl_code),
                              f'{DEVICE_NAME}_scoreboard.sv': templates['scoreboard'].format(DEVICE_NAME=DEVICE_NAME),
                          })
    creator.add_structure(
        folder_name=os.path.join('testbench', 'hdl_top'),
        files={
            #   f'{DEVICE_NAME}_dut.sv': templates['dut'].format(DEVICE_NAME=DEVICE_NAME, PORT=dut_port_code, DIR=dut_dir_code),
            f'testbench.sv': templates['testbench'].format(DEVICE_NAME=DEVICE_NAME, CLK=top_clk, RST=top_rst, IF_INS=top_if_ins, DUT_INS=top_dut_ins),
        })
    creator.add_structure(folder_name=os.path.join('..', '..', 'design_file', f'{DEVICE_NAME}_ip'), files={
        f'{DEVICE_NAME}_dut.v': templates['dut'].format(DEVICE_NAME=DEVICE_NAME, PORT=dut_port_code, DIR=dut_dir_code),
    })
    creator.add_structure(folder_name=os.path.join('testbench', 'tests'), files={f'{DEVICE_NAME}_testcase.sv': templates['testcase'].format(DEVICE_NAME=DEVICE_NAME)})

    os.makedirs(os.path.join(script_dir, f'{DEVICE_NAME}_dv', 'script'), exist_ok=True)
    os.makedirs(os.path.join(script_dir, f'{DEVICE_NAME}_dv', 'filelists'), exist_ok=True)
    # os.makedirs(os.path.join(script_dir, f'design_file'), exist_ok=True)
    # 创建结构
    creator.create_structure()
