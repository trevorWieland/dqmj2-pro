/* ov000 row 0x021e85f8: 152 bytes.
 *
 * What it does: 38 instructions; 10 call(s) to 0x021e7d18, 0x0203d294, 0x021e865c, +7 more; loops (back edge at +0x28); returns through pop {r4, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x10 -> +0x90
 *   branch +0x40 -> +0x64
 *   branch +0x60 -> +0x7c
 *   test +0x0c cmp r1, #1
 *   test +0x38 cmp r0, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e85f8; the literal pool and
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

extern void native_fn_021e7d18(void);
extern void native_fn_0203d294(void);
extern void native_fn_02025a28(void);
extern void native_fn_02024e0c(void);
extern void native_fn_02025ca4(void);
extern void native_fn_020259b4(void);


asm u32 native_ov000_021e85f8 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    ldrb r1, [r4, #0x2a9]
    cmp r1, #1
    bne ov000_021e85f8_L90
    add r3, r4, #512
    mov r12, #30
    mov r1, #1
    mov r2, #0
    strh r12, [r3, #172]
    bl native_fn_021e7d18
    mov r0, #1
    bl native_fn_0203d294
    add r0, r0, #5
    cmp r0, #0
    mov r0, #1
    ble ov000_021e85f8_L64
    bl native_fn_0203d294
    add r0, r0, #5
    mov r0, r0, lsl #12
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov000_021e85f8_L7c
ov000_021e85f8_L64:
    bl native_fn_0203d294
    add r0, r0, #5
    mov r0, r0, lsl #12
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov000_021e85f8_L7c:
    bl native_fn_020259b4
    str r0, [r4, #0x2b0]
    add r0, r4, #512
    mov r1, #30
    strh r1, [r0, #174]
ov000_021e85f8_L90:
    mov r0, #0
    ldmia sp!, {r4, pc}
}
