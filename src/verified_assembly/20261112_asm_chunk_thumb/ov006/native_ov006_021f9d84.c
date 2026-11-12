/* ov006 row 0x021f9d84: 604 bytes.
 *
 * What it does: Writes 2 blocks of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x21c -> native_data2_0221c0e8 (image word 0x0221c0e8)
 *   pool +0x220 -> constant 0xffffb17d (image word 0xffffb17d)
 *   pool +0x224 -> constant 0xffffadf9 (image word 0xffffadf9)
 *   pool +0x228 -> constant 0xffffa629 (image word 0xffffa629)
 *   pool +0x22c -> constant 0xffffa241 (image word 0xffffa241)
 *   pool +0x230 -> constant 0xffff3cb1 (image word 0xffff3cb1)
 *   pool +0x234 -> constant 0xffff3866 (image word 0xffff3866)
 *   pool +0x238 -> constant 0xffff34e1 (image word 0xffff34e1)
 *   pool +0x23c -> constant 0xffff33b5 (image word 0xffff33b5)
 *   pool +0x240 -> constant 0xffff30f9 (image word 0xffff30f9)
 *   pool +0x244 -> constant 0xffff2fcd (image word 0xffff2fcd)
 *   pool +0x248 -> native_data_0220b6d4 (image word 0x0220b6d4)
 *   pool +0x24c -> constant 0x0221c098 (image word 0x0221c098)
 *   pool +0x250 -> native_data_0220de74 (image word 0x0220de74)
 *   pool +0x254 -> native_data_0220b6e6 (image word 0x0220b6e6)
 *   pool +0x258 -> native_data_0220b6e4 (image word 0x0220b6e4)
 *   branch +0x14 -> +0x1a
 *   branch +0x18 -> +0x18e
 *   branch +0x1e -> +0x24
 *   branch +0x22 -> +0x18e
 *   branch +0x28 -> +0x2e
 *   branch +0x2c -> +0x18e
 *   branch +0x34 -> +0x3a
 *   branch +0x38 -> +0x18e
 *   branch +0x40 -> +0x46
 *   branch +0x44 -> +0x18e
 *   branch +0x4c -> +0x52
 *   branch +0x50 -> +0x18e
 *   branch +0x56 -> +0x5c
 *   branch +0x5a -> +0x18e
 *   branch +0x60 -> +0x66
 *   branch +0x64 -> +0x18e
 *   branch +0x6a -> +0x70
 *   branch +0x6e -> +0x18e
 *   branch +0x74 -> +0x7a
 *   branch +0x78 -> +0x18e
 *   branch +0x7e -> +0x84
 *   branch +0x82 -> +0x18e
 *   branch +0x88 -> +0x8e
 *   branch +0x8c -> +0x18e
 *   branch +0x92 -> +0x98
 *   branch +0x96 -> +0x18e
 *   branch +0x9e -> +0xa4
 *   branch +0xa2 -> +0x18e
 *   branch +0xa8 -> +0xb8
 *   branch +0xae -> +0xb4
 *   branch +0xb2 -> +0x18e
 *   branch +0xb6 -> +0x18e
 *   branch +0xbc -> +0xc2
 *   branch +0xc0 -> +0x18e
 *   branch +0xc6 -> +0xd6
 *   branch +0xcc -> +0xd2
 *   branch +0xd0 -> +0x18e
 *   branch +0xd4 -> +0x18e
 *   branch +0xda -> +0xe0
 *   branch +0xde -> +0x18e
 *   branch +0xe4 -> +0xea
 *   branch +0xe8 -> +0x18e
 *   branch +0xf0 -> +0xf6
 *   branch +0xf4 -> +0x18e
 *   branch +0xfc -> +0x102
 *   branch +0x100 -> +0x18e
 *   branch +0x108 -> +0x10e
 *   branch +0x10c -> +0x18e
 *   branch +0x112 -> +0x118
 *   branch +0x116 -> +0x18e
 *   branch +0x11c -> +0x122
 *   branch +0x120 -> +0x18e
 *   branch +0x126 -> +0x12c
 *   branch +0x12a -> +0x18e
 *   branch +0x130 -> +0x136
 *   branch +0x134 -> +0x18e
 *   branch +0x13c -> +0x142
 *   branch +0x140 -> +0x18e
 *   branch +0x148 -> +0x14e
 *   branch +0x14c -> +0x18e
 *   branch +0x154 -> +0x15a
 *   branch +0x158 -> +0x18e
 *   branch +0x15e -> +0x164
 *   branch +0x162 -> +0x18e
 *   branch +0x168 -> +0x16e
 *   branch +0x16c -> +0x18e
 *   branch +0x172 -> +0x178
 *   branch +0x176 -> +0x18e
 *   branch +0x17c -> +0x182
 *   branch +0x180 -> +0x18e
 *   branch +0x186 -> +0x18c
 *   branch +0x18a -> +0x18e
 *   branch +0x1f2 -> +0x210
 *   test +0x12 cmp r1, r2
 *   test +0x1c cmp r1, r0
 *   test +0x26 cmp r1, r0
 *   test +0x32 cmp r1, r0
 *   test +0x3e cmp r1, r0
 *   test +0x4a cmp r1, r0
 *   test +0x54 cmp r1, r2
 *   test +0x5e cmp r1, r0
 *   test +0x68 cmp r1, r0
 *   test +0x72 cmp r1, r0
 *   test +0x7c cmp r1, r2
 *   test +0x86 cmp r1, r0
 *   test +0x90 cmp r1, r0
 *   test +0x9c cmp r1, r0
 *   test +0xa6 cmp r1, r2
 *   test +0xac cmp r0, #0x2
 *   test +0xba cmp r1, r0
 *   test +0xc4 cmp r1, r2
 *   test +0xca cmp r0, #0x2
 *   test +0xd8 cmp r1, r2
 *   test +0xe2 cmp r1, r2
 *   test +0xee cmp r1, r2
 *   test +0xfa cmp r1, r2
 *   test +0x106 cmp r1, r2
 *   test +0x110 cmp r1, r0
 *   test +0x11a cmp r1, r2
 *   test +0x124 cmp r1, r0
 *   test +0x12e cmp r1, r0
 *   test +0x13a cmp r1, r0
 *   test +0x146 cmp r1, r0
 *   test +0x152 cmp r1, r0
 *   test +0x15c cmp r1, r2
 *   test +0x166 cmp r1, r0
 *   test +0x170 cmp r1, r0
 *   test +0x17a cmp r1, r0
 *   test +0x184 cmp r1, r0
 *   test +0x1f0 cmp r5, #0x0
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f9d84; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 604 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021f530c(void);
extern u8 native_data2_0221c0e8[];
extern void native_fn_021f5328(void);
extern u8 native_data_0220b6d4[];
extern void native_fn_022034dc(void);
extern void native_fn_021f5418(void);
extern u8 native_data_0220de74[];
extern void native_fn_020061ac(void);
extern void native_fn_022045e0(void);
extern u8 native_data_0220b6e6[];
extern u8 native_data_0220b6e4[];
extern void native_fn_0220374c(void);
extern void native_fn_021f290c(void);
extern void native_fn_022037c0(void);
extern void native_fn_022038ac(void);


asm u32 native_ov006_021f9d84 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0x2c
    mov r0, #0x0
    add r1, sp, #0x18
    bl native_fn_021f530c
    ldr r0, =native_data2_0221c0e8
    ldr r2, =0xffffb17d
    ldr r1, [r0, #0]
    cmp r1, r2
    blt ov006_021f9d84_L1a
    mov r5, #0x0
    b ov006_021f9d84_L18e
ov006_021f9d84_L1a:
    sub r0, r2, #0x1
    cmp r1, r0
    blt ov006_021f9d84_L24
    mov r5, #0x2
    b ov006_021f9d84_L18e
ov006_021f9d84_L24:
    sub r0, r2, #0x2
    cmp r1, r0
    blt ov006_021f9d84_L2e
    mov r5, #0x13
    b ov006_021f9d84_L18e
ov006_021f9d84_L2e:
    add r0, r2, #0x0
    sub r0, #0x8
    cmp r1, r0
    blt ov006_021f9d84_L3a
    mov r5, #0x2
    b ov006_021f9d84_L18e
ov006_021f9d84_L3a:
    add r0, r2, #0x0
    sub r0, #0x9
    cmp r1, r0
    blt ov006_021f9d84_L46
    mov r5, #0x12
    b ov006_021f9d84_L18e
ov006_021f9d84_L46:
    add r0, r2, #0x0
    sub r0, #0xa
    cmp r1, r0
    blt ov006_021f9d84_L52
    mov r5, #0x2
    b ov006_021f9d84_L18e
ov006_021f9d84_L52:
    sub r2, #0xb
    cmp r1, r2
    blt ov006_021f9d84_L5c
    mov r5, #0x3
    b ov006_021f9d84_L18e
ov006_021f9d84_L5c:
    ldr r0, =0xffffadf9
    cmp r1, r0
    blt ov006_021f9d84_L66
    mov r5, #0x2
    b ov006_021f9d84_L18e
ov006_021f9d84_L66:
    ldr r0, =0xffffa629
    cmp r1, r0
    blt ov006_021f9d84_L70
    mov r5, #0x0
    b ov006_021f9d84_L18e
ov006_021f9d84_L70:
    ldr r0, =0xffffa241
    cmp r1, r0
    blt ov006_021f9d84_L7a
    mov r5, #0x13
    b ov006_021f9d84_L18e
ov006_021f9d84_L7a:
    ldr r2, =0xffff3cb1
    cmp r1, r2
    blt ov006_021f9d84_L84
    mov r5, #0x0
    b ov006_021f9d84_L18e
ov006_021f9d84_L84:
    sub r0, r2, #0x3
    cmp r1, r0
    blt ov006_021f9d84_L8e
    mov r5, #0x7
    b ov006_021f9d84_L18e
ov006_021f9d84_L8e:
    sub r0, r2, #0x4
    cmp r1, r0
    blt ov006_021f9d84_L98
    mov r5, #0x5
    b ov006_021f9d84_L18e
ov006_021f9d84_L98:
    add r0, r2, #0x0
    sub r0, #0x63
    cmp r1, r0
    blt ov006_021f9d84_La4
    mov r5, #0x0
    b ov006_021f9d84_L18e
ov006_021f9d84_La4:
    sub r2, #0x64
    cmp r1, r2
    blt ov006_021f9d84_Lb8
    ldr r0, [sp, #0x18]
    cmp r0, #0x2
    bne ov006_021f9d84_Lb4
    mov r5, #0x5
    b ov006_021f9d84_L18e
ov006_021f9d84_Lb4:
    mov r5, #0x7
    b ov006_021f9d84_L18e
ov006_021f9d84_Lb8:
    ldr r0, =0xffff3866
    cmp r1, r0
    blt ov006_021f9d84_Lc2
    mov r5, #0x0
    b ov006_021f9d84_L18e
ov006_021f9d84_Lc2:
    sub r2, r0, #0x1
    cmp r1, r2
    blt ov006_021f9d84_Ld6
    ldr r0, [sp, #0x18]
    cmp r0, #0x2
    bne ov006_021f9d84_Ld2
    mov r5, #0x5
    b ov006_021f9d84_L18e
ov006_021f9d84_Ld2:
    mov r5, #0x8
    b ov006_021f9d84_L18e
ov006_021f9d84_Ld6:
    sub r2, r0, #0x4
    cmp r1, r2
    blt ov006_021f9d84_Le0
    mov r5, #0x9
    b ov006_021f9d84_L18e
ov006_021f9d84_Le0:
    sub r2, r0, #0x5
    cmp r1, r2
    blt ov006_021f9d84_Lea
    mov r5, #0x5
    b ov006_021f9d84_L18e
ov006_021f9d84_Lea:
    add r2, r0, #0x0
    sub r2, #0x65
    cmp r1, r2
    blt ov006_021f9d84_Lf6
    mov r5, #0x0
    b ov006_021f9d84_L18e
ov006_021f9d84_Lf6:
    add r2, r0, #0x0
    sub r2, #0xc9
    cmp r1, r2
    blt ov006_021f9d84_L102
    mov r5, #0x14
    b ov006_021f9d84_L18e
ov006_021f9d84_L102:
    add r2, r0, #0x0
    sub r2, #0xcc
    cmp r1, r2
    blt ov006_021f9d84_L10e
    mov r5, #0x15
    b ov006_021f9d84_L18e
ov006_021f9d84_L10e:
    sub r0, #0xcd
    cmp r1, r0
    blt ov006_021f9d84_L118
    mov r5, #0x4
    b ov006_021f9d84_L18e
ov006_021f9d84_L118:
    ldr r2, =0xffff34e1
    cmp r1, r2
    blt ov006_021f9d84_L122
    mov r5, #0x0
    b ov006_021f9d84_L18e
ov006_021f9d84_L122:
    sub r0, r2, #0x3
    cmp r1, r0
    blt ov006_021f9d84_L12c
    mov r5, #0xa
    b ov006_021f9d84_L18e
ov006_021f9d84_L12c:
    sub r0, r2, #0x4
    cmp r1, r0
    blt ov006_021f9d84_L136
    mov r5, #0x16
    b ov006_021f9d84_L18e
ov006_021f9d84_L136:
    add r0, r2, #0x0
    sub r0, #0x64
    cmp r1, r0
    blt ov006_021f9d84_L142
    mov r5, #0x0
    b ov006_021f9d84_L18e
ov006_021f9d84_L142:
    add r0, r2, #0x0
    sub r0, #0x68
    cmp r1, r0
    blt ov006_021f9d84_L14e
    mov r5, #0xb
    b ov006_021f9d84_L18e
ov006_021f9d84_L14e:
    add r0, r2, #0x0
    sub r0, #0xc8
    cmp r1, r0
    blt ov006_021f9d84_L15a
    mov r5, #0x0
    b ov006_021f9d84_L18e
ov006_021f9d84_L15a:
    sub r2, #0xcc
    cmp r1, r2
    blt ov006_021f9d84_L164
    mov r5, #0xb
    b ov006_021f9d84_L18e
ov006_021f9d84_L164:
    ldr r0, =0xffff33b5
    cmp r1, r0
    blt ov006_021f9d84_L16e
    mov r5, #0x0
    b ov006_021f9d84_L18e
ov006_021f9d84_L16e:
    sub r0, #0x64
    cmp r1, r0
    blt ov006_021f9d84_L178
    mov r5, #0x2
    b ov006_021f9d84_L18e
ov006_021f9d84_L178:
    ldr r0, =0xffff30f9
    cmp r1, r0
    blt ov006_021f9d84_L182
    mov r5, #0x0
    b ov006_021f9d84_L18e
ov006_021f9d84_L182:
    ldr r0, =0xffff2fcd
    cmp r1, r0
    blt ov006_021f9d84_L18c
    mov r5, #0x2
    b ov006_021f9d84_L18e
ov006_021f9d84_L18c:
    mov r5, #0x0
ov006_021f9d84_L18e:
    bl native_fn_021f5328
    add r2, r0, #0x0
    ldr r1, =native_data_0220b6d4
    mov r0, #0x0
    ldrb r1, [r1, r2]
    bl native_fn_022034dc
    add r4, r0, #0x0
    ldr r0, =0x0221c098
    add r1, r5, #0x0
    ldr r0, [r0, #0]
    bl native_fn_021f5418
    ldr r3, =native_data2_0221c0e8
    add r7, r0, #0x0
    ldr r3, [r3, #0]
    ldr r2, =native_data_0220de74
    add r0, sp, #0x10
    mov r1, #0x8
    neg r3, r3
    blx native_fn_020061ac
    add r0, sp, #0x1c
    add r1, sp, #0x10
    mov r2, #0x8
    bl native_fn_022045e0
    bl native_fn_021f5328
    lsl r1, r0, #0x2
    ldr r0, =native_data_0220b6e6
    ldrh r6, [r0, r1]
    bl native_fn_021f5328
    lsl r1, r0, #0x2
    ldr r0, =native_data_0220b6e4
    add r2, r6, #0x0
    ldrh r1, [r0, r1]
    mov r0, #0xa
    str r0, [sp]
    add r0, sp, #0x1c
    str r0, [sp, #0x4]
    mov r0, #0x0
    str r0, [sp, #0x8]
    add r0, r4, #0x0
    mov r3, #0x2
    bl native_fn_0220374c
    cmp r5, #0x0
    beq ov006_021f9d84_L210
    bl native_fn_021f290c
    mov r1, #0x5e
    str r1, [sp]
    mov r1, #0x2
    str r1, [sp, #0x4]
    str r0, [sp, #0x8]
    add r0, r4, #0x0
    mov r1, #0xd
    mov r2, #0x3c
    mov r3, #0xe6
    str r7, [sp, #0xc]
    bl native_fn_022037c0
ov006_021f9d84_L210:
    add r0, r4, #0x0
    bl native_fn_022038ac
    add sp, #0x2c
    pop {r4, r5, r6, r7, pc}
    mov r8, r8
}
