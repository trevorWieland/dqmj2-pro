/* ov001 row 0x02204944: 180 bytes.
 *
 * What it does: 45 instructions; 8 call(s) to 0x021db530, 0x02204270, 0x02204250, +5 more; loops (back edge at +0x10); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 8 calls (45 instructions, 8 calls, 1 branch, 8 back edges, 0 literal slots).
 *
 *   branch +0x8c -> +0x9c
 *   test +0x1c cmp r5, #127
 *   test +0x88 cmp r6, #0
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02204944; the literal pool and
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

extern void native_fn_021db530(void);
extern void native_fn_02204270(void);
extern void native_fn_02204250(void);
extern void native_fn_02204244(void);
extern void native_fn_022042ac(void);
extern void native_fn_02202384(void);
extern void native_fn_02202398(void);
extern void native_fn_022047d0(void);


asm u32 native_ov001_02204944 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r8, r0
    mov r7, r1
    mov r6, r2
    bl native_fn_021db530
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
    mov r1, #2
    mov r0, r8, lsl #24
    str r1, [r4]
    sub r1, r1, #3
    str r1, [r4, #0x2c]
    str r8, [r4, #0x30]
    str r7, [r4, #0x34]
    mov r1, #0
    mov r0, r0, asr #24
    strb r1, [r4, #0x24]
    bl native_fn_02202384
    mov r1, r7, lsl #24
    mov r2, r8, lsl #24
    mov r1, r1, asr #24
    strh r0, [r4, #20]
    mov r0, r2, asr #24
    bl native_fn_02202398
    strh r0, [r4, #22]
    cmp r6, #0
    beq ov001_02204944_L9c
    mov r0, r8
    mov r1, r7
    bl native_fn_022047d0
ov001_02204944_L9c:
    mov r0, #6
    strb r0, [r4, #0x20]
    mov r1, #3
    mov r0, r5
    strb r1, [r4, #0x21]
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
