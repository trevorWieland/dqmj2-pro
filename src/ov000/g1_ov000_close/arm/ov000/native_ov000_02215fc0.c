/* ov000 row 0x02215fc0: 244 bytes.
 *
 * What it does: 56 instructions; 10 call(s) to 0x02215fd0, 0x0202a37c, 0x02003edc, +7 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xe0 -> constant 0x0224535c (image word 0x0224535c)
 *   pool +0xe4 -> constant 0x0224532c (image word 0x0224532c)
 *   pool +0xe8 -> native_data_0222f918 (image word 0x0222f918)
 *   pool +0xec -> constant 0x0224536c (image word 0x0224536c)
 *   pool +0xf0 -> constant 0x022459b4 (image word 0x022459b4)
 *   back edge +0x1c -> +0x10
 *   branch +0x38 -> +0x68
 *   branch +0x74 -> +0x84
 *   branch +0x7c -> +0x8c
 *   branch +0x80 -> +0x94
 *   branch +0x88 -> +0xa4
 *   branch +0x90 -> +0xa4
 *   back edge +0xc8 -> +0xac
 *   test +0x18 cmp r2, #4
 *   test +0x34 cmp r0, #0
 *   test +0x70 cmp r0, #0
 *   test +0x78 cmp r0, #14
 *   test +0xc0 cmp r5, #12
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02215fc0; the literal pool and
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

extern u8 native_data_0222f918[];
extern void native_fn_0202a37c(void);
extern void native_fn_02003edc(void);
extern void native_fn_02008e0c(void);
extern void native_fn_021f9a18(void);
extern void native_fn_0222214c(void);
extern void native_fn_022160b4(void);
extern void native_fn_02063270(void);
extern void native_fn_02217308(void);


asm u32 native_ov000_02215fc0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r0, =0x0224535c
    mov r2, #0
    mov r1, #32
ov000_02215fc0_L10:
    str r1, [r0, r2, lsl #2]
    add r2, r2, #1
    cmp r2, #4
    blt ov000_02215fc0_L10
    ldr r0, =0x0224532c
    ldr r1, =native_data_0222f918
    ldr r0, [r0, #0x14]
    mov r2, #18
    strh r2, [r1, #2]
    cmp r0, #0
    bne ov000_02215fc0_L68
    mov r0, #2
    mov r1, #2048
    mov r2, #4
    bl native_fn_0202a37c
    ldr r1, =0x0224532c
    str r0, [r1, #0x14]
    bl native_fn_02003edc
    ldr r1, =0x0224532c
    mov r2, #2048
    ldr r1, [r1, #0x14]
    bl native_fn_02008e0c
ov000_02215fc0_L68:
    ldr r0, =0x0224536c
    ldrsb r0, [r0, #16]
    cmp r0, #0
    beq ov000_02215fc0_L84
    cmp r0, #14
    beq ov000_02215fc0_L8c
    b ov000_02215fc0_L94
ov000_02215fc0_L84:
    bl native_fn_021f9a18
    b ov000_02215fc0_La4
ov000_02215fc0_L8c:
    bl native_fn_0222214c
    b ov000_02215fc0_La4
ov000_02215fc0_L94:
    bl native_fn_022160b4
    ldr r0, =0x022459b4
    mov r1, #1
    strb r1, [r0, #0x494]
ov000_02215fc0_La4:
    ldr r4, =0x022459b4
    mov r5, #0
ov000_02215fc0_Lac:
    and r0, r5, #255
    strb r0, [r4, #0x484]
    bl native_fn_02063270
    add r5, r5, #1
    strb r0, [r4, #0x478]
    cmp r5, #12
    add r4, r4, #1
    blt ov000_02215fc0_Lac
    ldr r0, =0x0224536c
    ldrsb r0, [r0, #16]
    bl native_fn_02217308
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
