.section .text
.arm
.global native_arm7_wram_hw_037fc64c
.type native_arm7_wram_hw_037fc64c, @function
native_arm7_wram_hw_037fc64c:
    add r1, r0, #0
    mrs r2, cpsr
    str r2, [r1], #4
    mov r0, #0xd3
    msr cpsr_c, r0
    str sp, [r1, #0x40]
    msr cpsr_c, r2
    mov r0, #1
    stmia r1, {r0, r1, r2, r3, r4, r5, r6, r7, r8, sb, sl, fp, ip, sp, lr}
    add r0, pc, #8
    str r0, [r1, #0x3c]
    mov r0, #0
    bx lr
.size native_arm7_wram_hw_037fc64c, .-native_arm7_wram_hw_037fc64c
