/* ov001 row 0x0220261c: 56 bytes.
 *
 * What it does: 14 instructions; 3 call(s) to 0x021fd074, 0x021fefb0, 0x02048308; loops (back edge at +0x18); returns through pop {r4, pc}
 *
 * Decoded shape: loop with 3 calls (14 instructions, 3 calls, 0 branches, 3 back edges, 0 literal slots).
 *
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220261c; the literal pool and
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
extern void native_fn_021fefb0(void);
extern void native_fn_02048308(void);


asm u32 native_ov001_0220261c (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    mov r0, r4, lsl #24
    mov r1, r1, lsl #24
    mov r0, r0, asr #24
    mov r1, r1, asr #24
    bl native_fn_021fd074
    ldrsb r1, [r0, #12]
    mov r2, r4, lsl #24
    mov r0, r2, asr #24
    mov r2, #0
    bl native_fn_021fefb0
    bl native_fn_02048308
    ldmia sp!, {r4, pc}
}
