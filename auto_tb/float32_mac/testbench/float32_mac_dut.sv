
module float32_mac_dut (
    clk_i,
    rst_ni,
    op_mask_i,
    const_en_i,
    opmode_i,
    rounding_mode_i,
    floata_i,
    floatb_i,
    constc_i,
    floatq_o,
    overflow_o,
    exception_o
);
    input [0:0] clk_i;
    input [0:0] rst_ni;
    input [15:0] op_mask_i;
    input [0:0] const_en_i;
    input [1:0] opmode_i;
    input [1:0] rounding_mode_i;
    input [511:0] floata_i;
    input [511:0] floatb_i;
    input [31:0] constc_i;
    output [511:0] floatq_o;
    output [1:0] overflow_o;
    output [0:0] exception_o;
    
    
endmodule
