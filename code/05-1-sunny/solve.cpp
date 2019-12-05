// c++ -O3 -std=c++17 solve.cpp -o solve
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

typedef uint8_t u8;
typedef uint32_t u32;
typedef int32_t i32;

using std::cout, std::cin, std::clog, std::endl, std::ifstream;
using std::getline, std::stoi, std::string;
using std::vector;


void emu(vector<i32>& mem) {
    for (size_t ip = 0; ip < mem.size(); ) {
        u32 op = mem[ip];
        u32 ma = op / 100 % 10;
        u32 mb = op / 1000 % 10;
        op %= 100;

        switch (op) {

            case 1: {
                u32 a = mem[ip + 1];
                u32 b = mem[ip + 2];
                u32 c = mem[ip + 3];
                i32 x = ma ? a : mem[a];
                i32 y = mb ? b : mem[b];
                mem[c] = x + y;
                ip += 4;
            }
                break;

            case 2: {
                u32 a = mem[ip + 1];
                u32 b = mem[ip + 2];
                u32 c = mem[ip + 3];
                i32 x = ma ? a : mem[a];
                i32 y = mb ? b : mem[b];
                mem[c] = x * y;
                ip += 4;
            }
                break;

            case 3: {
                u32 a = mem[ip + 1];
                string s;
                getline(cin, s);
                i32 x = stoi(s);
                mem[a] = x;
                ip += 2;
            }
                break;

            case 4: {
                u32 a = mem[ip + 1];
                i32 x = ma ? a : mem[a];
                cout << x << endl;
                ip += 2;
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

    vector<i32> data;

    ifstream fp(argv[1]);
    string tok;
    while (getline(fp, tok, ',')) {
        i32 x = stoi(tok);
        data.push_back(x);
    }

    emu(data);

    return 0;
}
