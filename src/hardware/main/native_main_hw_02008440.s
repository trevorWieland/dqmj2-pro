.section .text
.arm
.global native_main_hw_02008440
.type native_main_hw_02008440, @function
native_main_hw_02008440:
    mov r0, #0x0
    mcr p15, 0, r0, c7, c0, 4
    bx lr
.size native_main_hw_02008440, .-native_main_hw_02008440
