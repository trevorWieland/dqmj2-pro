/* ov000 row 0x02201990: 208 bytes.
 *
 * What it does: 50 instructions; 11 call(s) to 0x02215698, 0x022156d4, 0x02216664, +8 more; loops (back edge at +0x60); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xc8 -> constant 0x02237d94 (image word 0x02237d94)
 *   pool +0xcc -> constant 0x02237e8c (image word 0x02237e8c)
 *   branch +0x14 -> +0x2c
 *   branch +0x1c -> +0x34
 *   branch +0x24 -> +0x9c
 *   branch +0x28 -> +0xbc
 *   branch +0x30 -> +0xbc
 *   branch +0x44 -> +0x94
 *   branch +0x90 -> +0xbc
 *   branch +0x98 -> +0xbc
 *   test +0x10 cmp r5, #1
 *   test +0x18 cmp r5, #3
 *   test +0x20 cmp r5, #5
 *   test +0x40 cmp r0, #7
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02201990; the literal pool and
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

extern void native_fn_02215698(void);
extern void native_fn_022156d4(void);
extern void native_fn_02216664(void);
extern void native_fn_02215078(void);
extern void native_fn_02049ad0(void);
extern void native_fn_022162c0(void);
extern void native_fn_0204b61c(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_02217c9c(void);
extern void native_fn_0204b5d4(void);


asm u32 native_ov000_02201990 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    bl native_fn_02215698
    mov r4, r0
    cmp r5, #1
    beq ov000_02201990_L2c
    cmp r5, #3
    beq ov000_02201990_L34
    cmp r5, #5
    beq ov000_02201990_L9c
    b ov000_02201990_Lbc
ov000_02201990_L2c:
    bl native_fn_022156d4
    b ov000_02201990_Lbc
ov000_02201990_L34:
    ldr r0, =0x02237d94
    ldr r5, =0x02237e8c
    ldr r0, [r0, #0x4]
    cmp r0, #7
    beq ov000_02201990_L94
    mov r0, r5
    bl native_fn_02216664
    add r0, r5, #168
    mov r1, #1
    bl native_fn_02215078
    mov r0, #1
    bl native_fn_02049ad0
    bl native_fn_022162c0
    ldr r2, =0x02237d94
    add r0, r4, #16
    ldr r1, [r2, #0x4]
    mov r3, #7
    str r1, [r2]
    mov r1, #0
    str r3, [r2, #0x4]
    bl native_fn_0204b61c
    mov r0, #83
    bl native_fn_021e7b9c
    b ov000_02201990_Lbc
ov000_02201990_L94:
    bl native_fn_022156d4
    b ov000_02201990_Lbc
ov000_02201990_L9c:
    mov r0, #1
    bl native_fn_02217c9c
    add r0, r4, #16
    mov r1, #36
    bl native_fn_0204b5d4
    ldr r0, =0x02237d94
    mov r1, #1
    str r1, [r0]
ov000_02201990_Lbc:
    ldr r0, =0x02237d94
    ldr r0, [r0]
    ldmia sp!, {r3, r4, r5, pc}
}
