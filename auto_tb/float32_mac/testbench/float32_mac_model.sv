
class float32_mac_model extends uvm_component;
    `uvm_component_utils(float32_mac_model)
    uvm_blocking_get_port #(float32_mac_transaction) get_port;
    uvm_analysis_port #(float32_mac_transaction) ap;

    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        get_port = new("get_port", this);
        ap = new("ap", this);
    endfunction

    task main_phase(uvm_phase phase);
        float32_mac_transaction tr_i;
        float32_mac_transaction tr_o;
        super.main_phase(phase);
        tr_o = new("tr_o");
        while (1) begin
            tr_o.clear();
            get_port.get(tr_i);
            tr_o.rst_ni = tr_i.rst_ni;
            tr_o.op_mask_i = tr_i.op_mask_i;
            tr_o.const_en_i = tr_i.const_en_i;
            tr_o.opmode_i = tr_i.opmode_i;
            tr_o.rounding_mode_i = tr_i.rounding_mode_i;
            tr_o.floata_i = tr_i.floata_i;
            tr_o.floatb_i = tr_i.floatb_i;
            tr_o.constc_i = tr_i.constc_i;
            tr_o.floatq_o = tr_i.floatq_o;
            tr_o.overflow_o = tr_i.overflow_o;
            tr_o.exception_o = tr_i.exception_o;
            // tr_i.print();
            // tr_o.print();
            ap.write(tr_o);
        end
    endtask
endclass
