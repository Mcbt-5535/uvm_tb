
`timescale 1ns / 1ps
`include "uvm_macros.svh"

import uvm_pkg::*;
`include "float32_mac_transaction.sv"
`include "float32_mac_driver.sv"
`include "float32_mac_interface.sv"
`include "float32_mac_monitor.sv"
`include "float32_mac_model.sv"
`include "float32_mac_scoreboard.sv"
`include "float32_mac_sequence.sv"
`include "float32_mac_sequencer.sv"
`include "float32_mac_agent.sv"
`include "float32_mac_env.sv"
`include "float32_mac_testcase.sv"
module float32_mac_top;

    reg clk_i;
    initial begin
        clk_i = 0;
        forever begin
            #10 clk_i = ~clk_i;
        end
    end

    reg rst_ni_top;

    initial begin
        rst_ni_top = 0;
        #100;
        rst_ni_top = 1;
    end

    
    float32_mac_if u_float32_mac_if (
        .clk_i (clk_i_top),
        .rst_ni (rst_ni_top)
    );

    float32_mac_dut u_float32_mac_dut (
        .clk_i (clk_i_top),
        .rst_ni (rst_ni_top),
        
        .op_mask_i  (u_float32_mac_if.op_mask_i),
        .const_en_i  (u_float32_mac_if.const_en_i),
        .opmode_i  (u_float32_mac_if.opmode_i),
        .rounding_mode_i  (u_float32_mac_if.rounding_mode_i),
        .floata_i  (u_float32_mac_if.floata_i),
        .floatb_i  (u_float32_mac_if.floatb_i),
        .constc_i  (u_float32_mac_if.constc_i),

        .floatq_o  (u_float32_mac_if.floatq_o),
        .overflow_o  (u_float32_mac_if.overflow_o),
        .exception_o  (u_float32_mac_if.exception_o)
    );

    initial begin
        run_test();
    end

    initial begin
        uvm_config_db#(virtual float32_mac_if )::set(null, "uvm_test_top.env.agt_i.drv",
                                                            "vif", u_float32_mac_if);
        uvm_config_db#(virtual float32_mac_if )::set(null, "uvm_test_top.env.agt_i.mon",
                                                            "vif", u_float32_mac_if);
        uvm_config_db#(virtual float32_mac_if )::set(null, "uvm_test_top.env.agt_o.mon",
                                                            "vif", u_float32_mac_if);
    end

    initial begin
        // Dump waves
        $dumpvars(0, float32_mac_top);
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
