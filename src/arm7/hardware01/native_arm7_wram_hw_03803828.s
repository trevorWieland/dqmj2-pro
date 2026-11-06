.section .text
.thumb
.global native_arm7_wram_hw_03803828
.type native_arm7_wram_hw_03803828, @function
native_arm7_wram_hw_03803828:
    swi 0x1b
    bx lr
.size native_arm7_wram_hw_03803828, .-native_arm7_wram_hw_03803828
