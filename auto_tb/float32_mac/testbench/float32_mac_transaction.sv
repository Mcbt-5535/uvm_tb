
class float32_mac_transaction extends uvm_sequence_item;
   
    bit [0:0] rst_ni;
    rand bit [15:0] op_mask_i;
    bit [0:0] const_en_i;
    rand bit [1:0] opmode_i;
    rand bit [1:0] rounding_mode_i;
    rand bit [511:0] floata_i;
    rand bit [511:0] floatb_i;
    rand bit [31:0] constc_i;
    bit [511:0] floatq_o;
    bit [1:0] overflow_o;
    bit [0:0] exception_o;
    

    function new(string name = "float32_mac_transaction");
        super.new(name);
    endfunction
    
    `uvm_object_utils_begin(float32_mac_transaction)
        `uvm_field_int(rst_ni, UVM_ALL_ON)
        `uvm_field_int(op_mask_i, UVM_ALL_ON)
        `uvm_field_int(const_en_i, UVM_ALL_ON)
        `uvm_field_int(opmode_i, UVM_ALL_ON)
        `uvm_field_int(rounding_mode_i, UVM_ALL_ON)
        `uvm_field_int(floata_i, UVM_ALL_ON)
        `uvm_field_int(floatb_i, UVM_ALL_ON)
        `uvm_field_int(constc_i, UVM_ALL_ON)
        `uvm_field_int(floatq_o, UVM_ALL_ON)
        `uvm_field_int(overflow_o, UVM_ALL_ON)
        `uvm_field_int(exception_o, UVM_ALL_ON)
        
    `uvm_object_utils_end
    
    function void clear();
        rst_ni = 1'b0;
        op_mask_i = {16{1'b0}};
        const_en_i = 1'b0;
        opmode_i = {2{1'b0}};
        rounding_mode_i = {2{1'b0}};
        floata_i = {512{1'b0}};
        floatb_i = {512{1'b0}};
        constc_i = {32{1'b0}};
        floatq_o = {512{1'b0}};
        overflow_o = {2{1'b0}};
        exception_o = 1'b0;
         
    endfunction
    
    function void copy_input(float32_mac_transaction tr);
        rst_ni = tr.rst_ni;
        op_mask_i = tr.op_mask_i;
        const_en_i = tr.const_en_i;
        opmode_i = tr.opmode_i;
        rounding_mode_i = tr.rounding_mode_i;
        floata_i = tr.floata_i;
        floatb_i = tr.floatb_i;
        constc_i = tr.constc_i;
        
    endfunction
    
    function void copy_output(float32_mac_transaction tr);
        floatq_o = tr.floatq_o;
        overflow_o = tr.overflow_o;
        exception_o = tr.exception_o;
        
    endfunction
    
    function int compare_1(float32_mac_transaction compare_tr);
        if (rst_ni !== compare_tr.rst_ni) begin
            return 0;
        end
        if (op_mask_i !== compare_tr.op_mask_i) begin
            return 1;
        end
        if (const_en_i !== compare_tr.const_en_i) begin
            return 2;
        end
        if (opmode_i !== compare_tr.opmode_i) begin
            return 3;
        end
        if (rounding_mode_i !== compare_tr.rounding_mode_i) begin
            return 4;
        end
        if (floata_i !== compare_tr.floata_i) begin
            return 5;
        end
        if (floatb_i !== compare_tr.floatb_i) begin
            return 6;
        end
        if (constc_i !== compare_tr.constc_i) begin
            return 7;
        end
        if (floatq_o !== compare_tr.floatq_o) begin
            return 8;
        end
        if (overflow_o !== compare_tr.overflow_o) begin
            return 9;
        end
        if (exception_o !== compare_tr.exception_o) begin
            return 10;
        end
        
        return 0;
    endfunction
    
endclass
    