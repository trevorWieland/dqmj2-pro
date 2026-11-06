.extern native_data_027e0000
.extern native_fn_01ff82b4
.text
.arm
.global native_itcm_01ff81e8
.type native_itcm_01ff81e8, @function
native_itcm_01ff81e8:
    mov ip, #0x4000000
    str ip, [ip, #0x208]
    ldr r1, local_01ff8294
    add r1, r1, #0x3fc0
    add r1, r1, #0x3c
    mov r0, #0x0
    str r0, [r1, #0x0]
    ldr r1, local_01ff8298
local_01ff8208:
    ldrh r0, [r1, #0x0]
    and r0, r0, #0xf
    cmp r0, #0x1
    bne local_01ff8208
    mov r0, #0x100
    strh r0, [r1, #0x0]
    mov r0, #0x0
    ldr r3, local_01ff829c
    ldr r4, [r3, #0x0]
    ldr r1, local_01ff82a0
    mov r2, #0x80
    bl native_fn_01ff82b4
    str r4, [r3, #0x0]
    ldr r1, local_01ff82a4
    mov r2, #0x18
    bl native_fn_01ff82b4
    ldr r1, local_01ff82a8
    strh r0, [r1, #0x0]
    ldr r1, local_01ff82ac
    mov r2, #0x64
    bl native_fn_01ff82b4
    ldr r1, local_01ff8298
local_01ff8260:
    ldrh r0, [r1, #0x0]
    and r0, r0, #0xf
    cmp r0, #0x1
    beq local_01ff8260
    mov r0, #0x0
    strh r0, [r1, #0x0]
    ldr r3, local_01ff82b0
    ldr ip, [r3, #0x24]
    mov lr, ip
    ldr r11, local_01ff82a4
    ldmia r11, {r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10}
    mov r11, #0x0
    bx ip
local_01ff8294: .word native_data_027e0000
local_01ff8298: .word 0x4000180
local_01ff829c: .word 0x27ffd9c
local_01ff82a0: .word 0x27ffd80
local_01ff82a4: .word 0x27fff80
local_01ff82a8: .word 0x27fff98
local_01ff82ac: .word 0x27fff9c
local_01ff82b0: .word 0x27ffe00
.size native_itcm_01ff81e8, .-native_itcm_01ff81e8
