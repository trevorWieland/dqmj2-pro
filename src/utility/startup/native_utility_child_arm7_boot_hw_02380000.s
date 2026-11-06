.extern native_utility_child_arm7_boot_params_02380198
.extern native_utility_child_arm7_thumb_037f83a1
.extern native_utility_child_arm7_arm_037fb934
.extern native_utility_child_arm7_boot_hw_02380100
.extern native_utility_child_arm7_boot_hw_0238015c
.section .text
.arm
.global native_utility_child_arm7_boot_hw_02380000
.type native_utility_child_arm7_boot_hw_02380000, @function
native_utility_child_arm7_boot_hw_02380000:
local_02380000:
    mov ip, #0x4000000
local_02380004:
    str ip, [ip, #0x208]
local_02380008:
    ldr r1, local_023800cc
local_0238000c:
    mov r0, #0x3800000
local_02380010:
    cmp r0, r1
local_02380014:
    movpl r1, r0
local_02380018:
    ldr r2, local_023800d0
local_0238001c:
    mov r0, #0
local_02380020:
    cmp r1, r2
local_02380024:
    stmltia r1!, {r0}
local_02380028:
    blt local_02380020
local_0238002c:
    mov r0, #0x13
local_02380030:
    msr cpsr_c, r0
local_02380034:
    ldr sp, local_023800d4
local_02380038:
    mov r0, #0x12
local_0238003c:
    msr cpsr_c, r0
local_02380040:
    ldr r0, local_023800d8
local_02380044:
    mov sp, r0
local_02380048:
    ldr r1, local_023800dc
local_0238004c:
    sub r1, r0, r1
local_02380050:
    mov r0, #0x1f
local_02380054:
    msr cpsr_fsxc, r0
local_02380058:
    sub sp, r1, #4
local_0238005c:
    ldr r0, local_023800e0
local_02380060:
    ldr r1, local_023800e4
local_02380064:
    add r2, r1, #0x160
local_02380068:
    ldr r3, [r0], #4
local_0238006c:
    str r3, [r1], #4
local_02380070:
    cmp r1, r2
local_02380074:
    bmi local_02380068
local_02380078:
    ldr r0, local_023800e8
local_0238007c:
    add r2, r1, #0x20
local_02380080:
    ldr r3, [r0], #4
local_02380084:
    str r3, [r1], #4
local_02380088:
    cmp r1, r2
local_0238008c:
    bmi local_02380080
local_02380090:
    bl native_utility_child_arm7_boot_hw_02380100
local_02380094:
    ldr r0, local_023800ec
local_02380098:
    ldr r1, [r0, #0xc]
local_0238009c:
    ldr r2, [r0, #0x10]
local_023800a0:
    mov r0, #0
local_023800a4:
    cmp r1, r2
local_023800a8:
    strlo r0, [r1], #4
local_023800ac:
    blo local_023800a4
local_023800b0:
    bl native_utility_child_arm7_boot_hw_0238015c
local_023800b4:
    ldr r1, local_023800f0
local_023800b8:
    ldr r0, local_023800f4
local_023800bc:
    str r0, [r1]
local_023800c0:
    ldr r1, local_023800f8
local_023800c4:
    ldr lr, local_023800fc
local_023800c8:
    bx r1
local_023800cc: .word 0x23801b0
local_023800d0: .word 0x380ff00
local_023800d4: .word 0x380ffc0
local_023800d8: .word 0x380ff80
local_023800dc: .word 0x400
local_023800e0: .word 0x23fe940
local_023800e4: .word 0x27ffa80
local_023800e8: .word 0x23fe904
local_023800ec: .word native_utility_child_arm7_boot_params_02380198
local_023800f0: .word 0x380fffc
local_023800f4: .word native_utility_child_arm7_arm_037fb934
local_023800f8: .word native_utility_child_arm7_thumb_037f83a1
local_023800fc: .word 0xffff0000
.size native_utility_child_arm7_boot_hw_02380000, .-native_utility_child_arm7_boot_hw_02380000
