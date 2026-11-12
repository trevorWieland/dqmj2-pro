/* ov000 row 0x021e1328: 344 bytes.
 *
 * What it does: 86 instructions; 7 call(s) to 0x021dd440, 0x0221394c, 0x02212394, +4 more; loops (back edge at +0x28); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: predicated block copy.
 *
 *   branch +0x44 -> +0x5c
 *   branch +0x60 -> +0x88
 *   branch +0x8c -> +0xb4
 *   branch +0xb8 -> +0x14c
 *   branch +0xc8 -> +0xe0
 *   branch +0xdc -> +0xf8
 *   branch +0xfc -> +0x110
 *   branch +0x10c -> +0x14c
 *   branch +0x114 -> +0x148
 *   branch +0x130 -> +0x148
 *   branch +0x144 -> +0x14c
 *   test +0x30 cmp r4, #1
 *   test +0x40 cmp r4, #0
 *   test +0x54 cmp r0, #0
 *   test +0x5c cmp r4, #0
 *   test +0x78 cmp r4, #1
 *   test +0x88 cmp r4, #0
 *   test +0xa4 cmp r4, #1
 *   test +0xb4 cmp r4, #0
 *   test +0xc4 tst r0, #1
 *   test +0xf8 cmp r0, #0
 *   test +0x110 cmp r5, #0
 *   test +0x12c cmp r0, #0
 *   10 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e1328; the literal pool and
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

extern void native_fn_021dd440(void);
extern void native_fn_0221394c(void);
extern void native_fn_02212394(void);
extern void native_fn_021e59e4(void);
extern void native_fn_021dc374(void);
extern void native_fn_021dbc18(void);
extern void native_fn_021dd170(void);


asm u32 native_ov000_021e1328 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #16
    mov r7, r0
    movs r5, r2
    addne r8, r7, #184
    mov r6, r1
    moveq r8, #0
    add r2, sp, #4
    mov r0, r6
    mov r1, r8
    bl native_fn_021dd440
    mov r4, r0
    cmp r4, #1
    addeq r0, sp, #4
    ldmeqia r0, {r0, r1, r2}
    stmeqia r6, {r0, r1, r2}
    cmp r4, #0
    bne ov000_021e1328_L5c
    mov r0, r6
    add r1, r7, #112
    bl native_fn_0221394c
    cmp r0, #0
    movne r4, #2
ov000_021e1328_L5c:
    cmp r4, #0
    bne ov000_021e1328_L88
    add r2, sp, #4
    mov r0, r6
    mov r1, r8
    bl native_fn_02212394
    mov r4, r0
    cmp r4, #1
    addeq r0, sp, #4
    ldmeqia r0, {r0, r1, r2}
    stmeqia r6, {r0, r1, r2}
ov000_021e1328_L88:
    cmp r4, #0
    bne ov000_021e1328_Lb4
    add r2, sp, #4
    mov r0, r6
    mov r1, r8
    bl native_fn_021e59e4
    mov r4, r0
    cmp r4, #1
    addeq r0, sp, #4
    ldmeqia r0, {r0, r1, r2}
    stmeqia r6, {r0, r1, r2}
ov000_021e1328_Lb4:
    cmp r4, #0
    bne ov000_021e1328_L14c
    ldrb r0, [r7, #0x162]
    add r2, sp, #4
    tst r0, #1
    beq ov000_021e1328_Le0
    mov r0, r6
    add r1, r7, #528
    mov r3, #1
    bl native_fn_021dc374
    b ov000_021e1328_Lf8
ov000_021e1328_Le0:
    mov r12, #1
    mov r0, r6
    mov r3, r5
    add r1, r7, #528
    str r12, [sp]
    bl native_fn_021dbc18
ov000_021e1328_Lf8:
    cmp r0, #0
    beq ov000_021e1328_L110
    add r0, sp, #4
    ldmia r0, {r0, r1, r2}
    stmia r6, {r0, r1, r2}
    b ov000_021e1328_L14c
ov000_021e1328_L110:
    cmp r5, #0
    beq ov000_021e1328_L148
    add r3, sp, #4
    mov r0, r6
    add r1, r7, #112
    add r2, r7, #528
    bl native_fn_021dd170
    cmp r0, #0
    beq ov000_021e1328_L148
    add r0, sp, #4
    ldmia r0, {r0, r1, r2}
    mov r4, #1
    stmia r6, {r0, r1, r2}
    b ov000_021e1328_L14c
ov000_021e1328_L148:
    mov r4, #2
ov000_021e1328_L14c:
    mov r0, r4
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
