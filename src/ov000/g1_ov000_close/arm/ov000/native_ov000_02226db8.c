/* ov000 row 0x02226db8: 144 bytes.
 *
 * What it does: 34 instructions; 5 call(s) to 0x02226af8, 0x01ffb324, 0x01ffb230, +2 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x88 -> constant 0x022468b8 (image word 0x022468b8)
 *   pool +0x8c -> native_data_0222feb4 (image word 0x0222feb4)
 *   branch +0x24 -> +0x30
 *   branch +0x38 -> +0x5c
 *   branch +0x50 -> +0x5c
 *   branch +0x74 -> +0x80
 *   test +0x20 cmp r0, #0
 *   test +0x34 cmp r0, #0
 *   test +0x4c cmp r0, #3
 *   test +0x70 cmp r0, #1
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02226db8; the literal pool and
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

extern u8 native_data_0222feb4[];
extern void native_fn_02226af8(void);
extern void native_fn_01ffb324(void);
extern void native_fn_01ffb230(void);
extern void native_fn_02068f60(void);
extern void native_fn_020c9414(void);


asm u32 native_ov000_02226db8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r0, =0x022468b8
    ldr r4, =native_data_0222feb4
    ldrsb r0, [r0, #24]
    add r5, r0, r0, lsl #2
    bl native_fn_02226af8
    ldr r0, =0x022468b8
    ldrsb r0, [r0, #28]
    cmp r0, #0
    beq ov000_02226db8_L30
    mov r0, #1
    bl native_fn_01ffb324
ov000_02226db8_L30:
    bl native_fn_01ffb230
    cmp r0, #0
    bne ov000_02226db8_L5c
    ldr r0, =0x022468b8
    mov r1, #3
    str r1, [r0, #0x14]
    ldrsb r0, [r0, #24]
    cmp r0, #3
    bne ov000_02226db8_L5c
    mov r0, #1
    bl native_fn_02068f60
ov000_02226db8_L5c:
    ldrsb r0, [r4, r5]
    sub r0, r0, #3
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    and r0, r0, #255
    cmp r0, #1
    bhi ov000_02226db8_L80
    mov r0, #10
    bl native_fn_020c9414
ov000_02226db8_L80:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
