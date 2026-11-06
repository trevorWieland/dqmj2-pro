.section .text
.arm
.global native_main_hw_02007748
.type native_main_hw_02007748, @function
native_main_hw_02007748:
    mrc p15, 0, r2, c5, c0, 2
    bic r2, r2, r0
    orr r2, r2, r1
    mcr p15, 0, r2, c5, c0, 2
    bx lr
.size native_main_hw_02007748, .-native_main_hw_02007748
