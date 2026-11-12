/* ov001 row 0x021e081c: 160 bytes.
 *
 * What it does: 39 instructions; 5 call(s) to 0x02216634, 0x021dda80, 0x021e66f8, +2 more; loops (back edge at +0x30); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 5 calls (39 instructions, 5 calls, 11 branches, 2 back edges, 1 literal slot).
 *
 *   pool +0x9c -> constant 0x022388ec (image word 0x022388ec)
 *   branch +0x0c -> +0x94
 *   branch +0x18 -> +0x90
 *   branch +0x1c -> +0x90
 *   branch +0x20 -> +0x30
 *   branch +0x24 -> +0x44
 *   branch +0x28 -> +0x5c
 *   branch +0x2c -> +0x6c
 *   branch +0x40 -> +0x90
 *   branch +0x58 -> +0x90
 *   branch +0x68 -> +0x90
 *   branch +0x80 -> +0x90
 *   test +0x08 cmp r0, #0
 *   test +0x10 cmp r0, #4
 *   test +0x70 cmp r0, #0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e081c; the literal pool and
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

extern void native_fn_02216634(void);
extern void native_fn_021dda80(void);
extern void native_fn_021e66f8(void);
extern void native_fn_0221669c(void);


asm u32 native_ov001_021e081c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_02216634
    cmp r0, #0
    beq ov001_021e081c_L94
    cmp r0, #4
    addls pc, pc, r0, lsl #2
    b ov001_021e081c_L90
    b ov001_021e081c_L90
    b ov001_021e081c_L30
    b ov001_021e081c_L44
    b ov001_021e081c_L5c
    b ov001_021e081c_L6c
ov001_021e081c_L30:
    bl native_fn_021dda80
    ldr r0, =0x022388ec
    mov r1, #54
    strb r1, [r0, #0x8]
    b ov001_021e081c_L90
ov001_021e081c_L44:
    mov r0, #2
    bl native_fn_021e66f8
    ldr r0, =0x022388ec
    mov r1, #54
    strb r1, [r0, #0x8]
    b ov001_021e081c_L90
ov001_021e081c_L5c:
    ldr r0, =0x022388ec
    mov r1, #21
    strb r1, [r0, #0x8]
    b ov001_021e081c_L90
ov001_021e081c_L6c:
    bl native_fn_021dda80
    cmp r0, #0
    ldreq r0, =0x022388ec
    moveq r1, #28
    streqb r1, [r0, #0x8]
    beq ov001_021e081c_L90
    ldr r0, =0x022388ec
    mov r1, #54
    strb r1, [r0, #0x8]
ov001_021e081c_L90:
    bl native_fn_0221669c
ov001_021e081c_L94:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
