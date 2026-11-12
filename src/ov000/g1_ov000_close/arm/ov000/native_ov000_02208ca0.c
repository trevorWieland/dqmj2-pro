/* ov000 row 0x02208ca0: 284 bytes.
 *
 * What it does: 70 instructions; 14 call(s) to 0x0202a8e0, 0x0203cc2c, 0x0204820c, +11 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x118 -> native_data_0222ba9c (image word 0x0222ba9c)
 *   branch +0x28 -> +0x78
 *   branch +0x34 -> +0x78
 *   branch +0x80 -> +0xc4
 *   branch +0x8c -> +0xc4
 *   branch +0xcc -> +0x110
 *   branch +0xd8 -> +0x110
 *   test +0x1c cmp r0, #0
 *   test +0x7c cmp r0, #0
 *   test +0xc8 cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02208ca0; the literal pool and
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

extern u8 native_data_0222ba9c[];
extern void native_fn_0202a8e0(void);
extern void native_fn_0203cc2c(void);
extern void native_fn_0204820c(void);
extern void native_fn_02048308(void);
extern void native_fn_0202a498(void);
extern void native_fn_02045490(void);
extern void native_fn_02045994(void);


asm u32 native_ov000_02208ca0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r1, #12
    mul r1, r0, r1
    ldr r2, =native_data_0222ba9c
    mov r3, #255
    ldr r0, [r2, r1]
    strh r3, [sp]
    cmp r0, #0
    add r7, r2, r1
    mov r6, #0
    beq ov000_02208ca0_L78
    bl native_fn_0202a8e0
    movs r4, r0
    beq ov000_02208ca0_L78
    ldr r0, [r7]
    mov r1, #2
    bl native_fn_0203cc2c
    mov r2, r4
    mov r1, r6
    mov r4, r0
    bl native_fn_0204820c
    add r0, sp, #0
    mov r1, r6
    mov r2, #2
    bl native_fn_0204820c
    bl native_fn_02048308
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    orr r6, r6, #1
ov000_02208ca0_L78:
    ldr r0, [r7, #0x4]
    cmp r0, #0
    beq ov000_02208ca0_Lc4
    bl native_fn_0202a8e0
    movs r5, r0
    beq ov000_02208ca0_Lc4
    ldr r0, [r7, #0x4]
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    mov r0, #0
    mov r1, r4
    mov r2, r0
    mov r3, r5
    bl native_fn_02045490
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    orr r6, r6, #2
ov000_02208ca0_Lc4:
    ldr r0, [r7, #0x8]
    cmp r0, #0
    beq ov000_02208ca0_L110
    bl native_fn_0202a8e0
    movs r5, r0
    beq ov000_02208ca0_L110
    ldr r0, [r7, #0x8]
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    mov r0, #0
    mov r1, r4
    mov r2, r0
    mov r3, r5
    bl native_fn_02045994
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    orr r6, r6, #4
ov000_02208ca0_L110:
    mov r0, r6
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
