.section .text
.arm
.global native_main_hw_02007308
.type native_main_hw_02007308, @function
native_main_hw_02007308:
    mov ip, #0x0
    add r1, r1, r0
    bic r0, r0, #0x1f
.L_02007314:
    mcr p15, 0, ip, c7, c10, 4
    mcr p15, 0, r0, c7, c14, 1
    add r0, r0, #0x20
    cmp r0, r1
    blt .L_02007314
    bx lr
.size native_main_hw_02007308, .-native_main_hw_02007308
