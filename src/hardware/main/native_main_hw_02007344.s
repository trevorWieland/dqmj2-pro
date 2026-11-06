.section .text
.arm
.global native_main_hw_02007344
.type native_main_hw_02007344, @function
native_main_hw_02007344:
    add r1, r1, r0
    bic r0, r0, #0x1f
.L_0200734c:
    mcr p15, 0, r0, c7, c5, 1
    add r0, r0, #0x20
    cmp r0, r1
    blt .L_0200734c
    bx lr
.size native_main_hw_02007344, .-native_main_hw_02007344
