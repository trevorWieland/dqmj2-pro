/* ov006 row 0x021efd60: 468 bytes.
 *
 * What it does: Writes 13 blocks of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x1b8 -> constant 0x00000201 (image word 0x00000201)
 *   pool +0x1bc -> constant 0x0221ae24 (image word 0x0221ae24)
 *   pool +0x1c0 -> native_data3_0221ae50 (image word 0x0221ae50)
 *   pool +0x1c4 -> native_data2_0221ad24 (image word 0x0221ad24)
 *   pool +0x1c8 -> native_data3_0221ae88 (image word 0x0221ae88)
 *   pool +0x1cc -> constant 0x00000206 (image word 0x00000206)
 *   pool +0x1d0 -> constant 0x0221af20 (image word 0x0221af20)
 *   branch +0x3c -> +0x40
 *   branch +0x3e -> +0x1b0
 *   branch +0x48 -> +0xce
 *   branch +0x88 -> +0x19a
 *   branch +0xa4 -> +0x19a
 *   back edge +0xcc -> +0xc4
 *   branch +0xce -> +0x19a
 *   back edge +0xf6 -> +0xee
 *   branch +0xf8 -> +0x19a
 *   branch +0x114 -> +0x19a
 *   branch +0x132 -> +0x160
 *   branch +0x146 -> +0x19a
 *   back edge +0x15c -> +0x14a
 *   branch +0x15e -> +0x19a
 *   branch +0x174 -> +0x19a
 *   branch +0x1ac -> +0x1b0
 *   back edge +0x1ae -> +0x40
 *   test +0x46 cmp r1, #0x9
 *   test +0xca cmp r0, #0x4
 *   test +0xf4 cmp r1, #0x4
 *   test +0x130 cmp r0, #0x1
 *   test +0x144 cmp r0, #0x0
 *   test +0x15a cmp r6, r0
 *   13 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021efd60; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021ef8c8(void);
extern void native_fn_0201b19c(void);
extern u8 native_data3_0221ae50[];
extern u8 native_data2_0221ad24[];
extern u8 native_data3_0221ae88[];
extern void native_fn_0201b208(void);
extern void native_fn_021f1f40(void);


asm u32 native_ov006_021efd60 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x18
    add r1, r0, #0x0
    str r1, [sp, #0x4]
    add r1, #0x8
    str r1, [sp, #0x4]
    str r1, [sp, #0x14]
    mov r1, #0x0
    str r1, [sp]
    ldrh r1, [r0, #0]
    add r3, sp, #0xc
    asr r0, r1, #0x8
    lsl r0, r0, #0x18
    lsr r2, r0, #0x18
    mov r0, #0xff
    lsl r1, r1, #0x8
    lsl r0, r0, #0x8
    and r0, r1
    orr r0, r2
    lsl r0, r0, #0x10
    lsr r0, r0, #0x10
    str r0, [sp, #0x8]
    ldr r2, [sp, #0x4]
    ldr r1, [sp, #0x8]
    add r0, sp, #0x14
    add r1, r2, r1
    add r2, sp, #0x10
    bl native_fn_021ef8c8
    add r5, r0, #0x0
    bne ov006_021efd60_L40
    b ov006_021efd60_L1b0
ov006_021efd60_L40:
    ldr r2, [sp, #0x10]
    ldr r0, =0x00000201
    sub r1, r2, r0
    cmp r1, #0x9
    bhi ov006_021efd60_Lce
    add r1, r1, r1
    add r1, pc
    ldrh r1, [r1, #0x6]
    lsl r1, r1, #0x10
    asr r1, r1, #0x10
    add pc, r1
    lsl r2, r2, #0
    lsl r2, r6, #0
    lsl r6, r1, #0x1
    lsl r0, r7, #0x1
    lsl r2, r4, #0x2
    lsl r6, r7, #0x2
    lsl r6, r7, #0x2
    lsl r6, r7, #0x2
    lsl r6, r7, #0x2
    lsl r6, r3, #0x4
    ldr r3, =0x0221ae24
    mov r0, #0x0
    add r2, r3, #0x0
    add r1, r0, #0x0
    stmia r2!, {r0, r1}
    stmia r2!, {r0, r1}
    stmia r2!, {r0, r1}
    stmia r2!, {r0, r1}
    ldr r2, [sp, #0xc]
    add r0, r3, #0x0
    add r1, r5, #0x0
    blx native_fn_0201b19c
    mov r0, #0x1
    str r0, [sp]
    b ov006_021efd60_L19a
    ldrh r1, [r5, #0]
    asr r0, r1, #0x8
    lsl r0, r0, #0x18
    lsr r2, r0, #0x18
    mov r0, #0xff
    lsl r1, r1, #0x8
    lsl r0, r0, #0x8
    and r0, r1
    orr r0, r2
    lsl r0, r0, #0x10
    lsr r1, r0, #0x10
    ldr r0, =native_data3_0221ae50
    str r1, [r0, #0]
    b ov006_021efd60_L19a
    ldrh r3, [r5, #0]
    ldr r1, =native_data2_0221ad24
    mov r0, #0x0
    asr r2, r3, #0x8
    lsl r2, r2, #0x18
    lsr r4, r2, #0x18
    mov r2, #0xff
    lsl r3, r3, #0x8
    lsl r2, r2, #0x8
    and r2, r3
    orr r2, r4
    lsl r2, r2, #0x10
    lsr r3, r2, #0x10
    mov r2, #0x57
    lsl r2, r2, #0x2
ov006_021efd60_Lc4:
    add r0, r0, #0x1
    str r3, [r1, r2]
    add r1, #0x28
    cmp r0, #0x4
    blt ov006_021efd60_Lc4
ov006_021efd60_Lce:
    b ov006_021efd60_L19a
    ldrh r3, [r5, #0]
    ldr r0, =native_data2_0221ad24
    mov r1, #0x0
    asr r2, r3, #0x8
    lsl r2, r2, #0x18
    lsr r4, r2, #0x18
    mov r2, #0xff
    lsl r3, r3, #0x8
    lsl r2, r2, #0x8
    and r2, r3
    orr r2, r4
    lsl r2, r2, #0x10
    lsr r3, r2, #0x10
    mov r2, #0x16
    lsl r2, r2, #0x4
ov006_021efd60_Lee:
    add r1, r1, #0x1
    str r3, [r0, r2]
    add r0, #0x28
    cmp r1, #0x4
    blt ov006_021efd60_Lee
    b ov006_021efd60_L19a
    ldrh r1, [r5, #0]
    asr r0, r1, #0x8
    lsl r0, r0, #0x18
    lsr r2, r0, #0x18
    mov r0, #0xff
    lsl r1, r1, #0x8
    lsl r0, r0, #0x8
    and r0, r1
    orr r0, r2
    lsl r0, r0, #0x10
    lsr r1, r0, #0x10
    ldr r0, =native_data3_0221ae50
    str r1, [r0, #0x4]
    b ov006_021efd60_L19a
    add r0, r0, #0x5
    sub r2, r2, r0
    mov r0, #0x28
    mul r0, r2
    ldr r1, =native_data3_0221ae88
    mov r2, #0x20
    add r0, r1, r0
    mov r1, #0x0
    blx native_fn_0201b208
    ldr r0, =native_data3_0221ae50
    ldr r1, =0x00000206
    ldr r0, [r0, #0x30]
    cmp r0, #0x1
    bne ov006_021efd60_L160
    ldr r2, [sp, #0x10]
    ldr r0, =native_data3_0221ae88
    sub r2, r2, r1
    mov r1, #0x28
    mul r1, r2
    add r4, r0, r1
    ldr r0, [sp, #0xc]
    mov r6, #0x0
    cmp r0, #0x0
    ble ov006_021efd60_L19a
    add r7, r6, #0x0
ov006_021efd60_L14a:
    ldrsb r1, [r5, r7]
    add r0, r4, #0x0
    add r5, r5, #0x1
    bl native_fn_021f1f40
    add r4, r4, r0
    ldr r0, [sp, #0xc]
    add r6, r6, #0x1
    cmp r6, r0
    blt ov006_021efd60_L14a
    b ov006_021efd60_L19a
ov006_021efd60_L160:
    ldr r2, [sp, #0x10]
    ldr r0, =native_data3_0221ae88
    sub r2, r2, r1
    mov r1, #0x28
    mul r1, r2
    add r0, r0, r1
    ldr r2, [sp, #0xc]
    add r1, r5, #0x0
    blx native_fn_0201b19c
    b ov006_021efd60_L19a
    ldr r3, =0x0221af20
    mov r0, #0x0
    add r2, r3, #0x0
    add r1, r0, #0x0
    stmia r2!, {r0, r1}
    stmia r2!, {r0, r1}
    stmia r2!, {r0, r1}
    stmia r2!, {r0, r1}
    stmia r2!, {r0, r1}
    stmia r2!, {r0, r1}
    stmia r2!, {r0, r1}
    stmia r2!, {r0, r1}
    stmia r2!, {r0, r1}
    ldr r2, [sp, #0xc]
    add r0, r3, #0x0
    add r1, r5, #0x0
    blx native_fn_0201b19c
ov006_021efd60_L19a:
    ldr r2, [sp, #0x4]
    ldr r1, [sp, #0x8]
    add r0, sp, #0x14
    add r1, r2, r1
    add r2, sp, #0x10
    add r3, sp, #0xc
    bl native_fn_021ef8c8
    add r5, r0, #0x0
    beq ov006_021efd60_L1b0
    b ov006_021efd60_L40
ov006_021efd60_L1b0:
    ldr r0, [sp]
    add sp, #0x18
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
