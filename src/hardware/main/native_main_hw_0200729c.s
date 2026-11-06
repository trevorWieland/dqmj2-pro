.section .text
.arm
.global native_main_hw_0200729c
.type native_main_hw_0200729c, @function
native_main_hw_0200729c:
    mov ip, #0x0
    mov r1, #0x0
.L_020072a4:
    mov r0, #0x0
.L_020072a8:
    orr r2, r1, r0
    mcr p15, 0, ip, c7, c10, 4
    mcr p15, 0, r2, c7, c14, 2
    add r0, r0, #0x20
    cmp r0, #0x400
    blt .L_020072a8
    add r1, r1, #0x40000000
    cmp r1, #0x0
    bne .L_020072a4
    bx lr
.size native_main_hw_0200729c, .-native_main_hw_0200729c
