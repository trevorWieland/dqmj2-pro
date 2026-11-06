.section .text
.arm
.global native_main_hw_0202549c
.type native_main_hw_0202549c, @function
native_main_hw_0202549c:
    mov r3, #0xff000000
    cmp r3, r0, lsl #0x1
    blo .L_020254f0
    cmp r3, r1, lsl #0x1
    blo .L_020254f0
    orr r3, r0, r1
    movs r3, r3, lsl #0x1
    moveq r0, #0x1
    bne .L_020254d0
    mrs ip, cpsr
    orr ip, ip, #0x40000000
    msr cpsr_f, ip
    bx lr
.L_020254d0:
    cmp r0, r1
    moveq r0, #0x1
    movne r0, #0x0
    mrs ip, cpsr
    orreq ip, ip, #0x40000000
    bicne ip, ip, #0x40000000
    msr cpsr_f, ip
    bx lr
.L_020254f0:
    mov r0, #0x0
    mrs ip, cpsr
    bic ip, ip, #0x40000000
    msr cpsr_f, ip
    bx lr
.size native_main_hw_0202549c, .-native_main_hw_0202549c
