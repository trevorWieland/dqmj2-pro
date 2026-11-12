/* ov001 row 0x021f11e8: 112 bytes.
 *
 * What it does: 26 instructions; 2 call(s) to 0x020485b4, 0x020484dc; loops (back edge at +0x1c); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (26 instructions, 2 calls, 2 branches, 2 back edges, 2 literal slots).
 *
 *   pool +0x68 -> constant 0x02238f58 (image word 0x02238f58)
 *   pool +0x6c -> native_data_0222ecb0 (image word 0x0222ecb0)
 *   branch +0x18 -> +0x2c
 *   branch +0x38 -> +0x50
 *   test +0x04 cmp r0, #3
 *   test +0x14 cmp r0, #0
 *   test +0x34 cmp r1, #127
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f11e8; the literal pool and
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

extern void native_fn_020485b4(void);
extern u8 native_data_0222ecb0[];
extern void native_fn_020484dc(void);


asm u32 native_ov001_021f11e8 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    cmp r0, #3
    ldmeqia sp!, {r3, pc}
    ldr r0, =0x02238f58
    ldr r0, [r0, #0xc]
    cmp r0, #0
    beq ov001_021f11e8_L2c
    bl native_fn_020485b4
    ldr r0, =0x02238f58
    mov r1, #0
    str r1, [r0, #0xc]
ov001_021f11e8_L2c:
    ldr r0, =native_data_0222ecb0
    ldrb r1, [r0]
    cmp r1, #127
    beq ov001_021f11e8_L50
    mov r0, #0
    bl native_fn_020484dc
    ldr r0, =native_data_0222ecb0
    mov r1, #127
    strb r1, [r0]
ov001_021f11e8_L50:
    ldr r0, =0x02238f58
    mov r1, #0
    str r1, [r0, #0x10]
    mov r1, #3
    strb r1, [r0]
    ldmia sp!, {r3, pc}
}
