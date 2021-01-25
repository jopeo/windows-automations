from os import path, getcwd, scandir, stat, stat_result
from shutil import rmtree, copytree, ignore_patterns, copy2

def fmt_n_log(str_chr: list, le=60, str_log=''):
    """
    to omit the header linebreak '\n', place False as third item in tuple [(s1,c1, False), (s2,c2)]
    :param str_chr: a list of tuples [(s1,c1), (s2,c2)] with 'string to log', 'character to fill'
    :param le: length of line output, including fill characters
    :param str_log: a string you want to append this to
    :return: the formatted string
    """
    try:
        for s in range(len(str_chr)):
            if len(str_chr[s]) > 2 and str_chr[s][2] is False:
                str_log += str_chr[s][0]
            else:
                p1 = f'{str_chr[s][0]:{str_chr[s][1]}^{le}}'
                str_log += '\n' + p1
        return str_log
    except:
        pass

    return


def print_list(inlist: list) -> int:
    if inlist:
        for i in inlist:
            print(f'        {i}')
    else:
        print(f'        None')
    return len(inlist)


def sloppy_copy(src: str, dst: str, ignore_glob: str = 'None'):
    """copies any file or folder type where:
    :param src: source folder path
    :param dest: destination folder path
    :param
    :return
    # todo: finish docstrings later
    """
    d = [[],  #  (str, float)  dest_bef_files   , mod_time
         [],  #  (str, float)  dest_bef_folders , mod_time
         [],  #  (str, float)  dest_aft_files   , mod_time
         []]  #  (str, float)  dest_aft_folders , mod_time

    s = [[],  #   (str, float)  src_bef_files   , mod_time
         [],  #   (str, float)  src_bef_folders , mod_time
         [],  #   (str, float)  src_aft_files   , mod_time
         []]  #   (str, float)  src_aft_folders , mod_time

    res = []   #  [(list, int),     # files copied, number
               #   (list, int),     # folders copied, number
               #   (list, int),     # files ignored, number
               #   (list, int)]     # folders ignored, number

    def pr_start():
        start = fmt_n_log([('START', '\\')])
        print(f'{start}\n\n'
              f'Copying from {src}\n    To {dst}')
        return

    def scan(inpth: str = dst, sORd: list = d, bef_cpy: bool = True):
        """find contents of Source OR Dest path before or after copy
        by looking at name and modification time"""
        if path.isdir(inpth):
            with scandir(inpth) as it:
                for entry in it:
                    if bef_cpy and entry.is_file():
                        sORd[0].append((entry.name, stat(entry).st_mtime))
                    elif bef_cpy and entry.is_dir():
                        sORd[1].append((entry.name, stat(entry).st_mtime))
                    elif entry.is_file() and not bef_cpy:
                        sORd[2].append((entry.name, stat(entry).st_mtime))
                    elif entry.is_dir() and not bef_cpy:
                        sORd[3].append((entry.name, stat(entry).st_mtime))
                return
        elif path.isfile(inpth):
            if bef_cpy:
                sORd[0].append((entry.name, stat(entry).st_mtime))
            else:
                sORd[2].append((entry.name, stat(entry).st_mtime))
            return

    def check():
        """input final and inital lists, get out names and number that were copied
        first generator comprehension is for anything modified
        second gen comp is for anything not there before"""

        def find_copied(fin: list, ini: list):
            # fyfo == 0 for files, 1 for folders
            fyfo = 0 if (d.index(fin) % 2 == 0) else 1

            copied = list((tp[0] for tp in fin for bf in ini if tp[0] == bf[0] and tp[1] != bf[1])) \
                         + list((tp[0] for tp in fin if (tp[0] not in [n[0] for n in ini])))
            cpynum = len(copied)

            ignored = list((tp[0] for tp in fin for bf in ini if tp[0] == bf[0] and tp[1] == bf[1])) \
                             + list((tp[0] for tp in s[fyfo] if (tp[0] not in [n[0] for n in fin])))
            ignum = len(ignored)

            return ((copied, cpynum), (ignored, ignum))

        rslt_fy  = find_copied(d[2], d[0])     # files
        rslt_fo  = find_copied(d[3], d[1])     # folders

        res.append(rslt_fy[0])
        res.append(rslt_fo[0])
        res.append(rslt_fy[1])
        res.append(rslt_fo[1])

        if s[0] != s[2] or s[1] != s[3]:    # the source shouldn't change, if so there was a problem
            return False
        else:
            return True

    def copy2_pr(src1, dst1):
        new1 = copy2(src1, dst1)
        # if path.isdir(src1):
        #     cfolders.append(src1)
        # elif path.isfile(src1):
        #     cfiles.append(src1)
        return new1

    def try_copy():
        try:
            if path.isdir(src):
                copytree(src, dst,
                         ignore=ignore_patterns(*ignore_glob),
                         copy_function=copy2_pr,  # source and dest of ind. file as args
                         dirs_exist_ok=True)
            elif path.isfile(src):
                copy2_pr(src, dst)
        except Exception as e1:
            print(f'{e1}')
        finally:
            return

    def pr_end():
        end = fmt_n_log([('END', '/')])
        print(f'\nTotal items copied: {res[0][1] + res[1][1]}')
        print(f'    Source files copied: {res[0][1]}')
        print_list(res[0][0])
        print(f'    Source folders copied: {res[1][1]}')
        print_list(res[1][0])
        print(f'    Ignored glob:\n'
              f'        {ignore_glob}\n'
              f'    Files Ignored: {res[2][1]}')
        print_list(res[2][0])
        print(f'    Folders Ignored: {res[3][1]}')
        print_list(res[3][0])
        print(f'{end}')
        return

    pr_start()

    scan(inpth=dst, sORd=d, bef_cpy=True)
    scan(inpth=src, sORd=s, bef_cpy=True)

    try_copy()

    scan(inpth=dst, sORd=d, bef_cpy=False)
    scan(inpth=src, sORd=s, bef_cpy=False)

    mycheck = check()
    if mycheck:
        pr_end()
    else:
        print('!!!!!!!!!!!!!!!!!!!!'
              'There was a problem!'
              '!!!!!!!!!!!!!!!!!!!!')
    # print(*d)
    # print(*s)
    # print(*res)
    return