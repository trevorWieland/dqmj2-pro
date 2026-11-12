/* ov001 row 0x02203b18: 100 bytes.
 *
 * What it does: 25 instructions; 5 call(s) to 0x0206bc80, 0x022035a0, 0x0220b3e4, +2 more; loops (back edge at +0x10)
 *
 * Decoded shape: loop with 5 calls (25 instructions, 5 calls, 0 branches, 3 back edges, 0 literal slots).
 *
 *   test +0x1c cmp r0, #0
 *   3 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02203b18; the literal pool and
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

extern void native_fn_0206bc80(void);
extern void native_fn_022035a0(void);
extern void native_fn_0220b3e4(void);
extern void native_fn_0206bd24(void);


asm u32 native_ov001_02203b18 (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #28
    add r0, sp, #16
    add r1, sp, #0
    bl native_fn_0206bc80
    add r0, sp, #16
    bl native_fn_022035a0
    cmp r0, #0
    addeq sp, sp, #28
    ldmeqia sp!, {pc}
    ldr r1, [sp, #0x10]
    ldr r2, [sp, #0x14]
    ldr r3, [sp, #0x18]
    mov r0, #0
    bl native_fn_0220b3e4
    add r0, sp, #4
    add r1, sp, #0
    bl native_fn_0206bd24
    ldr r1, [sp, #0x4]
    ldr r2, [sp, #0x8]
    ldr r3, [sp, #0xc]
    mov r0, #2
    bl native_fn_0220b3e4
    add sp, sp, #28
    ldmia sp!, {pc}
}
