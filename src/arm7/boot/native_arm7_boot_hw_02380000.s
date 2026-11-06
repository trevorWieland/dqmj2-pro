.extern native_arm7_boot_hw_02380118
.extern native_arm7_boot_hw_0238018c
.section .text
.arm
.global native_arm7_boot_hw_02380000
.type native_arm7_boot_hw_02380000, @function
native_arm7_boot_hw_02380000:
local_02380000:
    mov ip, #0x4000000
local_02380004:
    str ip, [ip, #0x208]
local_02380008:
    ldr r1, local_023800e4
local_0238000c:
    mov r0, #0x3800000
local_02380010:
    cmp r0, r1
local_02380014:
    bpl local_0238001c
local_02380018:
    b local_02380020
local_0238001c:
    mov r1, r0
local_02380020:
    ldr r2, local_023800e8
local_02380024:
    mov r0, #0
local_02380028:
    cmp r1, r2
local_0238002c:
    blt local_02380034
local_02380030:
    b local_02380038
local_02380034:
    stmia r1!, {r0}
local_02380038:
    blt local_02380028
local_0238003c:
    mov r0, #0x13
local_02380040:
    msr cpsr_c, r0
local_02380044:
    ldr sp, local_023800ec
local_02380048:
    mov r0, #0x12
local_0238004c:
    msr cpsr_c, r0
local_02380050:
    ldr r0, local_023800f0
local_02380054:
    mov sp, r0
local_02380058:
    ldr r1, local_023800f4
local_0238005c:
    sub r1, r0, r1
local_02380060:
    mov r0, #0x1f
local_02380064:
    msr cpsr_fsxc, r0
local_02380068:
    sub sp, r1, #4
local_0238006c:
    ldr r0, local_023800f8
local_02380070:
    ldr r1, local_023800fc
local_02380074:
    add r2, r1, #0x160
local_02380078:
    ldr r3, [r0], #4
local_0238007c:
    str r3, [r1], #4
local_02380080:
    cmp r1, r2
local_02380084:
    bmi local_02380078
local_02380088:
    ldr r0, local_02380100
local_0238008c:
    add r2, r1, #0x20
local_02380090:
    ldr r3, [r0], #4
local_02380094:
    str r3, [r1], #4
local_02380098:
    cmp r1, r2
local_0238009c:
    bmi local_02380090
local_023800a0:
    bl native_arm7_boot_hw_02380118
local_023800a4:
    ldr r0, local_02380104
local_023800a8:
    ldr r1, [r0, #0xc]
local_023800ac:
    ldr r2, [r0, #0x10]
local_023800b0:
    mov r0, #0
local_023800b4:
    cmp r1, r2
local_023800b8:
    blo local_023800c0
local_023800bc:
    b local_023800c4
local_023800c0:
    str r0, [r1], #4
local_023800c4:
    blo local_023800b4
local_023800c8:
    bl native_arm7_boot_hw_0238018c
local_023800cc:
    ldr r1, local_02380108
local_023800d0:
    ldr r0, local_0238010c
local_023800d4:
    str r0, [r1]
local_023800d8:
    ldr r1, local_02380110
local_023800dc:
    ldr lr, local_02380114
local_023800e0:
    bx r1
local_023800e4: .word 0x238021c
local_023800e8: .word 0x380ff00
local_023800ec: .word 0x380ffc0
local_023800f0: .word 0x380ff80
local_023800f4: .word 0x400
local_023800f8: .word 0x23fe940
local_023800fc: .word 0x27ffa80
local_02380100: .word 0x23fe904
local_02380104: .word 0x2380204
local_02380108: .word 0x380fffc
local_0238010c: .word 0x37fb488
local_02380110: .word 0x37f8000
local_02380114: .word 0xffff0000
.size native_arm7_boot_hw_02380000, .-native_arm7_boot_hw_02380000
