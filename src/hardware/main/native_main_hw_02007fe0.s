.section .text
.arm
.global native_main_hw_02007fe0
.type native_main_hw_02007fe0, @function
native_main_hw_02007fe0:
    mrs r0, cpsr
    bic r1, r0, #0x80
    msr cpsr_c, r1
    and r0, r0, #0x80
    bx lr
.size native_main_hw_02007fe0, .-native_main_hw_02007fe0
