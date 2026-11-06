.extern native_utility_child_arm7_boot_params_02380198
.section .text
.arm
.global native_utility_child_arm7_boot_hw_02380100
.type native_utility_child_arm7_boot_hw_02380100, @function
native_utility_child_arm7_boot_hw_02380100:
local_02380100:
    ldr r0, local_02380154
local_02380104:
    ldr r1, [r0]
local_02380108:
    ldr r2, [r0, #4]
local_0238010c:
    ldr r3, [r0, #8]
local_02380110:
    cmp r1, r2
local_02380114:
    beq local_02380150
local_02380118:
    ldr r4, [r1], #4
local_0238011c:
    ldr r5, [r1], #4
local_02380120:
    add r6, r4, r5
local_02380124:
    cmp r4, r6
local_02380128:
    ldrmi r7, [r3], #4
local_0238012c:
    strmi r7, [r4], #4
local_02380130:
    bmi local_02380124
local_02380134:
    ldr r5, [r1], #4
local_02380138:
    add r6, r4, r5
local_0238013c:
    mov r7, #0
local_02380140:
    cmp r4, r6
local_02380144:
    strlo r7, [r4], #4
local_02380148:
    blo local_02380140
local_0238014c:
    beq local_02380110
local_02380150:
    b local_02380158
local_02380154: .word native_utility_child_arm7_boot_params_02380198
local_02380158:
    bx lr
.size native_utility_child_arm7_boot_hw_02380100, .-native_utility_child_arm7_boot_hw_02380100
