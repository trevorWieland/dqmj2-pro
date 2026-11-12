/* ov001 row 0x02217f04: 88 bytes.
 *
 * What it does: 21 instructions; 6 call(s) to 0x021dba58, 0x021d8b4c, 0x021d8b78, +3 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block load (21 instructions, 6 calls, 0 branches, 6 back edges, 1 literal slot).
 *
 *   pool +0x54 -> constant 0x02242c50 (image word 0x02242c50)
 *   test +0x10 cmp r0, #0
 *   1 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02217f04; the literal pool and
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

extern void native_fn_021dba58(void);
extern void native_fn_021d8b4c(void);
extern void native_fn_021d8b78(void);
extern void native_fn_02217ec0(void);
extern void native_fn_02217ee8(void);
extern void native_fn_021d95b0(void);


asm u32 native_ov001_02217f04 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r0, #1
    mov r1, #2
    bl native_fn_021dba58
    cmp r0, #0
    movne r4, #9
    moveq r4, #8
    mov r0, r4
    mov r1, #0
    bl native_fn_021d8b4c
    mov r5, r0
    mov r0, r4
    bl native_fn_021d8b78
    mov r4, r0
    ldmia r5, {r0, r1, r2}
    bl native_fn_02217ec0
    mov r0, r4
    bl native_fn_02217ee8
    ldr r0, =0x02242c50
    bl native_fn_021d95b0
    ldmia sp!, {r3, r4, r5, pc}
}
