.section .text
.arm
.global native_itcm_01ff82b4
.type native_itcm_01ff82b4, @function
native_itcm_01ff82b4:
    add r12, r1, r2
local_clear_again:
    cmp r1, r12
    stmltia r1!, {r0}
    blt local_clear_again
    bx lr
.size native_itcm_01ff82b4, .-native_itcm_01ff82b4
