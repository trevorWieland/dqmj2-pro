/* ov001 row 0x0220473c: 148 bytes.
 *
 * What it does: 37 instructions; 8 call(s) to 0x021fd074, 0x02204270, 0x02204250, +5 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 8 calls (37 instructions, 8 calls, 0 branches, 8 back edges, 0 literal slots).
 *
 *   test +0x1c cmp r5, #127
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220473c; the literal pool and
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
extern void native_fn_02204270(void);
extern void native_fn_02204250(void);
extern void native_fn_02204244(void);
extern void native_fn_022042ac(void);
extern void native_fn_02202384(void);
extern void native_fn_02202398(void);
extern void native_fn_0206d250(void);


asm u32 native_ov001_0220473c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r8, r0
    mov r7, r1
    bl native_fn_021fd074
    mov r6, r0
    bl native_fn_02204270
    mov r5, r0
    cmp r5, #127
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    bl native_fn_02204250
    mov r4, r0
    bl native_fn_02204244
    mov r1, #1
    mov r0, r5
    strb r1, [r4, #0x22]
    bl native_fn_022042ac
    mov r1, #1
    mov r0, r8
    str r1, [r4]
    bl native_fn_02202384
    sub r2, r0, #2
    mov r0, r8
    mov r1, r7
    strh r2, [r4, #20]
    bl native_fn_02202398
    mov r7, r0
    ldrsb r0, [r6, #12]
    bl native_fn_0206d250
    mov r1, #40
    mla r1, r0, r1, r7
    strh r1, [r4, #22]
    mov r0, #6
    strb r0, [r4, #0x20]
    mov r1, #3
    mov r0, r5
    strb r1, [r4, #0x21]
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
