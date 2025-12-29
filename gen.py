#!/usr/bin/env python3


def parse_status_file(path):
    with open(path, 'r') as fp:
        status_file = fp.read()

    kv = dict()

    for line in status_file.split('\n'):
        if len(line) == 0:
            continue
        s = line.split('\t')
        key = s[0].split(':')[0]
        value = s[1].strip()
        # print(f'"{key}" => "{value}"')

        kv[key] = value

    def str_kb_to_int(value):
        s = value.split(' ')
        assert (len(s) == 2)
        unit = s[1].lower()
        if unit == 'kb':
            return int(s[0]) * 1024
        else:
            return None

    ret = dict()
    ret['VmData'] = str_kb_to_int(kv['VmData'])
    ret['VmPeak'] = str_kb_to_int(kv['VmPeak'])
    ret['VmHWM'] = str_kb_to_int(kv['VmHWM'])
    ret['VmRSS'] = str_kb_to_int(kv['VmRSS'])
    # print(f'{ret}')
    return ret


def write_results(results, path):
    with open(path, 'w') as fp:
        # fp.write(':orphan:\n')
        fp.write('\n')
        fp.write('.. list-table:: Memory usage\n')
        fp.write('   :header-rows: 1\n')
        fp.write('\n')
        fp.write('   * - VmData\n')
        fp.write('     - VmPeak\n')
        fp.write('     - VmHWM\n')
        fp.write('     - VmRSS\n')

        for r in results:
            fp.write(f'   * - {r["VmData"]}\n')
            fp.write(f'     - {r["VmPeak"]}\n')
            fp.write(f'     - {r["VmHWM"]}\n')
            fp.write(f'     - {r["VmRSS"]}\n')


def parse_map_file(path):
    ret = []

    import re
    r = re.compile(r'^(\.[a-z\.]+)[\t ]+([a-z0-9]+)[\t ]+([a-z0-9]+)$')
    with open(path, 'r') as fp:
        for line in fp.read().split('\n'):
            m = r.match(line)
            if m is not None:
                # print(f'{m[1]}: {m[2]} @ {m[3]}')
                section_name = m[1]
                offset = int(m[2], 16)
                size = int(m[3], 16)
                # print(f'{section_name}: {offset} @ {size}')
                ret.append((section_name, offset, size))

    return ret


def write_sections_sizes(sections, path):
    with open(path, 'w') as fp:
        # fp.write(':orphan:\n')
        fp.write('\n')
        fp.write('.. list-table:: Static memory usage\n')
        fp.write('   :header-rows: 1\n')
        fp.write('\n')

        for i, section in enumerate(sections):
            section_name = section[0]
            if i == 0:
                fp.write(f'   * - {section_name}\n')
            else:
                fp.write(f'     - {section_name}\n')

        for i, section in enumerate(sections):
            section_size = section[2]
            if i == 0:
                fp.write(f'   * - {section_size} bytes \n')
            else:
                fp.write(f'     - {section_size} bytes\n')


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--status-file', type=str)
    parser.add_argument('--output', type=str)
    parser.add_argument('--map-file', type=str)
    args = parser.parse_args()

    if args.status_file is not None:
        result = parse_status_file(args.status_file)
        if args.output is not None:
            write_results([result], args.output)

    elif args.map_file is not None:
        sections = parse_map_file(args.map_file)
        output_sections = []
        for section in sections:
            section_name = section[0]
            section_offset = section[1]
            section_size = section[2]

            known_sections = ['.text', '.data', '.bss']
            if section_name in known_sections:
                print(f'{section_name}: {section_offset} @ {section_size}')
                output_sections.append((section_name, section_offset,
                                        section_size))

        if args.output is not None:
            write_sections_sizes(output_sections, args.output)


if __name__ == '__main__':
    main()
