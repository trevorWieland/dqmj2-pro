/* ov001 row 0x02225354: 192 bytes.
 *
 * What it does: 48 instructions; 6 call(s) to 0x02008e0c, 0x02225380, 0x022253b8, +3 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, pc}
 *
 * Decoded shape: loop with 6 calls (48 instructions, 6 calls, 2 branches, 5 back edges, 0 literal slots).
 *
 *   branch +0x34 -> +0x48
 *   back edge +0x54 -> +0x2c
 *   branch +0x6c -> +0x80
 *   back edge +0x8c -> +0x64
 *   branch +0xa0 -> +0xb4
 *   test +0x30 cmp r0, #0
 *   test +0x40 cmp r0, r4
 *   test +0x4c cmp r2, #3
 *   test +0x68 cmp r0, #0
 *   test +0x78 cmp r0, r4
 *   test +0x84 cmp r3, #3
 *   test +0x9c cmp r4, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02225354; the literal pool and
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

extern void native_fn_02008e0c(void);
extern void native_fn_02223f20(void);


asm u32 native_ov001_02225354 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #12
    mov r5, r1
    add r1, sp, #0
    mov r2, #12
    mov r6, r0
    mov r4, #0
    bl native_fn_02008e0c
    mov r3, r5
    mov r2, r4
    add r1, sp, #0
ov001_02225354_L2c:
    ldr r0, [r1, r2, lsl #2]
    cmp r0, #0
    beq ov001_02225354_L48
    add r0, r3, #512
    ldrsb r0, [r0, #52]
    cmp r0, r4
    movgt r4, r0
ov001_02225354_L48:
    add r2, r2, #1
    cmp r2, #3
    add r3, r3, #1088
    blt ov001_02225354_L2c
    mov r3, #0
    mov r1, r3
    add r2, sp, #0
ov001_02225354_L64:
    ldr r0, [r2, r3, lsl #2]
    cmp r0, #0
    beq ov001_02225354_L80
    add r0, r5, #512
    ldrsb r0, [r0, #52]
    cmp r0, r4
    strlt r1, [r2, r3, lsl #2]
ov001_02225354_L80:
    add r3, r3, #1
    cmp r3, #3
    add r5, r5, #1088
    blt ov001_02225354_L64
    add r0, sp, #0
    bl native_fn_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_02225354_Lb4
    add r0, sp, #0
    mov r1, r6
    mov r2, #12
    bl native_fn_02008e0c
ov001_02225354_Lb4:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, pc}
}
