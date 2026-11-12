/* ov000 row 0x0222194c: 116 bytes.
 *
 * What it does: 28 instructions; 3 call(s) to 0x0202a498, 0x0202a498, 0x0222189c; loops (back edge at +0x18); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x70 -> constant 0x02246428 (image word 0x02246428)
 *   branch +0x10 -> +0x28
 *   branch +0x34 -> +0x4c
 *   test +0x0c cmp r1, #0
 *   test +0x30 cmp r1, #0
 *   test +0x54 cmp r0, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0222194c; the literal pool and
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

extern void native_fn_0202a498(void);
extern void native_fn_0222189c(void);


asm u32 native_ov000_0222194c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x02246428
    ldr r1, [r0, #0x8]
    cmp r1, #0
    beq ov000_0222194c_L28
    mov r0, #1
    bl native_fn_0202a498
    ldr r0, =0x02246428
    mov r1, #0
    str r1, [r0, #0x8]
ov000_0222194c_L28:
    ldr r0, =0x02246428
    ldr r1, [r0, #0x4]
    cmp r1, #0
    beq ov000_0222194c_L4c
    mov r0, #1
    bl native_fn_0202a498
    ldr r0, =0x02246428
    mov r1, #0
    str r1, [r0, #0x4]
ov000_0222194c_L4c:
    ldr r0, =0x02246428
    ldr r0, [r0]
    cmp r0, #0
    ldmeqia sp!, {r3, pc}
    bl native_fn_0222189c
    ldr r0, =0x02246428
    mov r1, #0
    str r1, [r0]
    ldmia sp!, {r3, pc}
}
