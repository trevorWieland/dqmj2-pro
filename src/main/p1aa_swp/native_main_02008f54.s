.section .text
.arm
.global native_main_02008f54
.type native_main_02008f54, @function
native_main_02008f54:
local_02008f54:
    stmfd sp!, {r4, r5, r6, r7, lr}
local_02008f58:
    ldr r5, [r0], #4
local_02008f5c:
    mov r2, r5, lsr #8
local_02008f60:
    mov r7, #0
local_02008f64:
    tst r5, #0xf
local_02008f68:
    movne r7, #1
local_02008f6c:
    cmp r2, #0
local_02008f70:
    ble local_0200902c
local_02008f74:
    ldrb lr, [r0], #1
local_02008f78:
    mov r4, #8
local_02008f7c:
    subs r4, r4, #1
local_02008f80:
    blt local_02008f6c
local_02008f84:
    tst lr, #0x80
local_02008f88:
    bne local_02008fa0
local_02008f8c:
    ldrb r6, [r0], #1
local_02008f90:
    swpb r6, r6, [r1]
local_02008f94:
    add r1, r1, #1
local_02008f98:
    sub r2, r2, #1
local_02008f9c:
    b local_0200901c
local_02008fa0:
    ldrb r5, [r0]
local_02008fa4:
    cmp r7, #0
local_02008fa8:
    moveq r6, #3
local_02008fac:
    beq local_02008fe8
local_02008fb0:
    tst r5, #0xe0
local_02008fb4:
    movne r6, #1
local_02008fb8:
    bne local_02008fe8
local_02008fbc:
    add r0, r0, #1
local_02008fc0:
    and r6, r5, #0xf
local_02008fc4:
    mov r6, r6, lsl #4
local_02008fc8:
    tst r5, #0x10
local_02008fcc:
    beq local_02008fe0
local_02008fd0:
    mov r6, r6, lsl #8
local_02008fd4:
    ldrb r5, [r0], #1
local_02008fd8:
    add r6, r6, r5, lsl #4
local_02008fdc:
    add r6, r6, #0x100
local_02008fe0:
    add r6, r6, #0x11
local_02008fe4:
    ldrb r5, [r0]
local_02008fe8:
    add r3, r6, r5, asr #4
local_02008fec:
    add r0, r0, #1
local_02008ff0:
    and r5, r5, #0xf
local_02008ff4:
    mov ip, r5, lsl #8
local_02008ff8:
    ldrb r6, [r0], #1
local_02008ffc:
    orr r5, r6, ip
local_02009000:
    add ip, r5, #1
local_02009004:
    sub r2, r2, r3
local_02009008:
    ldrb r5, [r1, -ip]
local_0200900c:
    swpb r5, r5, [r1]
local_02009010:
    add r1, r1, #1
local_02009014:
    subs r3, r3, #1
local_02009018:
    bgt local_02009008
local_0200901c:
    cmp r2, #0
local_02009020:
    movgt lr, lr, lsl #1
local_02009024:
    bgt local_02008f7c
local_02009028:
    b local_02008f6c
local_0200902c:
    ldmfd sp!, {r4, r5, r6, r7, lr}
local_02009030:
    bx lr
.size native_main_02008f54, .-native_main_02008f54
