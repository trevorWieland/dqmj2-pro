.section .text
.arm
.global native_arm7_wram_hw_037fc680
.type native_arm7_wram_hw_037fc680, @function
native_arm7_wram_hw_037fc680:
    mrs r1, cpsr
    bic r1, r1, #0x1f
    orr r1, r1, #0xd3
    msr cpsr_c, r1
    ldr r1, [r0], #4
    msr spsr_fsxc, r1
    ldr sp, [r0, #0x40]
    ldr lr, [r0, #0x3c]
    ldmia r0, {r0, r1, r2, r3, r4, r5, r6, r7, r8, sb, sl, fp, ip, sp, lr} ^
    mov r0, r0
    subs pc, lr, #4
.size native_arm7_wram_hw_037fc680, .-native_arm7_wram_hw_037fc680
