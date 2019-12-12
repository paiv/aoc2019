import io


class IntcodeDisasm:
    def process(self, image, output=None):
        return self._generate(image.program, ip=image.ip, output=output)

    def _generate(self, mem, ip=0, output=None):
        so = output or io.StringIO()

        def write_line(*args, end='\n'):
            print(*args, end=end, file=so)

        def ref(m, a):
            return f'[base+{a}]' if m == 2 else f'[{a}]' if m == 0 else str(a)

        known_ops = {1, 2, 3, 4, 5, 6, 7, 8, 99}

        skipped = list()

        while ip < len(mem):
            op = mem[ip]
            ma = op // 100 % 10
            mb = op // 1000 % 10
            op %= 100

            if op in known_ops:
                if skipped:
                    o = ip - len(skipped)
                    for i in range(0, len(skipped), 8):
                        s = ', '.join(map(str, skipped[i:i+8]))
                        write_line(f'{o:05}:', end=' ')
                        write_line(f'dw {s}')
                        o += 8
                    skipped = list()

            if op == 1:
                a = mem[ip + 1]
                b = mem[ip + 2]
                c = mem[ip + 3]
                write_line(f'{ip:05}:', end=' ')
                ip += 4
                write_line(f'add [{c}], {ref(ma, a)}, {ref(mb, b)}')

            elif op == 2:
                a = mem[ip + 1]
                b = mem[ip + 2]
                c = mem[ip + 3]
                write_line(f'{ip:05}:', end=' ')
                ip += 4
                write_line(f'mul [{c}], {ref(ma, a)}, {ref(mb, b)}')

            elif op == 3:
                a = mem[ip + 1]
                write_line(f'{ip:05}:', end=' ')
                ip += 2
                write_line(f'in [{a}]')

            elif op == 4:
                a = mem[ip + 1]
                write_line(f'{ip:05}:', end=' ')
                ip += 2
                write_line(f'out {ref(ma, a)}')

            elif op == 5:
                a = mem[ip + 1]
                b = mem[ip + 2]
                write_line(f'{ip:05}:', end=' ')
                ip += 3
                write_line(f'jnz {ref(ma, a)}, {ref(mb, b)}')

            elif op == 6:
                a = mem[ip + 1]
                b = mem[ip + 2]
                write_line(f'{ip:05}:', end=' ')
                ip += 3
                write_line(f'jz {ref(ma, a)}, {ref(mb, b)}')

            elif op == 7:
                a = mem[ip + 1]
                b = mem[ip + 2]
                c = mem[ip + 3]
                write_line(f'{ip:05}:', end=' ')
                ip += 4
                write_line(f'mov [{c}], {ref(ma, a)} < {ref(mb, b)}')

            elif op == 8:
                a = mem[ip + 1]
                b = mem[ip + 2]
                c = mem[ip + 3]
                write_line(f'{ip:05}:', end=' ')
                ip += 4
                write_line(f'mov [{c}], {ref(ma, a)} == {ref(mb, b)}')

            elif op == 9:
                a = mem[ip + 1]
                write_line(f'{ip:05}:', end=' ')
                ip += 2
                write_line(f'add base, {ref(ma, a)}')

            elif op == 99:
                write_line(f'{ip:05}:', end=' ')
                ip += 1
                write_line(f'hlt')

            else:
                skipped.append(mem[ip])
                ip += 1


        if hasattr(so, 'getvalue'):
            return so.getvalue()
        return so
