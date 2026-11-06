.section .text
.arm
.global native_arm7_wram_hw_037fdcec
.type native_arm7_wram_hw_037fdcec, @function
native_arm7_wram_hw_037fdcec:
    mrs r0, cpsr
    bic r1, r0, #0x80
    msr cpsr_c, r1
    and r0, r0, #0x80
    bx lr
.size native_arm7_wram_hw_037fdcec, .-native_arm7_wram_hw_037fdcec
