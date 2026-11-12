/* ov001 row 0x02203aa8: 112 bytes.
 *
 * What it does: 28 instructions; 9 call(s) to 0x02207938, 0x021fe6b8, 0x0206c110, +6 more; loops (back edge at +0x10); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 9 calls (28 instructions, 9 calls, 0 branches, 7 back edges, 0 literal slots).
 *
 *   test +0x3c cmp r4, #0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02203aa8; the literal pool and
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

extern void native_fn_02207938(void);
extern void native_fn_021fe6b8(void);
extern void native_fn_0206c110(void);
extern void native_fn_0206c120(void);
extern void native_fn_02203610(void);
extern void native_fn_02202b88(void);
extern void native_fn_022023dc(void);
extern void native_fn_021dc2f8(void);
extern void native_fn_02207944(void);


asm u32 native_ov001_02203aa8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    bl native_fn_02207938
    mov r5, r0
    mov r0, #4
    bl native_fn_021fe6b8
    mov r6, r0
    bl native_fn_0206c110
    mov r7, r0
    bl native_fn_0206c120
    mov r4, r0
    bl native_fn_02203610
    mov r8, r0
    bl native_fn_02202b88
    mov r0, #2
    bl native_fn_022023dc
    cmp r4, #0
    moveq r0, #0
    movne r0, #2
    str r0, [r5, #0x24]
    str r7, [r5, #0x28]
    ldr r0, [r8]
    bl native_fn_021dc2f8
    str r0, [r5, #0x10]
    str r8, [r5, #0x538]
    ldr r0, [r6]
    bl native_fn_02207944
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
