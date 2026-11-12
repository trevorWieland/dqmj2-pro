/* ov006 row 0x021fd580: 172 bytes.
 *
 * What it does: 67 instructions; 7 call(s) to 0x021f5344, 0x021ff6d4, 0x021f5344, +4 more; loops (back edge at +0x0a); returns through pop {r4, r5, r6, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x94 -> constant 0x0221c114 (image word 0x0221c114)
 *   pool +0x98 -> native_data_0220b8d6 (image word 0x0220b8d6)
 *   pool +0x9c -> native_data_0220b940 (image word 0x0220b940)
 *   pool +0xa0 -> native_data_0220b944 (image word 0x0220b944)
 *   pool +0xa4 -> native_data_0220b942 (image word 0x0220b942)
 *   pool +0xa8 -> native_data_0220b946 (image word 0x0220b946)
 *   branch +0x20 -> +0x92
 *   branch +0x24 -> +0x2a
 *   branch +0x30 -> +0x3c
 *   branch +0x3a -> +0x40
 *   test +0x1e cmp r1, r0
 *   test +0x22 cmp r1, #0x0
 *   test +0x2e cmp r1, r0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fd580; the literal pool and
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

extern void native_fn_021f5344(void);
extern u8 native_data_0220b8d6[];
extern void native_fn_021ff6d4(void);
extern u8 native_data_0220b940[];
extern u8 native_data_0220b944[];
extern u8 native_data_0220b942[];
extern u8 native_data_0220b946[];
extern void native_fn_021f29bc(void);


asm u32 native_ov006_021fd580 (register u32 a0)
{
    push {r4, r5, r6, lr}
    ldr r1, =0x0221c114
    add r5, r0, #0x0
    mov r0, #0x1
    ldrsb r4, [r1, r0]
    bl native_fn_021f5344
    lsl r2, r0, #0x4
    ldr r0, =native_data_0220b8d6
    lsl r1, r4, #0x2
    add r0, r0, r2
    add r0, r1, r0
    ldrsb r1, [r5, r0]
    mov r0, #0x0
    mvn r0, r0
    cmp r1, r0
    beq ov006_021fd580_L92
    cmp r1, #0x0
    bne ov006_021fd580_L2a
    ldr r0, =0x0221c114
    strb r4, [r0, #0]
ov006_021fd580_L2a:
    mov r0, #0x1
    mvn r0, r0
    cmp r1, r0
    bne ov006_021fd580_L3c
    ldr r1, =0x0221c114
    mov r0, #0x0
    ldrsb r0, [r1, r0]
    strb r0, [r1, #0x1]
    b ov006_021fd580_L40
ov006_021fd580_L3c:
    ldr r0, =0x0221c114
    strb r1, [r0, #0x1]
ov006_021fd580_L40:
    mov r0, #0x8
    bl native_fn_021ff6d4
    mov r0, #0x1
    bl native_fn_021f5344
    add r5, r0, #0x0
    mov r0, #0x1
    bl native_fn_021f5344
    add r4, r0, #0x0
    mov r0, #0x1
    bl native_fn_021f5344
    add r6, r0, #0x0
    mov r0, #0x1
    bl native_fn_021f5344
    lsl r1, r5, #0x5
    add r3, r0, #0x0
    ldr r0, =native_data_0220b940
    ldr r5, =0x0221c114
    mov r2, #0x1
    ldrsb r2, [r5, r2]
    add r0, r0, r1
    ldr r1, =native_data_0220b944
    lsl r5, r2, #0x3
    lsl r2, r4, #0x5
    add r1, r1, r2
    ldr r2, =native_data_0220b942
    lsl r4, r6, #0x5
    add r2, r2, r4
    lsl r4, r3, #0x5
    ldr r3, =native_data_0220b946
    ldrh r0, [r5, r0]
    add r3, r3, r4
    ldrh r1, [r5, r1]
    ldrh r2, [r5, r2]
    ldrh r3, [r5, r3]
    bl native_fn_021f29bc
ov006_021fd580_L92:
    pop {r4, r5, r6, pc}
}
