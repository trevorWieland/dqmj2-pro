.section .text
.arm
.global native_arm7_wram_hw_037fdd14
.type native_arm7_wram_hw_037fdd14, @function
native_arm7_wram_hw_037fdd14:
    mrs r1, cpsr
    bic r2, r1, #0x80
    orr r2, r2, r0
    msr cpsr_c, r2
    and r0, r1, #0x80
    bx lr
.size native_arm7_wram_hw_037fdd14, .-native_arm7_wram_hw_037fdd14
