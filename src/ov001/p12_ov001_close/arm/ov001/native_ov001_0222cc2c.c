/* ov001 row 0x0222cc2c: 212 bytes.
 *
 * What it does: 52 instructions; 3 call(s) to 0x02008d78, 0x0203d294, 0x02044cdc; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 3 calls (52 instructions, 3 calls, 10 branches, 4 back edges, 1 literal slot).
 *
 *   pool +0xd0 -> constant 0x02249830 (image word 0x02249830)
 *   branch +0x40 -> +0x58
 *   branch +0x48 -> +0x7c
 *   branch +0x50 -> +0xa0
 *   branch +0x54 -> +0xc0
 *   branch +0x5c -> +0xc0
 *   branch +0x78 -> +0xc0
 *   branch +0x80 -> +0xc0
 *   branch +0x9c -> +0xc0
 *   branch +0xa4 -> +0xc0
 *   back edge +0xc4 -> +0x28
 *   test +0x3c cmp r0, #0
 *   test +0x44 cmp r0, #1
 *   test +0x4c cmp r0, #2
 *   test +0x58 cmp r5, #3
 *   test +0x7c cmp r5, #2
 *   test +0xa0 cmp r5, #0
 *   test +0xc0 cmp r5, #3
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0222cc2c; the literal pool and
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

extern void native_fn_02008d78(void);
extern void native_fn_0203d294(void);
extern void native_fn_02044cdc(void);


asm u32 native_ov001_0222cc2c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    mov r8, r0
    mov r5, #0
    mov r7, r1
    ldr r0, =0x02249830
    mov r1, r5
    mov r2, #12
    mov r6, r5
    bl native_fn_02008d78
    ldr r4, =0x02249830
ov001_0222cc2c_L28:
    mov r0, r7
    bl native_fn_0203d294
    mov r9, r0
    ldr r0, [r8, r9, lsl #2]
    bl native_fn_02044cdc
    cmp r0, #0
    beq ov001_0222cc2c_L58
    cmp r0, #1
    beq ov001_0222cc2c_L7c
    cmp r0, #2
    beq ov001_0222cc2c_La0
    b ov001_0222cc2c_Lc0
ov001_0222cc2c_L58:
    cmp r5, #3
    bhs ov001_0222cc2c_Lc0
    ldr r2, [r8, r9, lsl #2]
    add r1, r5, #1
    add r0, r6, #1
    str r2, [r4, r6, lsl #2]
    and r5, r1, #255
    and r6, r0, #255
    b ov001_0222cc2c_Lc0
ov001_0222cc2c_L7c:
    cmp r5, #2
    bhs ov001_0222cc2c_Lc0
    ldr r2, [r8, r9, lsl #2]
    add r1, r5, #2
    add r0, r6, #1
    str r2, [r4, r6, lsl #2]
    and r5, r1, #255
    and r6, r0, #255
    b ov001_0222cc2c_Lc0
ov001_0222cc2c_La0:
    cmp r5, #0
    bne ov001_0222cc2c_Lc0
    ldr r2, [r8, r9, lsl #2]
    add r1, r5, #3
    add r0, r6, #1
    str r2, [r4, r6, lsl #2]
    and r5, r1, #255
    and r6, r0, #255
ov001_0222cc2c_Lc0:
    cmp r5, #3
    bne ov001_0222cc2c_L28
    mov r0, r6
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
