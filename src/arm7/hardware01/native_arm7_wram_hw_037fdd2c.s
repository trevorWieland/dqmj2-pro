.section .text
.arm
.global native_arm7_wram_hw_037fdd2c
.type native_arm7_wram_hw_037fdd2c, @function
native_arm7_wram_hw_037fdd2c:
    mrs r0, cpsr
    orr r1, r0, #0xc0
    msr cpsr_c, r1
    and r0, r0, #0xc0
    bx lr
.size native_arm7_wram_hw_037fdd2c, .-native_arm7_wram_hw_037fdd2c
