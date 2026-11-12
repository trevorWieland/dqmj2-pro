/* ov006 row 0x021e0000: 188 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x6c -> +0x7c
 *   branch +0x88 -> +0xac
 *   branch +0x9c -> +0xac
 *   test +0x68 cmp r0, #0
 *   test +0x84 cmp r0, #0
 *   test +0x90 cmp r0, #47
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e0000; the literal pool and
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

extern void native_fn_020633b0(void);
extern void native_fn_02068a68(void);
extern void native_fn_02008e0c(void);
extern void native_fn_02067748(void);
extern void native_fn_0206442c(void);
extern void native_fn_020679f0(void);
extern void native_fn_02068a88(void);


asm u32 native_ov006_021e0000 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #76
    bl native_fn_020633b0
    mov r4, r0
    add r0, sp, #0
    bl native_fn_02068a68
    add r1, sp, #0
    mov r0, r4
    mov r2, #20
    bl native_fn_02008e0c
    bl native_fn_02067748
    add r1, sp, #20
    add r0, r0, #16
    mov r2, #24
    bl native_fn_02008e0c
    bl native_fn_0206442c
    ldrh r0, [r0]
    strh r0, [sp, #44]
    bl native_fn_020679f0
    ldr r1, [r0]
    mov r0, #0
    str r1, [sp, #0x30]
    str r0, [sp, #0x34]
    str r0, [sp, #0x38]
    bl native_fn_020679f0
    ldr r0, [r0, #0x4]
    cmp r0, #0
    beq ov006_021e0000_L7c
    bl native_fn_020679f0
    ldr r0, [r0, #0x4]
    str r0, [sp, #0x34]
ov006_021e0000_L7c:
    bl native_fn_020679f0
    ldr r0, [r0, #0x38]
    cmp r0, #0
    beq ov006_021e0000_Lac
    ldrh r0, [sp, #44]
    cmp r0, #47
    movhi r0, #0
    strhi r0, [sp, #0x38]
    bhi ov006_021e0000_Lac
    bl native_fn_020679f0
    ldr r0, [r0, #0x38]
    str r0, [sp, #0x38]
ov006_021e0000_Lac:
    add r0, sp, #0
    bl native_fn_02068a88
    add sp, sp, #76
    ldmia sp!, {r3, r4, pc}
}
