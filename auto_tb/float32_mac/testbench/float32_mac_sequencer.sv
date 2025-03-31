
class float32_mac_sequencer extends uvm_sequencer #(float32_mac_transaction);
    `uvm_component_utils(float32_mac_sequencer)

    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction
endclass
