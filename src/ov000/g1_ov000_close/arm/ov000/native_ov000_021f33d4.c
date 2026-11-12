/* ov000 row 0x021f33d4: 216 bytes.
 *
 * What it does: 50 instructions; 3 call(s) to 0x0203cc2c, 0x0203cc2c, 0x0203cc2c; loops (back edge at +0x24); returns through pop {r4, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xc8 -> constant 0x02236ec0 (image word 0x02236ec0)
 *   pool +0xcc -> native_data_0222eec0 (image word 0x0222eec0)
 *   pool +0xd0 -> native_data_0222eed0 (image word 0x0222eed0)
 *   pool +0xd4 -> native_data_0222eee0 (image word 0x0222eee0)
 *   branch +0x3c -> +0x48
 *   branch +0x78 -> +0x84
 *   branch +0xb4 -> +0xc0
 *   test +0x10 cmp r0, #0
 *   test +0x2c cmp r0, #0
 *   test +0x4c cmp r0, #0
 *   test +0x68 cmp r0, #0
 *   test +0x88 cmp r0, #0
 *   test +0xa4 cmp r0, #0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f33d4; the literal pool and
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

extern u8 native_data_0222eec0[];
extern void native_fn_0203cc2c(void);
extern u8 native_data_0222eed0[];
extern u8 native_data_0222eee0[];


asm u32 native_ov000_021f33d4 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r1, =0x02236ec0
    mov r4, r0
    ldr r0, [r1, #0x10]
    cmp r0, #0
    movne r0, #0
    ldmneia sp!, {r4, pc}
    ldr r0, =native_data_0222eec0
    mov r1, r4
    bl native_fn_0203cc2c
    ldr r1, =0x02236ec0
    cmp r0, #0
    str r0, [r1, #0x10]
    addne r0, r0, #8
    strne r0, [r1, #0xc]
    bne ov000_021f33d4_L48
    mov r0, #0
    ldmia sp!, {r4, pc}
ov000_021f33d4_L48:
    ldr r0, [r1, #0x8]
    cmp r0, #0
    movne r0, #0
    ldmneia sp!, {r4, pc}
    ldr r0, =native_data_0222eed0
    mov r1, r4
    bl native_fn_0203cc2c
    ldr r1, =0x02236ec0
    cmp r0, #0
    str r0, [r1, #0x8]
    addne r0, r0, #8
    strne r0, [r1, #0x4]
    bne ov000_021f33d4_L84
    mov r0, #0
    ldmia sp!, {r4, pc}
ov000_021f33d4_L84:
    ldr r0, [r1]
    cmp r0, #0
    movne r0, #0
    ldmneia sp!, {r4, pc}
    ldr r0, =native_data_0222eee0
    mov r1, r4
    bl native_fn_0203cc2c
    ldr r1, =0x02236ec0
    cmp r0, #0
    str r0, [r1]
    addne r0, r0, #8
    strne r0, [r1, #0x14]
    bne ov000_021f33d4_Lc0
    mov r0, #0
    ldmia sp!, {r4, pc}
ov000_021f33d4_Lc0:
    mov r0, #1
    ldmia sp!, {r4, pc}
}
