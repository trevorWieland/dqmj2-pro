/* ov000 row 0x02225d74: 124 bytes.
 *
 * What it does: 29 instructions; 4 call(s) to 0x0202a634, 0x02225d1c, 0x02225bf0, +1 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x74 -> constant 0x00000ff7 (image word 0x00000ff7)
 *   pool +0x78 -> constant 0x02246c84 (image word 0x02246c84)
 *   branch +0x1c -> +0x6c
 *   branch +0x34 -> +0x4c
 *   branch +0x48 -> +0x54
 *   branch +0x50 -> +0x60
 *   test +0x14 tst r1, r0
 *   test +0x30 cmp r1, #3
 *   test +0x44 cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02225d74; the literal pool and
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
extern void native_fn_02225d1c(void);
extern void native_fn_02225bf0(void);
extern void native_fn_0205e7a8(void);


asm u32 native_ov000_02225d74 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    bl native_fn_0202a634
    ldrh r1, [r0, #2]
    ldr r0, =0x00000ff7
    ldr r4, =0x02246c84
    tst r1, r0
    mov r5, #0
    beq ov000_02225d74_L6c
    ldrb r0, [r4, #0x191]
    add r0, r0, #1
    and r1, r0, #255
    strb r0, [r4, #0x191]
    cmp r1, #3
    bhs ov000_02225d74_L4c
    mov r0, #132
    mla r0, r1, r0, r4
    ldrsh r0, [r0, #24]
    cmp r0, #0
    bne ov000_02225d74_L54
ov000_02225d74_L4c:
    mov r5, #1
    b ov000_02225d74_L60
ov000_02225d74_L54:
    bl native_fn_02225d1c
    ldrb r0, [r4, #0x191]
    bl native_fn_02225bf0
ov000_02225d74_L60:
    mvn r0, #0
    mov r1, #82
    bl native_fn_0205e7a8
ov000_02225d74_L6c:
    mov r0, r5
    ldmia sp!, {r3, r4, r5, pc}
}
