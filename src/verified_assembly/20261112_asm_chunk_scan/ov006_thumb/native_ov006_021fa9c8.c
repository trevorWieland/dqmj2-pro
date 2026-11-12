/* ov006 row 0x021fa9c8: 540 bytes.
 *
 * What it does: Moves 5-register chunks between two pointers with writeback block moves (one load, 2 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x1f0 -> native_data_0221c0ec (image word 0x0221c0ec)
 *   pool +0x1f4 -> native_data_0220ded0 (image word 0x0220ded0)
 *   pool +0x1f8 -> constant 0x0200494c (image word 0x0200494c)
 *   pool +0x1fc -> native_data_04000010 (image word 0x04000010)
 *   pool +0x200 -> native_fn_021f8d4c+1 (image word 0x021f8d4d)
 *   pool +0x204 -> native_fn_021f94ac+1 (image word 0x021f94ad)
 *   pool +0x208 -> native_fn_021fd660+1 (image word 0x021fd661)
 *   pool +0x20c -> native_fn_021fb93c+1 (image word 0x021fb93d)
 *   pool +0x210 -> native_fn_021fc870+1 (image word 0x021fc871)
 *   pool +0x214 -> native_fn_021fd11c+1 (image word 0x021fd11d)
 *   pool +0x218 -> native_data_0221c0f4 (image word 0x0221c0f4)
 *   branch +0x0a -> +0x16
 *   branch +0x14 -> +0x18
 *   branch +0x16 -> +0x1ee
 *   back edge +0x46 -> +0x36
 *   branch +0x50 -> +0x56
 *   branch +0x6e -> +0x74
 *   back edge +0x98 -> +0x88
 *   branch +0xd4 -> +0xd8
 *   branch +0xd6 -> +0x1e8
 *   branch +0x112 -> +0x1e8
 *   branch +0x118 -> +0x11c
 *   branch +0x132 -> +0x1e8
 *   branch +0x14e -> +0x17c
 *   branch +0x184 -> +0x192
 *   branch +0x1a8 -> +0x1e8
 *   branch +0x1b6 -> +0x1e8
 *   branch +0x1bc -> +0x1ce
 *   branch +0x1cc -> +0x1e8
 *   test +0x08 cmp r0, #0x0
 *   test +0x12 cmp r0, #0x0
 *   test +0x44 cmp r5, #0x7
 *   test +0x4e cmp r0, #0x0
 *   test +0x6c cmp r0, #0xc
 *   test +0x96 cmp r5, #0x2
 *   test +0xd2 cmp r0, #0xd
 *   test +0x116 cmp r0, #0x9
 *   test +0x14c cmp r0, #0x0
 *   test +0x182 cmp r0, #0x0
 *   test +0x1ba cmp r0, #0x0
 *   5 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fa9c8; the literal pool and
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

extern void native_fn_02203188(void);
extern u8 native_data8_0221c0ec[];
extern void native_fn_0220498c(void);
extern void native_fn_022043a4(void);
extern void native_fn_021fe690(void);
extern void native_fn_02203690(void);
extern void native_fn_021f2a4c(void);
extern void native_fn_021f2774(void);
extern void native_fn_021fe4dc(void);
extern void native_fn_02202b24(void);
extern u8 native_data_0220ded0[];
extern void native_fn_021f27d4(void);
extern void native_fn_02203954(void);
extern u8 native_data_04000010[];
extern void native_fn_021f5300(void);
extern void native_fn_021f52d8(void);
extern void native_fn_021f8d4c(void);
extern void native_fn_021f52cc(void);
extern void native_fn_021f94ac(void);
extern void native_fn_021fedc8(void);
extern void native_fn_020a48e4(void);
extern void native_fn_02008d78(void);
extern void native_fn_021fd660(void);
extern void native_fn_021fb93c(void);
extern void native_fn_021fc870(void);
extern void native_fn_021ff0d0(void);
extern void native_fn_021fd11c(void);
extern u8 native_data_0221c0f4[];
extern void native_fn_02203c20(void);


asm u32 native_ov006_021fa9c8 (register u32 a0)
{
    push {r4, r5, r6, lr}
    mov r0, #0x1
    bl native_fn_02203188
    cmp r0, #0x0
    bne ov006_021fa9c8_L16
    mov r0, #0x0
    bl native_fn_02203188
    cmp r0, #0x0
    beq ov006_021fa9c8_L18
ov006_021fa9c8_L16:
    b ov006_021fa9c8_L1ee
ov006_021fa9c8_L18:
    ldr r1, =native_data8_0221c0ec
    mov r0, #0x0
    ldr r1, [r1, #0x8]
    ldr r1, [r1, #0]
    bl native_fn_0220498c
    ldr r1, =native_data8_0221c0ec
    mov r0, #0x1
    ldr r1, [r1, #0x8]
    ldr r1, [r1, #0x3c]
    bl native_fn_0220498c
    mov r5, #0x0
    ldr r6, =native_data8_0221c0ec
    add r4, r5, #0x0
ov006_021fa9c8_L36:
    ldr r0, [r6, #0x8]
    add r0, r0, r4
    ldr r0, [r0, #0x18]
    bl native_fn_022043a4
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0x7
    blt ov006_021fa9c8_L36
    ldr r0, =native_data8_0221c0ec
    ldr r0, [r0, #0x8]
    ldr r0, [r0, #0x34]
    cmp r0, #0x0
    beq ov006_021fa9c8_L56
    bl native_fn_022043a4
ov006_021fa9c8_L56:
    bl native_fn_021fe690
    mov r0, #0x0
    bl native_fn_02203690
    bl native_fn_021f2a4c
    ldr r0, =native_data8_0221c0ec
    ldr r0, [r0, #0x8]
    add r0, #0x40
    ldrb r0, [r0, #0]
    cmp r0, #0xc
    beq ov006_021fa9c8_L74
    bl native_fn_021f2774
ov006_021fa9c8_L74:
    bl native_fn_021fe4dc
    ldr r0, =native_data8_0221c0ec
    ldr r0, [r0, #0x8]
    ldr r0, [r0, #0x8]
    bl native_fn_02202b24
    mov r5, #0x0
    ldr r6, =native_data8_0221c0ec
    add r4, r5, #0x0
ov006_021fa9c8_L88:
    ldr r0, [r6, #0x8]
    add r0, r0, r4
    ldr r0, [r0, #0xc]
    bl native_fn_02202b24
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0x2
    blt ov006_021fa9c8_L88
    ldr r0, =native_data_0220ded0
    ldr r1, =0x0200494c
    bl native_fn_021f27d4
    mov r0, #0x1
    add r1, r0, #0x0
    bl native_fn_02203954
    mov r0, #0x0
    mov r1, #0x1d
    bl native_fn_02203954
    ldr r0, =native_data_04000010
    mov r1, #0x0
    str r1, [r0, #0]
    str r1, [r0, #0x8]
    sub r3, r0, #0x4
    ldrh r2, [r3, #0]
    mov r0, #0x43
    and r2, r0
    mov r0, #0xe1
    lsl r0, r0, #0x4
    orr r0, r2
    ldr r2, =native_data8_0221c0ec
    strh r0, [r3, #0]
    ldr r0, [r2, #0x8]
    add r0, #0x40
    ldrb r0, [r0, #0]
    cmp r0, #0xd
    bls ov006_021fa9c8_Ld8
    b ov006_021fa9c8_L1e8
ov006_021fa9c8_Ld8:
    add r3, r0, r0
    add r3, pc
    ldrh r3, [r3, #0x6]
    lsl r3, r3, #0x10
    asr r3, r3, #0x10
    add pc, r3
    lsl r2, r3, #0
    lsl r2, r3, #0
    lsl r2, r0, #0x4
    lsl r2, r0, #0x4
    lsl r6, r5, #0
    lsl r6, r5, #0
    lsl r6, r5, #0
    lsl r2, r0, #0x4
    lsl r2, r0, #0x4
    lsl r6, r5, #0
    lsl r6, r5, #0
    lsl r6, r1, #0x1
    lsl r4, r0, #0x3
    lsl r2, r2, #0x3
    bl native_fn_021f5300
    mov r0, #0x2
    mov r1, #0x0
    bl native_fn_021f52d8
    ldr r0, =native_fn_021f8d4c+1
    bl native_fn_021f52cc
    b ov006_021fa9c8_L1e8
    sub r4, r0, #0x4
    cmp r0, #0x9
    blo ov006_021fa9c8_L11c
    sub r4, r4, #0x2
ov006_021fa9c8_L11c:
    mov r0, #0x2
    mov r1, #0x0
    bl native_fn_021f52d8
    add r0, r4, #0x0
    mov r1, #0x0
    bl native_fn_021f5300
    ldr r0, =native_fn_021f94ac+1
    bl native_fn_021f52cc
    b ov006_021fa9c8_L1e8
    bl native_fn_021fedc8
    add r4, r0, #0x0
    add r0, #0xf0
    bl native_fn_020a48e4
    add r1, r4, #0x0
    add r1, #0xd0
    strb r0, [r1, #0]
    add r0, r4, #0x0
    add r0, #0xf5
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq ov006_021fa9c8_L17c
    add r0, r4, #0x0
    add r0, #0xc0
    mov r1, #0x0
    mov r2, #0x4
    blx native_fn_02008d78
    add r0, r4, #0x0
    add r0, #0xc4
    mov r1, #0x0
    mov r2, #0x4
    blx native_fn_02008d78
    add r0, r4, #0x0
    add r0, #0xf0
    mov r1, #0x0
    mov r2, #0x4
    blx native_fn_02008d78
    add r0, r4, #0x0
    mov r1, #0x0
    add r0, #0xd0
    strb r1, [r0, #0]
ov006_021fa9c8_L17c:
    add r0, r4, #0x0
    add r0, #0xf6
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq ov006_021fa9c8_L192
    add r4, #0xc8
    add r0, r4, #0x0
    mov r1, #0x0
    mov r2, #0x8
    blx native_fn_02008d78
ov006_021fa9c8_L192:
    mov r0, #0x2
    mov r1, #0x0
    bl native_fn_021f52d8
    mov r0, #0x0
    add r1, r0, #0x0
    bl native_fn_021f5300
    ldr r0, =native_fn_021fd660+1
    bl native_fn_021f52cc
    b ov006_021fa9c8_L1e8
    add r0, r1, #0x0
    bl native_fn_021f52d8
    ldr r0, =native_fn_021fb93c+1
    bl native_fn_021f52cc
    b ov006_021fa9c8_L1e8
    ldrb r0, [r2, #0x1]
    cmp r0, #0x0
    bne ov006_021fa9c8_L1ce
    mov r0, #0x2
    mov r1, #0x1
    bl native_fn_021f52d8
    ldr r0, =native_fn_021fc870+1
    bl native_fn_021f52cc
    b ov006_021fa9c8_L1e8
ov006_021fa9c8_L1ce:
    bl native_fn_021fedc8
    add r0, #0xf4
    ldrb r0, [r0, #0]
    bl native_fn_021ff0d0
    mov r0, #0x0
    mov r1, #0x1
    bl native_fn_021f52d8
    ldr r0, =native_fn_021fd11c+1
    bl native_fn_021f52cc
ov006_021fa9c8_L1e8:
    ldr r0, =native_data_0221c0f4
    bl native_fn_02203c20
ov006_021fa9c8_L1ee:
    pop {r4, r5, r6, pc}
}
