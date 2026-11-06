.section .text
.arm
.global native_main_hw_020072ec
.type native_main_hw_020072ec, @function
native_main_hw_020072ec:
    add r1, r1, r0
    bic r0, r0, #0x1f
.L_020072f4:
    mcr p15, 0, r0, c7, c10, 1
    add r0, r0, #0x20
    cmp r0, r1
    blt .L_020072f4
    bx lr
.size native_main_hw_020072ec, .-native_main_hw_020072ec
