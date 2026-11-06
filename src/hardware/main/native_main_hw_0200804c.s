.section .text
.arm
.global native_main_hw_0200804c
.type native_main_hw_0200804c, @function
native_main_hw_0200804c:
    mrs r0, cpsr
    and r0, r0, #0x80
    bx lr
.size native_main_hw_0200804c, .-native_main_hw_0200804c
