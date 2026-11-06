.section .text
.thumb
.global native_arm7_wram_hw_03803804
.type native_arm7_wram_hw_03803804, @function
native_arm7_wram_hw_03803804:
    swi 0xe
    bx lr
.size native_arm7_wram_hw_03803804, .-native_arm7_wram_hw_03803804
