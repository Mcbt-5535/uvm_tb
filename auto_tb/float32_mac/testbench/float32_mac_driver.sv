
class float32_mac_driver extends uvm_driver #(float32_mac_transaction);
    `uvm_component_utils(float32_mac_driver)
    virtual float32_mac_if  vif;
    float32_mac_transaction tr;

    function new(string name = "float32_mac_driver", uvm_component parent = null);
        super.new(name, parent);
    endfunction  //new()

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        if (!uvm_config_db#(virtual float32_mac_if)::get(this, "", "vif", vif))
            `uvm_fatal("float32_mac_driver", "virtual interface must be set for vif!!!")
    endfunction

    virtual task main_phase(uvm_phase phase);
        vif.op_mask_i <= {16{1'b0}};
        vif.const_en_i <= 1'b0;
        vif.opmode_i <= {2{1'b0}};
        vif.rounding_mode_i <= {2{1'b0}};
        vif.floata_i <= {512{1'b0}};
        vif.floatb_i <= {512{1'b0}};
        vif.constc_i <= {32{1'b0}};
        
        while (1) begin
            seq_item_port.try_next_item(tr);
            if (tr == null) begin
                @(negedge vif.clk_i);
            end else begin
                vif.op_mask_i <= tr.op_mask_i;
                vif.const_en_i <= tr.const_en_i;
                vif.opmode_i <= tr.opmode_i;
                vif.rounding_mode_i <= tr.rounding_mode_i;
                vif.floata_i <= tr.floata_i;
                vif.floatb_i <= tr.floatb_i;
                vif.constc_i <= tr.constc_i;
                
                @(negedge vif.clk_i);
                seq_item_port.item_done();
            end
        end
    endtask

endclass  //float32_mac_driver
