/* ov006 row 0x021f5568: 368 bytes.
 *
 * What it does: Writes 2 blocks of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x15c -> native_data_0221c090 (image word 0x0221c090)
 *   pool +0x160 -> constant 0x0001e2a0 (image word 0x0001e2a0)
 *   pool +0x164 -> constant 0x0001e280 (image word 0x0001e280)
 *   pool +0x168 -> constant 0x0001e298 (image word 0x0001e298)
 *   pool +0x16c -> native_data_0221c090 (image word 0x0221c090)
 *   branch +0x12 -> +0x2c
 *   branch +0x1a -> +0x2c
 *   branch +0x22 -> +0x26
 *   branch +0x24 -> +0x15a
 *   branch +0x3c -> +0x86
 *   branch +0x3e -> +0x10a
 *   branch +0x42 -> +0x80
 *   branch +0x46 -> +0x4a
 *   branch +0x48 -> +0x15a
 *   branch +0x82 -> +0xe8
 *   branch +0x88 -> +0x8e
 *   branch +0x8a -> +0x10a
 *   branch +0x90 -> +0x14c
 *   branch +0x98 -> +0x15a
 *   branch +0xb8 -> +0xc0
 *   branch +0xcc -> +0x15a
 *   branch +0xd8 -> +0xe0
 *   branch +0xee -> +0x15a
 *   branch +0xfa -> +0x102
 *   branch +0x110 -> +0x15a
 *   branch +0x11c -> +0x124
 *   branch +0x130 -> +0x15a
 *   branch +0x13c -> +0x144
 *   test +0x10 cmp r0, #0x0
 *   test +0x18 cmp r0, #0x0
 *   test +0x20 cmp r1, #0x0
 *   test +0x3a cmp r1, #0x1a
 *   test +0x40 cmp r1, #0x14
 *   test +0x44 cmp r1, #0x0
 *   test +0x80 cmp r1, #0x17
 *   test +0x86 cmp r1, #0x1d
 *   test +0x8e cmp r1, #0x22
 *   test +0x96 cmp r0, #0x0
 *   test +0xb6 cmp r1, #0x0
 *   test +0xca cmp r0, #0x0
 *   test +0xd6 cmp r1, #0x0
 *   test +0xec cmp r0, #0x0
 *   test +0xf8 cmp r1, #0x0
 *   test +0x10e cmp r0, #0x0
 *   test +0x11a cmp r1, #0x0
 *   test +0x12e cmp r0, #0x0
 *   test +0x13a cmp r1, #0x0
 *   5 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f5568; the literal pool and
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

extern void native_fn_02202018(void);
extern u8 native_data7_0221c090[];
extern void native_fn_022022ac(void);
extern void native_fn_022022e4(void);
extern void native_fn_02008bf8(void);
extern void native_fn_02204974(void);
extern u8 native_data8_0221c090[];
extern void native_fn_02203c20(void);


asm u32 native_ov006_021f5568 (register u32 a0)
{
    push {r3, r4, r5, lr}
    add r4, r0, #0x0
    bl native_fn_02202018
    ldr r0, =native_data7_0221c090
    ldr r1, =0x0001e2a0
    ldr r2, [r0, #0]
    ldrb r0, [r2, r1]
    cmp r0, #0x0
    beq ov006_021f5568_L2c
    add r0, r1, #0x1
    ldrb r0, [r2, r0]
    cmp r0, #0x0
    bne ov006_021f5568_L2c
    sub r1, #0x8
    ldr r1, [r2, r1]
    cmp r1, #0x0
    bne ov006_021f5568_L26
    b ov006_021f5568_L15a
ov006_021f5568_L26:
    mov r0, #0x0
    blx r1
    pop {r3, r4, r5, pc}
ov006_021f5568_L2c:
    add r0, sp, #0x0
    add r0, #0x1
    add r1, sp, #0x0
    bl native_fn_022022ac
    add r0, sp, #0x0
    ldrb r1, [r0, #0x1]
    cmp r1, #0x1a
    bgt ov006_021f5568_L86
    bge ov006_021f5568_L10a
    cmp r1, #0x14
    bgt ov006_021f5568_L80
    cmp r1, #0x0
    bge ov006_021f5568_L4a
    b ov006_021f5568_L15a
ov006_021f5568_L4a:
    add r2, r1, r1
    add r2, pc
    ldrh r2, [r2, #0x6]
    lsl r2, r2, #0x10
    asr r2, r2, #0x10
    add pc, r2
    lsl r2, r0, #0x4
    lsl r2, r0, #0x4
    lsl r2, r0, #0x4
    lsl r2, r0, #0x4
    lsl r2, r0, #0x4
    lsl r4, r7, #0
    lsl r2, r0, #0x4
    lsl r2, r0, #0x4
    lsl r2, r0, #0x4
    lsl r2, r0, #0x4
    lsl r2, r0, #0x4
    lsl r2, r0, #0x4
    lsl r4, r2, #0x3
    lsl r0, r6, #0x1
    lsl r2, r0, #0x4
    lsl r2, r0, #0x4
    lsl r2, r0, #0x4
    lsl r2, r0, #0x4
    lsl r2, r0, #0x4
    lsl r2, r0, #0x4
    lsl r0, r2, #0x2
ov006_021f5568_L80:
    cmp r1, #0x17
    beq ov006_021f5568_Le8
    pop {r3, r4, r5, pc}
ov006_021f5568_L86:
    cmp r1, #0x1d
    bgt ov006_021f5568_L8e
    beq ov006_021f5568_L10a
    pop {r3, r4, r5, pc}
ov006_021f5568_L8e:
    cmp r1, #0x22
    beq ov006_021f5568_L14c
    pop {r3, r4, r5, pc}
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq ov006_021f5568_L15a
    ldr r0, =native_data7_0221c090
    ldr r4, =0x0001e280
    ldr r5, [r0, #0]
    bl native_fn_022022e4
    add r1, r5, r4
    mov r2, #0x16
    blx native_fn_02008bf8
    ldr r0, =native_data7_0221c090
    ldr r2, [r0, #0]
    add r0, r4, #0x0
    add r0, #0x18
    ldr r1, [r2, r0]
    cmp r1, #0x0
    beq ov006_021f5568_Lc0
    mov r0, #0x0
    blx r1
    pop {r3, r4, r5, pc}
ov006_021f5568_Lc0:
    mov r1, #0x1
    add r0, #0x8
    strb r1, [r2, r0]
    pop {r3, r4, r5, pc}
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq ov006_021f5568_L15a
    ldr r0, =native_data7_0221c090
    ldr r2, [r0, #0]
    ldr r0, =0x0001e298
    ldr r1, [r2, r0]
    cmp r1, #0x0
    beq ov006_021f5568_Le0
    mov r0, #0x1
    blx r1
    pop {r3, r4, r5, pc}
ov006_021f5568_Le0:
    mov r1, #0x1
    add r0, #0x8
    strb r1, [r2, r0]
    pop {r3, r4, r5, pc}
ov006_021f5568_Le8:
    add r0, sp, #0x0
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq ov006_021f5568_L15a
    ldr r0, =native_data7_0221c090
    ldr r2, [r0, #0]
    ldr r0, =0x0001e298
    ldr r1, [r2, r0]
    cmp r1, #0x0
    beq ov006_021f5568_L102
    mov r0, #0x3
    blx r1
    pop {r3, r4, r5, pc}
ov006_021f5568_L102:
    mov r1, #0x1
    add r0, #0x8
    strb r1, [r2, r0]
    pop {r3, r4, r5, pc}
ov006_021f5568_L10a:
    add r0, sp, #0x0
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq ov006_021f5568_L15a
    ldr r0, =native_data7_0221c090
    ldr r2, [r0, #0]
    ldr r0, =0x0001e298
    ldr r1, [r2, r0]
    cmp r1, #0x0
    beq ov006_021f5568_L124
    mov r0, #0x4
    blx r1
    pop {r3, r4, r5, pc}
ov006_021f5568_L124:
    mov r1, #0x1
    add r0, #0x8
    strb r1, [r2, r0]
    pop {r3, r4, r5, pc}
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq ov006_021f5568_L15a
    ldr r0, =native_data7_0221c090
    ldr r2, [r0, #0]
    ldr r0, =0x0001e298
    ldr r1, [r2, r0]
    cmp r1, #0x0
    beq ov006_021f5568_L144
    mov r0, #0x2
    blx r1
    pop {r3, r4, r5, pc}
ov006_021f5568_L144:
    mov r1, #0x1
    add r0, #0x8
    strb r1, [r2, r0]
    pop {r3, r4, r5, pc}
ov006_021f5568_L14c:
    mov r0, #0x0
    add r1, r4, #0x0
    bl native_fn_02204974
    ldr r0, =native_data8_0221c090
    bl native_fn_02203c20
ov006_021f5568_L15a:
    pop {r3, r4, r5, pc}
}
