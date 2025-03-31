
class float32_mac_sequence extends uvm_sequence #(float32_mac_transaction);

    `uvm_object_utils(float32_mac_sequence)
    function new(string name = "float32_mac_sequence");
        super.new(name);
    endfunction

    virtual task pre_body();
        if (starting_phase != null) starting_phase.raise_objection(this);
    endtask
    virtual task post_body();
        if (starting_phase != null) starting_phase.drop_objection(this);
    endtask
    virtual task body();
        float32_mac_transaction tr;
        tr = new("tr");
        repeat (10) begin
            // assert (tr.randomize with {tr.mode_i == 13'h0000;});
            tr.randomize();
            `uvm_send(tr)
        end
    endtask
endclass
