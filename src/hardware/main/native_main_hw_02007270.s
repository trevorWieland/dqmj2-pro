.section .text
.arm
.global native_main_hw_02007270
.type native_main_hw_02007270, @function
native_main_hw_02007270:
    mov r1, #0x0
.L_02007274:
    mov r0, #0x0
.L_02007278:
    orr r2, r1, r0
    mcr p15, 0, r2, c7, c10, 2
    add r0, r0, #0x20
    cmp r0, #0x400
    blt .L_02007278
    add r1, r1, #0x40000000
    cmp r1, #0x0
    bne .L_02007274
    bx lr
.size native_main_hw_02007270, .-native_main_hw_02007270
