/* ov000 row 0x02205ea8: 432 bytes.
 *
 * What it does: 101 instructions; 29 call(s) to 0x0205c1d0, 0x0205e408, 0x0207df2c, +26 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, pc}; 7 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x194 -> native_data_0222b9f8 (image word 0x0222b9f8)
 *   pool +0x198 -> native_data_0222f5ac (image word 0x0222f5ac)
 *   pool +0x19c -> native_data_0222f5bc (image word 0x0222f5bc)
 *   pool +0x1a0 -> native_data_0222f5cc (image word 0x0222f5cc)
 *   pool +0x1a4 -> native_data_0222f5dc (image word 0x0222f5dc)
 *   pool +0x1a8 -> native_data_0222f5ec (image word 0x0222f5ec)
 *   pool +0x1ac -> native_data_0222f5fc (image word 0x0222f5fc)
 *   back edge +0x64 -> +0x44
 *   branch +0x6c -> +0x8c
 *   branch +0x88 -> +0x94
 *   branch +0xdc -> +0x10c
 *   branch +0x118 -> +0x14c
 *   branch +0x158 -> +0x18c
 *   test +0x24 cmp r0, #0
 *   test +0x44 tst lr, r5, lsl r12
 *   test +0x60 cmp r12, #7
 *   test +0x68 cmp r4, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02205ea8; the literal pool and
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

extern void native_fn_0205c1d0(void);
extern void native_fn_0205e408(void);
extern void native_fn_0207df2c(void);
extern u8 native_data_0222b9f8[];
extern void native_fn_0203d294(void);
extern void native_fn_0205e3c0(void);
extern void native_fn_020625cc(void);
extern void native_fn_02045654(void);
extern void native_fn_02004224(void);
extern void native_fn_02008d78(void);
extern void native_fn_0203d50c(void);
extern u8 native_data_0222f5ac[];
extern void native_fn_0202a8e0(void);
extern u8 native_data_0222f5bc[];
extern void native_fn_0203cc2c(void);
extern void native_fn_020481b8(void);
extern void native_fn_02048308(void);
extern void native_fn_0202a498(void);
extern u8 native_data_0222f5cc[];
extern u8 native_data_0222f5dc[];
extern void native_fn_0204540c(void);
extern u8 native_data_0222f5ec[];
extern u8 native_data_0222f5fc[];
extern void native_fn_0204594c(void);


asm u32 native_ov000_02205ea8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #160
    mov r4, #0
    sub r0, r4, #1
    bl native_fn_0205c1d0
    bl native_fn_0205e408
    add r1, sp, #16
    mov r0, r4
    bl native_fn_0207df2c
    cmp r0, #0
    moveq r0, r4
    streqb r0, [sp, #0x97]
    ldrb lr, [sp, #0x97]
    ldr r3, =native_data_0222b9f8
    mov r12, #0
    add r0, sp, #0
    mov r5, #1
ov000_02205ea8_L44:
    tst lr, r5, lsl r12
    addne r1, r3, r12, lsl #1
    ldrnesh r2, [r1, #2]
    movne r1, r4, lsl #1
    add r12, r12, #1
    addne r4, r4, #1
    strneh r2, [r0, r1]
    cmp r12, #7
    blt ov000_02205ea8_L44
    cmp r4, #0
    ble ov000_02205ea8_L8c
    mov r0, r4
    bl native_fn_0203d294
    add r1, sp, #0
    mov r0, r0, lsl #1
    ldrsh r0, [r1, r0]
    bl native_fn_0205e3c0
    b ov000_02205ea8_L94
ov000_02205ea8_L8c:
    mov r0, #109
    bl native_fn_0205e3c0
ov000_02205ea8_L94:
    bl native_fn_020625cc
    mov r0, #1
    bl native_fn_02045654
    mov r0, #2
    bl native_fn_02045654
    mov r0, #3
    bl native_fn_02045654
    bl native_fn_02004224
    mov r1, #0
    mov r2, #64
    bl native_fn_02008d78
    mov r0, #1
    bl native_fn_0203d50c
    mov r0, #3
    bl native_fn_02045654
    ldr r0, =native_data_0222f5ac
    bl native_fn_0202a8e0
    movs r5, r0
    beq ov000_02205ea8_L10c
    ldr r0, =native_data_0222f5bc
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    mov r2, r5
    mov r1, #0
    bl native_fn_020481b8
    bl native_fn_02048308
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
ov000_02205ea8_L10c:
    ldr r0, =native_data_0222f5cc
    bl native_fn_0202a8e0
    movs r5, r0
    beq ov000_02205ea8_L14c
    ldr r0, =native_data_0222f5dc
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    mov r1, r4
    mov r3, r5
    mov r0, #3
    mov r2, #0
    bl native_fn_0204540c
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
ov000_02205ea8_L14c:
    ldr r0, =native_data_0222f5ec
    bl native_fn_0202a8e0
    movs r5, r0
    beq ov000_02205ea8_L18c
    ldr r0, =native_data_0222f5fc
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    mov r1, r4
    mov r3, r5
    mov r0, #3
    mov r2, #0
    bl native_fn_0204594c
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
ov000_02205ea8_L18c:
    add sp, sp, #160
    ldmia sp!, {r3, r4, r5, pc}
}
