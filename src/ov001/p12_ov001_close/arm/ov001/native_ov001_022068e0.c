/* ov001 row 0x022068e0: 288 bytes.
 *
 * What it does: 71 instructions; 8 call(s) to 0x022068a0, 0x021fcde8, 0x0220704c, +5 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 8 calls (71 instructions, 8 calls, 1 branch, 6 back edges, 1 literal slot).
 *
 *   pool +0x11c -> native_data_0222f028 (image word 0x0222f028)
 *   branch +0x34 -> +0xfc
 *   back edge +0xf8 -> +0x48
 *   test +0x2c cmp r10, #0
 *   test +0xf0 cmp r10, r0, asr #24
 *   0 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022068e0; the literal pool and
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
extern void native_fn_021fcde8(void);
extern void native_fn_0220704c(void);
extern u8 native_data_0222f028[];
extern void native_fn_0206d250(void);
extern void native_fn_021fe4ac(void);
extern void native_fn_02045efc(void);
extern void native_fn_02206a00(void);


asm u32 native_ov001_022068e0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #20
    mov r10, r0
    bl native_fn_022068a0
    mov r7, r0
    mov r0, #0
    str r0, [r7, #0x74]
    str r0, [r7, #0x78]
    str r10, [r7, #0x80]
    bl native_fn_021fcde8
    bl native_fn_0220704c
    cmp r10, #0
    mov r6, #0
    ble ov001_022068e0_Lfc
    ldr r4, =native_data_0222f028
    mov r9, r6
    mov r5, r6
    mov r11, #1
ov001_022068e0_L48:
    add r0, r7, r6, lsl #5
    ldr r0, [r0, #0x28]
    ldrb r1, [r0, #0x5]
    ldrsb r0, [r0, #12]
    mov r1, r1, asr #3
    sub r1, r1, #1
    and r8, r1, #255
    bl native_fn_0206d250
    add r0, r0, r0, lsl #2
    mov r0, r0, asr #1
    and r0, r0, #255
    add r0, r8, r0
    and r2, r0, #255
    ldrb r1, [r4, #0x7]
    mov r0, r9, lsl #24
    mov r0, r0, asr #24
    add r1, r2, r1
    and r1, r1, #255
    str r1, [sp]
    ldrb r3, [r4, #0x8]
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    str r3, [sp, #0x4]
    ldrb r3, [r4, #0x9]
    mov r1, #8
    mov r2, #31
    str r3, [sp, #0x8]
    str r5, [sp, #0xc]
    str r11, [sp, #0x10]
    ldrb r3, [r4, #0x6]
    add r3, r3, #9
    and r3, r3, #255
    bl native_fn_021fe4ac
    add r2, r7, r6, lsl #5
    str r0, [r2, #0x14]
    ldr r0, [r2, #0x24]
    add r9, r9, #2
    ldrb r1, [r0, #0x1fc]
    add r0, r6, #1
    mov r0, r0, lsl #24
    strb r1, [r2, #0x30]
    strb r1, [r2, #0x31]
    cmp r10, r0, asr #24
    mov r6, r0, asr #24
    bgt ov001_022068e0_L48
ov001_022068e0_Lfc:
    mov r0, #1
    str r0, [r7, #0x10]
    mov r1, #0
    strb r1, [r7, #0x91]
    bl native_fn_02045efc
    bl native_fn_02206a00
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
