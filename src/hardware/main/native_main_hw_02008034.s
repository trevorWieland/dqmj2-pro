.section .text
.arm
.global native_main_hw_02008034
.type native_main_hw_02008034, @function
native_main_hw_02008034:
    mrs r1, cpsr
    bic r2, r1, #0xc0
    orr r2, r2, r0
    msr cpsr_c, r2
    and r0, r1, #0xc0
    bx lr
.size native_main_hw_02008034, .-native_main_hw_02008034
