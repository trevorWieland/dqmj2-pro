/* ov001 row 0x02213048: 268 bytes.
 *
 * What it does: 67 instructions; 7 call(s) to 0x02212f74, 0x02212a64, 0x0205f98c, +4 more; loops (back edge at +0x30); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 7 calls (67 instructions, 7 calls, 14 branches, 7 back edges, 0 literal slots).
 *
 *   branch +0x18 -> +0xf4
 *   branch +0x1c -> +0x2c
 *   branch +0x20 -> +0x48
 *   branch +0x24 -> +0x48
 *   branch +0x28 -> +0xec
 *   branch +0x44 -> +0xf4
 *   branch +0x54 -> +0x64
 *   branch +0x60 -> +0x6c
 *   branch +0x70 -> +0x9c
 *   branch +0x98 -> +0xf4
 *   branch +0xa0 -> +0xb4
 *   branch +0xb0 -> +0xf4
 *   back edge +0xdc -> +0xb8
 *   branch +0xe8 -> +0xf4
 *   branch +0xf8 -> +0x104
 *   back edge +0x100 -> +0x00
 *   test +0x10 cmp r2, #3
 *   test +0x4c cmp r2, #1
 *   test +0x58 cmp r0, #2
 *   test +0x64 cmp r0, #0
 *   test +0x6c cmp r1, #0
 *   test +0x80 cmp r0, #1
 *   test +0x9c cmp r2, #1
 *   test +0xd8 cmp r6, #24
 *   test +0xf4 cmp r4, #0
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02213048; the literal pool and
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

extern void native_fn_02212f74(void);
extern void native_fn_02212a64(void);
extern void native_fn_0205f98c(void);
extern void native_fn_02048a60(void);
extern void native_fn_02212f14(void);


asm u32 native_ov001_02213048 (register u32 a0)
{
ov001_02213048_L0:
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, r0
    ldr r2, [r5, #0x34]
    mov r4, #0
    cmp r2, #3
    addls pc, pc, r2, lsl #2
    b ov001_02213048_Lf4
    b ov001_02213048_L2c
    b ov001_02213048_L48
    b ov001_02213048_L48
    b ov001_02213048_Lec
ov001_02213048_L2c:
    strh r4, [r5, #38]
    bl native_fn_02212f74
    mov r0, r4
    strb r0, [r5, #0x24]
    mov r4, #1
    str r4, [r5, #0x34]
    b ov001_02213048_Lf4
ov001_02213048_L48:
    mov r1, r4
    cmp r2, #1
    ldrsb r0, [r5, #36]
    bne ov001_02213048_L64
    cmp r0, #2
    movgt r1, #1
    b ov001_02213048_L6c
ov001_02213048_L64:
    cmp r0, #0
    movle r1, #1
ov001_02213048_L6c:
    cmp r1, #0
    bne ov001_02213048_L9c
    mov r0, r5
    bl native_fn_02212a64
    ldr r0, [r5, #0x34]
    cmp r0, #1
    ldrsb r0, [r5, #36]
    addeq r0, r0, #2
    streqb r0, [r5, #0x24]
    subne r0, r0, #1
    strneb r0, [r5, #0x24]
    b ov001_02213048_Lf4
ov001_02213048_L9c:
    cmp r2, #1
    bne ov001_02213048_Lb4
    mov r0, #2
    str r0, [r5, #0x34]
    mov r4, #1
    b ov001_02213048_Lf4
ov001_02213048_Lb4:
    mov r6, #0
ov001_02213048_Lb8:
    ldr r0, [r5, #0x1c]
    mov r1, r6
    bl native_fn_0205f98c
    ldrsh r1, [r5, #20]
    ldrsh r2, [r5, #22]
    bl native_fn_02048a60
    add r0, r6, #1
    and r6, r0, #255
    cmp r6, #24
    blo ov001_02213048_Lb8
    mov r0, #3
    str r0, [r5, #0x34]
    b ov001_02213048_Lf4
ov001_02213048_Lec:
    mov r1, #1
    bl native_fn_02212f14
ov001_02213048_Lf4:
    cmp r4, #0
    beq ov001_02213048_L104
    mov r0, r5
    bl ov001_02213048_L0
ov001_02213048_L104:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
