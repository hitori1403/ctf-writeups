use std::fs;

const JZ_JNZ_OBF: [u8; 5] = [0x74, 0x3, 0x75, 0x1, 0xe8];

fn main() {
    let mut data = fs::read("/tmp/nano").unwrap();

    for i in 0..data.len() - JZ_JNZ_OBF.len() {
        let mut matched = true;
        for j in 0..JZ_JNZ_OBF.len() {
            if data[i + j] != JZ_JNZ_OBF[j] {
                matched = false;
                break;
            }
        }
        if matched {
            for j in 0..JZ_JNZ_OBF.len() {
                data[i + j] = 0x90;
            }
        }
    }

    _ = fs::write("/tmp/nano_patched", data);
}
