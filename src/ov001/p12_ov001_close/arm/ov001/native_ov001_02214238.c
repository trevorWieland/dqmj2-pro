/* ov001 row 0x02214238: 100 bytes.
 *
 * What it does: 24 instructions; 4 call(s) to 0x02213ce4, 0x0221415c, 0x022141f0, +1 more; loops (back edge at +0x2c); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 4 calls (24 instructions, 4 calls, 9 branches, 5 back edges, 1 literal slot).
 *
 *   pool +0x60 -> constant 0x02242aac (image word 0x02242aac)
 *   branch +0x18 -> +0x50
 *   branch +0x1c -> +0x2c
 *   branch +0x20 -> +0x34
 *   branch +0x24 -> +0x3c
 *   branch +0x28 -> +0x44
 *   branch +0x30 -> +0x50
 *   branch +0x38 -> +0x50
 *   branch +0x40 -> +0x50
 *   back edge +0x54 -> +0x0c
 *   test +0x10 cmp r1, #3
 *   test +0x50 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02214238; the literal pool and
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

extern void native_fn_02213ce4(void);
extern void native_fn_0221415c(void);
extern void native_fn_022141f0(void);
extern void native_fn_02214234(void);


asm u32 native_ov001_02214238 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r4, =0x02242aac
    mov r0, #1
ov001_02214238_Lc:
    ldrsb r1, [r4, #1]
    cmp r1, #3
    addls pc, pc, r1, lsl #2
    b ov001_02214238_L50
    b ov001_02214238_L2c
    b ov001_02214238_L34
    b ov001_02214238_L3c
    b ov001_02214238_L44
ov001_02214238_L2c:
    bl native_fn_02213ce4
    b ov001_02214238_L50
ov001_02214238_L34:
    bl native_fn_0221415c
    b ov001_02214238_L50
ov001_02214238_L3c:
    bl native_fn_022141f0
    b ov001_02214238_L50
ov001_02214238_L44:
    bl native_fn_02214234
    mov r0, #1
    ldmia sp!, {r4, pc}
ov001_02214238_L50:
    cmp r0, #0
    bne ov001_02214238_Lc
    mov r0, #0
    ldmia sp!, {r4, pc}
}
