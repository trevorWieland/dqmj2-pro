/* ov006 row 0x021e9e8c: 136 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x80 -> constant 0x022192e4 (image word 0x022192e4)
 *   pool +0x84 -> constant 0x02219290 (image word 0x02219290)
 *   back edge +0x40 -> +0x2c
 *   test +0x3c cmp r5, #4
 *   test +0x54 cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e9e8c; the literal pool and
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

extern void native_fn_020406a8(void);
extern void native_fn_020612ec(void);
extern void native_fn_0206257c(void);
extern void native_fn_0204b9d0(void);
extern void native_fn_020ba574(void);
extern void native_fn_0204bb08(void);
extern void native_fn_0206256c(void);
extern void native_fn_020bb334(void);


asm u32 native_ov006_021e9e8c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r4, r0
    mov r0, #1
    bl native_fn_020406a8
    mov r0, r4
    mov r1, #1
    mov r2, #32768
    mov r3, #0
    bl native_fn_020612ec
    ldr r4, =0x022192e4
    mov r5, #0
ov006_021e9e8c_L2c:
    bl native_fn_0206257c
    add r1, r5, #1
    str r0, [r4, r5, lsl #2]
    and r5, r1, #255
    cmp r5, #4
    blo ov006_021e9e8c_L2c
    mov r1, r4
    mov r0, #1
    bl native_fn_0204b9d0
    bl native_fn_020ba574
    cmp r0, #0
    movge r0, #0
    movlt r0, #1
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_0204bb08
    ldr r0, =0x02219290
    ldr r0, [r0, #0x58]
    bl native_fn_0206256c
    bl native_fn_020bb334
    ldmia sp!, {r3, r4, r5, pc}
}
