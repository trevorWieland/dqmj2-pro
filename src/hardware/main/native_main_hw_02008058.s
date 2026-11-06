.section .text
.arm
.global native_main_hw_02008058
.type native_main_hw_02008058, @function
native_main_hw_02008058:
    mrs r0, cpsr
    and r0, r0, #0x1f
    bx lr
.size native_main_hw_02008058, .-native_main_hw_02008058
