.section .text
.arm
.global native_main_hw_020072d0
.type native_main_hw_020072d0, @function
native_main_hw_020072d0:
    add r1, r1, r0
    bic r0, r0, #0x1f
.L_020072d8:
    mcr p15, 0, r0, c7, c6, 1
    add r0, r0, #0x20
    cmp r0, r1
    blt .L_020072d8
    bx lr
.size native_main_hw_020072d0, .-native_main_hw_020072d0
