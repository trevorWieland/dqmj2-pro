/* ov000 row 0x021e4014: 876 bytes.
 *
 * What it does: 201 instructions; 38 call(s) to 0x0205bf9c, 0x021df1f0, 0x02008c14, +35 more; loops (back edge at +0x28); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 18 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x324 -> native_data_0222b888 (image word 0x0222b888)
 *   pool +0x328 -> constant 0x02234388 (image word 0x02234388)
 *   pool +0x32c -> native_data_0222ecc0 (image word 0x0222ecc0)
 *   pool +0x330 -> native_data_0222eca8 (image word 0x0222eca8)
 *   pool +0x334 -> constant 0x00534f50 (image word 0x00534f50)
 *   pool +0x338 -> native_data_0222ecdc (image word 0x0222ecdc)
 *   pool +0x33c -> native_data_0222ece0 (image word 0x0222ece0)
 *   pool +0x340 -> native_data_0222ecd8 (image word 0x0222ecd8)
 *   pool +0x344 -> native_data_0222ece4 (image word 0x0222ece4)
 *   pool +0x348 -> native_data_0222ece8 (image word 0x0222ece8)
 *   pool +0x34c -> native_data_0222ecec (image word 0x0222ecec)
 *   pool +0x350 -> native_data_0222ecf0 (image word 0x0222ecf0)
 *   pool +0x354 -> native_data_0222ecf4 (image word 0x0222ecf4)
 *   pool +0x358 -> native_data_0222ecf8 (image word 0x0222ecf8)
 *   pool +0x35c -> native_data_0222ecfc (image word 0x0222ecfc)
 *   pool +0x360 -> native_data_0222ed00 (image word 0x0222ed00)
 *   pool +0x364 -> native_data_0222ed08 (image word 0x0222ed08)
 *   pool +0x368 -> native_data_0222ed0c (image word 0x0222ed0c)
 *   branch +0x34 -> +0x40
 *   branch +0x80 -> +0xb4
 *   branch +0xb0 -> +0xd0
 *   branch +0xe0 -> +0x108
 *   branch +0x104 -> +0x114
 *   back edge +0x110 -> +0x7c
 *   branch +0x11c -> +0x318
 *   branch +0x130 -> +0x318
 *   branch +0x160 -> +0x16c
 *   branch +0x168 -> +0x304
 *   branch +0x180 -> +0x18c
 *   branch +0x188 -> +0x304
 *   branch +0x1a0 -> +0x1b0
 *   branch +0x1ac -> +0x304
 *   branch +0x1c4 -> +0x1d4
 *   branch +0x1d0 -> +0x304
 *   branch +0x1e8 -> +0x1f8
 *   branch +0x1f4 -> +0x304
 *   branch +0x20c -> +0x21c
 *   branch +0x218 -> +0x304
 *   branch +0x230 -> +0x23c
 *   branch +0x238 -> +0x304
 *   branch +0x250 -> +0x260
 *   branch +0x25c -> +0x304
 *   branch +0x274 -> +0x284
 *   branch +0x280 -> +0x304
 *   branch +0x298 -> +0x2a8
 *   branch +0x2a4 -> +0x304
 *   branch +0x2bc -> +0x2c8
 *   branch +0x2c4 -> +0x304
 *   branch +0x2dc -> +0x2e8
 *   branch +0x2e4 -> +0x304
 *   branch +0x2f8 -> +0x304
 *   back edge +0x314 -> +0x148
 *   test +0x30 cmp r4, #255
 *   test +0x7c cmp r8, #0
 *   test +0xdc cmp r0, #0
 *   test +0xf0 cmp r2, r1
 *   test +0x10c cmp r8, #2
 *   test +0x118 cmp r0, #0
 *   test +0x128 cmp r0, #0
 *   test +0x158 cmp r0, #0
 *   test +0x178 cmp r0, #0
 *   test +0x198 cmp r0, #0
 *   test +0x1bc cmp r0, #0
 *   test +0x1e0 cmp r0, #0
 *   test +0x204 cmp r0, #0
 *   test +0x228 cmp r0, #0
 *   test +0x248 cmp r0, #0
 *   test +0x26c cmp r0, #0
 *   test +0x290 cmp r0, #0
 *   test +0x2b4 cmp r0, #0
 *   test +0x2d4 cmp r0, #0
 *   test +0x2f4 cmp r0, #0
 *   test +0x310 cmp r8, r0
 *   3 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e4014; the literal pool and
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

extern u8 native_data_0222b888[];
extern void native_fn_0205bf9c(void);
extern void native_fn_021df1f0(void);
extern void native_fn_02008c14(void);
extern void native_fn_021df220(void);
extern u8 native_data_0222ecc0[];
extern u8 native_data_0222eca8[];
extern void native_fn_0205bfd4(void);
extern void native_fn_0201d444(void);
extern void native_fn_021df210(void);
extern void native_fn_02040d18(void);
extern u8 native_data_0222ecdc[];
extern u8 native_data_0222ece0[];
extern u8 native_data_0222ecd8[];
extern void native_fn_0201d914(void);
extern void native_fn_021e3540(void);
extern void native_fn_021e3948(void);
extern void native_fn_021e39e4(void);
extern u8 native_data_0222ece4[];
extern u8 native_data_0222ece8[];
extern void native_fn_021e3aa4(void);
extern u8 native_data_0222ecec[];
extern u8 native_data_0222ecf0[];
extern void native_fn_021e3c0c(void);
extern u8 native_data_0222ecf4[];
extern void native_fn_021e3b5c(void);
extern u8 native_data_0222ecf8[];
extern u8 native_data_0222ecfc[];
extern u8 native_data_0222ed00[];
extern void native_fn_021e3d94(void);
extern u8 native_data_0222ed08[];
extern void native_fn_021e3f98(void);
extern u8 native_data_0222ed0c[];
extern void native_fn_021e3d1c(void);


asm u32 native_ov000_021e4014 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #44
    mov r4, r0
    mov r0, #0
    str r0, [sp, #0x8]
    ldr r1, =native_data_0222b888
    add r3, sp, #16
    ldmia r1, {r0, r1, r2}
    ldr r9, [sp, #0x8]
    stmia r3, {r0, r1, r2}
    bl native_fn_0205bf9c
    mov r10, r0
    cmp r4, #255
    bne ov000_021e4014_L40
    bl native_fn_021df1f0
    mov r4, r0
ov000_021e4014_L40:
    ldr r1, =0x02234388
    mov r0, #0
    mov r2, #3328
    bl native_fn_02008c14
    add r1, sp, #14
    add r2, sp, #13
    add r3, sp, #12
    mov r0, r4
    bl native_fn_021df220
    mov r8, #0
    ldr r11, =native_data_0222ecc0
    ldr r5, =native_data_0222eca8
    mov r4, r8
    add r6, sp, #28
    add r7, sp, #16
ov000_021e4014_L7c:
    cmp r8, #0
    bne ov000_021e4014_Lb4
    bl native_fn_0205bfd4
    ldrb r2, [sp, #0xc]
    mov r1, r5
    str r2, [sp]
    ldr r2, [r7, r0, lsl #2]
    mov r0, r6
    add r2, r10, r2
    str r2, [sp, #0x4]
    ldrsb r2, [sp, #14]
    ldrb r3, [sp, #0xd]
    bl native_fn_0201d444
    b ov000_021e4014_Ld0
ov000_021e4014_Lb4:
    ldrb r2, [sp, #0xc]
    mov r0, r6
    mov r1, r11
    stmia sp, {r2, r4}
    ldrsb r2, [sp, #14]
    ldrb r3, [sp, #0xd]
    bl native_fn_0201d444
ov000_021e4014_Ld0:
    bl native_fn_021df210
    mov r1, r6
    bl native_fn_02040d18
    cmp r0, #0
    beq ov000_021e4014_L108
    ldr r2, [r0]
    ldr r1, =0x00534f50
    mov r9, r0
    cmp r2, r1
    moveq r0, #1
    streq r0, [sp, #0x8]
    movne r0, #0
    strne r0, [sp, #0x8]
    b ov000_021e4014_L114
ov000_021e4014_L108:
    add r8, r8, #1
    cmp r8, #2
    blt ov000_021e4014_L7c
ov000_021e4014_L114:
    ldr r0, [sp, #0x8]
    cmp r0, #0
    beq ov000_021e4014_L318
    ldr r0, [r9, #0x4]
    add r10, r9, #8
    cmp r0, #0
    mov r8, #0
    ble ov000_021e4014_L318
    mov r4, #2
    ldr r5, =native_data_0222ecdc
    ldr r11, =native_data_0222ece0
    ldr r7, =native_data_0222ecd8
    mov r6, r4
ov000_021e4014_L148:
    mov r0, r10
    mov r1, r7
    mov r2, r6
    bl native_fn_0201d914
    cmp r0, #0
    mov r0, r10
    bne ov000_021e4014_L16c
    bl native_fn_021e3540
    b ov000_021e4014_L304
ov000_021e4014_L16c:
    mov r1, r5
    mov r2, r4
    bl native_fn_0201d914
    cmp r0, #0
    mov r0, r10
    bne ov000_021e4014_L18c
    bl native_fn_021e3948
    b ov000_021e4014_L304
ov000_021e4014_L18c:
    mov r1, r11
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    mov r0, r10
    bne ov000_021e4014_L1b0
    mov r1, #0
    bl native_fn_021e39e4
    b ov000_021e4014_L304
ov000_021e4014_L1b0:
    ldr r1, =native_data_0222ece4
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    mov r0, r10
    bne ov000_021e4014_L1d4
    mov r1, #1
    bl native_fn_021e39e4
    b ov000_021e4014_L304
ov000_021e4014_L1d4:
    ldr r1, =native_data_0222ece8
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    mov r0, r10
    bne ov000_021e4014_L1f8
    mov r1, #0
    bl native_fn_021e3aa4
    b ov000_021e4014_L304
ov000_021e4014_L1f8:
    ldr r1, =native_data_0222ecec
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    mov r0, r10
    bne ov000_021e4014_L21c
    mov r1, #1
    bl native_fn_021e3aa4
    b ov000_021e4014_L304
ov000_021e4014_L21c:
    ldr r1, =native_data_0222ecf0
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    mov r0, r10
    bne ov000_021e4014_L23c
    bl native_fn_021e3c0c
    b ov000_021e4014_L304
ov000_021e4014_L23c:
    ldr r1, =native_data_0222ecf4
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    mov r0, r10
    bne ov000_021e4014_L260
    mov r1, #0
    bl native_fn_021e3b5c
    b ov000_021e4014_L304
ov000_021e4014_L260:
    ldr r1, =native_data_0222ecf8
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    mov r0, r10
    bne ov000_021e4014_L284
    mov r1, #1
    bl native_fn_021e3b5c
    b ov000_021e4014_L304
ov000_021e4014_L284:
    ldr r1, =native_data_0222ecfc
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    mov r0, r10
    bne ov000_021e4014_L2a8
    mov r1, #2
    bl native_fn_021e3b5c
    b ov000_021e4014_L304
ov000_021e4014_L2a8:
    ldr r1, =native_data_0222ed00
    mov r2, #5
    bl native_fn_0201d914
    cmp r0, #0
    mov r0, r10
    bne ov000_021e4014_L2c8
    bl native_fn_021e3d94
    b ov000_021e4014_L304
ov000_021e4014_L2c8:
    ldr r1, =native_data_0222ed08
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    mov r0, r10
    bne ov000_021e4014_L2e8
    bl native_fn_021e3f98
    b ov000_021e4014_L304
ov000_021e4014_L2e8:
    ldr r1, =native_data_0222ed0c
    mov r2, #2
    bl native_fn_0201d914
    cmp r0, #0
    bne ov000_021e4014_L304
    mov r0, r10
    bl native_fn_021e3d1c
ov000_021e4014_L304:
    add r8, r8, #1
    add r10, r10, #72
    ldr r0, [r9, #0x4]
    cmp r8, r0
    blt ov000_021e4014_L148
ov000_021e4014_L318:
    ldr r0, [sp, #0x8]
    add sp, sp, #44
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
