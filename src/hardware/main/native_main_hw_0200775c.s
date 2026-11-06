.section .text
.arm
.global native_main_hw_0200775c
.type native_main_hw_0200775c, @function
native_main_hw_0200775c:
    mcr p15, 0, r0, c6, c1, 0
    bx lr
.size native_main_hw_0200775c, .-native_main_hw_0200775c
