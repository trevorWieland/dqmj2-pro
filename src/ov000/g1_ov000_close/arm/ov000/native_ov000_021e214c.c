/* ov000 row 0x021e214c: 204 bytes.
 *
 * What it does: 49 instructions; 8 call(s) to 0x021e4388, 0x021e48dc, 0x02213b68, +5 more; no back edge; returns through pop {r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xc4 -> constant 0x02232344 (image word 0x02232344)
 *   pool +0xc8 -> constant 0x022322d4 (image word 0x022322d4)
 *   branch +0x28 -> +0xb8
 *   branch +0x44 -> +0xb8
 *   branch +0x60 -> +0x78
 *   branch +0x74 -> +0xb8
 *   branch +0x90 -> +0xb8
 *   branch +0xa8 -> +0xb8
 *   test +0x20 cmp r0, #0
 *   test +0x3c cmp r0, #0
 *   test +0x5c cmp r0, #0
 *   test +0x6c cmp r0, #0
 *   test +0x88 cmp r0, #0
 *   test +0xa4 tst r0, #7
 *   test +0xb0 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e214c; the literal pool and
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

extern void native_fn_021e4388(void);
extern void native_fn_021e48dc(void);
extern void native_fn_02213b68(void);
extern void native_fn_02213f4c(void);
extern void native_fn_02213f74(void);
extern void native_fn_021e45b8(void);
extern void native_fn_021e55d8(void);
extern void native_fn_021e57ac(void);


asm u32 native_ov000_021e214c (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #52
    ldr r0, =0x02232344
    add r2, sp, #0
    mov r1, #1
    mov r4, #0
    ldr r5, =0x022322d4
    bl native_fn_021e4388
    cmp r0, #0
    movne r4, #1
    bne ov000_021e214c_Lb8
    add r2, sp, #0
    mov r0, r5
    mov r1, #2
    bl native_fn_021e48dc
    cmp r0, #0
    movne r4, #1
    bne ov000_021e214c_Lb8
    mov r2, r4
    ldr r1, [r5, #0x8c]
    mov r3, r2
    add r0, r5, #112
    bl native_fn_02213b68
    cmp r0, #0
    beq ov000_021e214c_L78
    bl native_fn_02213f4c
    bl native_fn_02213f74
    cmp r0, #0
    moveq r4, #1
    b ov000_021e214c_Lb8
ov000_021e214c_L78:
    ldr r1, [r5, #0x8c]
    add r2, sp, #0
    add r0, r5, #112
    bl native_fn_021e45b8
    cmp r0, #0
    movne r4, #1
    bne ov000_021e214c_Lb8
    mov r1, #1
    mov r0, r5
    mov r2, r1
    bl native_fn_021e55d8
    tst r0, #7
    beq ov000_021e214c_Lb8
    bl native_fn_021e57ac
    cmp r0, #0
    movne r4, #1
ov000_021e214c_Lb8:
    mov r0, r4
    add sp, sp, #52
    ldmia sp!, {r4, r5, pc}
}
