.section .text
.arm
.global native_main_hw_020253d8
.type native_main_hw_020253d8, @function
native_main_hw_020253d8:
    mov r3, #0xff000000
    cmp r3, r0, lsl #0x1
    cmphs r3, r1, lsl #0x1
    blo .L_02025428
    cmp r0, #0x0
    bicmi r0, r0, #0x80000000
    rsbmi r0, r0, #0x0
    cmp r1, #0x0
    bicmi r1, r1, #0x80000000
    rsbmi r1, r1, #0x0
    cmp r0, r1
    movle r0, #0x1
    movgt r0, #0x0
    mrs ip, cpsr
    orrgt ip, ip, #0x20000000
    bicgt ip, ip, #0x40000000
    bicle ip, ip, #0x20000000
    orrle ip, ip, #0x40000000
    msr cpsr_f, ip
    bx lr
.L_02025428:
    mov r0, #0x0
    mrs ip, cpsr
    bic ip, ip, #0x40000000
    orr ip, ip, #0x20000000
    msr cpsr_f, ip
    bx lr
.size native_main_hw_020253d8, .-native_main_hw_020253d8
