.extern native_utility_child_arm9_data_027e0000
.extern native_utility_child_arm9_itcm_hw_01ff8058
.text
.arm
.global native_utility_child_arm9_itcm_hw_01ff8000
.type native_utility_child_arm9_itcm_hw_01ff8000, @function
native_utility_child_arm9_itcm_hw_01ff8000:
    stmdb sp!, {lr}
    mov ip, #0x4000000
    add ip, ip, #0x210
    ldr r1, [ip, #-0x8]
    cmp r1, #0x0
    ldmeqia sp!, {pc}
    ldmia ip, {r1, r2}
    ands r1, r1, r2
    ldmeqia sp!, {pc}
    mov r3, #0x80000000
local_01ff8028:
    clz r0, r1
    bics r1, r1, r3, lsr r0
    bne local_01ff8028
    mov r1, r3, lsr r0
    str r1, [ip, #0x4]
    rsbs r0, r0, #0x1f
    ldr r1, local_01ff8050
    ldr r0, [r1, r0, lsl #0x2]
    ldr lr, local_01ff8054
    bx r0
local_01ff8050: .word native_utility_child_arm9_data_027e0000
local_01ff8054: .word native_utility_child_arm9_itcm_hw_01ff8058
.size native_utility_child_arm9_itcm_hw_01ff8000, .-native_utility_child_arm9_itcm_hw_01ff8000
