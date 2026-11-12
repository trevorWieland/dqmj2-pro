/* ov000 row 0x021f8c84: 144 bytes.
 *
 * What it does: 35 instructions; 6 call(s) to 0x0202a634, 0x0205f98c, 0x02048a54, +3 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x8c -> constant 0x02236f74 (image word 0x02236f74)
 *   branch +0x2c -> +0x58
 *   branch +0x34 -> +0x58
 *   branch +0x40 -> +0x58
 *   branch +0x60 -> +0x80
 *   test +0x10 cmp r0, #0
 *   test +0x28 cmp r1, #0
 *   test +0x30 cmp r1, #1
 *   test +0x3c cmp r0, #0
 *   test +0x5c cmp r0, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f8c84; the literal pool and
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

extern void native_fn_0202a634(void);
extern void native_fn_0205f98c(void);
extern void native_fn_02048a54(void);
extern void native_fn_0204b178(void);
extern void native_fn_0205f9e4(void);


asm u32 native_ov000_021f8c84 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    bl native_fn_0202a634
    ldr r4, =0x02236f74
    ldr r0, [r4, #0x1c]
    cmp r0, #0
    ldmeqia sp!, {r3, r4, r5, pc}
    mov r1, #0
    bl native_fn_0205f98c
    ldr r1, [r4, #0x10]
    mov r5, r0
    cmp r1, #0
    beq ov000_021f8c84_L58
    cmp r1, #1
    bne ov000_021f8c84_L58
    bl native_fn_02048a54
    cmp r0, #0
    bne ov000_021f8c84_L58
    mov r0, r5
    mov r1, #29
    bl native_fn_0204b178
    mov r0, #0
    str r0, [r4, #0x10]
ov000_021f8c84_L58:
    ldr r0, [r4, #0x2c]
    cmp r0, #0
    beq ov000_021f8c84_L80
    mov r0, r5
    mov r1, #30
    bl native_fn_0204b178
    mov r1, #1
    mov r0, #0
    str r1, [r4, #0x10]
    str r0, [r4, #0x2c]
ov000_021f8c84_L80:
    mov r0, r4
    bl native_fn_0205f9e4
    ldmia sp!, {r3, r4, r5, pc}
}
