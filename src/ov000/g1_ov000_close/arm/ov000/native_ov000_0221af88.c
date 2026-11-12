/* ov000 row 0x0221af88: 232 bytes.
 *
 * What it does: 56 instructions; 10 call(s) to 0x02062378, 0x02062520, 0x02041814, +7 more; loops (back edge at +0x30); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xe0 -> constant 0x022460d4 (image word 0x022460d4)
 *   pool +0xe4 -> constant 0x02246090 (image word 0x02246090)
 *   branch +0x10 -> +0x20
 *   branch +0x18 -> +0xac
 *   branch +0x1c -> +0xd0
 *   branch +0x2c -> +0x80
 *   branch +0x38 -> +0x90
 *   branch +0x44 -> +0x90
 *   branch +0x50 -> +0x90
 *   branch +0xa8 -> +0xd8
 *   branch +0xcc -> +0xd8
 *   test +0x0c cmp r0, #9
 *   test +0x14 cmp r0, #10
 *   test +0x28 cmp r0, #0
 *   test +0x34 cmp r0, #16
 *   test +0x40 cmp r0, #0
 *   test +0x4c cmp r0, #1
 *   test +0x84 cmp r0, #1
 *   test +0xb0 cmp r0, #1
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221af88; the literal pool and
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

extern void native_fn_02062378(void);
extern void native_fn_02062520(void);
extern void native_fn_02041814(void);
extern void native_fn_022212b8(void);
extern void native_fn_021eada8(void);
extern void native_fn_0207ce20(void);
extern void native_fn_0221e6cc(void);


asm u32 native_ov000_0221af88 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x022460d4
    ldrsb r0, [r0, #16]
    cmp r0, #9
    beq ov000_0221af88_L20
    cmp r0, #10
    beq ov000_0221af88_Lac
    b ov000_0221af88_Ld0
ov000_0221af88_L20:
    ldr r0, =0x02246090
    ldr r0, [r0, #0x30]
    cmp r0, #0
    beq ov000_0221af88_L80
    bl native_fn_02062378
    cmp r0, #16
    bne ov000_0221af88_L90
    bl native_fn_02062520
    cmp r0, #0
    beq ov000_0221af88_L90
    bl native_fn_02041814
    cmp r0, #1
    beq ov000_0221af88_L90
    add r0, sp, #2
    add r1, sp, #0
    bl native_fn_022212b8
    ldrsh r0, [sp, #2]
    ldrb r1, [sp]
    bl native_fn_021eada8
    ldr r0, =0x02246090
    mov r1, #0
    str r1, [r0, #0x30]
    mov r0, #1
    ldmia sp!, {r3, pc}
ov000_0221af88_L80:
    bl native_fn_02041814
    cmp r0, #1
    movne r0, #1
    ldmneia sp!, {r3, pc}
ov000_0221af88_L90:
    ldr r0, =0x022460d4
    bl native_fn_0207ce20
    ldr r1, =0x02246090
    ldr r0, =0x022460d4
    ldr r1, [r1, #0x20]
    bl native_fn_0221e6cc
    b ov000_0221af88_Ld8
ov000_0221af88_Lac:
    bl native_fn_02041814
    cmp r0, #1
    movne r0, #1
    ldmneia sp!, {r3, pc}
    ldr r1, =0x02246090
    ldr r0, =0x022460d4
    ldr r1, [r1, #0x20]
    bl native_fn_0221e6cc
    b ov000_0221af88_Ld8
ov000_0221af88_Ld0:
    mov r0, #1
    ldmia sp!, {r3, pc}
ov000_0221af88_Ld8:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
