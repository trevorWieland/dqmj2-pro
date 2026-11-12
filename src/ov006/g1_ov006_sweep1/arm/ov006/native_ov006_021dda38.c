/* ov006 row 0x021dda38: 240 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xe8 -> native_data4_0220f4e8 (image word 0x0220f4e8)
 *   pool +0xec -> native_data_0220d060 (image word 0x0220d060)
 *   branch +0x28 -> +0x54
 *   branch +0x2c -> +0xa0
 *   branch +0x34 -> +0xb0
 *   branch +0x3c -> +0xb0
 *   branch +0x40 -> +0xa0
 *   branch +0x4c -> +0x80
 *   branch +0x50 -> +0xb0
 *   branch +0x58 -> +0x64
 *   branch +0x5c -> +0xa0
 *   branch +0x60 -> +0xb0
 *   branch +0x68 -> +0xb0
 *   branch +0x70 -> +0xb0
 *   branch +0x78 -> +0xa0
 *   branch +0x7c -> +0xb0
 *   branch +0x9c -> +0xc8
 *   branch +0xac -> +0xc8
 *   test +0x24 cmp r0, #48
 *   test +0x30 cmp r0, #35
 *   test +0x38 cmp r0, #32
 *   test +0x44 cmp r0, #34
 *   test +0x48 cmpne r0, #35
 *   test +0x54 cmp r0, #49
 *   test +0x64 cmp r0, #52
 *   test +0x6c cmp r0, #50
 *   test +0x74 cmpne r0, #52
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021dda38; the literal pool and
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

extern void native_fn_021df4c8(void);
extern void native_fn_02048e8c(void);
extern void native_fn_021dda10(void);
extern void native_fn_021df960(void);
extern void native_fn_020414c8(void);
extern void native_fn_020642dc(void);
extern u8 native_data4_0220f4e8[];
extern void native_fn_02041538(void);
extern u8 native_data_0220d060[];


asm u32 native_ov006_021dda38 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mvn r0, #0
    bl native_fn_021df4c8
    bl native_fn_02048e8c
    bl native_fn_021dda10
    bl native_fn_021df960
    mov r0, #63
    bl native_fn_020414c8
    bl native_fn_020642dc
    cmp r0, #48
    bgt ov006_021dda38_L54
    bge ov006_021dda38_La0
    cmp r0, #35
    bgt ov006_021dda38_Lb0
    cmp r0, #32
    blt ov006_021dda38_Lb0
    beq ov006_021dda38_La0
    cmp r0, #34
    cmpne r0, #35
    beq ov006_021dda38_L80
    b ov006_021dda38_Lb0
ov006_021dda38_L54:
    cmp r0, #49
    bgt ov006_021dda38_L64
    beq ov006_021dda38_La0
    b ov006_021dda38_Lb0
ov006_021dda38_L64:
    cmp r0, #52
    bgt ov006_021dda38_Lb0
    cmp r0, #50
    blt ov006_021dda38_Lb0
    cmpne r0, #52
    beq ov006_021dda38_La0
    b ov006_021dda38_Lb0
ov006_021dda38_L80:
    ldr r3, =native_data4_0220f4e8
    mov r12, #3
    mov r0, #0
    mov r1, #2
    mov r2, #10
    str r12, [r3, #0x4]
    bl native_fn_02041538
    b ov006_021dda38_Lc8
ov006_021dda38_La0:
    ldr r0, =native_data4_0220f4e8
    mov r1, #4
    str r1, [r0, #0x4]
    b ov006_021dda38_Lc8
ov006_021dda38_Lb0:
    ldr r3, =native_data4_0220f4e8
    mov r0, #0
    mov r1, #2
    mov r2, #10
    str r0, [r3, #0x4]
    bl native_fn_02041538
ov006_021dda38_Lc8:
    ldr r1, =native_data4_0220f4e8
    mov r0, #12
    ldr r2, [r1, #0x4]
    ldr r1, =native_data_0220d060
    mul r0, r2, r0
    ldr r0, [r1, r0]
    blx r0
    ldmia sp!, {r3, pc}
}
