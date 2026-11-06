.section .text
.arm
.global native_arm7_boot_hw_02380118
.type native_arm7_boot_hw_02380118, @function
native_arm7_boot_hw_02380118:
local_02380118:
    ldr r0, local_02380184
local_0238011c:
    ldr r1, [r0]
local_02380120:
    ldr r2, [r0, #4]
local_02380124:
    ldr r3, [r0, #8]
local_02380128:
    cmp r1, r2
local_0238012c:
    beq local_02380180
local_02380130:
    ldr r4, [r1], #4
local_02380134:
    ldr r5, [r1], #4
local_02380138:
    add r6, r4, r5
local_0238013c:
    cmp r4, r6
local_02380140:
    bmi local_02380148
local_02380144:
    b local_0238014c
local_02380148:
    ldr r7, [r3], #4
local_0238014c:
    bmi local_02380154
local_02380150:
    b local_02380158
local_02380154:
    str r7, [r4], #4
local_02380158:
    bmi local_0238013c
local_0238015c:
    ldr r5, [r1], #4
local_02380160:
    add r6, r4, r5
local_02380164:
    mov r7, #0
local_02380168:
    cmp r4, r6
local_0238016c:
    blo local_02380174
local_02380170:
    b local_02380178
local_02380174:
    str r7, [r4], #4
local_02380178:
    blo local_02380168
local_0238017c:
    beq local_02380128
local_02380180:
    b local_02380188
local_02380184: .word 0x2380204
local_02380188:
    bx lr
.size native_arm7_boot_hw_02380118, .-native_arm7_boot_hw_02380118
