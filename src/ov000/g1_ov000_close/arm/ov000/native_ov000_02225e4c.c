/* ov000 row 0x02225e4c: 108 bytes.
 *
 * What it does: 25 instructions; 4 call(s) to 0x0202a634, 0x02225b08, 0x02225df0, +1 more; loops (back edge at +0x04); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x64 -> constant 0x00000ff7 (image word 0x00000ff7)
 *   pool +0x68 -> constant 0x02246aa8 (image word 0x02246aa8)
 *   branch +0x1c -> +0x5c
 *   branch +0x34 -> +0x44
 *   branch +0x40 -> +0x4c
 *   branch +0x48 -> +0x50
 *   test +0x14 tst r1, r0
 *   test +0x30 cmp r0, #3
 *   test +0x3c cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02225e4c; the literal pool and
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

extern void native_fn_0202a634(void);
extern void native_fn_02225b08(void);
extern void native_fn_02225df0(void);
extern void native_fn_0205e7a8(void);


asm u32 native_ov000_02225e4c (register u32 a0)
{
    stmdb sp!, {r4, lr}
    bl native_fn_0202a634
    ldrh r1, [r0, #2]
    ldr r0, =0x00000ff7
    ldr r2, =0x02246aa8
    tst r1, r0
    mov r4, #0
    beq ov000_02225e4c_L5c
    ldrb r0, [r2, #0x191]
    add r1, r0, #1
    and r0, r1, #255
    strb r1, [r2, #0x191]
    cmp r0, #3
    bhs ov000_02225e4c_L44
    bl native_fn_02225b08
    cmp r0, #0
    bne ov000_02225e4c_L4c
ov000_02225e4c_L44:
    mov r4, #1
    b ov000_02225e4c_L50
ov000_02225e4c_L4c:
    bl native_fn_02225df0
ov000_02225e4c_L50:
    mvn r0, #0
    mov r1, #82
    bl native_fn_0205e7a8
ov000_02225e4c_L5c:
    mov r0, r4
    ldmia sp!, {r4, pc}
}
