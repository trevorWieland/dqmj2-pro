/* ov000 row 0x021f10ec: 196 bytes.
 *
 * What it does: 48 instructions; 8 call(s) to 0x021f27b8, 0x021f27a0, 0x020c48bc, +5 more; loops (back edge at +0x34); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xc0 -> constant 0x02236d98 (image word 0x02236d98)
 *   branch +0x3c -> +0x50
 *   branch +0x44 -> +0x90
 *   branch +0x4c -> +0xa4
 *   branch +0x54 -> +0x68
 *   branch +0x60 -> +0x7c
 *   branch +0x64 -> +0xb4
 *   branch +0x78 -> +0xb4
 *   branch +0x8c -> +0xb4
 *   branch +0xa0 -> +0xb4
 *   test +0x20 cmp r4, #3
 *   test +0x38 cmp r4, #0
 *   test +0x40 cmp r4, #1
 *   test +0x48 cmp r4, #2
 *   test +0x50 cmp r5, #2
 *   test +0x58 cmp r5, #4
 *   test +0x5c cmpne r5, #6
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f10ec; the literal pool and
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

extern void native_fn_021f27b8(void);
extern void native_fn_021f27a0(void);
extern void native_fn_020c48bc(void);
extern void native_fn_020c48d0(void);
extern void native_fn_020c48e8(void);


asm u32 native_ov000_021f10ec (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r0, =0x02236d98
    ldr r0, [r0, #0x8]
    ldrsb r5, [r0, #32]
    mov r0, r5
    bl native_fn_021f27b8
    add r0, r0, #1
    and r4, r0, #255
    cmp r4, #3
    movhs r4, #0
    mov r0, r5
    mov r1, r4
    bl native_fn_021f27a0
    bl native_fn_020c48bc
    cmp r4, #0
    beq ov000_021f10ec_L50
    cmp r4, #1
    beq ov000_021f10ec_L90
    cmp r4, #2
    b ov000_021f10ec_La4
ov000_021f10ec_L50:
    cmp r5, #2
    beq ov000_021f10ec_L68
    cmp r5, #4
    cmpne r5, #6
    beq ov000_021f10ec_L7c
    b ov000_021f10ec_Lb4
ov000_021f10ec_L68:
    mov r0, #9
    mov r1, #5
    mov r2, #32
    bl native_fn_020c48d0
    b ov000_021f10ec_Lb4
ov000_021f10ec_L7c:
    mov r0, #9
    mov r1, #5
    mov r2, #31
    bl native_fn_020c48d0
    b ov000_021f10ec_Lb4
ov000_021f10ec_L90:
    mov r0, #9
    mov r1, #5
    mov r2, #33
    bl native_fn_020c48d0
    b ov000_021f10ec_Lb4
ov000_021f10ec_La4:
    mov r0, #9
    mov r1, #5
    mov r2, #34
    bl native_fn_020c48d0
ov000_021f10ec_Lb4:
    mov r0, #87
    bl native_fn_020c48e8
    ldmia sp!, {r3, r4, r5, pc}
}
