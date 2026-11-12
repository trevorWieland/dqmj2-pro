/* ov006 row 0x021e767c: 116 bytes.
 *
 * What it does: 29 instructions; 3 call(s) to 0x02049ad0, 0x0204a04c, 0x02085270; loops (back edge at +0x10); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x28 -> +0x6c
 *   test +0x1c cmpne r0, #0
 *   test +0x24 cmpne r5, #0
 *   test +0x48 cmp r0, #127
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e767c; the literal pool and
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

extern void native_fn_02049ad0(void);
extern void native_fn_0204a04c(void);
extern void native_fn_02085270(void);


asm u32 native_ov006_021e767c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r6, r1
    bl native_fn_02049ad0
    movs r4, r0
    ldrne r0, [r4]
    cmpne r0, #0
    ldrne r5, [r0, #0x4]
    cmpne r5, #0
    beq ov006_021e767c_L6c
    ldrb r1, [r6]
    ldrb r2, [r6, #0x1]
    ldrh r3, [r6, #2]
    mov r0, r5
    bl native_fn_0204a04c
    ldrsb r0, [r4, #5]
    mov r2, #0
    cmp r0, #127
    moveq r0, #0
    movne r0, #8
    mov r1, r0, lsl #16
    add r0, r5, #60
    mov r1, r1, asr #16
    bl native_fn_02085270
    mov r0, #1
    ldmia sp!, {r4, r5, r6, pc}
ov006_021e767c_L6c:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
