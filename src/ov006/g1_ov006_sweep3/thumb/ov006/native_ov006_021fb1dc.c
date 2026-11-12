/* ov006 row 0x021fb1dc: 380 bytes.
 *
 * What it does: 170 instructions; 14 call(s) to 0x02203fac, 0x02002480, 0x022040cc, +11 more; loops (back edge at +0x1a); returns through pop {r3, r4, r5, r6, r7, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x168 -> native_data_0220bb60 (image word 0x0220bb60)
 *   pool +0x16c -> constant 0x0221c0ec (image word 0x0221c0ec)
 *   pool +0x170 -> native_data_0220b704 (image word 0x0220b704)
 *   pool +0x174 -> native_data_0220b7e4 (image word 0x0220b7e4)
 *   pool +0x178 -> native_data_0220b792 (image word 0x0220b792)
 *   branch +0x0c -> +0x14
 *   branch +0x3a -> +0x52
 *   branch +0x3e -> +0x52
 *   branch +0x48 -> +0x52
 *   back edge +0x5e -> +0x38
 *   branch +0x6e -> +0xca
 *   branch +0x98 -> +0xa0
 *   branch +0xc2 -> +0xd2
 *   back edge +0xd0 -> +0x6c
 *   branch +0xe0 -> +0x13c
 *   branch +0x10a -> +0x112
 *   branch +0x134 -> +0x144
 *   back edge +0x142 -> +0xde
 *   branch +0x150 -> +0x15a
 *   back edge +0x160 -> +0x148
 *   test +0x0a cmp r0, #0x0
 *   test +0x38 cmp r4, #0x2
 *   test +0x3c cmp r4, #0x6
 *   test +0x46 cmp r0, #0x0
 *   test +0x5c cmp r5, #0x4
 *   test +0x6c cmp r0, #0x2
 *   test +0x96 cmp r0, #0x0
 *   test +0xc0 cmp r0, #0x0
 *   test +0xce cmp r1, #0x4
 *   test +0xde cmp r0, #0x6
 *   test +0x108 cmp r0, #0x0
 *   test +0x132 cmp r0, #0x0
 *   test +0x140 cmp r1, #0x4
 *   test +0x14e cmp r0, #0x0
 *   test +0x15e cmp r5, #0x3
 *   0 block transfer(s), 25 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fb1dc; the literal pool and
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
extern void native_fn_02002480(void);
extern u8 native_data_0220b704[];
extern void native_fn_022040cc(void);
extern u8 native_data_0220b7e4[];
extern u8 native_data_0220b792[];


asm u32 native_ov006_021fb1dc (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    ldr r0, =native_data_0220bb60
    bl native_fn_02203fac
    cmp r0, #0x0
    bne ov006_021fb1dc_L14
    add sp, #0x8
    mov r0, #0xe
    pop {r3, r4, r5, r6, r7, pc}
ov006_021fb1dc_L14:
    ldr r0, =0x0221c0ec
    mov r1, #0x1d
    ldrh r0, [r0, #0x4]
    blx native_fn_02002480
    add r4, r0, #0x0
    ldr r0, =native_data_0220b704
    add r6, sp, #0x0
    ldrh r1, [r0, #0x4]
    add r7, sp, #0x0
    mov r5, #0x0
    strh r1, [r6, #0]
    ldrh r1, [r0, #0x6]
    strh r1, [r6, #0x2]
    ldrh r1, [r0, #0x8]
    ldrh r0, [r0, #0xa]
    strh r1, [r6, #0x4]
    strh r0, [r6, #0x6]
ov006_021fb1dc_L38:
    cmp r4, #0x2
    beq ov006_021fb1dc_L52
    cmp r4, #0x6
    beq ov006_021fb1dc_L52
    add r0, r7, #0x0
    bl native_fn_022040cc
    cmp r0, #0x0
    beq ov006_021fb1dc_L52
    ldr r0, =native_data_0220b7e4
    add sp, #0x8
    ldrb r0, [r0, r4]
    pop {r3, r4, r5, r6, r7, pc}
ov006_021fb1dc_L52:
    ldrh r0, [r6, #0x2]
    add r5, r5, #0x1
    add r4, r4, #0x1
    add r0, #0x1d
    strh r0, [r6, #0x2]
    cmp r5, #0x4
    blt ov006_021fb1dc_L38
    ldr r0, =0x0221c0ec
    mov r1, #0x1d
    ldrh r0, [r0, #0x4]
    blx native_fn_02002480
    mov r1, #0x0
ov006_021fb1dc_L6c:
    cmp r0, #0x2
    bne ov006_021fb1dc_Lca
    ldr r2, =native_data_0220b704
    add r3, sp, #0x0
    ldrh r4, [r2, #0x14]
    add r0, sp, #0x0
    strh r4, [r3, #0]
    ldrh r4, [r2, #0x16]
    strh r4, [r3, #0x2]
    ldrh r4, [r2, #0x18]
    ldrh r2, [r2, #0x1a]
    strh r4, [r3, #0x4]
    strh r2, [r3, #0x6]
    add r4, r1, #0x0
    mov r2, #0x1d
    ldrh r1, [r3, #0x2]
    mul r4, r2
    add r1, r1, r4
    strh r1, [r3, #0x2]
    bl native_fn_022040cc
    cmp r0, #0x0
    beq ov006_021fb1dc_La0
    add sp, #0x8
    mov r0, #0x2
    pop {r3, r4, r5, r6, r7, pc}
ov006_021fb1dc_La0:
    ldr r2, =native_data_0220b704
    add r1, sp, #0x0
    ldrh r3, [r2, #0xc]
    add r0, sp, #0x0
    strh r3, [r1, #0]
    ldrh r3, [r2, #0xe]
    strh r3, [r1, #0x2]
    ldrh r3, [r2, #0x10]
    ldrh r2, [r2, #0x12]
    strh r3, [r1, #0x4]
    strh r2, [r1, #0x6]
    ldrh r2, [r1, #0x2]
    add r2, r2, r4
    strh r2, [r1, #0x2]
    bl native_fn_022040cc
    cmp r0, #0x0
    beq ov006_021fb1dc_Ld2
    add sp, #0x8
    mov r0, #0x3
    pop {r3, r4, r5, r6, r7, pc}
ov006_021fb1dc_Lca:
    add r1, r1, #0x1
    add r0, r0, #0x1
    cmp r1, #0x4
    blt ov006_021fb1dc_L6c
ov006_021fb1dc_Ld2:
    ldr r0, =0x0221c0ec
    mov r1, #0x1d
    ldrh r0, [r0, #0x4]
    blx native_fn_02002480
    mov r1, #0x0
ov006_021fb1dc_Lde:
    cmp r0, #0x6
    bne ov006_021fb1dc_L13c
    ldr r2, =native_data_0220b704
    add r3, sp, #0x0
    ldrh r4, [r2, #0x14]
    add r0, sp, #0x0
    strh r4, [r3, #0]
    ldrh r4, [r2, #0x16]
    strh r4, [r3, #0x2]
    ldrh r4, [r2, #0x18]
    ldrh r2, [r2, #0x1a]
    strh r4, [r3, #0x4]
    strh r2, [r3, #0x6]
    add r4, r1, #0x0
    mov r2, #0x1d
    ldrh r1, [r3, #0x2]
    mul r4, r2
    add r1, r1, r4
    strh r1, [r3, #0x2]
    bl native_fn_022040cc
    cmp r0, #0x0
    beq ov006_021fb1dc_L112
    add sp, #0x8
    mov r0, #0x7
    pop {r3, r4, r5, r6, r7, pc}
ov006_021fb1dc_L112:
    ldr r2, =native_data_0220b704
    add r1, sp, #0x0
    ldrh r3, [r2, #0xc]
    add r0, sp, #0x0
    strh r3, [r1, #0]
    ldrh r3, [r2, #0xe]
    strh r3, [r1, #0x2]
    ldrh r3, [r2, #0x10]
    ldrh r2, [r2, #0x12]
    strh r3, [r1, #0x4]
    strh r2, [r1, #0x6]
    ldrh r2, [r1, #0x2]
    add r2, r2, r4
    strh r2, [r1, #0x2]
    bl native_fn_022040cc
    cmp r0, #0x0
    beq ov006_021fb1dc_L144
    add sp, #0x8
    mov r0, #0x8
    pop {r3, r4, r5, r6, r7, pc}
ov006_021fb1dc_L13c:
    add r1, r1, #0x1
    add r0, r0, #0x1
    cmp r1, #0x4
    blt ov006_021fb1dc_Lde
ov006_021fb1dc_L144:
    ldr r4, =native_data_0220b792
    mov r5, #0x0
ov006_021fb1dc_L148:
    add r0, r4, #0x0
    bl native_fn_02203fac
    cmp r0, #0x0
    beq ov006_021fb1dc_L15a
    add r5, #0xb
    add sp, #0x8
    add r0, r5, #0x0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021fb1dc_L15a:
    add r5, r5, #0x1
    add r4, #0x8
    cmp r5, #0x3
    blt ov006_021fb1dc_L148
    mov r0, #0xe
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
}
