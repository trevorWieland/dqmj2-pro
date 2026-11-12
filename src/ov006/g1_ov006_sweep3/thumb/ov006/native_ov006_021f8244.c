/* ov006 row 0x021f8244: 388 bytes.
 *
 * What it does: 162 instructions; 29 call(s) to 0x02203fac, 0x02203fac, 0x021f23a0, +26 more; loops (back edge at +0x4a); returns through pop {r3, r4, r5, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x178 -> constant 0x0221c0d8 (image word 0x0221c0d8)
 *   pool +0x17c -> native_data_0220bb60 (image word 0x0220bb60)
 *   pool +0x180 -> native_data_0220b604 (image word 0x0220b604)
 *   branch +0x0a -> +0x14
 *   branch +0x12 -> +0x16
 *   branch +0x14 -> +0x176
 *   branch +0x1e -> +0x60
 *   branch +0x38 -> +0x58
 *   branch +0x3c -> +0x48
 *   branch +0x46 -> +0x60
 *   back edge +0x5e -> +0x30
 *   branch +0x68 -> +0xac
 *   branch +0x76 -> +0xa4
 *   branch +0x82 -> +0xac
 *   branch +0x8a -> +0x94
 *   branch +0x92 -> +0xac
 *   back edge +0xaa -> +0x6e
 *   branch +0xb4 -> +0xc2
 *   branch +0xca -> +0xd4
 *   branch +0xde -> +0xe6
 *   branch +0xf0 -> +0xfe
 *   branch +0x108 -> +0x110
 *   branch +0x11a -> +0x128
 *   branch +0x130 -> +0x13a
 *   branch +0x142 -> +0x150
 *   branch +0x158 -> +0x162
 *   branch +0x16a -> +0x176
 *   test +0x08 cmp r0, #0x0
 *   test +0x10 cmp r0, #0x0
 *   test +0x1c cmp r0, #0x0
 *   test +0x36 cmp r0, #0x0
 *   test +0x3a cmp r4, #0x4
 *   test +0x5c cmp r4, #0x5
 *   test +0x66 cmp r0, #0x0
 *   test +0x74 cmp r0, #0x0
 *   test +0x80 cmp r0, r4
 *   test +0x88 cmp r4, r0
 *   test +0xa8 cmp r4, #0x4
 *   test +0xb2 cmp r0, #0x0
 *   test +0xc8 cmp r0, #0x0
 *   test +0xdc cmp r0, #0x0
 *   test +0xee cmp r0, #0x0
 *   test +0x106 cmp r0, #0x0
 *   test +0x118 cmp r0, #0x0
 *   test +0x12e cmp r0, #0x0
 *   test +0x140 cmp r0, #0x0
 *   test +0x156 cmp r0, #0x0
 *   test +0x168 cmp r0, #0x0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f8244; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220bb60[];
extern void native_fn_02203fac(void);
extern u8 native_data_0220b604[];
extern void native_fn_021f23a0(void);
extern void native_fn_021f8b3c(void);
extern void native_fn_0220406c(void);
extern void native_fn_021ff6d4(void);
extern void native_fn_02203ebc(void);
extern void native_fn_021fe6e8(void);
extern void native_fn_02203eec(void);
extern void native_fn_021f8c94(void);
extern void native_fn_02203f1c(void);
extern void native_fn_021f8c4c(void);
extern void native_fn_021f8b70(void);


asm u32 native_ov006_021f8244 (register u32 a0)
{
    push {r3, r4, r5, lr}
    ldr r0, =0x0221c0d8
    ldr r1, [r0, #0x4]
    ldr r0, [r1, #0x38]
    cmp r0, #0x0
    bne ov006_021f8244_L14
    add r1, #0x57
    ldrb r0, [r1, #0]
    cmp r0, #0x0
    beq ov006_021f8244_L16
ov006_021f8244_L14:
    b ov006_021f8244_L176
ov006_021f8244_L16:
    ldr r0, =native_data_0220bb60
    bl native_fn_02203fac
    cmp r0, #0x0
    beq ov006_021f8244_L60
    ldr r0, =0x0221c0d8
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    mvn r1, r1
    add r0, #0x50
    ldr r5, =native_data_0220b604
    strb r1, [r0, #0]
    mov r4, #0x0
ov006_021f8244_L30:
    add r0, r5, #0x0
    bl native_fn_02203fac
    cmp r0, #0x0
    beq ov006_021f8244_L58
    cmp r4, #0x4
    bge ov006_021f8244_L48
    ldr r0, =0x0221c0d8
    ldr r0, [r0, #0x4]
    add r0, #0x50
    strb r4, [r0, #0]
    b ov006_021f8244_L60
ov006_021f8244_L48:
    mov r0, #0x1
    bl native_fn_021f23a0
    ldr r0, =0x0221c0d8
    strb r4, [r0, #0]
    bl native_fn_021f8b3c
    pop {r3, r4, r5, pc}
ov006_021f8244_L58:
    add r4, r4, #0x1
    add r5, #0x8
    cmp r4, #0x5
    blo ov006_021f8244_L30
ov006_021f8244_L60:
    ldr r0, =native_data_0220bb60
    bl native_fn_0220406c
    cmp r0, #0x0
    beq ov006_021f8244_Lac
    ldr r5, =native_data_0220b604
    mov r4, #0x0
ov006_021f8244_L6e:
    add r0, r5, #0x0
    bl native_fn_0220406c
    cmp r0, #0x0
    beq ov006_021f8244_La4
    ldr r0, =0x0221c0d8
    ldr r1, [r0, #0x4]
    mov r0, #0x50
    ldrsb r0, [r1, r0]
    cmp r0, r4
    bne ov006_021f8244_Lac
    add r1, #0x51
    ldrb r0, [r1, #0]
    cmp r4, r0
    blt ov006_021f8244_L94
    mov r0, #0x9
    bl native_fn_021ff6d4
    b ov006_021f8244_Lac
ov006_021f8244_L94:
    mov r0, #0x1
    bl native_fn_021f23a0
    ldr r0, =0x0221c0d8
    strb r4, [r0, #0]
    bl native_fn_021f8b3c
    pop {r3, r4, r5, pc}
ov006_021f8244_La4:
    add r4, r4, #0x1
    add r5, #0x8
    cmp r4, #0x4
    blt ov006_021f8244_L6e
ov006_021f8244_Lac:
    mov r0, #0x1
    bl native_fn_02203ebc
    cmp r0, #0x0
    beq ov006_021f8244_Lc2
    mov r0, #0x1
    bl native_fn_021f23a0
    bl native_fn_021fe6e8
    pop {r3, r4, r5, pc}
ov006_021f8244_Lc2:
    mov r0, #0x2
    bl native_fn_02203ebc
    cmp r0, #0x0
    beq ov006_021f8244_Ld4
    mov r0, #0x0
    bl native_fn_021f23a0
    pop {r3, r4, r5, pc}
ov006_021f8244_Ld4:
    mov r0, #0x2
    lsl r0, r0, #0x8
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021f8244_Le6
    bl native_fn_021f8c94
    pop {r3, r4, r5, pc}
ov006_021f8244_Le6:
    mov r0, #0x2
    lsl r0, r0, #0x8
    bl native_fn_02203f1c
    cmp r0, #0x0
    beq ov006_021f8244_Lfe
    ldr r0, =0x0221c0d8
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    add r0, #0x59
    strb r1, [r0, #0]
    pop {r3, r4, r5, pc}
ov006_021f8244_Lfe:
    mov r0, #0x1
    lsl r0, r0, #0x8
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021f8244_L110
    bl native_fn_021f8c4c
    pop {r3, r4, r5, pc}
ov006_021f8244_L110:
    mov r0, #0x1
    lsl r0, r0, #0x8
    bl native_fn_02203f1c
    cmp r0, #0x0
    beq ov006_021f8244_L128
    ldr r0, =0x0221c0d8
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    add r0, #0x59
    strb r1, [r0, #0]
    pop {r3, r4, r5, pc}
ov006_021f8244_L128:
    mov r0, #0x40
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021f8244_L13a
    mov r0, #0x1
    bl native_fn_021f8b70
    pop {r3, r4, r5, pc}
ov006_021f8244_L13a:
    mov r0, #0x40
    bl native_fn_02203f1c
    cmp r0, #0x0
    beq ov006_021f8244_L150
    ldr r0, =0x0221c0d8
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    add r0, #0x59
    strb r1, [r0, #0]
    pop {r3, r4, r5, pc}
ov006_021f8244_L150:
    mov r0, #0x80
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021f8244_L162
    mov r0, #0x3
    bl native_fn_021f8b70
    pop {r3, r4, r5, pc}
ov006_021f8244_L162:
    mov r0, #0x80
    bl native_fn_02203f1c
    cmp r0, #0x0
    beq ov006_021f8244_L176
    ldr r0, =0x0221c0d8
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    add r0, #0x59
    strb r1, [r0, #0]
ov006_021f8244_L176:
    pop {r3, r4, r5, pc}
}
