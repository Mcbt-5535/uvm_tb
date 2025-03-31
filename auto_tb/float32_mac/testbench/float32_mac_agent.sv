
class float32_mac_agent extends uvm_agent;
    float32_mac_driver drv;
    float32_mac_monitor mon;
    float32_mac_sequencer sqr;

    uvm_analysis_port #(float32_mac_transaction) ap;
    `uvm_component_utils(float32_mac_agent)

    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        if (is_active == UVM_ACTIVE) begin
            drv = float32_mac_driver::type_id::create("drv", this);
            sqr = float32_mac_sequencer::type_id::create("sqr", this);
        end
        mon = float32_mac_monitor::type_id::create("mon", this);
    endfunction

    virtual function void connect_phase(uvm_phase phase);
        super.connect_phase(phase);
        if (is_active == UVM_ACTIVE) begin
            drv.seq_item_port.connect(sqr.seq_item_export);
        end
        ap = mon.ap;
    endfunction

endclass
