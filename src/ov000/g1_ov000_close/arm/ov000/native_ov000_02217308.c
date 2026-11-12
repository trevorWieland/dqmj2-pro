/* ov000 row 0x02217308: 272 bytes.
 *
 * What it does: 65 instructions; 7 call(s) to 0x0203cc2c, 0x0204518c, 0x02045490, +4 more; loops (back edge at +0x2c); returns through pop {r4, r5, r6, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x104 -> constant 0x0224532c (image word 0x0224532c)
 *   pool +0x108 -> native_data_0222f918 (image word 0x0222f918)
 *   pool +0x10c -> native_data_0222f9e0 (image word 0x0222f9e0)
 *   back edge +0x2c -> +0x14
 *   branch +0x48 -> +0x58
 *   branch +0x50 -> +0x64
 *   branch +0x54 -> +0x70
 *   branch +0x60 -> +0x78
 *   branch +0x6c -> +0x78
 *   test +0x38 cmp r1, #0
 *   test +0x44 cmp r0, #0
 *   test +0x4c cmp r0, #4
 *   test +0x80 cmp r5, r0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02217308; the literal pool and
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

extern u8 native_data_0222f918[];
extern u8 native_data_0222f9e0[];
extern void native_fn_0203cc2c(void);
extern void native_fn_0204518c(void);
extern void native_fn_02045490(void);
extern void native_fn_02008e0c(void);
extern void native_fn_0202a498(void);
extern void native_fn_022172dc(void);


asm u32 native_ov000_02217308 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #40
    add r3, sp, #8
    mov r2, #8
    mov r1, #0
ov000_02217308_L14:
    strb r1, [r3]
    strb r1, [r3, #0x1]
    strb r1, [r3, #0x2]
    strb r1, [r3, #0x3]
    add r3, r3, #4
    subs r2, r2, #1
    bne ov000_02217308_L14
    ldr r1, =0x0224532c
    ldr r1, [r1, #0x14]
    cmp r1, #0
    addeq sp, sp, #40
    ldmeqia sp!, {r4, r5, r6, pc}
    cmp r0, #0
    beq ov000_02217308_L58
    cmp r0, #4
    beq ov000_02217308_L64
    b ov000_02217308_L70
ov000_02217308_L58:
    mov r5, #13
    mov r6, #14
    b ov000_02217308_L78
ov000_02217308_L64:
    mov r5, #1
    mov r6, #3
    b ov000_02217308_L78
ov000_02217308_L70:
    mov r5, #1
    mov r6, #2
ov000_02217308_L78:
    ldr r0, =native_data_0222f918
    ldrh r0, [r0, #2]
    cmp r5, r0
    addeq sp, sp, #40
    ldmeqia sp!, {r4, r5, r6, pc}
    ldr r0, =native_data_0222f9e0
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    add r0, sp, #0
    mov r1, r4
    mov r2, r5
    bl native_fn_0204518c
    ldr r1, [sp]
    ldr r3, [sp, #0x4]
    mov r0, #1
    mov r2, #0
    bl native_fn_02045490
    mov r2, r6
    add r0, sp, #0
    mov r1, r4
    bl native_fn_0204518c
    ldr r1, =0x0224532c
    ldr r0, [sp]
    ldr r2, [sp, #0x4]
    ldr r1, [r1, #0x14]
    bl native_fn_02008e0c
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    bl native_fn_022172dc
    ldr r0, =native_data_0222f918
    strh r5, [r0, #2]
    add sp, sp, #40
    ldmia sp!, {r4, r5, r6, pc}
}
