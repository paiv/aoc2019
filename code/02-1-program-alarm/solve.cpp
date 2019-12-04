// c++ -O3 -std=c++17 solve.c -o solve
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

typedef uint8_t u8;
typedef uint32_t u32;

using std::cout, std::clog, std::endl, std::ifstream;
using std::getline, std::stoi, std::string;
using std::vector;


void emu(vector<u32>& mem) {
    for (size_t ip = 0; ip < mem.size(); ) {
        u32 op = mem[ip];
        switch (op) {

            case 1: {
                u32 a = mem[ip + 1];
                u32 b = mem[ip + 2];
                u32 c = mem[ip + 3];
                mem[c] = mem[a] + mem[b];
                ip += 4;
            }
                break;

            case 2: {
                u32 a = mem[ip + 1];
                u32 b = mem[ip + 2];
                u32 c = mem[ip + 3];
                mem[c] = mem[a] * mem[b];
                ip += 4;
            }
                break;

            case 99:
                ip++;
                return;

            default:
                clog << "unhandled op " << op << endl;
                exit(1);
        }
    }
}


int main(int argc, char const *argv[]) {
    if (argc < 2) {
        clog << "usage: solve <input>" << endl;
        return 0;
    }

    vector<u32> data;

    ifstream fp(argv[1]);
    string tok;
    while (getline(fp, tok, ',')) {
        u32 x = stoi(tok);
        data.push_back(x);
    }

    auto mem = data;
    mem[1] = 12;
    mem[2] = 2;
    emu(mem);

    cout << mem[0] << endl;

    return 0;
}
