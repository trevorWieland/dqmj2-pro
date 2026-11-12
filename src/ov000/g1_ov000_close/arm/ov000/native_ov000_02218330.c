/* ov000 row 0x02218330: 412 bytes.
 *
 * What it does: 96 instructions; 20 call(s) to 0x021df3bc, 0x0201d444, 0x0201d444, +17 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, pc}; 7 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x180 -> native_data_0222fa10 (image word 0x0222fa10)
 *   pool +0x184 -> native_data_0222fa50 (image word 0x0222fa50)
 *   pool +0x188 -> native_data_0222fa5c (image word 0x0222fa5c)
 *   pool +0x18c -> native_data_0222fa64 (image word 0x0222fa64)
 *   pool +0x190 -> native_data_0222fa6c (image word 0x0222fa6c)
 *   pool +0x194 -> native_data_0222fa74 (image word 0x0222fa74)
 *   pool +0x198 -> constant 0x02245e54 (image word 0x02245e54)
 *   branch +0x34 -> +0x44
 *   branch +0x40 -> +0x50
 *   branch +0x6c -> +0xb0
 *   branch +0xcc -> +0x100
 *   branch +0x11c -> +0x150
 *   test +0x1c cmp r3, #255
 *   test +0x2c cmp r2, #127
 *   test +0x68 cmp r0, #0
 *   test +0x118 cmp r0, #0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02218330; the literal pool and
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

extern void native_fn_021df3bc(void);
extern u8 native_data_0222fa10[];
extern u8 native_data_0222fa50[];
extern void native_fn_0201d444(void);
extern u8 native_data_0222fa5c[];
extern u8 native_data_0222fa64[];
extern void native_fn_0202a8e0(void);
extern void native_fn_0203cc2c(void);
extern void native_fn_0204820c(void);
extern void native_fn_0202a498(void);
extern void native_fn_02048308(void);
extern u8 native_data_0222fa6c[];
extern void native_fn_02045490(void);
extern u8 native_data_0222fa74[];
extern void native_fn_02045e14(void);


asm u32 native_ov000_02218330 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #32
    bl native_fn_021df3bc
    ldrh r1, [r0]
    ldrb r3, [r0, #0x3]
    ldr r0, =native_data_0222fa10
    mov r1, r1, lsl #16
    cmp r3, #255
    addeq sp, sp, #32
    ldrb r2, [r0, r1, lsr #27]
    ldmeqia sp!, {r3, r4, r5, pc}
    cmp r2, #127
    add r0, sp, #0
    beq ov000_02218330_L44
    ldr r1, =native_data_0222fa50
    bl native_fn_0201d444
    b ov000_02218330_L50
ov000_02218330_L44:
    ldr r1, =native_data_0222fa5c
    mov r2, r3
    bl native_fn_0201d444
ov000_02218330_L50:
    ldr r1, =native_data_0222fa64
    add r0, sp, #16
    add r2, sp, #0
    bl native_fn_0201d444
    add r0, sp, #16
    bl native_fn_0202a8e0
    cmp r0, #0
    beq ov000_02218330_Lb0
    add r0, sp, #16
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    add r0, r4, #448
    mov r1, #448
    mov r2, #32
    bl native_fn_0204820c
    mov r0, r4
    mov r1, #0
    mov r2, #2
    bl native_fn_0204820c
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    bl native_fn_02048308
ov000_02218330_Lb0:
    ldr r1, =native_data_0222fa6c
    add r0, sp, #16
    add r2, sp, #0
    bl native_fn_0201d444
    add r0, sp, #16
    bl native_fn_0202a8e0
    movs r5, r0
    beq ov000_02218330_L100
    add r0, sp, #16
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    mov r1, r4
    mov r3, r5
    mov r0, #3
    mov r2, #0
    bl native_fn_02045490
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
ov000_02218330_L100:
    ldr r1, =native_data_0222fa74
    add r0, sp, #16
    add r2, sp, #0
    bl native_fn_0201d444
    add r0, sp, #16
    bl native_fn_0202a8e0
    cmp r0, #0
    beq ov000_02218330_L150
    add r0, sp, #16
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    mov r2, r4
    mov r0, #1
    mov r1, #3
    mov r3, #4
    bl native_fn_02045e14
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
ov000_02218330_L150:
    ldr r0, =0x02245e54
    mov r1, #0
    strb r1, [r0, #0x68]
    mov r1, #1024
    str r1, [r0, #0x78]
    mov r2, #64
    str r2, [r0, #0x84]
    mov r1, #2048
    str r1, [r0, #0x80]
    str r2, [r0, #0x8c]
    add sp, sp, #32
    ldmia sp!, {r3, r4, r5, pc}
}
