/* ov001 row 0x0220d468: 284 bytes.
 *
 * What it does: 71 instructions; 1 call(s) to 0x02065d88; loops (back edge at +0x08); returns through pop {r4, pc}
 *
 * Decoded shape: loop with 1 call (71 instructions, 1 call, 40 branches, 1 back edge, 0 literal slots).
 *
 *   branch +0x14 -> +0x6c
 *   branch +0x18 -> +0xc8
 *   branch +0x20 -> +0x60
 *   branch +0x24 -> +0xd0
 *   branch +0x30 -> +0x114
 *   branch +0x34 -> +0x114
 *   branch +0x38 -> +0x114
 *   branch +0x3c -> +0x114
 *   branch +0x40 -> +0x114
 *   branch +0x44 -> +0xb8
 *   branch +0x48 -> +0xc0
 *   branch +0x4c -> +0xd8
 *   branch +0x50 -> +0xe0
 *   branch +0x54 -> +0xe8
 *   branch +0x58 -> +0xf0
 *   branch +0x5c -> +0xf8
 *   branch +0x68 -> +0x114
 *   branch +0x70 -> +0x84
 *   branch +0x74 -> +0xe8
 *   branch +0x80 -> +0x114
 *   branch +0x88 -> +0x94
 *   branch +0x8c -> +0x100
 *   branch +0x90 -> +0x114
 *   branch +0xa0 -> +0x114
 *   branch +0xa4 -> +0x108
 *   branch +0xa8 -> +0x110
 *   branch +0xac -> +0x100
 *   branch +0xb0 -> +0x108
 *   branch +0xb4 -> +0x110
 *   branch +0xbc -> +0x114
 *   branch +0xc4 -> +0x114
 *   branch +0xcc -> +0x114
 *   branch +0xd4 -> +0x114
 *   branch +0xdc -> +0x114
 *   branch +0xe4 -> +0x114
 *   branch +0xec -> +0x114
 *   branch +0xf4 -> +0x114
 *   branch +0xfc -> +0x114
 *   branch +0x104 -> +0x114
 *   branch +0x10c -> +0x114
 *   test +0x10 cmp r0, #33
 *   test +0x1c cmp r0, #31
 *   test +0x28 cmp r0, #10
 *   test +0x60 cmp r0, #32
 *   test +0x6c cmp r0, #35
 *   test +0x78 cmp r0, #34
 *   test +0x84 cmp r0, #36
 *   test +0x98 cmp r0, #4
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220d468; the literal pool and
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

extern void native_fn_02065d88(void);


asm u32 native_ov001_0220d468 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, #0
    bl native_fn_02065d88
    ldrb r0, [r0, #0x28]
    cmp r0, #33
    bgt ov001_0220d468_L6c
    bge ov001_0220d468_Lc8
    cmp r0, #31
    bgt ov001_0220d468_L60
    bge ov001_0220d468_Ld0
    cmp r0, #10
    addls pc, pc, r0, lsl #2
    b ov001_0220d468_L114
    b ov001_0220d468_L114
    b ov001_0220d468_L114
    b ov001_0220d468_L114
    b ov001_0220d468_L114
    b ov001_0220d468_Lb8
    b ov001_0220d468_Lc0
    b ov001_0220d468_Ld8
    b ov001_0220d468_Le0
    b ov001_0220d468_Le8
    b ov001_0220d468_Lf0
    b ov001_0220d468_Lf8
ov001_0220d468_L60:
    cmp r0, #32
    orreq r4, r4, #1024
    b ov001_0220d468_L114
ov001_0220d468_L6c:
    cmp r0, #35
    bgt ov001_0220d468_L84
    bge ov001_0220d468_Le8
    cmp r0, #34
    orreq r4, r4, #256
    b ov001_0220d468_L114
ov001_0220d468_L84:
    cmp r0, #36
    bgt ov001_0220d468_L94
    beq ov001_0220d468_L100
    b ov001_0220d468_L114
ov001_0220d468_L94:
    sub r0, r0, #37
    cmp r0, #4
    addls pc, pc, r0, lsl #2
    b ov001_0220d468_L114
    b ov001_0220d468_L108
    b ov001_0220d468_L110
    b ov001_0220d468_L100
    b ov001_0220d468_L108
    b ov001_0220d468_L110
ov001_0220d468_Lb8:
    orr r4, r4, #64
    b ov001_0220d468_L114
ov001_0220d468_Lc0:
    orr r4, r4, #512
    b ov001_0220d468_L114
ov001_0220d468_Lc8:
    orr r4, r4, #2048
    b ov001_0220d468_L114
ov001_0220d468_Ld0:
    orr r4, r4, #3072
    b ov001_0220d468_L114
ov001_0220d468_Ld8:
    orr r4, r4, #3648
    b ov001_0220d468_L114
ov001_0220d468_Le0:
    orr r4, r4, #65536
    b ov001_0220d468_L114
ov001_0220d468_Le8:
    orr r4, r4, #2
    b ov001_0220d468_L114
ov001_0220d468_Lf0:
    orr r4, r4, #536870912
    b ov001_0220d468_L114
ov001_0220d468_Lf8:
    orr r4, r4, #32
    b ov001_0220d468_L114
ov001_0220d468_L100:
    orr r4, r4, #4
    b ov001_0220d468_L114
ov001_0220d468_L108:
    orr r4, r4, #8
    b ov001_0220d468_L114
ov001_0220d468_L110:
    orr r4, r4, #16
ov001_0220d468_L114:
    mov r0, r4
    ldmia sp!, {r4, pc}
}
