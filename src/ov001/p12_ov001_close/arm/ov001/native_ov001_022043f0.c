/* ov001 row 0x022043f0: 128 bytes.
 *
 * What it does: 32 instructions; 4 call(s) to 0x021fd074, 0x0204b1c4, 0x0204b380, +1 more; loops (back edge at +0x28); returns through pop {r4, r5, r6, r7, pc}
 *
 * Decoded shape: block fill (32 instructions, 4 calls, 0 branches, 3 back edges, 0 literal slots).
 *
 *   1 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022043f0; the literal pool and
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
extern void native_fn_0204b1c4(void);
extern void native_fn_0204b380(void);
extern void native_fn_02204470(void);


asm u32 native_ov001_022043f0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #12
    mov r5, r1
    mov r4, r2
    mov r2, r4, lsl #24
    mov r1, r5, lsl #24
    mov r6, r0
    mov r0, r1, asr #24
    mov r1, r2, asr #24
    mov r7, r3
    bl native_fn_021fd074
    ldrb r2, [r0, #0x4]
    mov r3, #5
    mov r1, #0
    strh r2, [sp, #8]
    ldrb r12, [r0, #0x5]
    mov r0, r6
    add r2, sp, #8
    strh r12, [sp, #10]
    stmia sp, {r3, r7}
    mov r3, #1
    bl native_fn_0204b1c4
    mov r0, r6
    mov r1, #1
    bl native_fn_0204b380
    mov r0, r6
    mov r1, r5
    mov r2, r4
    bl native_fn_02204470
    mov r0, #0
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, pc}
}
