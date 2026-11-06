.section .text
.arm
.global native_arm7_wram_hw_037fdd58
.type native_arm7_wram_hw_037fdd58, @function
native_arm7_wram_hw_037fdd58:
    mrs r0, cpsr
    and r0, r0, #0x1f
    bx lr
.size native_arm7_wram_hw_037fdd58, .-native_arm7_wram_hw_037fdd58
