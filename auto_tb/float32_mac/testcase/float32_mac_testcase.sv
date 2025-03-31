
class float32_mac_testcase extends uvm_test;
    `uvm_component_utils(float32_mac_testcase)
    float32_mac_env env;
    function new(string name = "float32_mac_testcase", uvm_component parent);
        super.new(name, parent);
    endfunction

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        env = float32_mac_env::type_id::create("env", this);

        uvm_config_db#(uvm_object_wrapper)::set(this, "env.agt_i.sqr.main_phase",
                                                "default_sequence",
                                                float32_mac_sequence::type_id::get());
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
    // +UVM_TESTNAME=float32_mac_testcase
endclass
