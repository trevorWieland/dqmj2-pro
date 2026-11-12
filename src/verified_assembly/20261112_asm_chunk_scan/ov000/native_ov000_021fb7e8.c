/* ov000 row 0x021fb7e8: 192 bytes.
 *
 * What it does: Copies a 2-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   branch +0x28 -> +0xb8
 *   branch +0x34 -> +0x58
 *   branch +0x54 -> +0x9c
 *   branch +0x6c -> +0x9c
 *   back edge +0xb4 -> +0x2c
 *   test +0x30 cmp r10, #0
 *   test +0x48 cmp r0, #0
 *   test +0x68 cmp r0, #0
 *   test +0xa0 cmp r8, r4
 *   test +0xb0 cmp r7, r9
 *   0 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fb7e8; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02062aa0(void);
extern void native_fn_02062ad0(void);
extern void native_fn_021fb97c(void);
extern void native_fn_02215d94(void);
extern void native_fn_0207c2b8(void);
extern void native_fn_0207c18c(void);


asm u32 native_ov000_021fb7e8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    mov r11, #255
    mov r8, #0
    bl native_fn_02062aa0
    mov r4, r0
    bl native_fn_02062ad0
    add r0, r4, r0
    ands r9, r0, #255
    mov r7, r8
    beq ov000_021fb7e8_Lb8
ov000_021fb7e8_L2c:
    mov r4, #0
    cmp r10, #0
    beq ov000_021fb7e8_L58
    mov r0, #52
    mul r1, r7, r0
    ldrb r0, [r10, r1]
    add r2, r10, r1
    cmp r0, #0
    ldmneib r2, {r0, r1}
    subne r4, r1, r0
    b ov000_021fb7e8_L9c
ov000_021fb7e8_L58:
    mov r0, r7
    bl native_fn_021fb97c
    mov r6, r0
    ldrb r0, [r6, #0x33]
    cmp r0, #0
    bne ov000_021fb7e8_L9c
    mov r0, r7
    bl native_fn_02215d94
    mov r5, r0
    mov r1, r5
    add r0, r6, #32
    bl native_fn_0207c2b8
    mov r4, r0
    add r0, r6, #32
    mov r1, r5
    bl native_fn_0207c18c
    sub r4, r4, r0
ov000_021fb7e8_L9c:
    add r0, r7, #1
    cmp r8, r4
    movlt r11, r7
    and r7, r0, #255
    movlt r8, r4
    cmp r7, r9
    blo ov000_021fb7e8_L2c
ov000_021fb7e8_Lb8:
    mov r0, r11
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
