/* ov000 row 0x021e4d04: 180 bytes.
 *
 * What it does: 42 instructions; 8 call(s) to 0x0202a1e0, 0x021df1f0, 0x021df220, +5 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xa8 -> native_data_0222ed10 (image word 0x0222ed10)
 *   pool +0xac -> native_data_0222ed20 (image word 0x0222ed20)
 *   pool +0xb0 -> constant 0x02233ae8 (image word 0x02233ae8)
 *   branch +0x1c -> +0x28
 *   branch +0x88 -> +0x94
 *   test +0x18 cmp r4, #255
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e4d04; the literal pool and
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

extern void native_fn_0202a1e0(void);
extern void native_fn_021df1f0(void);
extern void native_fn_021df220(void);
extern u8 native_data_0222ed10[];
extern void native_fn_0201d444(void);
extern u8 native_data_0222ed20[];
extern void native_fn_0204bc78(void);
extern void native_fn_0204c6e0(void);


asm u32 native_ov000_021e4d04 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #40
    mov r4, r0
    mov r0, #1
    bl native_fn_0202a1e0
    mov r5, r0
    cmp r4, #255
    bne ov000_021e4d04_L28
    bl native_fn_021df1f0
    mov r4, r0
ov000_021e4d04_L28:
    add r1, sp, #6
    add r2, sp, #5
    add r3, sp, #4
    mov r0, r4
    bl native_fn_021df220
    ldrb r2, [sp, #0x4]
    ldr r1, =native_data_0222ed10
    add r0, sp, #23
    str r2, [sp]
    ldrsb r2, [sp, #6]
    ldrb r3, [sp, #0x5]
    bl native_fn_0201d444
    ldrb r2, [sp, #0x4]
    ldr r1, =native_data_0222ed20
    add r0, sp, #7
    str r2, [sp]
    ldrsb r2, [sp, #6]
    ldrb r3, [sp, #0x5]
    bl native_fn_0201d444
    ldr r0, =0x02233ae8
    add r1, sp, #23
    add r2, sp, #7
    bl native_fn_0204bc78
    movs r4, r0
    beq ov000_021e4d04_L94
    bl native_fn_0204c6e0
    mov r4, #1
ov000_021e4d04_L94:
    mov r0, r5
    bl native_fn_0202a1e0
    mov r0, r4
    add sp, sp, #40
    ldmia sp!, {r3, r4, r5, pc}
}
