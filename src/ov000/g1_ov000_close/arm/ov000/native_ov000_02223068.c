/* ov000 row 0x02223068: 176 bytes.
 *
 * What it does: 42 instructions; 7 call(s) to 0x02041800, 0x0201d444, 0x02223390, +4 more; loops (back edge at +0x08); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xa8 -> native_data_0222fd3c (image word 0x0222fd3c)
 *   pool +0xac -> constant 0x02246574 (image word 0x02246574)
 *   test +0x0c cmp r0, #1
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02223068; the literal pool and
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

extern void native_fn_02041800(void);
extern u8 native_data_0222fd3c[];
extern void native_fn_0201d444(void);
extern void native_fn_02223390(void);
extern void native_fn_020414b0(void);
extern void native_fn_02041510(void);
extern void native_fn_02223328(void);
extern void native_fn_020456ac(void);


asm u32 native_ov000_02223068 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #40
    bl native_fn_02041800
    cmp r0, #1
    addeq sp, sp, #40
    moveq r0, #0
    ldmeqia sp!, {r3, pc}
    ldr r1, =native_data_0222fd3c
    add r0, sp, #8
    bl native_fn_0201d444
    add r0, sp, #8
    bl native_fn_02223390
    mov r0, #63
    bl native_fn_020414b0
    mov r0, #0
    mov r1, #2
    mov r2, #10
    bl native_fn_02041510
    ldr r0, =0x02246574
    mov r1, #9
    strb r1, [r0]
    bl native_fn_02223328
    mov r2, #67108864
    ldr r1, [r2]
    mov r0, #32
    bic r1, r1, #7936
    orr r1, r1, #2560
    str r1, [r2]
    str r0, [sp]
    mov r0, #24
    str r0, [sp, #0x4]
    mov r0, #0
    mov r1, #1
    mov r2, r0
    mov r3, #4
    bl native_fn_020456ac
    ldr r1, =0x02246574
    mov r2, #40
    mov r0, #0
    strb r2, [r1, #0x1]
    add sp, sp, #40
    ldmia sp!, {r3, pc}
}
