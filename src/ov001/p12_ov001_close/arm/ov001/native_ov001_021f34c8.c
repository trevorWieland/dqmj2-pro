/* ov001 row 0x021f34c8: 196 bytes.
 *
 * What it does: 46 instructions; 7 call(s) to 0x02041510, 0x021f3470, 0x021d78a4, +4 more; loops (back edge at +0x28); returns through pop {r3, r4, r5, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 7 calls (46 instructions, 7 calls, 8 branches, 7 back edges, 3 literal slots).
 *
 *   pool +0xb8 -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0xbc -> constant 0x00000492 (image word 0x00000492)
 *   pool +0xc0 -> constant 0x00000b33 (image word 0x00000b33)
 *   branch +0x18 -> +0xb0
 *   branch +0x30 -> +0x70
 *   branch +0x48 -> +0x5c
 *   branch +0x58 -> +0x68
 *   branch +0x6c -> +0xb0
 *   branch +0x78 -> +0xb0
 *   branch +0x94 -> +0xa4
 *   branch +0xa0 -> +0xac
 *   test +0x14 cmp r0, #0
 *   test +0x2c cmp r5, #1
 *   test +0x3c cmp r0, #0
 *   test +0x70 cmp r5, #2
 *   test +0x74 cmpne r5, #4
 *   test +0x84 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f34c8; the literal pool and
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

extern void native_fn_02041510(void);
extern void native_fn_021f3470(void);
extern void native_fn_021d78a4(void);


asm u32 native_ov001_021f34c8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r1, =0x0223989c
    mov r5, r0
    ldrb r0, [r1, #0x29]
    mov r4, #0
    cmp r0, #0
    beq ov001_021f34c8_Lb0
    mov r0, r4
    mov r1, #3
    mov r2, #20
    bl native_fn_02041510
    cmp r5, #1
    bne ov001_021f34c8_L70
    mvn r0, #0
    bl native_fn_021f3470
    cmp r0, #0
    ldr r1, =0x00000492
    mov r2, #30
    beq ov001_021f34c8_L5c
    mov r0, r4
    mov r3, #40960
    bl native_fn_021d78a4
    b ov001_021f34c8_L68
ov001_021f34c8_L5c:
    ldr r3, =0x00000b33
    mov r0, r4
    bl native_fn_021d78a4
ov001_021f34c8_L68:
    mov r4, #1
    b ov001_021f34c8_Lb0
ov001_021f34c8_L70:
    cmp r5, #2
    cmpne r5, #4
    bne ov001_021f34c8_Lb0
    mvn r0, #0
    bl native_fn_021f3470
    cmp r0, #0
    ldr r1, =0x00000492
    mov r0, #1
    mov r2, #40
    beq ov001_021f34c8_La4
    mov r3, #40960
    bl native_fn_021d78a4
    b ov001_021f34c8_Lac
ov001_021f34c8_La4:
    mov r3, #12288
    bl native_fn_021d78a4
ov001_021f34c8_Lac:
    mov r4, #1
ov001_021f34c8_Lb0:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
