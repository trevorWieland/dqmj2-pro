.section .text
.arm
.global native_main_hw_02008020
.type native_main_hw_02008020, @function
native_main_hw_02008020:
    mrs r0, cpsr
    orr r1, r0, #0xc0
    msr cpsr_c, r1
    and r0, r0, #0xc0
    bx lr
.size native_main_hw_02008020, .-native_main_hw_02008020
