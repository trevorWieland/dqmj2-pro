/* ov001 row 0x021d8b88: 212 bytes.
 *
 * What it does: 47 instructions; 4 call(s) to 0x0206531c, 0x021eea10, 0x0205ccb8, +1 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: loop with 4 calls (47 instructions, 4 calls, 18 branches, 3 back edges, 6 literal slots).
 *
 *   pool +0xbc -> constant 0x00000386 (image word 0x00000386)
 *   pool +0xc0 -> constant 0x00000385 (image word 0x00000385)
 *   pool +0xc4 -> constant 0x0000038b (image word 0x0000038b)
 *   pool +0xc8 -> constant 0x00000389 (image word 0x00000389)
 *   pool +0xcc -> constant 0x0000038a (image word 0x0000038a)
 *   pool +0xd0 -> constant 0x022316bc (image word 0x022316bc)
 *   branch +0x18 -> +0x74
 *   branch +0x1c -> +0x74
 *   branch +0x20 -> +0x3c
 *   branch +0x24 -> +0x44
 *   branch +0x28 -> +0x4c
 *   branch +0x2c -> +0x5c
 *   branch +0x30 -> +0x64
 *   branch +0x34 -> +0x6c
 *   branch +0x38 -> +0x54
 *   branch +0x40 -> +0x78
 *   branch +0x48 -> +0x78
 *   branch +0x50 -> +0x78
 *   branch +0x58 -> +0x78
 *   branch +0x60 -> +0x78
 *   branch +0x68 -> +0x78
 *   branch +0x70 -> +0x78
 *   branch +0x84 -> +0xb4
 *   branch +0x98 -> +0xb0
 *   test +0x10 cmp r0, #7
 *   test +0x7c cmp r4, #0
 *   test +0x94 cmp r6, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021d8b88; the literal pool and
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

extern void native_fn_0206531c(void);
extern void native_fn_021eea10(void);
extern void native_fn_0205ccb8(void);
extern void native_fn_0205ce38(void);


asm u32 native_ov001_021d8b88 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    mov r5, #0
    bl native_fn_0206531c
    cmp r0, #7
    addls pc, pc, r0, lsl #2
    b ov001_021d8b88_L74
    b ov001_021d8b88_L74
    b ov001_021d8b88_L3c
    b ov001_021d8b88_L44
    b ov001_021d8b88_L4c
    b ov001_021d8b88_L5c
    b ov001_021d8b88_L64
    b ov001_021d8b88_L6c
    b ov001_021d8b88_L54
ov001_021d8b88_L3c:
    mov r4, #900
    b ov001_021d8b88_L78
ov001_021d8b88_L44:
    ldr r4, =0x00000386
    b ov001_021d8b88_L78
ov001_021d8b88_L4c:
    ldr r4, =0x00000385
    b ov001_021d8b88_L78
ov001_021d8b88_L54:
    ldr r4, =0x0000038b
    b ov001_021d8b88_L78
ov001_021d8b88_L5c:
    mov r4, #904
    b ov001_021d8b88_L78
ov001_021d8b88_L64:
    ldr r4, =0x00000389
    b ov001_021d8b88_L78
ov001_021d8b88_L6c:
    ldr r4, =0x0000038a
    b ov001_021d8b88_L78
ov001_021d8b88_L74:
    mov r4, #0
ov001_021d8b88_L78:
    ldr r0, =0x022316bc
    cmp r4, #0
    strh r4, [r0, #96]
    beq ov001_021d8b88_Lb4
    mov r0, r4
    mov r1, #1
    bl native_fn_021eea10
    cmp r6, #0
    beq ov001_021d8b88_Lb0
    mov r0, r4
    mov r1, #5120
    bl native_fn_0205ccb8
    mov r1, #18432
    bl native_fn_0205ce38
ov001_021d8b88_Lb0:
    mov r5, #1
ov001_021d8b88_Lb4:
    mov r0, r5
    ldmia sp!, {r4, r5, r6, pc}
}
