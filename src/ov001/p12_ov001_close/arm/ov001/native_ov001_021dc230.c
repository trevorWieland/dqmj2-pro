/* ov001 row 0x021dc230: 200 bytes.
 *
 * What it does: 50 instructions; 7 call(s) to 0x021e259c, 0x021e28d0, 0x021d8dec, +4 more; loops (back edge at +0x50); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: loop with 7 calls (50 instructions, 7 calls, 8 branches, 2 back edges, 0 literal slots).
 *
 *   branch +0x10 -> +0x3c
 *   branch +0x1c -> +0xc0
 *   branch +0x38 -> +0xc0
 *   branch +0x44 -> +0xc0
 *   branch +0x5c -> +0x70
 *   branch +0x6c -> +0xa4
 *   branch +0x80 -> +0xa4
 *   branch +0x94 -> +0xa4
 *   back edge +0xac -> +0x4c
 *   test +0x08 cmp r1, #0
 *   test +0x18 cmp r1, #0
 *   test +0x40 cmp r0, #0
 *   test +0x58 tst r0, #16
 *   test +0x7c cmp r1, #0
 *   test +0xa8 cmp r5, #60
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021dc230; the literal pool and
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

extern void native_fn_021e259c(void);
extern void native_fn_021e28d0(void);
extern void native_fn_021d8dec(void);
extern void native_fn_021dc940(void);
extern void native_fn_022094bc(void);
extern void native_fn_022047ec(void);


asm u32 native_ov001_021dc230 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r4, r0
    cmp r1, #0
    mov r5, #0
    beq ov001_021dc230_L3c
    ldrb r1, [r4, #0x1ff]
    cmp r1, #0
    bne ov001_021dc230_Lc0
    mov r1, #1
    strb r1, [r4, #0x326]
    bl native_fn_021e259c
    mov r0, r4
    bl native_fn_021e28d0
    mov r5, #1
    b ov001_021dc230_Lc0
ov001_021dc230_L3c:
    ldrb r0, [r4, #0x1ff]
    cmp r0, #0
    beq ov001_021dc230_Lc0
    strb r5, [r4, #0x1ff]
ov001_021dc230_L4c:
    mov r0, r5
    bl native_fn_021d8dec
    ldrb r0, [r0, #0x3]
    tst r0, #16
    bne ov001_021dc230_L70
    mov r0, r4
    mov r1, r5
    bl native_fn_021dc940
    b ov001_021dc230_La4
ov001_021dc230_L70:
    add r0, r4, r5
    add r0, r0, #512
    ldrsb r1, [r0, #44]
    cmp r1, #0
    beq ov001_021dc230_La4
    ldrsb r2, [r0, #104]
    mov r0, r5
    bl native_fn_022094bc
    movs r2, r0
    bmi ov001_021dc230_La4
    ldrb r0, [r4, #0x31e]
    ldrb r1, [r4, #0x31f]
    bl native_fn_022047ec
ov001_021dc230_La4:
    add r5, r5, #1
    cmp r5, #60
    blt ov001_021dc230_L4c
    add r0, r4, #256
    mov r1, #0
    strh r1, [r0, #240]
    mov r5, #1
ov001_021dc230_Lc0:
    mov r0, r5
    ldmia sp!, {r3, r4, r5, pc}
}
