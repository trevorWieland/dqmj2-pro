.section .text
.arm
.global native_main_hw_02007338
.type native_main_hw_02007338, @function
native_main_hw_02007338:
    mov r0, #0x0
    mcr p15, 0, r0, c7, c5, 0
    bx lr
.size native_main_hw_02007338, .-native_main_hw_02007338
