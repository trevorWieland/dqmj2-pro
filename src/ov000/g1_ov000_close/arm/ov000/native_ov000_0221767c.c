/* ov000 row 0x0221767c: 408 bytes.
 *
 * What it does: 101 instructions; 12 call(s) to 0x0221754c, 0x02217534, 0x02217554, +9 more; loops (back edge at +0x14); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x194 -> constant 0x0224532c (image word 0x0224532c)
 *   branch +0x1c -> +0x30
 *   branch +0x38 -> +0x4c
 *   branch +0x54 -> +0x68
 *   branch +0x70 -> +0x84
 *   branch +0x8c -> +0xa0
 *   branch +0xac -> +0xc0
 *   branch +0xc8 -> +0xdc
 *   branch +0xe8 -> +0xfc
 *   branch +0x11c -> +0x130
 *   branch +0x13c -> +0x150
 *   branch +0x15c -> +0x170
 *   test +0x18 cmp r0, #0
 *   test +0x34 cmp r0, #0
 *   test +0x50 cmp r0, #0
 *   test +0x6c cmp r0, #0
 *   test +0x88 cmp r0, #0
 *   test +0xa8 cmp r0, #0
 *   test +0xc4 cmp r0, #2
 *   test +0xe4 cmp r0, #0
 *   test +0x104 tst r1, #128
 *   test +0x118 cmp r0, #0
 *   test +0x138 cmp r0, #0
 *   test +0x158 cmp r0, #0
 *   test +0x178 cmp r0, #0
 *   0 block transfer(s), 14 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221767c; the literal pool and
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

extern void native_fn_0221754c(void);
extern void native_fn_02217534(void);
extern void native_fn_02217554(void);
extern void native_fn_0221756c(void);
extern void native_fn_02217674(void);
extern void native_fn_02217590(void);
extern void native_fn_021fbcb8(void);
extern void native_fn_02063b40(void);
extern void native_fn_0205c25c(void);


asm u32 native_ov000_0221767c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mov r1, #0
    ldr r0, =0x0224532c
    orr r1, r1, #784
    str r1, [r0, #0x28]
    bl native_fn_0221754c
    cmp r0, #0
    beq ov000_0221767c_L30
    ldr r0, =0x0224532c
    ldr r1, [r0, #0x28]
    orr r1, r1, #1
    str r1, [r0, #0x28]
ov000_0221767c_L30:
    bl native_fn_02217534
    cmp r0, #0
    beq ov000_0221767c_L4c
    ldr r0, =0x0224532c
    ldr r1, [r0, #0x28]
    orr r1, r1, #2
    str r1, [r0, #0x28]
ov000_0221767c_L4c:
    bl native_fn_02217554
    cmp r0, #0
    beq ov000_0221767c_L68
    ldr r0, =0x0224532c
    ldr r1, [r0, #0x28]
    orr r1, r1, #4
    str r1, [r0, #0x28]
ov000_0221767c_L68:
    bl native_fn_0221756c
    cmp r0, #0
    beq ov000_0221767c_L84
    ldr r0, =0x0224532c
    ldr r1, [r0, #0x28]
    orr r1, r1, #8
    str r1, [r0, #0x28]
ov000_0221767c_L84:
    bl native_fn_02217674
    cmp r0, #0
    beq ov000_0221767c_La0
    ldr r0, =0x0224532c
    ldr r1, [r0, #0x28]
    orr r1, r1, #32
    str r1, [r0, #0x28]
ov000_0221767c_La0:
    mov r0, #1
    bl native_fn_02217590
    cmp r0, #0
    beq ov000_0221767c_Lc0
    ldr r0, =0x0224532c
    ldr r1, [r0, #0x28]
    orr r1, r1, #1024
    str r1, [r0, #0x28]
ov000_0221767c_Lc0:
    bl native_fn_021fbcb8
    cmp r0, #2
    bne ov000_0221767c_Ldc
    ldr r0, =0x0224532c
    ldr r1, [r0, #0x28]
    orr r1, r1, #64
    str r1, [r0, #0x28]
ov000_0221767c_Ldc:
    mov r0, #4
    bl native_fn_02063b40
    cmp r0, #0
    bne ov000_0221767c_Lfc
    ldr r0, =0x0224532c
    ldr r1, [r0, #0x28]
    orr r1, r1, #128
    str r1, [r0, #0x28]
ov000_0221767c_Lfc:
    ldr r0, =0x0224532c
    ldr r1, [r0, #0x28]
    tst r1, #128
    orrne r1, r1, #2048
    strne r1, [r0, #0x28]
    mov r0, #2
    bl native_fn_0205c25c
    cmp r0, #0
    beq ov000_0221767c_L130
    ldr r0, =0x0224532c
    ldr r1, [r0, #0x28]
    orr r1, r1, #4096
    str r1, [r0, #0x28]
ov000_0221767c_L130:
    mov r0, #4
    bl native_fn_0205c25c
    cmp r0, #0
    beq ov000_0221767c_L150
    ldr r0, =0x0224532c
    ldr r1, [r0, #0x28]
    orr r1, r1, #32768
    str r1, [r0, #0x28]
ov000_0221767c_L150:
    mov r0, #6
    bl native_fn_0205c25c
    cmp r0, #0
    beq ov000_0221767c_L170
    ldr r0, =0x0224532c
    ldr r1, [r0, #0x28]
    orr r1, r1, #8192
    str r1, [r0, #0x28]
ov000_0221767c_L170:
    mov r0, #7
    bl native_fn_0205c25c
    cmp r0, #0
    ldmeqia sp!, {r3, pc}
    ldr r0, =0x0224532c
    ldr r1, [r0, #0x28]
    orr r1, r1, #16384
    str r1, [r0, #0x28]
    ldmia sp!, {r3, pc}
}
