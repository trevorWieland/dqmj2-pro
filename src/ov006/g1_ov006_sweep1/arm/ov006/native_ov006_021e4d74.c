/* ov006 row 0x021e4d74: 144 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x88 -> constant 0x02218d2c (image word 0x02218d2c)
 *   pool +0x8c -> constant 0x02218d30 (image word 0x02218d30)
 *   branch +0x0c -> +0x80
 *   branch +0x1c -> +0x30
 *   branch +0x2c -> +0x80
 *   branch +0x48 -> +0x58
 *   branch +0x54 -> +0x80
 *   test +0x08 cmp r0, #0
 *   test +0x18 cmp r0, #0
 *   test +0x44 cmp r0, #35
 *   test +0x60 cmp r1, #0
 *   test +0x68 cmpeq r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e4d74; the literal pool and
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

extern void native_fn_020bb1f8(void);
extern void native_fn_021e9268(void);
extern void native_fn_021e3f28(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_020642dc(void);
extern void native_fn_021e7e78(void);
extern void native_fn_021e3cd8(void);


asm u32 native_ov006_021e4d74 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_020bb1f8
    cmp r0, #0
    beq ov006_021e4d74_L80
    ldr r0, =0x02218d2c
    ldrsb r0, [r0]
    cmp r0, #0
    beq ov006_021e4d74_L30
    bl native_fn_021e9268
    mov r0, #51
    bl native_fn_021e3f28
    b ov006_021e4d74_L80
ov006_021e4d74_L30:
    bl native_fn_021e9268
    mvn r0, #0
    mov r1, #87
    bl native_fn_0205e7a8
    bl native_fn_020642dc
    cmp r0, #35
    bne ov006_021e4d74_L58
    mov r0, #76
    bl native_fn_021e3f28
    b ov006_021e4d74_L80
ov006_021e4d74_L58:
    ldr r0, =0x02218d30
    ldr r1, [r0, #0x20]
    cmp r1, #0
    ldreq r0, [r0, #0x10]
    cmpeq r0, #0
    movne r0, #1
    moveq r0, #0
    bl native_fn_021e7e78
    mov r0, #13
    bl native_fn_021e3f28
ov006_021e4d74_L80:
    bl native_fn_021e3cd8
    ldmia sp!, {r3, pc}
}
