/* ov001 row 0x02206a78: 116 bytes.
 *
 * What it does: 29 instructions; 3 call(s) to 0x022068a0, 0x02206ad8, 0x0206cf44; loops (back edge at +0x04); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 3 calls (29 instructions, 3 calls, 1 branch, 3 back edges, 0 literal slots).
 *
 *   branch +0x18 -> +0x60
 *   back edge +0x5c -> +0x24
 *   test +0x14 cmp r0, #0
 *   test +0x58 cmp r1, r0, asr #24
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02206a78; the literal pool and
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

extern void native_fn_022068a0(void);
extern void native_fn_0206cf44(void);


asm u32 native_ov001_02206a78 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    bl native_fn_022068a0
    mov r6, r0
    ldr r0, [r6, #0x80]
    mov r7, #0
    cmp r0, #0
    ble ov001_02206a78_L60
    mov r5, #24
    mov r4, #1
ov001_02206a78_L24:
    add r0, r6, r7, lsl #5
    ldr r2, [r0, #0x28]
    and r1, r5, #255
    strb r5, [r2, #0x4]
    ldrsb r0, [r2, #12]
    ldrb r2, [r2, #0x5]
    bl native_fn_0206cf44
    add r0, r6, r7, lsl #5
    str r4, [r0, #0x2c]
    add r0, r7, #1
    mov r0, r0, lsl #24
    ldr r1, [r6, #0x80]
    mov r7, r0, asr #24
    cmp r1, r0, asr #24
    bgt ov001_02206a78_L24
ov001_02206a78_L60:
    mov r0, #1
    str r0, [r6, #0x74]
    mov r1, #0
    str r1, [r6, #0x78]
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
