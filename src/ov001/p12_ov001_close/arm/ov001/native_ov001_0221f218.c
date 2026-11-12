/* ov001 row 0x0221f218: 68 bytes.
 *
 * What it does: 17 instructions; 2 call(s) to 0x02044cdc, 0x021db578; loops (back edge at +0x10); returns through pop {r4, pc}
 *
 * Decoded shape: loop with 2 calls (17 instructions, 2 calls, 1 branch, 2 back edges, 0 literal slots).
 *
 *   branch +0x18 -> +0x3c
 *   test +0x14 cmp r0, #2
 *   test +0x20 cmp r0, #0
 *   test +0x30 cmp r0, #2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221f218; the literal pool and
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

extern void native_fn_02044cdc(void);
extern void native_fn_021db578(void);


asm u32 native_ov001_0221f218 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r4, [r0]
    ldr r0, [r4, #0x1e8]
    ldrsh r0, [r0, #42]
    bl native_fn_02044cdc
    cmp r0, #2
    bne ov001_0221f218_L3c
    ldrb r0, [r4, #0x31e]
    cmp r0, #0
    moveq r0, #1
    movne r0, #0
    bl native_fn_021db578
    cmp r0, #2
    movge r0, #1
    ldmgeia sp!, {r4, pc}
ov001_0221f218_L3c:
    mov r0, #0
    ldmia sp!, {r4, pc}
}
