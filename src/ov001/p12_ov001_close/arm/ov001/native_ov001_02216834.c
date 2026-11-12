/* ov001 row 0x02216834: 100 bytes.
 *
 * What it does: 24 instructions; 4 call(s) to 0x022166c8, 0x0221671c, 0x022167f0, +1 more; loops (back edge at +0x2c); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 4 calls (24 instructions, 4 calls, 9 branches, 5 back edges, 1 literal slot).
 *
 *   pool +0x60 -> constant 0x02242be8 (image word 0x02242be8)
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
 * ov001.bin at 0x02216834; the literal pool and
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

extern void native_fn_022166c8(void);
extern void native_fn_0221671c(void);
extern void native_fn_022167f0(void);
extern void native_fn_02216824(void);


asm u32 native_ov001_02216834 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r4, =0x02242be8
    mov r0, #1
ov001_02216834_Lc:
    ldrb r1, [r4, #0x1]
    cmp r1, #3
    addls pc, pc, r1, lsl #2
    b ov001_02216834_L50
    b ov001_02216834_L2c
    b ov001_02216834_L34
    b ov001_02216834_L3c
    b ov001_02216834_L44
ov001_02216834_L2c:
    bl native_fn_022166c8
    b ov001_02216834_L50
ov001_02216834_L34:
    bl native_fn_0221671c
    b ov001_02216834_L50
ov001_02216834_L3c:
    bl native_fn_022167f0
    b ov001_02216834_L50
ov001_02216834_L44:
    bl native_fn_02216824
    mov r0, #1
    ldmia sp!, {r4, pc}
ov001_02216834_L50:
    cmp r0, #0
    bne ov001_02216834_Lc
    mov r0, #0
    ldmia sp!, {r4, pc}
}
