/* ov000 row 0x022114dc: 84 bytes.
 *
 * What it does: 21 instructions; 4 call(s) to 0x02211210, 0x022112a8, 0x02211364, +1 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x14 -> +0x4c
 *   test +0x10 cmp r0, #0
 *   test +0x24 cmp r0, #0
 *   test +0x34 cmp r0, #0
 *   test +0x44 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022114dc; the literal pool and
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

extern void native_fn_02211210(void);
extern void native_fn_022112a8(void);
extern void native_fn_02211364(void);
extern void native_fn_02211420(void);


asm u32 native_ov000_022114dc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    mov r4, #0
    bl native_fn_02211210
    cmp r0, #0
    beq ov000_022114dc_L4c
    mov r0, r5
    orr r4, r4, #1
    bl native_fn_022112a8
    cmp r0, #0
    mov r0, r5
    orrgt r4, r4, #2
    bl native_fn_02211364
    cmp r0, #0
    mov r0, r5
    orrgt r4, r4, #4
    bl native_fn_02211420
    cmp r0, #0
    orrgt r4, r4, #8
ov000_022114dc_L4c:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
