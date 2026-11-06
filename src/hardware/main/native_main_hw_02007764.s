.section .text
.arm
.global native_main_hw_02007764
.type native_main_hw_02007764, @function
native_main_hw_02007764:
    mcr p15, 0, r0, c6, c2, 0
    bx lr
.size native_main_hw_02007764, .-native_main_hw_02007764
