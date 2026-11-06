.section .text
.arm
.global native_arm7_wram_hw_037fdd00
.type native_arm7_wram_hw_037fdd00, @function
native_arm7_wram_hw_037fdd00:
    mrs r0, cpsr
    orr r1, r0, #0x80
    msr cpsr_c, r1
    and r0, r0, #0x80
    bx lr
.size native_arm7_wram_hw_037fdd00, .-native_arm7_wram_hw_037fdd00
