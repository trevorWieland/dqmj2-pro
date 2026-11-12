/* ov001 row 0x022025a4: 120 bytes.
 *
 * What it does: 30 instructions; 6 call(s) to 0x021fd074, 0x022049f8, 0x022028c8, +3 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 6 calls (30 instructions, 6 calls, 1 branch, 3 back edges, 0 literal slots).
 *
 *   branch +0x38 -> +0x48
 *   test +0x34 cmp r5, #0
 *   test +0x60 cmp r7, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022025a4; the literal pool and
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

extern void native_fn_021fd074(void);
extern void native_fn_022049f8(void);
extern void native_fn_022028c8(void);
extern void native_fn_021fefb0(void);
extern void native_fn_02048308(void);
extern void native_fn_02204a04(void);


asm u32 native_ov001_022025a4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r5, r0
    mov r4, r1
    mov r0, r5, lsl #24
    mov r1, r4, lsl #24
    mov r0, r0, asr #24
    mov r1, r1, asr #24
    mov r7, r2
    bl native_fn_021fd074
    mov r6, r0
    mov r0, r5
    mov r1, r4
    bl native_fn_022049f8
    cmp r5, #0
    bne ov001_022025a4_L48
    mov r0, r4, lsl #24
    mov r0, r0, asr #24
    bl native_fn_022028c8
ov001_022025a4_L48:
    ldrsb r1, [r6, #12]
    mov r0, r5, lsl #24
    mov r0, r0, asr #24
    mov r2, #1
    bl native_fn_021fefb0
    bl native_fn_02048308
    cmp r7, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, pc}
    mov r0, r5
    mov r1, r4
    bl native_fn_02204a04
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
