/* ov001 row 0x02219fd4: 104 bytes.
 *
 * What it does: 26 instructions; 3 call(s) to 0x0207afec, 0x021db8d0, 0x0221a004; loops (back edge at +0x10); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: loop with 3 calls (26 instructions, 3 calls, 1 branch, 3 back edges, 0 literal slots).
 *
 *   branch +0x28 -> +0x60
 *   back edge +0x5c -> +0x30
 *   test +0x24 cmp r0, #2
 *   test +0x38 cmp r0, #0
 *   test +0x44 cmpne r0, #0
 *   test +0x54 cmp r5, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02219fd4; the literal pool and
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

extern void native_fn_0207afec(void);
extern void ov001_record_is_active_021db8d0(void);


asm u32 native_ov001_02219fd4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r5, [r0]
    ldr r4, [r0, #0x8]
    ldr r0, [r0, #0xc]
    bl native_fn_0207afec
    ldrb r1, [r0, #0x1f]
    ldr r0, [r5, #0x1e8]
    add r0, r0, r1
    ldrb r0, [r0, #0x86]
    cmp r0, #2
    bhi ov001_02219fd4_L60
    mov r5, #0
ov001_02219fd4_L30:
    mov r0, r4
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    addne r0, r4, #512
    ldrnesb r0, [r0, #71]
    cmpne r0, #0
    movne r0, #1
    ldmneia sp!, {r3, r4, r5, pc}
    add r5, r5, #1
    cmp r5, #3
    add r4, r4, #1088
    blt ov001_02219fd4_L30
ov001_02219fd4_L60:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
