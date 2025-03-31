
interface float32_mac_if (
    input bit clk_i,
    input bit rst_ni
);
    logic [15:0] op_mask_i;
    logic [0:0] const_en_i;
    logic [1:0] opmode_i;
    logic [1:0] rounding_mode_i;
    logic [511:0] floata_i;
    logic [511:0] floatb_i;
    logic [31:0] constc_i;
    logic [511:0] floatq_o;
    logic [1:0] overflow_o;
    logic [0:0] exception_o;
    
    
endinterface  //my_if

