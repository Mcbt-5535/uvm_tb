
class float32_mac_scoreboard extends uvm_scoreboard;
    `uvm_component_utils(float32_mac_scoreboard)
    float32_mac_transaction ref_queue[$];
    uvm_blocking_get_port #(float32_mac_transaction ) ref_port;
    uvm_blocking_get_port #(float32_mac_transaction ) dut_port;

    function new(string name = "float32_mac_scoreboard", uvm_component parent);
        super.new(name, parent);
    endfunction
    function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        ref_port = new("ref_port", this);
        dut_port = new("dut_port", this);
    endfunction

    task main_phase(uvm_phase phase);
        float32_mac_transaction ref_tr_i, dut_tr_i, ref_tr, temp_tr1;
        int result;
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
                    ref_tr = ref_queue.pop_front();
                    result  = ref_tr.compare_1(dut_tr_i);
                    if (result == 0) begin
                        `uvm_info("float32_mac_scb", "Compare pass", UVM_LOW);
                        if (get_report_verbosity_level() >= UVM_LOW) begin
                            dut_tr_i.print();
                            ref_tr.print();
                        end
                    end else begin
                        `uvm_error("float32_mac_scb", $sformatf("Compare FAILED!!!!! err:%d", result));
                        $display("dut out:");
                        dut_tr_i.print();
                        $display(" expect:");
                        ref_tr.print();
                        // `uvm_fatal("compare fail", "compare fail!!!!")
                    end
                end else begin
                    `uvm_error("float32_mac_scb", "the unexpected pkt is");
                    ref_tr_i.print();
                    // `uvm_fatal("my_scoreboard", "Received from DUT, while Expect Queue is empty");
                end
            end
        join
    endtask
endclass
