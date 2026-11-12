/* ov000 row 0x021fe78c: 100 bytes.
 *
 * What it does: 25 instructions; 3 call(s) to 0x0204b138, 0x0204b138, 0x020496b0; loops (back edge at +0x2c); returns through pop {r4, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   test +0x0c cmpne r0, #0
 *   test +0x1c cmp r0, #0
 *   test +0x40 cmp r1, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fe78c; the literal pool and
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

extern void native_fn_0204b138(void);
extern void native_fn_020496b0(void);


asm u32 native_ov000_021fe78c (register u32 a0)
{
    stmdb sp!, {r4, lr}
    movs r4, r0
    ldrne r0, [r4, #0xc4]
    cmpne r0, #0
    ldmeqia sp!, {r4, pc}
    ldr r0, [r4, #0x4]
    mov r1, #0
    cmp r0, #0
    movgt r2, #1
    movle r2, #0
    add r0, r4, #168
    bl native_fn_0204b138
    ldrh r1, [r4, #12]
    ldr r2, [r4, #0x4]
    ldrh r0, [r4, #14]
    add r1, r2, r1
    cmp r1, r0
    movlt r2, #1
    movge r2, #0
    add r0, r4, #168
    mov r1, #1
    bl native_fn_0204b138
    add r0, r4, #168
    bl native_fn_020496b0
    ldmia sp!, {r4, pc}
}
