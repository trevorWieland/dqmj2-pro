/* ov000 row 0x021f4774: 92 bytes.
 *
 * What it does: 22 instructions; 3 call(s) to 0x02061944, 0x021f47ec, 0x021f47ec; loops (back edge at +0x04); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x58 -> constant 0x02236ee4 (image word 0x02236ee4)
 *   branch +0x28 -> +0x38
 *   branch +0x34 -> +0x40
 *   test +0x24 tst r0, #1
 *   test +0x48 cmp r0, #42
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f4774; the literal pool and
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

extern void native_fn_02061944(void);
extern void native_fn_021f47ec(void);


asm u32 native_ov000_021f4774 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    bl native_fn_02061944
    ldr r1, =0x02236ee4
    mov r5, r0
    ldrb r0, [r1, #0x1]
    mov r4, #0
    add r2, r0, #1
    and r0, r2, #255
    strb r2, [r1, #0x1]
    tst r0, #1
    beq ov000_021f4774_L38
    mov r0, #1
    bl native_fn_021f47ec
    b ov000_021f4774_L40
ov000_021f4774_L38:
    mov r0, #2
    bl native_fn_021f47ec
ov000_021f4774_L40:
    add r0, r5, #512
    ldrsb r0, [r0, #108]
    cmp r0, #42
    movne r4, #1
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
