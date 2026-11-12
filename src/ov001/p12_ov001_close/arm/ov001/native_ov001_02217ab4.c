/* ov001 row 0x02217ab4: 108 bytes.
 *
 * What it does: 25 instructions; 3 call(s) to 0x021f1294, 0x0220f9a4, 0x02202568; loops (back edge at +0x0c); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 3 calls (25 instructions, 3 calls, 1 branch, 3 back edges, 2 literal slots).
 *
 *   pool +0x64 -> constant 0x02242c40 (image word 0x02242c40)
 *   pool +0x68 -> constant 0x02242c41 (image word 0x02242c41)
 *   branch +0x38 -> +0x58
 *   test +0x2c cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02217ab4; the literal pool and
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

extern void native_fn_021f1294(void);
extern void native_fn_0220f9a4(void);
extern void native_fn_02202568(void);


asm u32 native_ov001_02217ab4 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mov r0, #16
    mov r1, #2
    bl native_fn_021f1294
    ldr r0, =0x02242c40
    ldr r2, =0x02242c41
    ldr r3, [r0, #0x8]
    ldrh r1, [r0, #4]
    ldr r0, [r3, #0x1e8]
    add r0, r0, #70
    bl native_fn_0220f9a4
    cmp r0, #0
    ldreq r0, =0x02242c40
    moveq r1, #1
    beq ov001_02217ab4_L58
    ldr r0, =0x02242c40
    ldr r1, [r0, #0x8]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_02202568
    ldr r0, =0x02242c40
    mov r1, #2
ov001_02217ab4_L58:
    strb r1, [r0]
    mov r0, #1
    ldmia sp!, {r3, pc}
}
