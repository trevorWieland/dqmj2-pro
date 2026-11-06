.section .text
.arm
.global native_main_hw_02007728
.type native_main_hw_02007728, @function
native_main_hw_02007728:
    mrc p15, 0, r0, c1, c0, 0
    orr r0, r0, #0x1
    mcr p15, 0, r0, c1, c0, 0
    bx lr
.size native_main_hw_02007728, .-native_main_hw_02007728
