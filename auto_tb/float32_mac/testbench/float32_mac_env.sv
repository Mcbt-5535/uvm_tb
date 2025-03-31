
class float32_mac_env extends uvm_env;
    `uvm_component_utils(float32_mac_env)
    float32_mac_agent agt_i;
    float32_mac_agent agt_o;
    float32_mac_model ref_model;
    float32_mac_scoreboard scb;
    uvm_tlm_analysis_fifo #(float32_mac_transaction) ref_model_fifo;
    uvm_tlm_analysis_fifo #(float32_mac_transaction) ref_scb_fifo;
    uvm_tlm_analysis_fifo #(float32_mac_transaction) dut_scb_fifo;

    function new(string name = "float32_mac_env", uvm_component parent);
        super.new(name, parent);
    endfunction

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        agt_i = float32_mac_agent::type_id::create("agt_i", this);
        agt_o = float32_mac_agent::type_id::create("agt_o", this);
        ref_model = float32_mac_model::type_id::create("ref_model", this);
        scb = float32_mac_scoreboard::type_id::create("scb", this);
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
