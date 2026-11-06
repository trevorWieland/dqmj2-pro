.section .text
.arm
.global native_main_hw_02007264
.type native_main_hw_02007264, @function
native_main_hw_02007264:
    mov r0, #0x0
    mcr p15, 0, r0, c7, c6, 0
    bx lr
.size native_main_hw_02007264, .-native_main_hw_02007264
