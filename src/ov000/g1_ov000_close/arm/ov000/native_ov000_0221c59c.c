/* ov000 row 0x0221c59c: 188 bytes.
 *
 * What it does: 45 instructions; 9 call(s) to 0x022213ec, 0x020c48bc, 0x020c48d0, +6 more; loops (back edge at +0x30); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xb4 -> constant 0x022460d4 (image word 0x022460d4)
 *   pool +0xb8 -> constant 0x02246090 (image word 0x02246090)
 *   branch +0x14 -> +0xac
 *   branch +0x40 -> +0x58
 *   branch +0x48 -> +0x6c
 *   branch +0x50 -> +0x80
 *   branch +0x54 -> +0x90
 *   branch +0x68 -> +0x90
 *   branch +0x7c -> +0x90
 *   test +0x10 cmp r0, #2
 *   test +0x3c cmp r0, #1
 *   test +0x44 cmp r0, #2
 *   test +0x4c cmp r0, #3
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221c59c; the literal pool and
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

extern void native_fn_022213ec(void);
extern void native_fn_020c48bc(void);
extern void native_fn_020c48d0(void);
extern void native_fn_02048f7c(void);
extern void native_fn_020c484c(void);
extern void native_fn_020c48e8(void);
extern void native_fn_0221e7e8(void);


asm u32 native_ov000_0221c59c (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r0, =0x022460d4
    mov r4, #0
    ldrsb r0, [r0, #16]
    cmp r0, #2
    bne ov000_0221c59c_Lac
    ldr r0, =0x02246090
    ldr r0, [r0, #0x18]
    bl native_fn_022213ec
    ldr r1, =0x02246090
    mov r4, #1
    str r0, [r1, #0x18]
    bl native_fn_020c48bc
    ldr r0, =0x02246090
    ldr r0, [r0, #0x18]
    cmp r0, #1
    beq ov000_0221c59c_L58
    cmp r0, #2
    beq ov000_0221c59c_L6c
    cmp r0, #3
    beq ov000_0221c59c_L80
    b ov000_0221c59c_L90
ov000_0221c59c_L58:
    mov r0, #5
    mov r1, #6
    mov r2, #27
    bl native_fn_020c48d0
    b ov000_0221c59c_L90
ov000_0221c59c_L6c:
    mov r0, #5
    mov r1, #6
    mov r2, #28
    bl native_fn_020c48d0
    b ov000_0221c59c_L90
ov000_0221c59c_L80:
    mov r0, #5
    mov r1, #6
    mov r2, #29
    bl native_fn_020c48d0
ov000_0221c59c_L90:
    mov r0, #1
    bl native_fn_02048f7c
    bl native_fn_020c484c
    mov r0, #87
    bl native_fn_020c48e8
    mov r0, #0
    bl native_fn_0221e7e8
ov000_0221c59c_Lac:
    mov r0, r4
    ldmia sp!, {r4, pc}
}
