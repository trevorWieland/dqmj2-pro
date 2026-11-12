/* ov006 row 0x021f96e0: 496 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x1e4 -> native_data_0221c0e4 (image word 0x0221c0e4)
 *   pool +0x1e8 -> native_fn_021f9938+1 (image word 0x021f9939)
 *   pool +0x1ec -> constant 0xc1fffcff (image word 0xc1fffcff)
 *   branch +0x0a -> +0x12
 *   branch +0x0c -> +0x10
 *   branch +0x0e -> +0x1e0
 *   branch +0x10 -> +0x132
 *   branch +0x16 -> +0x1a
 *   branch +0x18 -> +0x132
 *   branch +0x38 -> +0x40
 *   branch +0x3e -> +0xb2
 *   branch +0x58 -> +0x5e
 *   branch +0x7e -> +0x8c
 *   branch +0x84 -> +0x8c
 *   branch +0x98 -> +0x1d8
 *   branch +0xa2 -> +0xb2
 *   branch +0xb0 -> +0xb4
 *   branch +0xb2 -> +0x1d8
 *   branch +0xca -> +0x1d8
 *   branch +0xe8 -> +0xfa
 *   branch +0xf8 -> +0x108
 *   branch +0x13a -> +0x146
 *   branch +0x144 -> +0x1d8
 *   branch +0x160 -> +0x166
 *   branch +0x164 -> +0x1a0
 *   branch +0x16c -> +0x18c
 *   branch +0x17a -> +0x1a0
 *   branch +0x184 -> +0x1a0
 *   branch +0x18a -> +0x1a0
 *   branch +0x19a -> +0x1a0
 *   branch +0x1ae -> +0x1b8
 *   branch +0x1b6 -> +0x1be
 *   branch +0x1c6 -> +0x1d8
 *   branch +0x1d0 -> +0x1d8
 *   test +0x08 cmp r4, #0x0
 *   test +0x14 cmp r0, #0x3
 *   test +0x36 cmp r0, #0x0
 *   test +0x3c cmp r0, #0x0
 *   test +0x56 cmp r1, #0x0
 *   test +0x7c cmp r0, #0x0
 *   test +0x82 cmp r0, #0x0
 *   test +0xa0 cmp r1, #0x3
 *   test +0xae cmp r0, #0x0
 *   test +0xe6 cmp r0, #0x0
 *   test +0x138 cmp r0, #0x3
 *   test +0x142 cmp r0, #0x0
 *   test +0x15e cmp r2, #0x0
 *   test +0x16a cmp r0, #0x0
 *   test +0x178 cmp r0, #0x0
 *   test +0x182 cmp r0, #0x3
 *   test +0x198 cmp r0, #0x3
 *   test +0x1ac cmp r0, #0x3
 *   test +0x1c4 cmp r0, #0x3
 *   test +0x1ce cmp r0, #0x0
 *   15 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f96e0; the literal pool and
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

extern void native_fn_021f4250(void);
extern u8 native_data14_0221c0e4[];
extern void native_fn_021ff6d4(void);
extern void native_fn_02008d78(void);
extern void native_fn_021f4260(void);
extern void native_fn_021f4270(void);
extern void native_fn_021f4280(void);
extern void native_fn2_021f9938(void);
extern void native_fn_021f52cc(void);
extern void native_fn_021f9bf0(void);
extern void native_fn_021f9ac4(void);
extern void native_fn_021f9ba8(void);
extern void native_fn_021f98d0(void);
extern void native_fn_021f9a44(void);


asm u32 native_ov006_021f96e0 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    bl native_fn_021f4250
    add r4, r0, #0x0
    cmp r4, #0x0
    bgt ov006_021f96e0_L12
    bne ov006_021f96e0_L10
    b ov006_021f96e0_L1e0
ov006_021f96e0_L10:
    b ov006_021f96e0_L132
ov006_021f96e0_L12:
    sub r0, #0x10
    cmp r0, #0x3
    bls ov006_021f96e0_L1a
    b ov006_021f96e0_L132
ov006_021f96e0_L1a:
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    lsl r0, r1, #0
    lsl r2, r6, #0x1
    lsl r4, r4, #0x2
    lsl r2, r7, #0x2
    pop {r3, r4, r5, r6, r7, pc}
    ldr r0, =native_data14_0221c0e4
    ldr r1, [r0, #0]
    ldrb r0, [r1, #0x14]
    cmp r0, #0x0
    bne ov006_021f96e0_L40
    ldrb r0, [r1, #0xa]
    cmp r0, #0x0
    beq ov006_021f96e0_Lb2
ov006_021f96e0_L40:
    mov r0, #0x3
    bl native_fn_021ff6d4
    ldr r0, =native_data14_0221c0e4
    ldr r0, [r0, #0]
    ldrb r2, [r0, #0x14]
    lsl r1, r2, #0x1
    add r1, r2, r1
    add r1, r1, #0x2
    add r1, r0, r1
    ldrb r1, [r1, #0x8]
    cmp r1, #0x0
    bne ov006_021f96e0_L5e
    sub r1, r2, #0x1
    strb r1, [r0, #0x14]
ov006_021f96e0_L5e:
    ldr r0, =native_data14_0221c0e4
    ldr r0, [r0, #0]
    ldrb r1, [r0, #0x14]
    add r2, r0, #0x0
    add r2, #0x8
    lsl r0, r1, #0x1
    add r0, r1, r0
    add r0, r2, r0
    mov r1, #0x0
    mov r2, #0x3
    blx native_fn_02008d78
    ldr r0, =native_data14_0221c0e4
    ldr r1, [r0, #0]
    ldrb r0, [r1, #0x14]
    cmp r0, #0x0
    bne ov006_021f96e0_L8c
    ldrb r0, [r1, #0xa]
    cmp r0, #0x0
    bne ov006_021f96e0_L8c
    mov r0, #0x0
    bl native_fn_021f4260
ov006_021f96e0_L8c:
    mov r0, #0x1
    bl native_fn_021f4270
    mov r0, #0x0
    bl native_fn_021f4280
    b ov006_021f96e0_L1d8
    ldr r0, =native_data14_0221c0e4
    ldr r2, [r0, #0]
    ldrb r1, [r2, #0x14]
    cmp r1, #0x3
    bhs ov006_021f96e0_Lb2
    lsl r0, r1, #0x1
    add r0, r1, r0
    add r0, r0, #0x2
    add r0, r2, r0
    ldrb r0, [r0, #0x8]
    cmp r0, #0x0
    bne ov006_021f96e0_Lb4
ov006_021f96e0_Lb2:
    b ov006_021f96e0_L1d8
ov006_021f96e0_Lb4:
    mov r0, #0x1
    bl native_fn_021ff6d4
    ldr r0, =native_data14_0221c0e4
    ldr r1, [r0, #0]
    ldrb r0, [r1, #0x14]
    add r0, r0, #0x1
    strb r0, [r1, #0x14]
    mov r0, #0x0
    bl native_fn_021f4280
    b ov006_021f96e0_L1d8
    ldr r0, =native_data14_0221c0e4
    mov r1, #0x0
    ldr r0, [r0, #0]
    strb r1, [r0, #0x15]
    mov r0, #0x7
    bl native_fn_021ff6d4
    ldr r0, =native_fn2_021f9938+1
    bl native_fn_021f52cc
    pop {r3, r4, r5, r6, r7, pc}
    bl native_fn_021f9bf0
    cmp r0, #0x0
    beq ov006_021f96e0_Lfa
    mov r0, #0x6
    bl native_fn_021ff6d4
    ldr r0, =native_data14_0221c0e4
    mov r1, #0x1
    ldr r0, [r0, #0]
    strb r1, [r0, #0x15]
    b ov006_021f96e0_L108
ov006_021f96e0_Lfa:
    ldr r0, =native_data14_0221c0e4
    mov r1, #0x2
    ldr r0, [r0, #0]
    strb r1, [r0, #0x15]
    mov r0, #0x9
    bl native_fn_021ff6d4
ov006_021f96e0_L108:
    ldr r0, =native_data14_0221c0e4
    mov r2, #0x3
    ldr r1, [r0, #0]
    strb r2, [r1, #0x14]
    ldr r0, [r0, #0]
    ldr r2, [r0, #0x4]
    ldr r0, =0xc1fffcff
    ldr r1, [r2, #0]
    and r1, r0
    mov r0, #0x2
    lsl r0, r0, #0x8
    orr r0, r1
    str r0, [r2, #0]
    bl native_fn_021f9ac4
    bl native_fn_021f9ba8
    ldr r0, =native_fn2_021f9938+1
    bl native_fn_021f52cc
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f96e0_L132:
    ldr r0, =native_data14_0221c0e4
    ldr r0, [r0, #0]
    ldrb r0, [r0, #0x14]
    cmp r0, #0x3
    bne ov006_021f96e0_L146
    mov r0, #0x1a
    bl native_fn_021f98d0
    cmp r0, #0x0
    bne ov006_021f96e0_L1d8
ov006_021f96e0_L146:
    mov r0, #0x1
    bl native_fn_021ff6d4
    ldr r7, =native_data14_0221c0e4
    ldr r0, [r7, #0]
    add r6, r0, #0x0
    ldrb r1, [r0, #0x14]
    add r6, #0x8
    lsl r0, r1, #0x1
    add r5, r1, r0
    add r3, r5, #0x2
    ldrb r2, [r6, r3]
    cmp r2, #0x0
    bne ov006_021f96e0_L166
    strb r4, [r6, r3]
    b ov006_021f96e0_L1a0
ov006_021f96e0_L166:
    add r1, r5, #0x1
    ldrb r0, [r6, r1]
    cmp r0, #0x0
    bne ov006_021f96e0_L18c
    strb r2, [r6, r1]
    mov r0, #0x1a
    strb r4, [r6, r3]
    bl native_fn_021f98d0
    cmp r0, #0x0
    beq ov006_021f96e0_L1a0
    add r0, r7, #0x0
    ldr r1, [r0, #0]
    ldrb r0, [r1, #0x14]
    cmp r0, #0x3
    bhs ov006_021f96e0_L1a0
    add r0, r0, #0x1
    strb r0, [r1, #0x14]
    b ov006_021f96e0_L1a0
ov006_021f96e0_L18c:
    strb r0, [r6, r5]
    ldrb r0, [r6, r3]
    strb r0, [r6, r1]
    strb r4, [r6, r3]
    ldr r1, [r7, #0]
    ldrb r0, [r1, #0x14]
    cmp r0, #0x3
    bhs ov006_021f96e0_L1a0
    add r0, r0, #0x1
    strb r0, [r1, #0x14]
ov006_021f96e0_L1a0:
    mov r0, #0x1
    bl native_fn_021f4260
    ldr r0, =native_data14_0221c0e4
    ldr r0, [r0, #0]
    ldrb r0, [r0, #0x14]
    cmp r0, #0x3
    bhs ov006_021f96e0_L1b8
    mov r0, #0x1
    bl native_fn_021f4280
    b ov006_021f96e0_L1be
ov006_021f96e0_L1b8:
    mov r0, #0x0
    bl native_fn_021f4280
ov006_021f96e0_L1be:
    ldr r0, =native_data14_0221c0e4
    ldr r0, [r0, #0]
    ldrb r0, [r0, #0x14]
    cmp r0, #0x3
    bne ov006_021f96e0_L1d8
    mov r0, #0x1a
    bl native_fn_021f98d0
    cmp r0, #0x0
    beq ov006_021f96e0_L1d8
    mov r0, #0x0
    bl native_fn_021f4270
ov006_021f96e0_L1d8:
    bl native_fn_021f9a44
    bl native_fn_021f9ac4
ov006_021f96e0_L1e0:
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
