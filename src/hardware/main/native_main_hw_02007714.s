.section .text
.arm
.global native_main_hw_02007714
.type native_main_hw_02007714, @function
native_main_hw_02007714:
    mrc p15, 0, r0, c9, c1, 0
    ldr r1, .L_02007724
    and r0, r0, r1
    bx lr
.L_02007724: .word 0xfffff000
.size native_main_hw_02007714, .-native_main_hw_02007714
