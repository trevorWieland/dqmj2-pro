/* ov006 row 0x021e6a58: 228 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xd8 -> constant 0x04001000 (image word 0x04001000)
 *   pool +0xdc -> constant 0xffcfffef (image word 0xffcfffef)
 *   pool +0xe0 -> constant 0x02218d90 (image word 0x02218d90)
 *   0 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e6a58; the literal pool and
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

extern void native_fn_020038a8(void);
extern void native_fn_02003950(void);
extern void native_fn_02002d00(void);


asm u32 native_ov006_021e6a58 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mov r0, #4
    bl native_fn_020038a8
    mov r0, #256
    bl native_fn_02003950
    mov r0, #0
    bl native_fn_02002d00
    ldr r0, =0x04001000
    ldr r1, =0xffcfffef
    ldr r3, [r0]
    ldr r2, =0x02218d90
    and r1, r3, r1
    orr r1, r1, #16
    str r1, [r0]
    ldr r3, [r0]
    mov r1, #0
    bic r3, r3, #7936
    orr r3, r3, #7936
    str r3, [r0]
    ldrh r3, [r0, #8]
    and r3, r3, #67
    orr r3, r3, #284
    strh r3, [r0, #8]
    ldrh r3, [r0, #10]
    and r3, r3, #67
    orr r3, r3, #20
    strh r3, [r0, #10]
    ldrh r3, [r0, #12]
    and r3, r3, #67
    orr r3, r3, #524
    strh r3, [r0, #12]
    ldrh r3, [r0, #14]
    and r3, r3, #67
    orr r3, r3, #776
    strh r3, [r0, #14]
    ldrh r3, [r0, #8]
    bic r3, r3, #3
    strh r3, [r0, #8]
    ldrh r3, [r0, #10]
    bic r3, r3, #3
    orr r3, r3, #3
    strh r3, [r0, #10]
    ldrh r3, [r0, #12]
    bic r3, r3, #3
    orr r3, r3, #1
    strh r3, [r0, #12]
    ldrh r3, [r0, #14]
    bic r3, r3, #3
    orr r3, r3, #2
    strh r3, [r0, #14]
    str r1, [r2, #0x28]
    str r1, [r2, #0x4c]
    str r1, [r2, #0x3c]
    ldmia sp!, {r3, pc}
}
