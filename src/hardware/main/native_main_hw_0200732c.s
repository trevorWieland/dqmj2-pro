.section .text
.arm
.global native_main_hw_0200732c
.type native_main_hw_0200732c, @function
native_main_hw_0200732c:
    mov r0, #0x0
    mcr p15, 0, r0, c7, c10, 4
    bx lr
.size native_main_hw_0200732c, .-native_main_hw_0200732c
