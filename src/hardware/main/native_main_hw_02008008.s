.section .text
.arm
.global native_main_hw_02008008
.type native_main_hw_02008008, @function
native_main_hw_02008008:
    mrs r1, cpsr
    bic r2, r1, #0x80
    orr r2, r2, r0
    msr cpsr_c, r2
    and r0, r1, #0x80
    bx lr
.size native_main_hw_02008008, .-native_main_hw_02008008
