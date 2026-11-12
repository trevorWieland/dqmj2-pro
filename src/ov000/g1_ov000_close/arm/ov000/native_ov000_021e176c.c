/* ov000 row 0x021e176c: 192 bytes.
 *
 * What it does: 43 instructions; 9 call(s) to 0x0205c208, 0x02025a28, 0x02025ca4, +6 more; loops (back edge at +0x04); returns through pop {r4, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xac -> constant 0x0b60b60b (image word 0x0b60b60b)
 *   pool +0xb0 -> constant 0x020d3fe0 (image word 0x020d3fe0)
 *   pool +0xb4 -> constant 0x45800000 (image word 0x45800000)
 *   pool +0xb8 -> constant 0x02232344 (image word 0x02232344)
 *   pool +0xbc -> constant 0x022322d4 (image word 0x022322d4)
 *   branch +0x10 -> +0x8c
 *   test +0x08 cmp r0, #0
 *   test +0x94 cmp r4, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e176c; the literal pool and
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

extern void native_fn_0205c208(void);
extern void native_fn_02025a28(void);
extern void native_fn_02025ca4(void);
extern void native_fn_020259b4(void);
extern void native_fn_02025578(void);
extern void native_fn_020259e8(void);
extern void native_fn_021e035c(void);
extern void native_fn_02042c0c(void);


asm u32 native_ov000_021e176c (register u32 a0)
{
    stmdb sp!, {r4, lr}
    bl native_fn_0205c208
    cmp r0, #0
    moveq r4, #31
    beq ov000_021e176c_L8c
    mov r0, #737280
    rsb r0, r0, #0
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
    bl native_fn_020259b4
    ldr r1, =0x0b60b60b
    mov r2, #182
    umull r12, r3, r0, r1
    mla r3, r0, r2, r3
    mov r0, r0, asr #31
    mla r3, r0, r1, r3
    adds r0, r12, #0
    adc r0, r3, #2048
    mov r0, r0, lsl #4
    mov r0, r0, lsr #16
    mov r1, r0, asr #4
    ldr r0, =0x020d3fe0
    mov r1, r1, lsl #2
    ldrsh r0, [r0, r1]
    add r0, r0, #4096
    mov r0, r0, asr #1
    mov r0, r0, lsl #4
    bl native_fn_02025a28
    ldr r1, =0x45800000
    bl native_fn_02025578
    bl native_fn_020259e8
    and r0, r0, #255
    add r0, r0, #4
    and r4, r0, #255
ov000_021e176c_L8c:
    ldr r0, =0x02232344
    bl native_fn_021e035c
    cmp r4, r0
    movhs r4, r0
    ldr r0, =0x022322d4
    mov r1, r4
    bl native_fn_02042c0c
    ldmia sp!, {r4, pc}
}
