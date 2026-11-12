/* ov000 row 0x02214970: 108 bytes.
 *
 * What it does: 23 instructions; 7 call(s) to 0x0205bfd4, 0x021d99ac, 0x02028dac, +4 more; loops (back edge at +0x04); returns through pop {r3, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x5c -> constant 0x02245028 (image word 0x02245028)
 *   pool +0x60 -> constant 0x02244fd0 (image word 0x02244fd0)
 *   pool +0x64 -> constant 0x02244f4c (image word 0x02244f4c)
 *   pool +0x68 -> constant 0x02244efc (image word 0x02244efc)
 *   test +0x08 cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02214970; the literal pool and
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

extern void native_fn_0205bfd4(void);
extern void native_fn_021d99ac(void);
extern void native_fn_02028dac(void);
extern void native_fn_020410a8(void);
extern void native_fn_0202ac4c(void);
extern void native_fn_0202a498(void);
extern void native_fn_02028280(void);


asm u32 native_ov000_02214970 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_0205bfd4
    cmp r0, #0
    movne r0, #2
    moveq r0, #0
    bl native_fn_021d99ac
    ldr r0, =0x02245028
    bl native_fn_02028dac
    ldr r0, =0x02244fd0
    bl native_fn_020410a8
    ldr r0, =0x02244f4c
    bl native_fn_0202ac4c
    ldr r1, =0x02244efc
    mov r0, #1
    ldr r1, [r1, #0x8]
    bl native_fn_0202a498
    ldr r0, =0x02244efc
    ldr r0, [r0, #0x4]
    bl native_fn_02028280
    ldr r0, =0x02244efc
    mov r1, #0
    strb r1, [r0, #0x1]
    ldmia sp!, {r3, pc}
}
