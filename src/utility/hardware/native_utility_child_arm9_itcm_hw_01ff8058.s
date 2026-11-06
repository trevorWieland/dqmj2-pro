.extern native_utility_child_arm9_data_02029300
.extern native_utility_child_arm9_data_027e0060
.extern native_utility_child_arm9_fn_0200fb78
.extern native_utility_child_arm9_fn_0200fbb8
.text
.arm
.global native_utility_child_arm9_itcm_hw_01ff8058
.type native_utility_child_arm9_itcm_hw_01ff8058, @function
native_utility_child_arm9_itcm_hw_01ff8058:
    ldr ip, local_01ff81a4
    mov r3, #0x0
    ldr ip, [ip, #0x0]
    mov r2, #0x1
    cmp ip, #0x0
    beq local_01ff80a8
local_01ff8070:
    str r2, [ip, #0x64]
    str r3, [ip, #0x78]
    str r3, [ip, #0x7c]
    ldr r0, [ip, #0x80]
    str r3, [ip, #0x80]
    mov ip, r0
    cmp ip, #0x0
    bne local_01ff8070
    ldr ip, local_01ff81a4
    str r3, [ip, #0x0]
    str r3, [ip, #0x4]
    ldr ip, local_01ff81a8
    mov r1, #0x1
    strh r1, [ip, #0x0]
local_01ff80a8:
    ldr ip, local_01ff81a8
    ldrh r1, [ip, #0x0]
    cmp r1, #0x0
    ldreq pc, [sp], #0x4
    mov r1, #0x0
    strh r1, [ip, #0x0]
    mov r3, #0xd2
    msr cpsr_c, r3
    add r2, ip, #0x8
    ldr r1, [r2, #0x0]
local_01ff80d0:
    cmp r1, #0x0
    ldrneh r0, [r1, #0x64]
    cmpne r0, #0x1
    ldrne r1, [r1, #0x68]
    bne local_01ff80d0
    cmp r1, #0x0
    bne local_01ff80f8
local_01ff80ec:
    mov r3, #0x92
    msr cpsr_c, r3
    ldr pc, [sp], #0x4
local_01ff80f8:
    ldr r0, [ip, #0x4]
    cmp r1, r0
    beq local_01ff80ec
    ldr r3, [ip, #0xc]
    cmp r3, #0x0
    beq local_01ff8120
    stmdb sp!, {r0, r1, ip}
    mov lr, pc
    bx r3
    ldmia sp!, {r0, r1, ip}
local_01ff8120:
    str r1, [ip, #0x4]
    mrs r2, spsr
    str r2, [r0, #0x0]!
    stmdb sp!, {r0, r1}
    add r0, r0, #0x0
    add r0, r0, #0x48
    ldr r1, local_01ff81ac
    blx r1
    ldmia sp!, {r0, r1}
    ldmib sp!, {r2, r3}
    stmib r0!, {r2, r3}
    ldmib sp!, {r2, r3, ip, lr}
    stmib r0!, {r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, ip, sp, lr}^
    stmib r0!, {lr}
    mov r3, #0xd3
    msr cpsr_c, r3
    stmib r0!, {sp}
    stmdb sp!, {r1}
    add r0, r1, #0x0
    add r0, r0, #0x48
    ldr r1, local_01ff81b0
    blx r1
    ldmia sp!, {r1}
    ldr sp, [r1, #0x44]
    mov r3, #0xd2
    msr cpsr_c, r3
    ldr r2, [r1, #0x0]!
    msr spsr_fc, r2
    ldr lr, [r1, #0x40]
    ldmib r1!, {r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, ip, sp, lr}^
    mov r0, r0
    stmda sp!, {r0, r1, r2, r3, ip, lr}
    ldmia sp!, {pc}
local_01ff81a4: .word native_utility_child_arm9_data_027e0060
local_01ff81a8: .word native_utility_child_arm9_data_02029300
local_01ff81ac: .word native_utility_child_arm9_fn_0200fb78
local_01ff81b0: .word native_utility_child_arm9_fn_0200fbb8
.size native_utility_child_arm9_itcm_hw_01ff8058, .-native_utility_child_arm9_itcm_hw_01ff8058
