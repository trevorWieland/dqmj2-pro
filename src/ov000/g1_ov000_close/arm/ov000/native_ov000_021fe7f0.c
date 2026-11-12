/* ov000 row 0x021fe7f0: 128 bytes.
 *
 * What it does: 30 instructions; 5 call(s) to 0x021fe830, 0x0205fa4c, 0x02063bdc, +2 more; loops (back edge at +0x38); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x78 -> constant 0x022372c4 (image word 0x022372c4)
 *   pool +0x7c -> constant 0x022373b4 (image word 0x022373b4)
 *   branch +0x2c -> +0x40
 *   branch +0x3c -> +0x58
 *   back edge +0x70 -> +0x20
 *   test +0x10 cmp r0, #0
 *   test +0x28 cmp r0, #47
 *   test +0x64 cmp r1, r0, asr #24
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fe7f0; the literal pool and
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

extern void native_fn_0205fa4c(void);
extern void native_fn_02063bdc(void);
extern void native_fn_0205f9e4(void);


asm u32 native_ov000_021fe7f0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r4, =0x022372c4
    mov r7, #0
    ldrh r0, [r4, #12]
    cmp r0, #0
    ldmleia sp!, {r3, r4, r5, r6, r7, pc}
    ldr r5, =0x022373b4
    mov r6, r7
ov000_021fe7f0_L20:
    ldr r0, [r4, #0x4]
    add r0, r0, r7
    cmp r0, #47
    blt ov000_021fe7f0_L40
    mov r0, r5
    mov r1, r6
    bl native_fn_0205fa4c
    b ov000_021fe7f0_L58
ov000_021fe7f0_L40:
    bl native_fn_02063bdc
    mov r1, r0
    mov r0, r5
    bl native_fn_0205fa4c
    mov r0, r5
    bl native_fn_0205f9e4
ov000_021fe7f0_L58:
    ldrh r1, [r4, #12]
    add r0, r7, #1
    mov r0, r0, lsl #24
    cmp r1, r0, asr #24
    add r5, r5, #72
    mov r7, r0, asr #24
    bgt ov000_021fe7f0_L20
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
