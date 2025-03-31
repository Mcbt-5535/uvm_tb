使用script下的gen_filelist.py生成filelist
脚本会先在design file、sequence、vseq、test每个文件夹生成单独的.f文件, 
之后将在filelists文件夹中生成总的tc_filelist.f

文件夹结构
  top
    ├─design
    └─test1_dv
        ├─filelists
        ├─script
        └─verif
            ├─agent
            │  ├─a_agent
            │  └─b_agent
            ├─env
            │  ├─aa_env
            │  └─bb_env
            └─testbench
                ├─hdl_top
                ├─sequences
                ├─tests
                └─vseqs
在各个子文件夹下的filelist中，排列顺序按照extend顺序排序，被extend的排在前面，具体的extend格式如：class s1 extends uvm_sequence;
在tc_filelist.f中，排列顺序如下：
    -f design files
    hdl_top
        testbench
    agent
        intf
        transaction
        driver
        monitor
        sequencer
        virtual_seqr
        agent
    env
        reference_model
        scoreboard
        env
    -f sequences
    -f vseqs
    -f tests