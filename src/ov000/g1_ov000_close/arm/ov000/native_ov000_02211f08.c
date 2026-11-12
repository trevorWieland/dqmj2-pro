/* ov000 row 0x02211f08: 100 bytes.
 *
 * What it does: 23 instructions; 3 call(s) to 0x02040838, 0x020410a8, 0x020408f0; loops (back edge at +0x20); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x5c -> constant 0x00000136 (image word 0x00000136)
 *   pool +0x60 -> constant 0x02240fbc (image word 0x02240fbc)
 *   branch +0x14 -> +0x54
 *   branch +0x30 -> +0x54
 *   branch +0x3c -> +0x54
 *   test +0x0c cmp r5, r1
 *   test +0x24 cmp r0, #0
 *   test +0x2c cmpne r1, #0
 *   test +0x38 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02211f08; the literal pool and
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

extern void native_fn_02040838(void);
extern void native_fn_020410a8(void);
extern void native_fn_020408f0(void);


asm u32 native_ov000_02211f08 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r1, =0x00000136
    mov r5, r0
    cmp r5, r1
    mov r4, #0
    bhs ov000_02211f08_L54
    ldr r1, =0x02240fbc
    mov r2, #16
    bl native_fn_02040838
    cmp r0, #0
    ldrneb r1, [r0, #0x39]
    cmpne r1, #0
    beq ov000_02211f08_L54
    bl native_fn_020410a8
    cmp r0, #0
    beq ov000_02211f08_L54
    ldr r1, =0x02240fbc
    mov r0, r5
    mov r2, #16
    bl native_fn_020408f0
    mov r4, #1
ov000_02211f08_L54:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
