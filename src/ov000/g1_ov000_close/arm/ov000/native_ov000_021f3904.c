/* ov000 row 0x021f3904: 364 bytes.
 *
 * What it does: 89 instructions; 9 call(s) to 0x021e7194, 0x021e6a40, 0x021e6aa0, +6 more; loops (back edge at +0x08); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x164 -> constant 0x02236ed8 (image word 0x02236ed8)
 *   pool +0x168 -> constant 0x02710000 (image word 0x02710000)
 *   branch +0x48 -> +0xc8
 *   branch +0xa0 -> +0xc8
 *   branch +0xb0 -> +0xc8
 *   back edge +0xe4 -> +0x2c
 *   branch +0xf4 -> +0x158
 *   branch +0x128 -> +0x138
 *   branch +0x144 -> +0x158
 *   back edge +0x154 -> +0x10c
 *   test +0x3c cmp r0, #0
 *   test +0x44 cmpne r0, #0
 *   test +0xac cmp r0, #0
 *   test +0xd0 cmp r0, #0
 *   test +0xdc cmp r5, #8
 *   test +0xec cmp r6, #0
 *   test +0x124 cmp r0, #0
 *   test +0x140 cmp r9, r4
 *   test +0x14c cmp r9, r6
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f3904; the literal pool and
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

extern void native_fn_021e7194(void);
extern void native_fn_021e6a40(void);
extern void native_fn_021e6aa0(void);
extern void native_fn_021e0754(void);
extern void native_fn_021f3870(void);
extern void native_fn_02042be8(void);


asm u32 native_ov000_021f3904 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #164
    bl native_fn_021e7194
    mov r1, #0
    str r0, [sp]
    bl native_fn_021e6a40
    mov r6, #0
    add r10, sp, #4
    mov r7, r0
    mov r5, r6
    mov r9, r6
ov000_021f3904_L2c:
    ldr r0, =0x02236ed8
    ldr r0, [r0, #0x4]
    add r8, r0, r9
    ldrb r0, [r8, #0x278]
    cmp r0, #0
    ldrneb r0, [r8, #0x279]
    cmpne r0, #0
    beq ov000_021f3904_Lc8
    mov r0, #0
    strb r0, [r8, #0x1e2]
    ldr r1, [r7, #0x4]
    ldr r0, [r8, #0x74]
    ldr r4, [r7]
    sub r2, r1, r0
    smull r1, r0, r2, r2
    ldr r2, [r8, #0x70]
    ldr r3, [r7, #0x8]
    sub r2, r4, r2
    smlal r1, r0, r2, r2
    ldr r2, [r8, #0x78]
    sub r2, r3, r2
    smlal r1, r0, r2, r2
    mov r11, r1, lsr #12
    mov r4, r0, asr #12
    orr r11, r11, r0, lsl #20
    ldr r0, =0x02710000
    subs r0, r11, r0
    mov r0, #0
    sbcs r0, r4, r0
    bge ov000_021f3904_Lc8
    add r0, r8, #112
    bl native_fn_021e6aa0
    cmp r0, #0
    beq ov000_021f3904_Lc8
    str r5, [r10]
    str r11, [r10, #0x8]
    str r4, [r10, #0xc]
    add r10, r10, #20
    add r6, r6, #1
ov000_021f3904_Lc8:
    ldr r0, [sp]
    add r5, r5, #1
    cmp r0, #0
    moveq r0, #0
    streqb r0, [r8, #0x27a]
    cmp r5, #8
    add r9, r9, #636
    blt ov000_021f3904_L2c
    bl native_fn_021e0754
    cmp r6, #0
    mov r9, #0
    ble ov000_021f3904_L158
    mov r5, #1
    ldr r11, =0x02236ed8
    add r8, sp, #4
    sub r4, r0, #1
    mov r7, r5
ov000_021f3904_L10c:
    ldr r2, [r11, #0x4]
    ldr r1, [r8]
    mov r0, #636
    mla r10, r1, r0, r2
    strb r7, [r10, #0x1e2]
    ldrb r0, [r10, #0x27a]
    cmp r0, #0
    bne ov000_021f3904_L138
    mov r0, r10
    bl native_fn_021f3870
    strb r5, [r10, #0x27a]
ov000_021f3904_L138:
    mov r0, r10
    bl native_fn_02042be8
    cmp r9, r4
    beq ov000_021f3904_L158
    add r9, r9, #1
    cmp r9, r6
    add r8, r8, #20
    blt ov000_021f3904_L10c
ov000_021f3904_L158:
    mov r0, r6
    add sp, sp, #164
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
