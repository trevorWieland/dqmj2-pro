/* ov001 row 0x02204c84: 124 bytes.
 *
 * What it does: 31 instructions; 5 call(s) to 0x02204270, 0x02204250, 0x02204244, +2 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 5 calls (31 instructions, 5 calls, 0 branches, 5 back edges, 0 literal slots).
 *
 *   test +0x1c cmp r5, #127
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02204c84; the literal pool and
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

extern void native_fn_02204270(void);
extern void native_fn_02204250(void);
extern void native_fn_02204244(void);
extern void native_fn_0204b85c(void);
extern void native_fn_0205fa4c(void);


asm u32 native_ov001_02204c84 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #16
    mov r8, r0
    mov r7, r1
    mov r6, r2
    bl native_fn_02204270
    mov r5, r0
    cmp r5, #127
    addeq sp, sp, #16
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    bl native_fn_02204250
    mov r4, r0
    bl native_fn_02204244
    strh r8, [sp, #12]
    strh r7, [sp, #14]
    str r6, [sp]
    mov r2, #192
    str r2, [sp, #0x4]
    mov r12, #9
    add r1, sp, #12
    mov r0, r4
    mov r2, #8
    mov r3, #1
    str r12, [sp, #0x8]
    bl native_fn_0204b85c
    mov r0, r4
    mov r1, #0
    bl native_fn_0205fa4c
    mov r0, r5
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
