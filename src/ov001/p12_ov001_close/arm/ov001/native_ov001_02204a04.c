/* ov001 row 0x02204a04: 156 bytes.
 *
 * What it does: 39 instructions; 9 call(s) to 0x021db438, 0x021db530, 0x02204270, +6 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 9 calls (39 instructions, 9 calls, 0 branches, 9 back edges, 0 literal slots).
 *
 *   test +0x24 cmp r5, #127
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02204a04; the literal pool and
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

extern void native_fn_021db438(void);
extern void native_fn_021db530(void);
extern void native_fn_02204270(void);
extern void native_fn_02204250(void);
extern void native_fn_02204244(void);
extern void native_fn_021db9e0(void);
extern void native_fn_022042ac(void);
extern void native_fn_02202384(void);
extern void native_fn_02202398(void);


asm u32 native_ov001_02204a04 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r7, r0
    mov r6, r1
    bl native_fn_021db438
    mov r8, r0
    mov r0, r7
    bl native_fn_021db530
    bl native_fn_02204270
    mov r5, r0
    cmp r5, #127
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    bl native_fn_02204250
    mov r4, r0
    bl native_fn_02204244
    mov r0, r8
    bl native_fn_021db9e0
    add r1, r0, #1
    str r1, [r4, #0x2c]
    mov r0, r5
    strb r1, [r4, #0x22]
    bl native_fn_022042ac
    mov r0, r7, lsl #24
    mov r1, #3
    mov r0, r0, asr #24
    str r1, [r4]
    bl native_fn_02202384
    mov r2, r6, lsl #24
    mov r1, r7, lsl #24
    strh r0, [r4, #20]
    mov r0, r1, asr #24
    mov r1, r2, asr #24
    bl native_fn_02202398
    strh r0, [r4, #22]
    mov r0, #5
    strb r0, [r4, #0x20]
    mov r1, #3
    mov r0, r5
    strb r1, [r4, #0x21]
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
