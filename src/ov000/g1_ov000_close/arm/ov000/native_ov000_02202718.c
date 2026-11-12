/* ov000 row 0x02202718: 276 bytes.
 *
 * What it does: 65 instructions; 10 call(s) to 0x022027bc, 0x0205fa4c, 0x020632f4, +7 more; loops (back edge at +0x50); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x104 -> constant 0x02237d9c (image word 0x02237d9c)
 *   pool +0x108 -> constant 0x02237d94 (image word 0x02237d94)
 *   pool +0x10c -> constant 0x02237f90 (image word 0x02237f90)
 *   pool +0x110 -> constant 0x02237e8c (image word 0x02237e8c)
 *   branch +0x14 -> +0xa4
 *   branch +0x44 -> +0x58
 *   branch +0x54 -> +0x90
 *   branch +0x68 -> +0x84
 *   branch +0x80 -> +0x90
 *   back edge +0xa0 -> +0x2c
 *   test +0x10 cmp r0, #0
 *   test +0x34 cmp r0, #0
 *   test +0x40 cmpne r0, #127
 *   test +0x64 cmp r0, #0
 *   test +0x9c cmp r10, r0
 *   test +0xac cmp r0, #0
 *   test +0xbc cmp r0, #0
 *   test +0xe0 cmp r1, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02202718; the literal pool and
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

extern void native_fn_0205fa4c(void);
extern void native_fn_020632f4(void);
extern void native_fn_0205f9e4(void);
extern void native_fn_0204b138(void);
extern void native_fn_020496b0(void);


asm u32 native_ov000_02202718 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    ldr r9, =0x02237d9c
    mov r10, #0
    ldrh r0, [r9, #12]
    cmp r0, #0
    ble ov000_02202718_La4
    ldr r6, =0x02237d94
    ldr r8, =0x02237f90
    add r5, r6, #256
    mov r11, r10
    mov r4, #72
ov000_02202718_L2c:
    ldrsb r0, [r5, #249]
    mul r7, r10, r4
    cmp r0, #0
    addne r0, r6, r10
    ldrneb r0, [r0, #0x1e8]
    cmpne r0, #127
    bne ov000_02202718_L58
    mov r1, r11
    add r0, r8, r7
    bl native_fn_0205fa4c
    b ov000_02202718_L90
ov000_02202718_L58:
    sub r0, r0, #12
    and r0, r0, #255
    bl native_fn_020632f4
    cmp r0, #0
    beq ov000_02202718_L84
    mov r1, #1
    add r0, r8, r7
    bl native_fn_0205fa4c
    add r0, r8, r7
    bl native_fn_0205f9e4
    b ov000_02202718_L90
ov000_02202718_L84:
    mov r1, #0
    add r0, r8, r7
    bl native_fn_0205fa4c
ov000_02202718_L90:
    ldrh r0, [r9, #12]
    add r1, r10, #1
    and r10, r1, #255
    cmp r10, r0
    blt ov000_02202718_L2c
ov000_02202718_La4:
    ldr r4, =0x02237e8c
    ldr r0, [r4, #0xc4]
    cmp r0, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r0, [r4, #0x4]
    mov r1, #0
    cmp r0, #0
    movgt r2, #1
    movle r2, #0
    add r0, r4, #168
    bl native_fn_0204b138
    ldrh r1, [r4, #12]
    ldr r2, [r4, #0x4]
    ldrh r0, [r4, #14]
    add r1, r2, r1
    cmp r1, r0
    movlt r2, #1
    movge r2, #0
    add r0, r4, #168
    mov r1, #1
    bl native_fn_0204b138
    add r0, r4, #168
    bl native_fn_020496b0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
