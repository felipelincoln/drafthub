"""Drafthub's command line utility for code and documentation build check
"""
import os
import sys

def main():
    """main()"""
    try:
        args = sys.argv[1:]
    except:
        args = []

    env = '&d3b2mg6&=twp3q*!n9f!1#(zp($j34m5ds=e7v2@+t7m&3z4o'
    SECRET_KEY = os.environ.get('SECRET_KEY', None)
    if SECRET_KEY != env:
        print('check.py doesn\'t work outside the docker container.')
        return

    check = {}

    class msg:
        """outro teste"""
        failed = '\033[91mfailed\033[0m'
        passed = '\033[92mpassed\033[0m'

        @staticmethod
        def cprint(text):
            print(f'\033[95m{text}\033[0m')


    def shell_call(command, output=True):
        import subprocess
        kwargs = {'stderr': None, 'stdout': None}

        if not output:
            kwargs = {
                'stderr': subprocess.DEVNULL,
                'stdout': subprocess.DEVNULL
            }

        return subprocess.call(command, shell=True, **kwargs)

    def test():
        msg.cprint('> test')
        try:
            import coverage
        except:
            print('Installing dependencies...')
            shell_call('pip install coverage')

        check['test'] = msg.failed
        failed = shell_call("make test")
        if not failed:
            check['test'] = msg.passed
        print()

    def coverage_():
        msg.cprint('> coverage')
        try:
            import coverage
        except:
            print('Installing dependencies...')
            shell_call('pip install coverage')

        try:
            with open('.coverage', 'r'):
                print('a coverage report was found!')
        except:
            print('a coverage report not found!')
            print('running test to generate it...')
            shell_call("make test")

        check['coverage'] = msg.failed
        failed = shell_call('make coverage')
        if not failed:
            check['coverage'] = msg.passed
        print()

    def lint():
        msg.cprint('> lint')
        try:
            import pylint
        except:
            print('Installing dependencies...')
            shell_call('pip install pylint')

        check['lint'] = msg.failed
        failed = shell_call('make lint')
        if not failed:
            check['lint'] = msg.passed

    def doc():
        msg.cprint('> doc')
        try:
            with open('docs/requirements.txt', 'r') as f:
                pkgs = f.read().split('\n')[:-1]
                for pkg in pkgs:
                    new_module = __import__(pkg.partition('=')[0])

        except:
            print('Installing dependencies...')
            shell_call('pip install -r docs/requirements.txt')

        check['doc'] = msg.failed
        shell_call('rm -rf docs/_build/*')
        shell_call('sphinx-apidoc -f -o docs/ .', output=False)
        failed = shell_call('make doc')
        if not failed:
            check['doc'] = msg.passed
            print('Documentation successfully built!')

    if not args:
        test()
        coverage_()
        lint()
        doc()
    else:
        if 'test' in args:
            test()
        if 'coverage' in args:
            coverage_()
        if 'lint' in args:
            lint()
        if 'doc' in args:
            doc()

    if check:
        print('\n-----------------------')
        for key, value in check.items():
            if key == 'coverage':
                print(key,'\t', value)
            else:
                print(key,'\t\t', value)


if __name__ == '__main__':
    main()
