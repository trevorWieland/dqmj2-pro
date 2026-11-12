/* ov000 row 0x0220fd30: 184 bytes.
 *
 * What it does: 46 instructions; 4 call(s) to 0x020c56b4, 0x020c56b4, 0x020c56b4, +1 more; loops (back edge at +0x2c); returns through pop {r4, pc}
 *
 * Decoded shape: chunk loop.
 *
 *   branch +0x14 -> +0xa4
 *   branch +0x38 -> +0x6c
 *   branch +0x50 -> +0x6c
 *   branch +0x68 -> +0x7c
 *   test +0x10 cmp r1, #9
 *   test +0x1c cmp r1, #0
 *   test +0x34 cmp r0, #5
 *   test +0x4c cmp r0, #6
 *   test +0x64 cmp r0, #8
 *   2 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220fd30; the literal pool and
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

extern void native_fn_020c56b4(void);
extern void native_fn_02209c68(void);


asm u32 native_ov000_0220fd30 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    ldrb r1, [r4, #0x278]
    mov r0, #0
    cmp r1, #9
    bne ov000_0220fd30_La4
    ldrb r1, [r4, #0x1e2]
    cmp r1, #0
    ldmneia sp!, {r4, pc}
    add r0, r4, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r0, [r0, #0xa]
    cmp r0, #5
    beq ov000_0220fd30_L6c
    add r0, r4, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r0, [r0, #0xa]
    cmp r0, #6
    beq ov000_0220fd30_L6c
    add r0, r4, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r0, [r0, #0xa]
    cmp r0, #8
    bne ov000_0220fd30_L7c
ov000_0220fd30_L6c:
    add r0, r4, #680
    add r3, r4, #112
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
ov000_0220fd30_L7c:
    mov r0, r4
    mov r1, #10
    bl native_fn_02209c68
    ldrb r2, [r4, #0x2c2]
    mov r1, #31
    mov r0, #1
    bic r2, r2, #15
    strb r2, [r4, #0x2c2]
    strb r1, [r4, #0x160]
    ldmia sp!, {r4, pc}
ov000_0220fd30_La4:
    ldrb r1, [r4, #0x2c2]
    mov r0, #1
    bic r1, r1, #15
    strb r1, [r4, #0x2c2]
    ldmia sp!, {r4, pc}
}
