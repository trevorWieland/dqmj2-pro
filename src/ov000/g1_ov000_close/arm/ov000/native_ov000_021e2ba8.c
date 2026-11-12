/* ov000 row 0x021e2ba8: 312 bytes.
 *
 * What it does: 74 instructions; 10 call(s) to 0x021d8c80, 0x021e0d78, 0x021e0078, +7 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x128 -> constant 0x022322c4 (image word 0x022322c4)
 *   pool +0x12c -> constant 0x022322d4 (image word 0x022322d4)
 *   pool +0x130 -> constant 0x022323e4 (image word 0x022323e4)
 *   pool +0x134 -> constant 0x02232344 (image word 0x02232344)
 *   branch +0x18 -> +0x48
 *   branch +0x54 -> +0x7c
 *   branch +0x64 -> +0x7c
 *   branch +0x88 -> +0xe8
 *   branch +0xa8 -> +0xd8
 *   branch +0xf0 -> +0x100
 *   test +0x14 cmp r0, #0
 *   test +0x50 cmp r0, #10
 *   test +0x60 cmp r0, #0
 *   test +0x84 cmp r0, #20
 *   test +0xa4 cmp r0, #0
 *   test +0xec cmp r0, #10
 *   4 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e2ba8; the literal pool and
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

extern void native_fn_021d8c80(void);
extern void native_fn_021e0d78(void);
extern void native_fn_021e0078(void);
extern void native_fn_021e01e4(void);
extern void native_fn_021e3140(void);
extern void native_fn_021e07f0(void);
extern void native_fn_0205f35c(void);
extern void native_fn_021d84e8(void);


asm u32 native_ov000_021e2ba8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r0, =0x022322c4
    mov r4, #0
    ldrb r0, [r0]
    ldr r5, =0x022322d4
    cmp r0, #0
    bne ov000_021e2ba8_L48
    mov r0, #1
    bl native_fn_021d8c80
    mov r1, r4
    mov r2, r1
    mov r0, #16
    bl native_fn_021e0d78
    mov r2, r4
    ldr r0, =0x022322c4
    mov r1, #10
    strb r2, [r5, #0x161]
    strb r1, [r0]
ov000_021e2ba8_L48:
    ldr r0, =0x022322c4
    ldrb r0, [r0]
    cmp r0, #10
    bne ov000_021e2ba8_L7c
    mov r0, r5
    bl native_fn_021e0078
    cmp r0, #0
    beq ov000_021e2ba8_L7c
    ldr r0, =0x022322c4
    mov r4, #1
    mov r1, #20
    strb r4, [r5, #0x15f]
    strb r1, [r0]
ov000_021e2ba8_L7c:
    ldr r0, =0x022322c4
    ldrb r0, [r0]
    cmp r0, #20
    bne ov000_021e2ba8_Le8
    mov r1, #0
    mov r2, r1
    mov r0, #17
    bl native_fn_021e0d78
    mov r0, r5
    bl native_fn_021e01e4
    cmp r0, #0
    beq ov000_021e2ba8_Ld8
    bl native_fn_021e3140
    mov r1, #0
    mov r0, #2
    strb r1, [r5, #0x210]
    bl native_fn_021e07f0
    mov r0, #1
    bl native_fn_021d8c80
    ldr r0, =0x022322c4
    mov r1, #0
    strb r1, [r0]
    mov r4, #1
ov000_021e2ba8_Ld8:
    ldr r3, =0x022323e4
    add r0, r5, #112
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
ov000_021e2ba8_Le8:
    ldrb r0, [r5, #0x161]
    cmp r0, #10
    bne ov000_021e2ba8_L100
    mvn r0, #0
    mov r1, #157
    bl native_fn_0205f35c
ov000_021e2ba8_L100:
    ldr r0, [r5, #0x8c]
    mov r1, #0
    add r0, r0, #737280
    bl native_fn_021d84e8
    ldr r0, =0x02232344
    ldr r3, =0x022323e4
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
