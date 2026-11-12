/* ov001 row 0x02204470: 88 bytes.
 *
 * What it does: 22 instructions; 4 call(s) to 0x021fd074, 0x0206d250, 0x0204b2d0, +1 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: loop with 4 calls (22 instructions, 4 calls, 0 branches, 4 back edges, 0 literal slots).
 *
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02204470; the literal pool and
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
extern void native_fn_0206d250(void);
extern void native_fn_0204b2d0(void);
extern void native_fn_0204b45c(void);


asm u32 native_ov001_02204470 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r1, r1, lsl #24
    mov r5, r0
    mov r2, r2, lsl #24
    mov r0, r1, asr #24
    mov r1, r2, asr #24
    bl native_fn_021fd074
    mov r4, r0
    ldrsb r0, [r4, #12]
    bl native_fn_0206d250
    ldrb r3, [r4, #0x4]
    mov r1, r0
    add r2, sp, #0
    strh r3, [sp]
    ldrb r3, [r4, #0x5]
    mov r0, r5
    strh r3, [sp, #2]
    bl native_fn_0204b2d0
    mov r0, r5
    mov r1, #0
    bl native_fn_0204b45c
    ldmia sp!, {r3, r4, r5, pc}
}
