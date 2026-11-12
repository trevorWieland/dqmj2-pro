/* ov006 row 0x021dacb8: 244 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xec -> constant 0x0220f358 (image word 0x0220f358)
 *   pool +0xf0 -> constant 0x0220f34c (image word 0x0220f34c)
 *   branch +0x30 -> +0xc8
 *   branch +0x68 -> +0x98
 *   branch +0x7c -> +0x98
 *   branch +0x94 -> +0xac
 *   back edge +0xc4 -> +0x34
 *   back edge +0xe4 -> +0x20
 *   test +0x14 cmp r0, #0
 *   test +0x2c cmp r8, #0
 *   test +0x64 cmp r0, #1
 *   test +0x78 cmp r0, #0
 *   test +0xb4 cmp r8, r0, asr #24
 *   test +0xe0 cmp r0, r4, asr #24
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021dacb8; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02062aa0(void);
extern void native_fn_02067748(void);
extern void native_fn_02062a50(void);
extern void native_fn_02064654(void);
extern void native_fn_02065bc4(void);


asm u32 native_ov006_021dacb8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r7, #0
    mov r11, r7
    mov r10, r7
    bl native_fn_02062aa0
    cmp r0, #0
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r9, =0x0220f358
ov006_021dacb8_L20:
    ldr r0, =0x0220f34c
    mov r5, #0
    ldr r8, [r0, r10, lsl #2]
    cmp r8, #0
    blt ov006_021dacb8_Lc8
ov006_021dacb8_L34:
    add r0, r11, r5
    add r0, r0, r0, lsl #2
    add r0, r0, #8
    mov r0, r0, lsl #24
    mov r6, r0, asr #24
    bl native_fn_02067748
    mov r4, r0
    mov r0, r10
    bl native_fn_02062a50
    mov r1, r0
    ldr r0, [r4, #0x4]
    bl native_fn_02064654
    cmp r0, #1
    bne ov006_021dacb8_L98
    mov r0, r10
    bl native_fn_02062a50
    ldrb r0, [r0, #0x1d]
    cmp r0, #0
    bne ov006_021dacb8_L98
    mov r0, r9
    mov r1, #3
    mov r2, r6
    add r3, r7, #2
    bl native_fn_02065bc4
    b ov006_021dacb8_Lac
ov006_021dacb8_L98:
    mov r0, r9
    mov r1, #3
    mov r2, r6
    mov r3, #11
    bl native_fn_02065bc4
ov006_021dacb8_Lac:
    add r0, r5, #1
    mov r0, r0, lsl #24
    cmp r8, r0, asr #24
    add r9, r9, #12
    add r7, r7, #1
    mov r5, r0, asr #24
    bge ov006_021dacb8_L34
ov006_021dacb8_Lc8:
    add r0, r10, #1
    add r1, r8, #1
    mov r4, r0, lsl #24
    add r11, r11, r1
    mov r10, r4, asr #24
    bl native_fn_02062aa0
    cmp r0, r4, asr #24
    bgt ov006_021dacb8_L20
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
