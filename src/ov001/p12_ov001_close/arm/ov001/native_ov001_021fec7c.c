/* ov001 row 0x021fec7c: 220 bytes.
 *
 * What it does: 51 instructions; 9 call(s) to 0x0201d444, 0x0202a8e0, 0x0203cc2c, +6 more; loops (back edge at +0x2c); returns through pop {r3, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: loop with 9 calls (51 instructions, 9 calls, 3 branches, 10 back edges, 4 literal slots).
 *
 *   pool +0xcc -> native_data_0222ef8c (image word 0x0222ef8c)
 *   pool +0xd0 -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0xd4 -> native_data_0222efa4 (image word 0x0222efa4)
 *   pool +0xd8 -> native_data_0222efbc (image word 0x0222efbc)
 *   back edge +0x2c -> +0x14
 *   branch +0x48 -> +0x60
 *   branch +0x78 -> +0x90
 *   test +0x44 cmp r0, #0
 *   test +0x74 cmp r0, #0
 *   test +0xa4 cmp r0, #0
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fec7c; the literal pool and
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

extern u8 native_data_0222ef8c[];
extern void native_fn_0201d444(void);
extern void native_fn_0202a8e0(void);
extern void native_fn_0203cc2c(void);
extern u8 native_data_0222efa4[];
extern u8 native_data_0222efbc[];


asm u32 native_ov001_021fec7c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #32
    add r2, sp, #0
    mov r1, #8
    mov r0, #0
ov001_021fec7c_L14:
    strb r0, [r2]
    strb r0, [r2, #0x1]
    strb r0, [r2, #0x2]
    strb r0, [r2, #0x3]
    add r2, r2, #4
    subs r1, r1, #1
    bne ov001_021fec7c_L14
    ldr r1, =native_data_0222ef8c
    add r0, sp, #0
    bl native_fn_0201d444
    add r0, sp, #0
    bl native_fn_0202a8e0
    cmp r0, #0
    beq ov001_021fec7c_L60
    add r0, sp, #0
    mov r1, #2
    bl native_fn_0203cc2c
    ldr r1, =0x02239c10
    str r0, [r1, #0x2c]
ov001_021fec7c_L60:
    ldr r1, =native_data_0222efa4
    add r0, sp, #0
    bl native_fn_0201d444
    add r0, sp, #0
    bl native_fn_0202a8e0
    cmp r0, #0
    beq ov001_021fec7c_L90
    add r0, sp, #0
    mov r1, #2
    bl native_fn_0203cc2c
    ldr r1, =0x02239c10
    str r0, [r1, #0x30]
ov001_021fec7c_L90:
    ldr r1, =native_data_0222efbc
    add r0, sp, #0
    bl native_fn_0201d444
    add r0, sp, #0
    bl native_fn_0202a8e0
    cmp r0, #0
    addeq sp, sp, #32
    ldmeqia sp!, {r3, pc}
    add r0, sp, #0
    mov r1, #2
    bl native_fn_0203cc2c
    ldr r1, =0x02239c10
    str r0, [r1, #0x34]
    add sp, sp, #32
    ldmia sp!, {r3, pc}
}
