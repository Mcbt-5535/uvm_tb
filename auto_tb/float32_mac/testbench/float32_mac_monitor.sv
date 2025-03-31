
class float32_mac_monitor extends uvm_monitor;

    `uvm_component_utils(float32_mac_monitor)
    virtual float32_mac_if vif;
    float32_mac_transaction tr;
    uvm_analysis_port #(float32_mac_transaction) ap;

    function new(string name = "float32_mac_monitor", uvm_component parent = null);
        super.new(name, parent);
    endfunction

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        if (!uvm_config_db#(virtual float32_mac_if)::get(this, "", "vif", vif))
            `uvm_fatal("float32_mac_monitor", "virtual interface must be set for vif!!!")
        ap = new("ap", this);
    endfunction

    virtual task main_phase(uvm_phase phase);
        tr = new("tr");
        while (1) begin
            @(negedge vif.clk_i);
            tr.rst_ni = vif.rst_ni;
            tr.op_mask_i = vif.op_mask_i;
            tr.const_en_i = vif.const_en_i;
            tr.opmode_i = vif.opmode_i;
            tr.rounding_mode_i = vif.rounding_mode_i;
            tr.floata_i = vif.floata_i;
            tr.floatb_i = vif.floatb_i;
            tr.constc_i = vif.constc_i;
            tr.floatq_o = vif.floatq_o;
            tr.overflow_o = vif.overflow_o;
            tr.exception_o = vif.exception_o;
            ap.write(tr);
        end
    endtask

endclass
