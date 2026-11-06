.section .text
.arm
.global native_main_hw_02025504
.type native_main_hw_02025504, @function
native_main_hw_02025504:
    mov r3, #0xff000000
    cmp r3, r0, lsl #0x1
    blo .L_02025558
    cmp r3, r1, lsl #0x1
    blo .L_02025558
    orr r3, r0, r1
    movs r3, r3, lsl #0x1
    moveq r0, #0x0
    bne .L_02025538
    mrs ip, cpsr
    orr ip, ip, #0x40000000
    msr cpsr_f, ip
    bx lr
.L_02025538:
    cmp r0, r1
    movne r0, #0x1
    moveq r0, #0x0
    mrs ip, cpsr
    bicne ip, ip, #0x40000000
    orreq ip, ip, #0x40000000
    msr cpsr_f, ip
    bx lr
.L_02025558:
    mov r0, #0x1
    mrs ip, cpsr
    bic ip, ip, #0x40000000
    msr cpsr_f, ip
    bx lr
.size native_main_hw_02025504, .-native_main_hw_02025504
