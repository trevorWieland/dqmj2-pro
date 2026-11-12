/* ov000 row 0x021f7878: 360 bytes.
 *
 * What it does: 89 instructions; 21 call(s) to 0x02061944, 0x021f78b8, 0x02025a28, +18 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x164 -> constant 0x30c30c31 (image word 0x30c30c31)
 *   branch +0x28 -> +0x40
 *   branch +0x3c -> +0x4c
 *   branch +0x68 -> +0x80
 *   branch +0x7c -> +0x8c
 *   branch +0x9c -> +0xa8
 *   branch +0xd8 -> +0xf0
 *   branch +0xec -> +0x130
 *   branch +0xf4 -> +0x110
 *   branch +0x10c -> +0x130
 *   back edge +0x14c -> +0xd4
 *   test +0x20 cmp r4, #0
 *   test +0x5c cmp r6, #0
 *   test +0xa0 cmp r6, #0
 *   test +0xd4 cmp r7, #0
 *   test +0xf0 cmp r7, #3
 *   test +0x144 cmp r6, #7
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f7878; the literal pool and
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

extern void native_fn_02061944(void);
extern void native_fn_02025a28(void);
extern void native_fn_02024e0c(void);
extern void native_fn_02025ca4(void);
extern void native_fn_020259b4(void);
extern void native_fn_02026144(void);
extern void native_fn_02065818(void);


asm u32 native_ov000_021f7878 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r4, r3
    mov r8, r0
    mov r10, r1
    mov r6, r2
    ldr r9, [sp, #0x28]
    bl native_fn_02061944
    mov r5, r0
    cmp r4, #0
    mov r0, r4, lsl #12
    ble ov000_021f7878_L40
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov000_021f7878_L4c
ov000_021f7878_L40:
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov000_021f7878_L4c:
    bl native_fn_020259b4
    ldr r2, =0x30c30c31
    mov r1, r0, lsr #31
    smull r0, r4, r2, r0
    cmp r6, #0
    add r4, r1, r4, asr #2
    mov r0, r6, lsl #12
    ble ov000_021f7878_L80
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov000_021f7878_L8c
ov000_021f7878_L80:
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov000_021f7878_L8c:
    bl native_fn_020259b4
    mov r1, r4
    bl native_fn_02026144
    movs r7, r0
    bne ov000_021f7878_La8
    cmp r6, #0
    movne r7, #1
ov000_021f7878_La8:
    mov r1, r8
    mov r2, r10
    add r0, r5, #88
    bl native_fn_02065818
    mov r1, #12
    add r0, r8, #1
    mov r0, r0, lsl #24
    mul r11, r9, r1
    mov r8, r0, asr #24
    add r4, r5, #16
    mov r6, #0
ov000_021f7878_Ld4:
    cmp r7, #0
    bne ov000_021f7878_Lf0
    mov r1, r8
    mov r2, r10
    add r0, r5, #100
    bl native_fn_02065818
    b ov000_021f7878_L130
ov000_021f7878_Lf0:
    cmp r7, #3
    blt ov000_021f7878_L110
    mov r1, r8
    mov r2, r10
    add r0, r4, r11
    bl native_fn_02065818
    sub r7, r7, #3
    b ov000_021f7878_L130
ov000_021f7878_L110:
    rsb r0, r7, #3
    add r1, r9, r0
    mov r0, #12
    mla r0, r1, r0, r4
    mov r1, r8
    mov r2, r10
    bl native_fn_02065818
    mov r7, #0
ov000_021f7878_L130:
    add r0, r6, #1
    add r2, r8, #1
    mov r1, r0, lsl #24
    mov r0, r2, lsl #24
    mov r6, r1, asr #24
    cmp r6, #7
    mov r8, r0, asr #24
    blt ov000_021f7878_Ld4
    mov r1, r8
    mov r2, r10
    add r0, r5, #112
    bl native_fn_02065818
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
