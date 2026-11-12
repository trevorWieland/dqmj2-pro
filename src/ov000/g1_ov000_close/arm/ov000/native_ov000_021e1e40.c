/* ov000 row 0x021e1e40: 352 bytes.
 *
 * What it does: 86 instructions; 5 call(s) to 0x021d8528, 0x021d8a44, 0x02028158, +2 more; loops (back edge at +0xf0); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x158 -> constant 0x022322c4 (image word 0x022322c4)
 *   pool +0x15c -> constant 0x022322d4 (image word 0x022322d4)
 *   branch +0x1c -> +0x48
 *   branch +0x20 -> +0xb0
 *   branch +0x28 -> +0x3c
 *   branch +0x2c -> +0x94
 *   branch +0x34 -> +0xa4
 *   branch +0x38 -> +0xe8
 *   branch +0x40 -> +0x7c
 *   branch +0x44 -> +0xe8
 *   branch +0x4c -> +0x60
 *   branch +0x50 -> +0x88
 *   branch +0x58 -> +0xbc
 *   branch +0x5c -> +0xe8
 *   branch +0x64 -> +0x70
 *   branch +0x68 -> +0xcc
 *   branch +0x6c -> +0xe8
 *   branch +0x74 -> +0xd8
 *   branch +0x78 -> +0xe8
 *   branch +0x84 -> +0xf0
 *   branch +0x90 -> +0xf0
 *   branch +0xa0 -> +0xf0
 *   branch +0xac -> +0xf0
 *   branch +0xb8 -> +0xf0
 *   branch +0xc8 -> +0xf0
 *   branch +0xd4 -> +0xf0
 *   branch +0xe4 -> +0xf0
 *   branch +0x11c -> +0x128
 *   test +0x18 cmp r0, #80
 *   test +0x24 cmp r0, #32
 *   test +0x30 cmp r0, #16
 *   test +0x3c cmp r0, #64
 *   test +0x48 cmp r0, #128
 *   test +0x54 cmp r0, #96
 *   test +0x60 cmp r0, #144
 *   test +0x70 cmp r0, #160
 *   test +0x114 cmp r0, r1
 *   test +0x120 cmp r0, #122880
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e1e40; the literal pool and
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

extern void native_fn_021d8528(void);
extern void native_fn_021d8a44(void);
extern void native_fn_02028158(void);


asm u32 native_ov000_021e1e40 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r0, =0x022322c4
    ldr r4, =0x022322d4
    ldr r0, [r0, #0x4]
    ldrh r0, [r0]
    and r0, r0, #240
    cmp r0, #80
    bgt ov000_021e1e40_L48
    bge ov000_021e1e40_Lb0
    cmp r0, #32
    bgt ov000_021e1e40_L3c
    bge ov000_021e1e40_L94
    cmp r0, #16
    beq ov000_021e1e40_La4
    b ov000_021e1e40_Le8
ov000_021e1e40_L3c:
    cmp r0, #64
    beq ov000_021e1e40_L7c
    b ov000_021e1e40_Le8
ov000_021e1e40_L48:
    cmp r0, #128
    bgt ov000_021e1e40_L60
    bge ov000_021e1e40_L88
    cmp r0, #96
    beq ov000_021e1e40_Lbc
    b ov000_021e1e40_Le8
ov000_021e1e40_L60:
    cmp r0, #144
    bgt ov000_021e1e40_L70
    beq ov000_021e1e40_Lcc
    b ov000_021e1e40_Le8
ov000_021e1e40_L70:
    cmp r0, #160
    beq ov000_021e1e40_Ld8
    b ov000_021e1e40_Le8
ov000_021e1e40_L7c:
    mov r5, #737280
    mov r0, #0
    b ov000_021e1e40_Lf0
ov000_021e1e40_L88:
    mov r5, #0
    mov r0, r5
    b ov000_021e1e40_Lf0
ov000_021e1e40_L94:
    mov r5, #368640
    rsb r5, r5, #0
    mov r0, #8192
    b ov000_021e1e40_Lf0
ov000_021e1e40_La4:
    mov r5, #368640
    sub r0, r5, #376832
    b ov000_021e1e40_Lf0
ov000_021e1e40_Lb0:
    mov r5, #552960
    sub r0, r5, #557056
    b ov000_021e1e40_Lf0
ov000_021e1e40_Lbc:
    mov r5, #552960
    rsb r5, r5, #0
    mov r0, #4096
    b ov000_021e1e40_Lf0
ov000_021e1e40_Lcc:
    mov r5, #184320
    sub r0, r5, #188416
    b ov000_021e1e40_Lf0
ov000_021e1e40_Ld8:
    mov r5, #184320
    rsb r5, r5, #0
    mov r0, #4096
    b ov000_021e1e40_Lf0
ov000_021e1e40_Le8:
    mov r5, #0
    mov r0, r5
ov000_021e1e40_Lf0:
    bl native_fn_021d8528
    bl native_fn_021d8a44
    ldr r1, [r0, #0x4c]
    ldr r0, [r4, #0x8c]
    sub r0, r0, r1
    sub r0, r5, r0
    bl native_fn_02028158
    mov r1, #122880
    rsb r1, r1, #0
    cmp r0, r1
    movlt r0, r1
    blt ov000_021e1e40_L128
    cmp r0, #122880
    movgt r0, #122880
ov000_021e1e40_L128:
    ldr r1, [r4, #0x8c]
    add r0, r1, r0
    str r0, [r4, #0x8c]
    bl native_fn_02028158
    mov r1, #1
    str r0, [r4, #0x8c]
    ldr r0, =0x022322d4
    strb r1, [r4, #0x9]
    mov r1, #0
    str r1, [r0, #0x274]
    mov r0, #4
    ldmia sp!, {r3, r4, r5, pc}
}
