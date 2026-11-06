.section .text
.arm
.global native_main_hw_02007ff4
.type native_main_hw_02007ff4, @function
native_main_hw_02007ff4:
    mrs r0, cpsr
    orr r1, r0, #0x80
    msr cpsr_c, r1
    and r0, r0, #0x80
    bx lr
.size native_main_hw_02007ff4, .-native_main_hw_02007ff4
