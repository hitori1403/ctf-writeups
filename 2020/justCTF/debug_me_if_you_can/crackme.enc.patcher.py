from struct import unpack

import ida_bytes


def decrypt(crackme_bytes, dec_key_data):
    xor_elem = dec_key_data[0] + dec_key_data[4]  #[4] is always 0 in this case

    x = dec_key_data[3] ^ (xor_elem & 0xff)  # 0x40
    y = dec_key_data[3] ^ (xor_elem >> 8)  # 0x42

    xor_res = x ^ (y << 8) ^ (x << 16) ^ (y << 24) ^ (x << 32) ^ (y << 40) ^ (
        x << 48) ^ (y << 56)

    dec_bytes = crackme_bytes ^ xor_res
    return dec_bytes


def start_patch():
    for leetbabe_addr, feedcode_addr, deadcode_addr in zip(leetbabes, feedcodes,
                                                           deadcodes):

        print("1337BABE @ " + hex(leetbabe_addr))
        print("FEEDC0DE @ " + hex(feedcode_addr))
        print("DEADC0DE @ " + hex(deadcode_addr))

        ref_bytes = ida_bytes.get_qword(leetbabe_addr + 4) & 0xffff

        for i in range(0, len(dec_key_data), 5):
            if dec_key_data[i] == ref_bytes:
                patch_addr = leetbabe_addr + 4 + (dec_key_data[i + 1]
                                                  & 0xff) + (dec_key_data[i + 1] >> 32)
                crackme_bytes = ida_bytes.get_qword(patch_addr)
                dec_res = decrypt(crackme_bytes, dec_key_data[i:i + 5])
                print("Patching " + hex(crackme_bytes) + " with " + hex(dec_res) +
                      " @ " + hex(patch_addr))
                ida_bytes.patch_qword(patch_addr, dec_res)

        print("Patching unnecessary code with NOPS :)")
        ida_bytes.patch_bytes(leetbabe_addr - 1,
                              b"\x90" * 7)  # 0xcc + 1337babe + 2 bytes
        ida_bytes.patch_bytes(feedcode_addr, b"\x90" * 4)  # feedc0de
        ida_bytes.patch_bytes(deadcode_addr - 1, b"\x90" * 5)  # 0xcc + deadc0de
        print("======================================")


dec_key_data = '7777000000000000180000000700000008000000000000004100000000000000000000000000000077770000000000001800000070000000080000000000000042000000000000000000000000000000777700000000000018000000db0000000800000000000000430000000000000000000000000000007777000000000000180000003b000000080000000000000027000000000000000000000000000000777700000000000018000000a300000008000000000000009400000000000000000000000000000007070000000000001400000007000000080000000000000041000000000000000000000000000000070700000000000014000000080000000800000000000000420000000000000000000000000000000707000000000000140000000b0000000800000000000000430000000000000000000000000000000707000000000000140000000700000008000000000000002700000000000000000000000000000007070000000000001400000007000000080000000000000094000000000000000000000000000000bbaa0000000000001400000007000000080000000000000041000000000000000000000000000000bbaa000000000000140000000b000000080000000000000042000000000000000000000000000000bbaa0000000000001400000012000000080000000000000043000000000000000000000000000000bbaa0000000000001400000008000000080000000000000027000000000000000000000000000000bbaa000000000000140000000c00000008000000000000009400000000000000000000000000000002020000000000001800000007000000080000000000000041000000000000000000000000000000020200000000000018000000900000000800000000000000420000000000000000000000000000000202000000000000180000001b0100000800000000000000430000000000000000000000000000000202000000000000180000004b000000080000000000000027000000000000000000000000000000020200000000000018000000d3000000080000000000000094000000000000000000000000000000cdab0000000000001800000007000000080000000000000041000000000000000000000000000000cdab0000000000001800000090000000080000000000000042000000000000000000000000000000cdab000000000000180000001c010000080000000000000043000000000000000000000000000000cdab000000000000180000004b000000080000000000000027000000000000000000000000000000cdab00000000000018000000d30000000800000000000000940000000000000000000000000000003412000000000000180000000700000008000000000000004100000000000000000000000000000034120000000000001800000077000000080000000000000042000000000000000000000000000000341200000000000018000000e90000000800000000000000430000000000000000000000000000003412000000000000180000003e000000080000000000000027000000000000000000000000000000341200000000000018000000ad0000000800000000000000940000000000000000000000000000000103000000000000180000000700000008000000000000004100000000000000000000000000000001030000000000001800000078000000080000000000000042000000000000000000000000000000010300000000000018000000ec0000000800000000000000430000000000000000000000000000000103000000000000180000003f000000080000000000000027000000000000000000000000000000010300000000000018000000af000000080000000000000094000000000000000000000000000000'

dec_key_data = unpack('<' + 'Q' * 175, bytes.fromhex(dec_key_data))

leetbabes = [0x123e, 0x1353, 0x139a, 0x13e8, 0x155a, 0x16b8, 0x17dd]
feedcodes = [0x1256, 0x1367, 0x13ae, 0x1400, 0x1572, 0x16d0, 0x17f5]
deadcodes = [0x133f, 0x1380, 0x13ce, 0x1529, 0x169c, 0x17c7, 0x18ef]

start_patch()
