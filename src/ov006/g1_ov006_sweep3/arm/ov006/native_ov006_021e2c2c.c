/* ov006 row 0x021e2c2c: 96 bytes.
 *
 * What it does: 24 instructions; 5 call(s) to 0x021dff78, 0x02063ee0, 0x02067b58, +2 more; loops (back edge at +0x04); returns through pop {r4, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x2c -> +0x48
 *   test +0x08 cmp r0, #0
 *   test +0x28 cmp r1, r0
 *   test +0x38 cmp r0, #0
 *   test +0x50 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e2c2c; the literal pool and
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

extern void native_fn_021dff78(void);
extern void native_fn_02063ee0(void);
extern void native_fn_02067b58(void);
extern void native_fn_021e2f38(void);
extern void native_fn_02067818(void);


asm u32 native_ov006_021e2c2c (register u32 a0)
{
    stmdb sp!, {r4, lr}
    bl native_fn_021dff78
    cmp r0, #0
    moveq r0, #0
    ldmeqia sp!, {r4, pc}
    bl native_fn_02063ee0
    mov r4, r0
    bl native_fn_02067b58
    ldr r1, [r4]
    ldr r0, [r0, #0x24]
    cmp r1, r0
    bhs ov006_021e2c2c_L48
    bl native_fn_021e2f38
    ldr r0, [r0]
    cmp r0, #0
    moveq r0, #0
    movne r0, #2
    ldmia sp!, {r4, pc}
ov006_021e2c2c_L48:
    bl native_fn_02067818
    ldr r0, [r0]
    cmp r0, #0
    movne r0, #1
    moveq r0, #0
    ldmia sp!, {r4, pc}
}
