import os


class FileStructureCreator:

    def __init__(self, base_path=None):
        # 获取脚本所在目录作为根路径，如果没有传入自定义路径
        self.base_path = base_path or os.path.dirname(os.path.abspath(__file__))
        self.structures = []

    def add_structure(self, folder_name, files, module_list=None):
        # 保存结构，并传入module_list用于动态生成内容
        self.structures.append((folder_name, files, module_list))

    def create_structure(self):
        for folder_name, files, module_list in self.structures:
            # 根据脚本所在目录构建文件夹路径
            folder_path = os.path.join(self.base_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            for file_name, content_template in files.items():
                file_path = os.path.join(folder_path, file_name)
                # 调用写入函数处理具体内容写入
                self.write_to_file(file_path, content_template, module_list)

    def write_to_file(self, file_path, content_template, module_list):
        """单独的文件写入函数，根据模板和模块列表写入文件"""
        if module_list:
            with open(file_path, 'w') as f:  # 'w' 模式重写文件
                for module in module_list:
                    # 使用模块名替换模板中的占位符
                    content = content_template.replace("{module}", module)
                    f.write(f"{content}\n")  # 每个模块内容换行
        else:
            # 没有模块列表时，直接写入模板内容
            with open(file_path, 'w') as f:
                f.write(content_template)


def generate_systemverilog_code(code_dict):

    def format_class(class_data):
        class_name = class_data['class_name']
        parameters = ', '.join([f'{param} = {value}' for param, value in class_data['parameters'].items()])
        extends = class_data['extends']
        macros = '\n'.join(class_data['macros'])
        methods = []

        for method_name, method_data in class_data['methods'].items():
            return_type = method_data['return_type']
            arguments = method_data['arguments']
            body = method_data['body'].strip()
            methods.append(f"{return_type} {method_name}({arguments});\n{body}\nend{method_data['return_type'][7:]}")

        members = []
        if 'members' in class_data:
            for member_name, member_type in class_data['members'].items():
                members.append(f"{member_type} {member_name};")

        members_str = '\n'.join(members)
        methods_str = '\n\n'.join(methods)

        return f"class {class_name} #({parameters}) extends {extends};\n\n" f"{macros}\n\n" f"{members_str}\n\n" f"{methods_str}\n" f"endclass"

    sequence_code = format_class(code_dict['sequence'])
    agent_code = format_class(code_dict['agent'])

    return f"sequence:\n{sequence_code}\n\nagent:\n{agent_code}"


templates = {
    #########################################################################
    ###                             SEQUENCE                              ###
    #########################################################################
    "sequence":
    '''
class {DEVICE_NAME}_sequence extends uvm_sequence #({DEVICE_NAME}_transaction);

    `uvm_object_utils({DEVICE_NAME}_sequence)
    function new(string name = "{DEVICE_NAME}_sequence");
        super.new(name);
    endfunction

    virtual task pre_body();
        if (starting_phase != null) starting_phase.raise_objection(this);
    endtask
    virtual task post_body();
        if (starting_phase != null) starting_phase.drop_objection(this);
    endtask
    virtual task body();
        {DEVICE_NAME}_transaction tr;
        repeat (10) begin
            tr = new("tr");
            // assert (tr.randomize with {{tr.mode_i == 13'h0000;}});
            tr.randomize();
            `uvm_send(tr)
        end
    endtask
endclass
''',
    #########################################################################
    ###                               AGENT                               ###
    #########################################################################
    "agent":
    '''
class {DEVICE_NAME}_agent extends uvm_agent;
    {DEVICE_NAME}_driver drv;
    {DEVICE_NAME}_monitor mon;
    {DEVICE_NAME}_sequencer sqr;

    uvm_analysis_port #({DEVICE_NAME}_transaction) ap;
    `uvm_component_utils({DEVICE_NAME}_agent)

    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        if (is_active == UVM_ACTIVE) begin
            drv = {DEVICE_NAME}_driver::type_id::create("drv", this);
            sqr = {DEVICE_NAME}_sequencer::type_id::create("sqr", this);
        end
        mon = {DEVICE_NAME}_monitor::type_id::create("mon", this);
    endfunction

    virtual function void connect_phase(uvm_phase phase);
        super.connect_phase(phase);
        if (is_active == UVM_ACTIVE) begin
            drv.seq_item_port.connect(sqr.seq_item_export);
        end
        ap = mon.ap;
    endfunction

endclass
''',
    #########################################################################
    ###                              DRIVER                               ###
    #########################################################################
    "driver":
    '''
class {DEVICE_NAME}_driver extends uvm_driver #({DEVICE_NAME}_transaction);
    `uvm_component_utils({DEVICE_NAME}_driver)
    virtual {DEVICE_NAME}_if  vif;
    {DEVICE_NAME}_transaction tr;

    function new(string name = "{DEVICE_NAME}_driver", uvm_component parent = null);
        super.new(name, parent);
    endfunction  //new()

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        if (!uvm_config_db#(virtual {DEVICE_NAME}_if)::get(this, "", "vif", vif))
            `uvm_fatal("{DEVICE_NAME}_driver", "virtual interface must be set for vif!!!")
    endfunction

    virtual task main_phase(uvm_phase phase);
        {INIT}
        while (1) begin
            seq_item_port.try_next_item(tr);
            if (tr == null) begin
                {DRV_DELAY}
            end else begin
                {DRV_CODE}
                {DRV_DELAY2}
                seq_item_port.item_done();
            end
        end
    endtask

endclass  //{DEVICE_NAME}_driver
''',
    #########################################################################
    ###                                DUT                                ###
    #########################################################################
    "dut":
    '''
module {DEVICE_NAME}_dut (
    {PORT}
);
    {DIR}
    
endmodule
''',
    #########################################################################
    ###                                ENV                                ###
    #########################################################################
    "env":
    '''
class {DEVICE_NAME}_env extends uvm_env;
    `uvm_component_utils({DEVICE_NAME}_env)
    {DEVICE_NAME}_agent agt_i;
    {DEVICE_NAME}_agent agt_o;
    {DEVICE_NAME}_model ref_model;
    {DEVICE_NAME}_scoreboard scb;
    uvm_tlm_analysis_fifo #({DEVICE_NAME}_transaction) ref_model_fifo;
    uvm_tlm_analysis_fifo #({DEVICE_NAME}_transaction) ref_scb_fifo;
    uvm_tlm_analysis_fifo #({DEVICE_NAME}_transaction) dut_scb_fifo;

    function new(string name = "{DEVICE_NAME}_env", uvm_component parent);
        super.new(name, parent);
    endfunction

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        agt_i = {DEVICE_NAME}_agent::type_id::create("agt_i", this);
        agt_o = {DEVICE_NAME}_agent::type_id::create("agt_o", this);
        ref_model = {DEVICE_NAME}_model::type_id::create("ref_model", this);
        scb = {DEVICE_NAME}_scoreboard::type_id::create("scb", this);
        agt_i.is_active = UVM_ACTIVE;
        agt_o.is_active = UVM_PASSIVE;
        ref_model_fifo = new("ref_model_fifo", this);
        ref_scb_fifo = new("ref_scb_fifo", this);
        dut_scb_fifo = new("dut_scb_fifo", this);

    endfunction

    virtual function void connect_phase(uvm_phase phase);
        super.connect_phase(phase);
        agt_i.ap.connect(ref_model_fifo.analysis_export);
        ref_model.get_port.connect(ref_model_fifo.blocking_get_export);

        ref_model.ap.connect(ref_scb_fifo.analysis_export);
        scb.ref_port.connect(ref_scb_fifo.blocking_get_export);

        agt_o.ap.connect(dut_scb_fifo.analysis_export);
        scb.dut_port.connect(dut_scb_fifo.blocking_get_export);
    endfunction

endclass
''',
    #########################################################################
    ###                             INTERFACE                             ###
    #########################################################################
    "interface":
    '''
interface {DEVICE_NAME}_if (
    {PORT}
);
    {CODE}
    
endinterface  //my_if

''',
    #########################################################################
    ###                               MODEL                               ###
    #########################################################################
    "model":
    '''
class {DEVICE_NAME}_model extends uvm_component;
    `uvm_component_utils({DEVICE_NAME}_model)
    uvm_blocking_get_port #({DEVICE_NAME}_transaction) get_port;
    uvm_analysis_port #({DEVICE_NAME}_transaction) ap;

    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        get_port = new("get_port", this);
        ap = new("ap", this);
    endfunction

    task main_phase(uvm_phase phase);
        {DEVICE_NAME}_transaction tr_i;
        {DEVICE_NAME}_transaction tr_o;
        super.main_phase(phase);
        tr_o = new("tr_o");
        while (1) begin
            tr_o.clear();
            get_port.get(tr_i);
            {CODE}
            // tr_i.print();
            // tr_o.print();
            ap.write(tr_o);
        end
    endtask
endclass
''',
    #########################################################################
    ###                              MONITOR                              ###
    #########################################################################
    "monitor":
    '''
class {DEVICE_NAME}_monitor extends uvm_monitor;

    `uvm_component_utils({DEVICE_NAME}_monitor)
    virtual {DEVICE_NAME}_if vif;
    {DEVICE_NAME}_transaction tr;
    uvm_analysis_port #({DEVICE_NAME}_transaction) ap;

    function new(string name = "{DEVICE_NAME}_monitor", uvm_component parent = null);
        super.new(name, parent);
    endfunction

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        if (!uvm_config_db#(virtual {DEVICE_NAME}_if)::get(this, "", "vif", vif))
            `uvm_fatal("{DEVICE_NAME}_monitor", "virtual interface must be set for vif!!!")
        ap = new("ap", this);
    endfunction

    virtual task main_phase(uvm_phase phase);
        while (1) begin
            tr = new("tr");
            {DELAY}
            {CODE}
            ap.write(tr);
        end
    endtask

endclass
''',
    #########################################################################
    ###                            SCOREBOARD                             ###
    #########################################################################
    "scoreboard":
    '''
class {DEVICE_NAME}_scoreboard extends uvm_scoreboard;
    `uvm_component_utils({DEVICE_NAME}_scoreboard)
    {DEVICE_NAME}_transaction ref_queue[$];
    uvm_blocking_get_port #({DEVICE_NAME}_transaction ) ref_port;
    uvm_blocking_get_port #({DEVICE_NAME}_transaction ) dut_port;

    function new(string name = "{DEVICE_NAME}_scoreboard", uvm_component parent);
        super.new(name, parent);
    endfunction
    function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        ref_port = new("ref_port", this);
        dut_port = new("dut_port", this);
    endfunction

    task main_phase(uvm_phase phase);
        {DEVICE_NAME}_transaction ref_tr_i, dut_tr_i, temp_tr, temp_tr1;
        bit result;
        super.main_phase(phase);
        temp_tr1 = new("temp_tr1");
        fork
            while (1) begin
                ref_port.get(ref_tr_i);
                temp_tr1.copy(ref_tr_i);
                ref_queue.push_back(temp_tr1);
            end
            while (1) begin
                dut_port.get(dut_tr_i);
                // while (ref_queue.size() == 0)
                //     pass;
                #1ps;
                if (ref_queue.size() > 0) begin
                    temp_tr = ref_queue.pop_front();
                    result  = temp_tr.compare(dut_tr_i);
                    if (result) begin
                        `uvm_info("{DEVICE_NAME}_scb", "Compare pass", UVM_LOW);
                        if (get_report_verbosity_level() >= UVM_LOW) begin
                            dut_tr_i.print();
                            temp_tr.print();
                        end

                    end else begin
                        `uvm_error("{DEVICE_NAME}_scb", "Compare FAILED");
                        $display("dut out:");
                        dut_tr_i.print();
                        $display(" expect:");
                        temp_tr.print();
                        // `uvm_fatal("compare fail", "compare fail!!!!")
                    end
                end else begin
                    `uvm_error("{DEVICE_NAME}_scb", "the unexpected pkt is");
                    ref_tr_i.print();
                    // `uvm_fatal("my_scoreboard", "Received from DUT, while Expect Queue is empty");
                end
            end
        join
    endtask
endclass
''',
    #########################################################################
    ###                             SEQUENCER                             ###
    #########################################################################
    "sequencer":
    '''
class {DEVICE_NAME}_sequencer extends uvm_sequencer #({DEVICE_NAME}_transaction);
    `uvm_component_utils({DEVICE_NAME}_sequencer)

    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction
endclass
''',
    #########################################################################
    ###                                TOP                                ###
    #########################################################################
    "top":
    '''
`timescale 1ns / 1ps
`include "uvm_macros.svh"

import uvm_pkg::*;
`include "{DEVICE_NAME}_transaction.sv"
`include "{DEVICE_NAME}_driver.sv"
`include "{DEVICE_NAME}_interface.sv"
`include "{DEVICE_NAME}_monitor.sv"
`include "{DEVICE_NAME}_model.sv"
`include "{DEVICE_NAME}_scoreboard.sv"
`include "{DEVICE_NAME}_sequence.sv"
`include "{DEVICE_NAME}_sequencer.sv"
`include "{DEVICE_NAME}_agent.sv"
`include "{DEVICE_NAME}_env.sv"
`include "{DEVICE_NAME}_testcase.sv"
module {DEVICE_NAME}_top;
    reg {CLK};
    {RST}
    
    initial begin
        {CLK} = 0;
        forever begin
            #10 {CLK} = ~{CLK};
        end
    end
    
    {DEVICE_NAME}_if u_{DEVICE_NAME}_if (
        {IF_INS}
    );

    {DEVICE_NAME}_dut u_{DEVICE_NAME}_dut (
        {IF_INS},
        {DUT_INS}
    );

    initial begin
        run_test();
    end

    initial begin
        uvm_config_db#(virtual {DEVICE_NAME}_if )::set(null, "uvm_test_top.env.agt_i.drv",
                                                            "vif", u_{DEVICE_NAME}_if);
        uvm_config_db#(virtual {DEVICE_NAME}_if )::set(null, "uvm_test_top.env.agt_i.mon",
                                                            "vif", u_{DEVICE_NAME}_if);
        uvm_config_db#(virtual {DEVICE_NAME}_if )::set(null, "uvm_test_top.env.agt_o.mon",
                                                            "vif", u_{DEVICE_NAME}_if);
    end

    initial begin
        // Dump waves
        $dumpvars(0, {DEVICE_NAME}_top);
        $dumpfile("top.vcd");
    end
    
    initial begin
        string tc_name;
        if ($value$plusargs("TC_NAME=%s", tc_name)) begin
            $display("tc_name=%s", tc_name);
        end
        `ifdef WAVE_DUMP
                $display("start dump wave");
                $fsdbDumpfile($sformatf("../wave/waves.fsdb"));
                $fsdbDumpvars(0, "+struct", "+mda", "+all");
        `endif
    end
endmodule
''',
    #########################################################################
    ###                             TESTCASE                              ###
    #########################################################################
    "testcase":
    '''
class {DEVICE_NAME}_testcase extends uvm_test;
    `uvm_component_utils({DEVICE_NAME}_testcase)
    {DEVICE_NAME}_env env;
    function new(string name = "{DEVICE_NAME}_testcase", uvm_component parent);
        super.new(name, parent);
    endfunction

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        env = {DEVICE_NAME}_env::type_id::create("env", this);

        uvm_config_db#(uvm_object_wrapper)::set(this, "env.agt_i.sqr.main_phase",
                                                "default_sequence",
                                                {DEVICE_NAME}_sequence::type_id::get());
    endfunction

    virtual function void report_phase(uvm_phase phase);
        uvm_report_server server;
        int err_cnt;
        super.report_phase(phase);
        server  = get_report_server();
        err_cnt = server.get_severity_count(UVM_ERROR);
        if (err_cnt != 0) begin
            $display("TEST CASE FAILED");
        end else begin
            $display("TEST CASE PASSED");
        end

    endfunction

    virtual function void end_of_elaboration();
        uvm_top.print_topology();
    endfunction
    // +UVM_TESTNAME={DEVICE_NAME}_testcase
endclass
''',
    #########################################################################
    ###                            TRANSACTION                            ###
    #########################################################################
    "transaction":
    '''
class {DEVICE_NAME}_transaction extends uvm_sequence_item;
   
    {VARIABLES}

    function new(string name = "{DEVICE_NAME}_transaction");
        super.new(name);
    endfunction
    
    `uvm_object_utils_begin({DEVICE_NAME}_transaction)
        {UVM_FIELDS}
    `uvm_object_utils_end
    
    function void clear();
        {CLEAR_VAR} 
    endfunction
    
    function void copy_output({DEVICE_NAME}_transaction tr);
        {COPY_OUTPUT}
    endfunction
    
endclass
    ''',
}
