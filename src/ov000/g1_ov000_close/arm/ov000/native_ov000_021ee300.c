/* ov000 row 0x021ee300: 132 bytes.
 *
 * What it does: 32 instructions; 3 call(s) to 0x02062d04, 0x021ee384, 0x021ee384; loops (back edge at +0x20); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x80 -> constant 0x02236bc4 (image word 0x02236bc4)
 *   branch +0x3c -> +0x5c
 *   test +0x18 cmp r0, #0
 *   test +0x38 cmp r0, #1
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021ee300; the literal pool and
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

extern void native_fn_02062d04(void);
extern void native_fn_021ee384(void);


asm u32 native_ov000_021ee300 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x02236bc4
    ldr r1, [r0, #0x4]
    ldr r0, [r1, #0x10]
    add r0, r1, r0, lsl #2
    ldr r0, [r0, #0x104]
    cmp r0, #0
    ldmeqia sp!, {r3, pc}
    bl native_fn_02062d04
    ldr r1, =0x02236bc4
    ldr r2, [r1, #0x4]
    strb r0, [r2, #0x505]
    ldr r0, [r1, #0x4]
    ldrsb r0, [r0, #32]
    cmp r0, #1
    bne ov000_021ee300_L5c
    mov r0, #99
    bl native_fn_021ee384
    ldr r1, =0x02236bc4
    ldr r1, [r1, #0x4]
    add r1, r1, #1280
    strh r0, [r1, #8]
    ldmia sp!, {r3, pc}
ov000_021ee300_L5c:
    mvn r0, #98
    bl native_fn_021ee384
    ldr r2, =0x02236bc4
    mvn r1, #0
    ldr r2, [r2, #0x4]
    smulbb r1, r0, r1
    add r0, r2, #1280
    strh r1, [r0, #8]
    ldmia sp!, {r3, pc}
}
