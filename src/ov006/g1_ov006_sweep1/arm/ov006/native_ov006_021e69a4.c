/* ov006 row 0x021e69a4: 180 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e69a4; the literal pool and
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

extern void native_fn_02002e5c(void);
extern void native_fn_02002c98(void);


asm u32 native_ov006_021e69a4 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mov r0, #3
    bl native_fn_02002e5c
    mov r0, #1
    mov r1, #3
    mov r2, #0
    bl native_fn_02002c98
    mov r0, #67108864
    ldr r1, [r0]
    bic r1, r1, #7936
    orr r1, r1, #3840
    str r1, [r0]
    ldrh r1, [r0, #8]
    and r1, r1, #67
    orr r1, r1, #264
    strh r1, [r0, #8]
    ldrh r1, [r0, #10]
    and r1, r1, #67
    orr r1, r1, #528
    strh r1, [r0, #10]
    ldrh r1, [r0, #12]
    and r1, r1, #67
    orr r1, r1, #792
    strh r1, [r0, #12]
    ldrh r1, [r0, #14]
    and r1, r1, #67
    orr r1, r1, #132
    orr r1, r1, #18432
    strh r1, [r0, #14]
    ldrh r1, [r0, #8]
    bic r1, r1, #3
    orr r1, r1, #1
    strh r1, [r0, #8]
    ldrh r1, [r0, #10]
    bic r1, r1, #3
    strh r1, [r0, #10]
    ldrh r1, [r0, #12]
    bic r1, r1, #3
    orr r1, r1, #2
    strh r1, [r0, #12]
    ldrh r1, [r0, #14]
    bic r1, r1, #3
    orr r1, r1, #3
    strh r1, [r0, #14]
    ldmia sp!, {r3, pc}
}
