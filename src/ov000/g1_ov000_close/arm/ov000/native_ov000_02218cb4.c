/* ov000 row 0x02218cb4: 108 bytes.
 *
 * What it does: 26 instructions; 4 call(s) to 0x0204ada4, 0x0204ad90, 0x0204ada4, +1 more; loops (back edge at +0x24); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x68 -> constant 0x02245e54 (image word 0x02245e54)
 *   branch +0x0c -> +0x2c
 *   branch +0x28 -> +0x54
 *   test +0x08 cmp r4, #400
 *   test +0x30 cmp r0, #2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02218cb4; the literal pool and
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

extern void native_fn_0204ada4(void);
extern void native_fn_0204ad90(void);
extern void native_fn_0205fbb4(void);


asm u32 native_ov000_02218cb4 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    cmp r4, #400
    bhs ov000_02218cb4_L2c
    ldr r0, =0x02245e54
    mov r1, r4
    ldr r0, [r0, #0x34]
    mov r2, #3
    mov r3, #1
    bl native_fn_0204ada4
    b ov000_02218cb4_L54
ov000_02218cb4_L2c:
    bl native_fn_0204ad90
    cmp r0, #2
    ldr r0, =0x02245e54
    movlt r2, #2
    movge r2, #1
    ldr r0, [r0, #0x4]
    mov r1, r4
    and r2, r2, #255
    mov r3, #1
    bl native_fn_0204ada4
ov000_02218cb4_L54:
    mov r0, r4
    mov r1, #0
    bl native_fn_0205fbb4
    mov r0, #1
    ldmia sp!, {r4, pc}
}
