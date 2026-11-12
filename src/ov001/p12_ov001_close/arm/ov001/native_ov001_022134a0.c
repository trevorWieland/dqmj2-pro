/* ov001 row 0x022134a0: 232 bytes.
 *
 * What it does: 57 instructions; 15 call(s) to 0x022134d4, 0x02025a28, 0x02024e0c, +12 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 15 calls (57 instructions, 15 calls, 2 branches, 13 back edges, 1 literal slot).
 *
 *   pool +0xe4 -> constant 0x2aaaaaab (image word 0x2aaaaaab)
 *   branch +0x1c -> +0x34
 *   branch +0x30 -> +0x40
 *   branch +0x5c -> +0x74
 *   branch +0x70 -> +0x80
 *   back edge +0xdc -> +0x9c
 *   test +0x14 cmp r1, #0
 *   test +0x50 cmp r5, #0
 *   test +0xac cmp r7, #0
 *   test +0xb8 cmp r7, #0
 *   test +0xd8 cmp r5, #24
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022134a0; the literal pool and
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

extern void native_fn_02025a28(void);
extern void native_fn_02024e0c(void);
extern void native_fn_02025ca4(void);
extern void native_fn_020259b4(void);
extern void native_fn_0205f98c(void);
extern void native_fn_021f1ba0(void);


asm u32 native_ov001_022134a0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    ldr r0, [r10, #0x38]
    mov r5, r2
    and r4, r0, #255
    cmp r1, #0
    mov r0, r1, lsl #12
    ble ov001_022134a0_L34
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov001_022134a0_L40
ov001_022134a0_L34:
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov001_022134a0_L40:
    bl native_fn_020259b4
    ldr r2, =0x2aaaaaab
    mov r1, r0, lsr #31
    smull r0, r6, r2, r0
    cmp r5, #0
    add r6, r1, r6, asr #2
    mov r0, r5, lsl #12
    ble ov001_022134a0_L74
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov001_022134a0_L80
ov001_022134a0_L74:
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov001_022134a0_L80:
    bl native_fn_020259b4
    mov r1, #24
    mul r9, r4, r1
    mov r5, #0
    mov r7, r0
    mov r11, r5
    mov r4, #1
ov001_022134a0_L9c:
    and r8, r5, #255
    ldr r0, [r10, #0x1c]
    mov r1, r8
    bl native_fn_0205f98c
    cmp r7, #0
    movgt r1, r4
    movle r1, r11
    cmp r7, #0
    str r1, [r0, #0x84]
    addgt r1, r8, r9
    andgt r8, r1, #255
    mov r1, r8
    subgt r7, r7, r6
    bl native_fn_021f1ba0
    add r5, r5, #1
    cmp r5, #24
    blt ov001_022134a0_L9c
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
